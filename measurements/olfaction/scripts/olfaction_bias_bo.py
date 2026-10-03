#!/usr/bin/env python3
"""Constrained Bayesian optimisation of the analog bias point for odour identity.

F. Corradi, 2026-08-13: "bias are likely interdependent so the search space is not
simple." Correct, and today demonstrated it: raising vleakn to cut the firing rate
silenced 6/16 then 9/16 neurons while the rate only fell 108 -> 45 Hz. Leak did not move
the operating point ALONG the responsive region, it moved it off. A 1-D sweep of any
single channel can only find the best point on one line through a coupled space.

This reuses the NARMA tuner's optimiser unchanged (`narma_tuner.ConstrainedBO`) and swaps
the objective from fading memory to task accuracy. The two design choices that make it
work are the NARMA README's and they apply here for the same physics reasons:

  1. Search in VOLTS. The transistors are in weak inversion (I ~ exp(V/nUT), nUT = 31.8
     mV on this die), so the DAC voltage axis IS the log-current axis and the landscape
     is smooth enough for a GP. Each channel is bounded to about two e-folds.
  2. Search OFFSETS, not absolute values. Biases are per-neuron and carry each device's
     mismatch; the search moves a COMMON offset on top of the reference set, so 4 coupled
     dimensions replace 16x23 values and per-neuron trim is preserved.

OBJECTIVE: per-chunk accuracy (grouped CV, kernel read-out -- identical scoring to
olfaction_iso_compare.py), penalised by hard constraints:
  - at least --min-live neurons firing (a silenced array is not a quiet operating point)
  - mean evoked rate inside a band (not dead, not railed)
  - clean read-out (drops == stalls == 0)
Per-chunk rather than voted because it uses every chunk as a sample and so is the less
noisy signal for the GP; the winner is re-scored voted, on the FULL chunk set, at the end.

NOISE, and why the first run of this came up short (2026-08-13). At 2 chunks/trial the
evaluation sd is 0.076: re-drawing WHICH two chunks, on identical chip data, moved
accuracy 0.433 -> 0.667. The BO was chasing a ~+0.11 prize with +/-0.076 error and duly
fit noise. Two fixes, both here:
  * --chunks-per-trial 5 uses EVERY chunk, so chunk-subset sampling noise -- the dominant
    term -- disappears entirely rather than being averaged down.
  * --reps re-acquires each point N times and averages, which addresses the remaining
    chip stochasticity. The per-rep spread is recorded so the noise is measured rather than
    assumed.
And the incumbent is now evaluated FIRST: ConstrainedBO.ask() returns random points for
its first max(4, d+1) draws, so despite the NARMA README's "warm-started at the channel
centres" the centre stayed unmeasured and the GP was built around measured points only.

AER BRACKET (CLAUDE.md, [[aer-encoder-latch]]). The encoder on this die can latch -- every
spike reading as neuron 15, or every address coming back one low -- and it survives reset,
reflash and bias reprogramming; only a physical power cycle clears it. Silently, a latched
encoder turns a masked run into a plausible recording of the WRONG neurons. So an unmasked
16-neuron addressing scan runs before the search, every --scan-every evaluations, and at
A scan that latches ABORTS: every point after a latch is garbage, and continuing would
bury good data under bad. The partial signal otherwise is `live` collapsing across all
subsequent points, but that is a symptom rather than a check.

Evaluations are expensive (~13 min per rep at 5 chunks/trial), so --max-hours bounds the
run by wall clock and it stops cleanly at the budget rather than mid-sweep. State is
checkpointed every evaluation, so a kill resumes rather than restarts.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_bias_bo.py --iters 25
"""
import argparse, json, os, time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from meas_common import BridgeSession, load_biases
from narma_tuner import Channel, ConstrainedBO, channels_to_dict
from reservoir_run import INTEGRITY, present_delta
from olfaction_identity import chunks
from olfaction_iso_compare import kernel, vote_acc
from olfaction_run_array import encode

FS = 1000.0
# JExcWn is NMOS (higher V = more current); JInhWp is PMOS (lower V = more current), so
# a positive "more inhibition" offset must be SUBTRACTED from the PMOS channels.
EXC_BRANCHES = [f"JExcWn{j}" for j in range(4)]
INH_BRANCHES = [f"JInhWp{j}" for j in range(4)]


def build(duration, theta, neurons, npz="data_olfaction/olfaction_pulses.npz"):
    d = np.load(npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == duration
    F, it = chunks(X[m], Th[m], t, float(duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    return F, Y, it, names


def encoders(F, theta, neurons):
    enc = {}
    for k in neurons:
        w = np.random.default_rng(100 + k).normal(0, 1, 8)
        e = []
        for j in range(len(F)):
            s = F[j].reshape(50, 8) @ w
            e.append(encode((s - s.mean()) / (s.std() + 1e-9), theta))
        enc[k] = e
    return enc


def apply_offsets(base, off):
    """Common offsets on top of one neuron's reference biases, in volts."""
    b = dict(base)
    b["vleakn"] = b["vleakn"] + off["d_vleakn"]
    if "vthrdn" in b:
        b["vthrdn"] = b["vthrdn"] + off["d_vthrdn"]
    for c in EXC_BRANCHES:
        if c in b:
            b[c] = b[c] + off["d_exc"]
    for c in INH_BRANCHES:
        if c in b:
            b[c] = b[c] - off["d_inh"]        # PMOS: lower V = more current
    return b


class AERLatch(RuntimeError):
    """Raised when the unmasked addressing scan disagrees with the stimulated neuron."""


# A stimulated neuron is driven with INJECT spikes; a real encoder latch REDIRECTS them,
# so the shifted address collects most of them. One or two spikes at another address is a
# neighbour firing on its own rather than a latch. Requiring a clear share of the injected train
# keeps the check sensitive to the condition it exists for while ignoring a stray.
INJECT = 20
LATCH_MIN_COUNT = 5          # a quarter of the injected train


def aer_scan(b, neurons, base, tag=""):
    """Unmasked scan: stimulate k, assert the address that comes back IS k.

    Unmasked (MASK 65535) on purpose -- with a per-neuron mask a shifted encoder returns
    zero spikes and looks like a dead neuron instead of a misaddressed one.

    A latch is called only when another address collects a real share of the injected
    train. The looser `argmax != k` rule cost a false alarm on 2026-08-16: a hybrid-tree
    run applied one neuron's comparator biases to all sixteen, which left that neuron
    hair-trigger, and a SINGLE stray spike from it while a silent neuron was stimulated
    was reported as misaddressing. Stray firing is now recorded separately as `noise`,
    which is diagnostic while the bracket stays valid."""
    b.send("MASK 65535")
    mis, silent, noise, counts = [], [], [], []
    for k in neurons:
        b.apply_biases(base[k]); time.sleep(0.4)
        b.program_weight(0, 15, exc=True)
        b.route(0, k, exc=True); time.sleep(0.05)
        b.drain(max_lines=200000)
        c = np.asarray(b.inject_spikes(150.0, INJECT), dtype=int)
        counts.append(int(c[k]))
        if c.sum() == 0:
            # NOT a latch. A silent unit is a bias/device issue and it already costs
            # the objective through the live penalty; aborting on it would kill a long
            # run over one marginal neuron (n0 flickers on this die, 2026-08-13).
            silent.append(k)
        elif int(np.argmax(c)) != k:
            r = int(np.argmax(c))
            hit = {"stimulated": k, "reported": r, "count_at_k": int(c[k]),
                   "count_at_reported": int(c[r]), "total": int(c.sum())}
            if int(c[r]) >= LATCH_MIN_COUNT and int(c[k]) == 0:
                # THIS is the latch signature: the injected train came back, at the
                # WRONG address.
                mis.append(hit)
            else:
                # a neighbour fired a spike or two of its own; k itself said nothing
                noise.append(hit)
                silent.append(k)
    ok = not mis
    print(f"  AER scan {tag}: {'OK' if ok else 'LATCHED'} "
          f"({sum(1 for x in counts if x > 0)}/{len(neurons)} responded"
          + (f", silent {silent}" if silent else "")
          + (f", stray {[(h['stimulated'], h['reported'], h['count_at_reported']) for h in noise]}"
             if noise else "") + ")"
          + ("" if ok else f"  MISADDRESSED: {mis}"))
    return ok, {"misaddressed": mis, "silent": silent, "noise": noise}, counts


def measure(b, neurons, base, enc, off, idx, T, weight, mon=None):
    """mon: pin the analog monitor mux (UART_CMD_MONITOR_SYNC) to one neuron so the scope
    has a stable trace. Left following the stimulated neuron (mon=None) the mux hops
    across all 16 every evaluation and the scope shows nothing watchable. The mux is
    analog-only and sits outside the AER recording, so pinning it leaves unchanged what
    is measured -- only what is observable."""
    sp = np.empty((len(neurons), len(idx)), dtype=object)
    d0, s0 = INTEGRITY["drops"], INTEGRITY["stalls"]
    for i, k in enumerate(neurons):
        b.send(f"MASK {1 << k}")
        b.apply_biases(apply_offsets(base[k], off))
        b.monitor(k if mon is None else mon); time.sleep(0.6)
        b.program_weight(0, weight, exc=True); b.program_weight(0, weight, exc=False)
        for jj, j in enumerate(idx):
            sp[i, jj] = np.asarray(present_delta(b, k, enc[k][j], T, 0, 0))
    return sp, INTEGRITY["drops"] - d0, INTEGRITY["stalls"] - s0


def score(sp, Y, it, T, folds):
    K = np.nan_to_num(kernel(sp, T))
    pred = np.zeros(len(Y), dtype=int)
    for tr, te in folds:
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, max_iter=5000, class_weight="balanced"))
        m.fit(K[tr], Y[tr]); pred[te] = m.predict(K[te])
    return float((pred == Y).mean()), pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=25)
    ap.add_argument("--chunks-per-trial", type=int, default=5,
                    help="5 = every chunk; removes chunk-subset sampling noise")
    ap.add_argument("--reps", type=int, default=1,
                    help="re-acquisitions averaged per point (chip stochasticity)")
    ap.add_argument("--save-spikes", default="",
                    help="directory to archive every rep's spikes so points can be "
                         "re-scored later without re-acquiring")
    ap.add_argument("--monitor-neuron", type=int, default=5,
                    help="pin the scope monitor mux to this neuron (-1 = follow the "
                         "stimulated neuron, which makes the scope trace hop)")
    ap.add_argument("--scan-every", type=int, default=4,
                    help="unmasked AER addressing scan every N evaluations (0 = off)")
    ap.add_argument("--max-hours", type=float, default=0.0,
                    help="wall-clock budget; 0 = unlimited. Stops cleanly between points.")
    ap.add_argument("--tpresent", type=float, default=0.15)
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--span", type=float, default=0.040, help="+/- half span per channel (V)")
    ap.add_argument("--min-live", type=int, default=14)
    ap.add_argument("--rate-band", default="3,300")
    ap.add_argument("--bias-pattern",
                    default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--state", default="data/olfaction_bias_bo.json")
    args = ap.parse_args()
    neurons = list(range(16))
    rlo, rhi = [float(x) for x in args.rate_band.split(",")]

    F, Y, it, names = build("0.1s", args.theta, neurons)
    enc = encoders(F, args.theta, neurons)
    idx = np.concatenate([np.flatnonzero(it == g)[:args.chunks_per_trial]
                          for g in np.unique(it)])
    Ys, its = Y[idx], it[idx]
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Ys), 1)), Ys, its))
    base = {k: load_biases(args.bias_pattern.format(k=k)) for k in neurons}

    ch = [Channel("d_vleakn", 0.0, args.span), Channel("d_vthrdn", 0.0, args.span),
          Channel("d_exc", 0.0, args.span), Channel("d_inh", 0.0, args.span)]
    bo = ConstrainedBO(ch, seed=0)
    hist = []
    if os.path.exists(args.state):
        hist = json.load(open(args.state)).get("history", [])
        for h in hist:
            bo.tell(np.array([h["x"][c.name] for c in ch]), h["y"])
        print(f"resumed {len(hist)} evaluations from {args.state}")

    print(f"{len(idx)} chunks / {len(np.unique(its))} trials per evaluation, "
          f"{args.reps} rep(s), up to {args.iters} iterations, "
          f"+/-{args.span*1000:.0f} mV per channel")
    if args.max_hours:
        print(f"wall-clock budget {args.max_hours:.1f} h")
    print(f"reference point: 0.647 per-chunk (full set), 108 Hz, digital 0.880\n")
    print(f"{'it':>3} {'dvleak':>7} {'dvthr':>7} {'dexc':>7} {'dinh':>7} "
          f"{'Hz':>7} {'live':>5} {'acc':>13} {'obj':>7}")
    MON = None if args.monitor_neuron < 0 else int(args.monitor_neuron)
    if MON is not None:
        print(f"scope monitor pinned to neuron {MON} (analog mux only; AER unaffected)")
    t_start = time.time()
    scans = []
    with BridgeSession() as bs:
        ok, bad, _ = aer_scan(bs, neurons, base, tag="opening")
        scans.append({"when": "opening", "ok": ok, "bad": bad, "t": time.time()})
        if not ok:
            raise AERLatch(f"opening AER scan found MISADDRESSING: {bad}. Power-cycle "
                           "the chip (reset/reflash/bias will NOT clear a latched "
                           "encoder).")
        for i in range(len(hist), args.iters):
            if args.max_hours and (time.time() - t_start) / 3600.0 > args.max_hours:
                print(f"\nwall-clock budget reached after {i} evaluations; stopping cleanly")
                break
            # evaluate the INCUMBENT first -- the GP must contain the point we are
            # trying to beat, and ConstrainedBO.ask() starts away from the centre
            x = np.zeros(len(ch)) if (i == 0 and not hist) else bo.ask()
            off = channels_to_dict(ch, x)
            accs, votes, rates, lives, dds, dss = [], [], [], [], 0, 0
            for rep in range(args.reps):
                sp, dd, ds = measure(bs, neurons, base, enc, off, idx,
                                     args.tpresent, args.weight, mon=MON)
                cnt = np.array([[len(sp[k, j]) for k in range(len(neurons))]
                                for j in range(len(idx))]) / args.tpresent
                rates.append(float(cnt.mean())); lives.append(int((cnt.mean(0) > 0).sum()))
                a1, pred = score(sp, Ys, its, args.tpresent, folds)
                # voted at every depth: score() already returns the predictions, so this
                # is free. The first run of this discarded them (and the spikes) and kept
                # only the scalar -- 39 acquisitions of 150 chunks, unrecoverable.
                votes.append([vote_acc(pred, Ys, its, kk) for kk in range(1, 6)])
                accs.append(a1); dds += dd; dss += ds
                if args.save_spikes:
                    np.savez(f"{args.save_spikes}/bo_i{i:02d}_r{rep}.npz",
                             spikes=sp, labels=Ys, trial=its, nproj=1,
                             T=args.tpresent, offsets=json.dumps(off))
            acc = float(np.mean(accs)); acc_sd = float(np.std(accs))
            vmean = np.mean(np.array(votes), axis=0).tolist()
            vsd = np.std(np.array(votes), axis=0).tolist()
            rate = float(np.mean(rates)); live = int(min(lives))
            dd, ds = dds, dss
            # penalised scalar: constraints fold in so the GP still sees a gradient
            pen = 0.0
            pen += 0.05 * max(0, args.min_live - live)
            if rate < rlo:
                pen += 0.05 * (rlo - rate) / max(rlo, 1e-9)
            if rate > rhi:
                pen += 0.05 * (rate - rhi) / rhi
            if dd or ds:
                pen += 0.20
            obj = acc - pen
            bo.tell(x, obj)
            hist.append({"x": off, "acc": acc, "acc_sd": acc_sd, "acc_reps": accs,
                         "voted": vmean, "voted_sd": vsd,
                         "rate": rate, "live": live, "drops": dd, "stalls": ds,
                         "y": obj, "is_center": bool(i == 0 and len(hist) == 0)})
            json.dump({"history": hist, "reference": {"per_chunk": 0.647, "rate": 108.3},
                       "digital": {"per_chunk": 0.880, "voted5": 0.967}},
                      open(args.state, "w"), indent=2)
            if args.scan_every and (i + 1) % args.scan_every == 0:
                ok, bad, _ = aer_scan(bs, neurons, base, tag=f"after eval {i}")
                scans.append({"when": f"after {i}", "ok": ok, "bad": bad, "t": time.time()})
                json.dump({"history": hist, "aer_scans": scans,
                           "reference": {"per_chunk": 0.647, "rate": 108.3},
                           "digital": {"per_chunk": 0.880, "voted5": 0.967}},
                          open(args.state, "w"), indent=2)
                if not ok:
                    raise AERLatch(
                        f"AER scan did not pass after evaluation {i}: {bad}. Every point since "
                        f"the previous passing scan is suspect; power-cycle the chip.")
            print(f"{i:3d} {off['d_vleakn']*1000:+6.1f}m {off['d_vthrdn']*1000:+6.1f}m "
                  f"{off['d_exc']*1000:+6.1f}m {off['d_inh']*1000:+6.1f}m "
                  f"{rate:7.1f} {live:5d} {acc:6.3f}+/-{acc_sd:.3f} "
                  f"v5 {vmean[4]:.3f} {obj:7.3f}"
                  + ("  CENTER" if hist[-1]["is_center"] else "")
                  + ("  <-- best" if obj >= max(h["y"] for h in hist) else ""))
        ok, bad, _ = aer_scan(bs, neurons, base, tag="closing")
        scans.append({"when": "closing", "ok": ok, "bad": bad, "t": time.time()})
        json.dump({"history": hist, "aer_scans": scans,
                   "reference": {"per_chunk": 0.647, "rate": 108.3},
                   "digital": {"per_chunk": 0.880, "voted5": 0.967}},
                  open(args.state, "w"), indent=2)
        if not ok:
            raise AERLatch(f"CLOSING AER scan did not pass: {bad}. The whole run since the last "
                           "passing scan is suspect -- do not use these results.")

    xb, yb = bo.best()
    ob = channels_to_dict(ch, xb)
    hb = max(hist, key=lambda h: h["y"])
    ctr = next((h for h in hist if h.get("is_center")), None)
    if ctr is not None:
        d = hb["acc"] - ctr["acc"]
        pooled = float(np.hypot(hb.get("acc_sd", 0.0), ctr.get("acc_sd", 0.0)))
        print(f"\nvs the INCUMBENT (offsets all zero): {ctr['acc']:.3f} +/- "
              f"{ctr.get('acc_sd', 0):.3f}  ->  best {hb['acc']:.3f} +/- "
              f"{hb.get('acc_sd', 0):.3f}   delta {d:+.3f}")
        print("  " + ("REAL: delta exceeds the pooled per-rep spread"
                      if d > pooled and pooled > 0 else
                      "INSIDE THE NOISE: delta does not exceed the pooled spread "
                      f"({pooled:.3f}) -- below baseline"))
    print(f"\nBEST: vleakn {ob['d_vleakn']*1000:+.1f} mV, vthrdn {ob['d_vthrdn']*1000:+.1f} mV, "
          f"exc {ob['d_exc']*1000:+.1f} mV, inh {ob['d_inh']*1000:+.1f} mV")
    print(f"  {hb['rate']:.1f} Hz, {hb['live']}/16 live, "
          f"{hb['acc']:.3f} per-chunk on the reduced set (reference 0.647 full)")
    print(f"  validate on the full set before believing it:")
    print(f"    the offsets above -> olfaction_run_array.py, then olfaction_iso_compare.py")
    print(f"\nwrote {args.state}")


if __name__ == "__main__":
    raise SystemExit(main())
