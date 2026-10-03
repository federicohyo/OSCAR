#!/usr/bin/env python3
"""Measure the analog tree's SLOT TIME -- the physical duration of one node visit.

This supplies the input the energy number needs. Rail energy is power x time, so the slot
time is what converts a measured 430 uW into joules per node visit, and it is the one
quantity the accuracy run does NOT measure: the 0.25 s I wait between bursts at the bench
is a settle window chosen for measurement reliability, not a property of the circuit.
Quoting it would inflate the rail term by three orders of magnitude.

Two components, measured separately because they are set by different things:

1. DELIVERY. The burst is N input spikes, each a REQ pulse of fixed width, so delivery
   time is linear in N. Timed against the chip's OWN spike stream -- m bursts are issued
   and the clock stops at the last spike to come back, which the chip cannot emit before
   it has processed all of them. The slope against N is the per-spike cost; the fixed
   UART and per-burst overheads are constant in N and land in the intercept. The scope
   cannot do this: it streams at ~1 kHz and one input pulse is tens of microseconds.

2. RE-ARM. After the burst the membrane has to return toward rest before the next
   comparison, or the next node inherits this node's charge. Measured on the scope, which
   IS the right instrument here: the decay is tens of milliseconds, hundreds of samples.
   Fitted as an exponential; re-arm is taken at 3 tau (95% recovered).

Reported per visit, and per visit at 16-way time multiplexing, where the same array rail
covers sixteen concurrent slots and the per-visit rail cost falls by 16 while delivery and
re-arm do not.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_hybrid_slot.py
"""
import argparse, json, time
import numpy as np

from meas_common import BridgeSession, load_biases
from olfaction_graded_hunt import Scope

BIAS = "ofxCaravanViewer/bin/comparator_n14_lvl{L}.biases"
P_ANALOG_W = 0.10e-3        # constants.py, corrected rail 2026-08-29 (was 0.43)
E_CYCLE_J = 372e-12         # constants.py
DRAIN_CYC = 105 + 480       # one AER drain call carrying one event
ROUTE_CYC = 532             # measured digital node visit


def delivery(b, k, ns, m, reps):
    """Wall time of m back-to-back bursts, against burst size.

    Synchronised on the chip's OWN spike stream rather than the host write. Host-side timing
    would measure how fast the host fills the FTDI buffer, which is neither the UART nor
    the chip. Instead the neuron is left firing, m bursts are issued, and the clock stops
    at the LAST spike to come back -- the chip emits it only after it has processed
    every burst. Dropped spikes are harmless: only the last arrival matters, and the ring
    is 2 deep, so most of them are dropped by design.

    The UART command itself costs ~0.83 ms per burst at 24 kbaud, in series with the
    chip's work. That is a constant in N, so it lands in the intercept and leaves the
    slope -- the per-input-spike cost -- clean, provided N goes high enough that the
    chip's own work dominates. Hence 255 in the sweep."""
    out = {}
    print(f"  {'N':>4} {'ms per burst':>13} {'us per spike':>13}")
    for n in ns:
        ts = []
        for _ in range(reps):
            b.drain(max_lines=200000)
            t0 = time.time()
            for _ in range(m):
                b.send(f"BURST {n}")
            last, quiet = t0, 0
            while quiet < 0.20 and time.time() - t0 < 60:
                c = [0] * 16
                b.drain(c)
                if c[k]:
                    last = time.time(); quiet = 0
                else:
                    quiet += 0.02
                time.sleep(0.02)
            ts.append((last - t0) / m)
        out[n] = float(np.median(ts))
        print(f"  {n:>4} {out[n]*1e3:13.3f} {out[n]/max(n,1)*1e6:13.1f}")
    # Drop points where the sync saw zero spikes (t stays at t0, so the entry is 0.0).
    # At N=255 the neuron is driven far past threshold into refractory for the whole
    # burst and the level-1 comparator emitted nothing the loop could catch; leaving the
    # zero in the fit produced a NEGATIVE us/spike, which is unphysical.
    good = {n: t for n, t in out.items() if t > 0}
    if len(good) < 3:
        return out, float("nan"), float("nan")
    x = np.array(list(good), float); y = np.array(list(good.values()))
    slope, icept = np.polyfit(x, y, 1)
    return out, float(slope), float(icept)


def rearm(b, sc, k, n, reps, wait=1.0):
    """Membrane decay after a burst, on the scope. Returns tau in seconds."""
    taus = []
    for _ in range(reps):
        b.drain(max_lines=100000)
        del sc.s[:-40000]
        time.sleep(0.4)
        t0 = time.time()
        b.send(f"BURST {n}")
        time.sleep(wait)
        a = np.array(sc.s)
        w = a[(a[:, 0] >= t0) & (a[:, 0] < t0 + wait)]
        if len(w) < 20:
            continue
        v = w[:, 1] * 1000.0
        # TIME BASE. Neither raw clock works for an interval this short. Host arrival is
        # batched (over the broadcast server a whole recv() is stamped alike, which reads
        # back as tau = 0). The board's own field is coarse: it streams 1001 samples/s but
        # updates its timestamp only every 10 ms, so ten samples share a value and an
        # 11 ms decay would span one tick. The sampling is uniform though, so the rate
        # recovered from the board anchors over the window gives exact per-sample time.
        tb = w[:, 2] if w.shape[1] > 2 else w[:, 0]
        span = float(tb[-1] - tb[0])
        if span <= 0:
            continue
        rate = (len(w) - 1) / span                      # ~1001 Hz, self-calibrating
        base = float(np.median(v[-max(5, len(v) // 5):]))
        pk = int(np.argmax(v))
        d = v[pk:] - base
        if d[0] <= 2.0:
            continue
        # first crossing of 1/e, read directly -- a log-linear fit is dominated by the
        # noise floor once the trace has decayed into it
        below = np.flatnonzero(d <= d[0] / np.e)
        if len(below) and below[0] > 0:
            taus.append(below[0] / rate)                # sample count / measured rate
    return (float(np.median(taus)) if taus else float("nan")), len(taus)


def sanity(tau, nfit):
    """A re-arm of zero is not a fast neuron, it is a broken time base."""
    if nfit == 0 or tau != tau:
        return "decay capture empty"
    if tau < 1e-3:
        return f"tau {tau*1e3:.3f} ms is below one sample period -- time base suspect"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--level", type=int, default=6,
                    help="delivery timing needs the neuron FIRING, so use the LOWEST "
                         "level that exists. Was 1; after the recalibration lvl1 was "
                         "dropped as a free-runner and its file no longer exists.")
    ap.add_argument("--m", type=int, default=100, help="bursts per timing point")
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--rearm-level", type=int, default=32,
                    help="a SUB-threshold level, so the decay measured is the membrane "
                         "returning to rest and not a spike")
    ap.add_argument("--visits", type=float, default=166.8, help="node visits per chunk")
    ap.add_argument("--out", default="data/olfaction_hybrid_slot.json")
    args = ap.parse_args()
    k = args.neuron
    sc = Scope()
    rec = {"neuron": k}
    with BridgeSession() as b:
        b.send(f"MASK {1 << k}")
        b.apply_biases(load_biases(BIAS.format(L=args.level)))
        b.monitor(k); time.sleep(0.85)
        b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.05)

        print("delivery (chip-bound, host saturating the link):")
        d, slope, icept = delivery(b, k, [1, 4, 16, 64, 128, 255], args.m, args.reps)
        print(f"  fit: {slope*1e6:.2f} us/spike + {icept*1e6:.1f} us fixed")

        print("\nre-arm (membrane decay on the scope, sub-threshold level 32):")
        b.apply_biases(load_biases(BIAS.format(L=args.rearm_level)))
        b.monitor(k); time.sleep(0.85)
        b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.05)
        tau, nfit = rearm(b, sc, k, 24, args.reps)
        print(f"  tau {tau*1e3:.1f} ms over {nfit} fits -> re-arm 3tau "
              f"{3*tau*1e3:.1f} ms")
        bad = sanity(tau, nfit)
        if bad:
            print(f"  REFUSING to report energy: {bad}")
            sc.stop()
            return 2
    sc.stop()

    nbar = 8.0                                   # mean burst size over the tree's nodes
    t_del = slope * nbar + icept
    t_slot = t_del + 3 * tau
    e_rail = P_ANALOG_W * t_slot
    e_aer = DRAIN_CYC * E_CYCLE_J
    e_rt = ROUTE_CYC * E_CYCLE_J
    e_visit = e_rail + e_aer + e_rt
    e_dec = e_visit * args.visits * 5            # voted over 5 chunks
    # /16 lies outside reach and the reference campaign has moved past it. The bias DACs are
    # array-wide, so the neurons in range share one threshold; weighting
    # levels by their share of node visits gives 1.13x (olfaction_mismatch_payoff.py).
    # Kept as an upper bound only, and labelled as one.
    e_visit16 = e_rail / 16 + e_aer + e_rt
    print(f"\nslot {t_slot*1e3:.1f} ms = {t_del*1e3:.2f} delivery + {3*tau*1e3:.1f} re-arm")
    print(f"per visit: rail {e_rail*1e9:.0f} nJ + AER {e_aer*1e9:.0f} + route "
          f"{e_rt*1e9:.0f} = {e_visit*1e9:.0f} nJ")
    print(f"per decision (x{args.visits:.1f} visits x5 chunks): {e_dec*1e6:.0f} uJ")
    print(f"16-way UPPER BOUND (not reachable: array-wide biases mean the neurons do "
          f"share one threshold; measured parallelism is 1.13x): "
          f"{e_visit16*1e9:.0f} nJ/visit, {e_visit16*args.visits*5*1e6:.0f} uJ/decision")
    rec.update(delivery_s=d, us_per_spike=slope * 1e6, us_fixed=icept * 1e6,
               tau_s=tau, t_slot_s=t_slot, nbar=nbar,
               e_visit_J=e_visit, e_visit16_J=e_visit16,
               e_decision_J=e_dec, e_decision16_J=e_visit16 * args.visits * 5,
               visits=args.visits)
    json.dump(rec, open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
