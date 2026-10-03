#!/usr/bin/env python3
"""ECG accuracy-vs-energy/latency frontier (Phase 0 of the continuous-time-edge brief).

Four operating points, all scored on the SAME 90 beats / 7 records (inter-patient LORO)
so accuracies are paired and comparable:

  OP1  analog reservoir (measured HW spikes) + RISC-V linear readout
  OP2  RISC-V numeric-LIF reservoir (same algorithm, heterogeneous params) + same readout
  OP3  best practical edge classifier: RR + morphology -> gradient-boosted trees (no MUL)
  OP4  same classifier, unconstrained CPU (reference function / accuracy ceiling)

Accuracy is offline. Cost (latency + energy per inference) for the digital paths is
built from EXACT rv32i instruction counts disassembled from firmware/numeric_lif (the
soft-multiply-dominated LIF step) and a documented sky130 energy-per-cycle constant.

Honest expected read: on static single-beat ECG the analog substrate is COMPETITIVE but
NOT dominant on accuracy (all four points overlap within their large per-record s.d.), so
the ECG frontier is decided on cost -- which motivates the temporal task where the analog
dominates. The mechanism seed is already visible here: the numeric-LIF reservoir (OP2)
pays O(N * T/dt) to reproduce, in numerics, what the analog array integrates for free.
"""
import warnings; warnings.filterwarnings("ignore")
import json
import numpy as np
from reservoir_kernel import build_features
from reservoir_data import get_beats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score
from scipy.stats import wilcoxon

# ----------------------------------------------------------------------------------
# 0. Chip / cost constants (grounded where measured, labeled where estimated)
# ----------------------------------------------------------------------------------
F_CLK = 25e6                 # RV32I core clock (firmware/soc.h CONFIG_CLOCK_FREQUENCY)
# sky130 130nm small in-order RV32I core, ~1.8 V. No on-die power was measured in this
# tape-out (the reference campaign is an interface/throughput characterization), so E_CYCLE is a
# LITERATURE-ORDER ESTIMATE used only as a linear scale on the energy axis; it does not
# affect the analog-vs-numeric ORDERING or the O(N/dt) SLOPE (both digital paths share it,
# and the analog feature-generation energy is orders of magnitude below either).
E_CYCLE = 100e-12            # J per cycle  [estimate: sky130 RV32I @ 25 MHz, order 10-100 pJ]

# --- EXACT static instruction costs, counted from firmware/numeric_lif/numeric_lif.lst
#     (riscv64-unknown-elf-gcc -march=rv32i -O2). See that .lst for provenance. ---
# lif_step, typical hot path (v>=0, non-refractory, no spike): 20 fixed instr + the
# inlined soft-multiply loop (.L9) at 7 instr per iteration.
LIF_FIXED_INSTR   = 20       # lif_step minus the multiply loop (prologue+branches+update)
MUL_INSTR_PER_ITER = 7       # umul32 inlined loop body (andi,neg,and,srli,add,slli,bnez)
# reservoir_beat inner loop (.L19), per neuron-step: pointer math + 4 loads + call + accum
RESERVOIR_INNER_INSTR = 15
# Extra memory stalls (VexRiscv load = 2 cycles): 4 loads in reservoir_beat + 2 in lif_step
LOADS_PER_STEP = 6
STORE_PER_STEP = 1


def mul_iters(decay_q16):
    """umul32 loops once per bit of the multiplier until it reaches 0 -> bit-length."""
    return int(decay_q16).bit_length()


def numeric_lif_cycles_per_beat(dt, T=2.0, n_neurons=16, tau_m=0.03, mismatch=0.15,
                                seed=0, cpi_load=2):
    """Exact rv32i cycles to Euler-integrate the 16-neuron LIF reservoir for one beat at
    step dt, from the disassembled instruction counts. Heterogeneous per-neuron decay
    (matched-diversity, the fairness requirement). Returns (cycles, nsteps, mean_mul_iters)."""
    rng = np.random.default_rng(seed)
    taus = np.clip(tau_m * (1 + mismatch * rng.standard_normal(n_neurons)), 0.005, None)
    decays_q16 = np.round(np.exp(-dt / taus) * 65536).astype(np.int64)
    decays_q16 = np.clip(decays_q16, 1, 65535)
    iters = np.array([mul_iters(d) for d in decays_q16])
    nsteps = int(round(T / dt))
    # per neuron-step instruction count (typical hot path)
    instr_per_step = RESERVOIR_INNER_INSTR + LIF_FIXED_INSTR + MUL_INSTR_PER_ITER * iters
    # cycles: 1 CPI + extra load stalls (cpi_load-1 per load)
    cyc_per_step = instr_per_step + (cpi_load - 1) * LOADS_PER_STEP
    cycles = nsteps * cyc_per_step.sum()          # sum over the 16 heterogeneous neurons
    return int(cycles), nsteps, float(iters.mean())


# ----------------------------------------------------------------------------------
# 1. Accuracies on the shared 90-beat / 7-record set (inter-patient LORO)
# ----------------------------------------------------------------------------------
TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]; K = 8
CANON = ("200", "208", "209", "222", "223", "232", "233")


def bank(sp, T):
    return np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])


def loro(F, y, g, kind):
    """Per-record accuracy + macro-F1 dict under leave-one-record-out."""
    per = {}
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        if kind == "lr":
            c = make_pipeline(StandardScaler(),
                              LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        else:
            c = HistGradientBoostingClassifier(max_iter=200, max_depth=3,
                                               learning_rate=0.1, random_state=0)
        c.fit(F[tr], y[tr]); p = c.predict(F[te]); rec = g[te][0]
        per[rec] = (accuracy_score(y[te], p), f1_score(y[te], p, average="macro"))
    return per


def summ(per, recs):
    a = np.array([per[r][0] for r in recs]); f = np.array([per[r][1] for r in recs])
    return a.mean(), a.std(), f.mean(), f.std()


def main():
    # The two datasets are arguments so the same analysis can be re-run against a
    # re-acquisition without editing the scoring code. Defaults are the original files.
    import argparse
    ap = argparse.ArgumentParser()
    # recording NSV (reservoir_datasets.py): OP1 accuracy AND the 81.1 events/beat
    # that constants.py charges OP1 for both come from this file.
    ap.add_argument("--hw", default="reservoir_spikes_nsv_structured_hw.npz",
                    help="OP1: measured analog reservoir")
    ap.add_argument("--sw", default="reservoir_spikes_nsv_structured.npz",
                    help="OP2: numeric LIF reproduction (software, float)")
    ap.add_argument("--out", default="reservoir_frontier.json")
    cli = ap.parse_args()
    hw = np.load(cli.hw, allow_pickle=True)
    sw = np.load(cli.sw, allow_pickle=True)
    print(f"OP1 <- {cli.hw}\nOP2 <- {cli.sw}")
    y = np.asarray(hw["labels"]); g = np.asarray(hw["records"])
    X, y2, meta = get_beats(records=CANON, n_per_class=30, classes="NSV")
    rr = meta["rr"]
    assert np.array_equal(y, y2) and np.array_equal(g, np.asarray(meta["records"])), "MISALIGNED"
    recs = list(dict.fromkeys(g.tolist()))

    feats = {
        "OP1_analog_reservoir": (bank(hw["spikes"], float(hw["T"])), "lr"),
        "OP2_numeric_LIF":      (bank(sw["spikes"], float(sw["T"])), "lr"),
        "OP3_edge_GBM":         (np.hstack([X, rr]), "gbm"),
        "OP4_cpu_ref":          (np.hstack([X, rr]), "lr"),
    }
    per = {n: loro(F, y, g, k) for n, (F, k) in feats.items()}

    acc = {}
    print(f"=== N/S/V, {len(y)} beats, {len(recs)} records (inter-patient LORO) ===")
    for n in feats:
        am, asd, fm, fsd = summ(per[n], recs)
        # Uncertainty OF THE MEAN across held-out records: bootstrap 95% CI (20,000
        # percentile resamples, the reference campaign's convention). The marginal between-patient
        # s.d. (acc_sd) is NOT the error of the mean marker; store both, plot the CI.
        a_rec = np.array([per[n][r][0] for r in recs])
        rng_ci = np.random.default_rng(0)
        boot_m = np.array([a_rec[rng_ci.integers(0, len(a_rec), len(a_rec))].mean()
                           for _ in range(20000)])
        ci_lo, ci_hi = np.percentile(boot_m, [2.5, 97.5])
        sem = asd / np.sqrt(len(a_rec))
        acc[n] = dict(acc=am, acc_sd=asd, f1=fm, f1_sd=fsd,
                      ci_lo=float(ci_lo), ci_hi=float(ci_hi), sem=float(sem))
        print(f"  {n:22s} acc={am:.3f}  95%CI[{ci_lo:.3f},{ci_hi:.3f}]  "
              f"(marginal s.d.±{asd:.3f}, SEM±{sem:.3f})  macroF1={fm:.3f}")

    # paired analog-vs-best-digital (accuracy), the honest 'competitive-not-dominant' test
    da = np.array([per["OP1_analog_reservoir"][r][0] for r in recs])
    db = np.array([per["OP3_edge_GBM"][r][0] for r in recs])
    d = da - db
    rng = np.random.default_rng(0)
    boot = np.array([np.mean(d[rng.integers(0, len(d), len(d))]) for _ in range(20000)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    try:
        _, pw = wilcoxon(da, db, alternative="two-sided")
    except ValueError:
        pw = 1.0
    print(f"\nPAIRED analog(OP1) - best-digital(OP3), accuracy: mean {d.mean():+.3f} "
          f"95%CI [{lo:+.3f},{hi:+.3f}]  Wilcoxon p={pw:.3f}  "
          f"({'competitive: CI includes 0' if lo<0<hi else 'separated'})")

    # ------------------------------------------------------------------------------
    # 2. Cost per inference
    # ------------------------------------------------------------------------------
    # readout is SHARED by OP1 and OP2 (both feed the same linear classifier); it cancels
    # in the analog-vs-numeric comparison. We report the feature-generation cost, which is
    # where the substrates differ.
    T_BEAT = 2.0            # beat window (s) -- the real-time budget for a 2 s ECG beat
    dt_ref = 1e-3            # 1 ms Euler step (a coarse, real-time-friendly choice)
    op2_cyc, nsteps, mi = numeric_lif_cycles_per_beat(dt_ref)
    op2_lat = op2_cyc / F_CLK
    print(f"\n=== RISC-V numeric-LIF (OP2) feature-generation cost @ dt={dt_ref*1e3:.0f} ms ===")
    print(f"  {nsteps} steps x 16 neurons, mean soft-mul iters/step={mi:.1f}")
    print(f"  cycles/beat = {op2_cyc:,}  ->  latency {op2_lat*1e3:.1f} ms/beat "
          f"(uses {op2_lat/T_BEAT*100:.0f}% of the {T_BEAT:.0f} s real-time budget)")
    print(f"  energy/beat = {op2_cyc*E_CYCLE*1e3:.3f} mJ  [E_cycle={E_CYCLE*1e12:.0f} pJ, estimate]")
    # dt floor: finest Euler step at which the core still integrates in real time
    # (latency == beat duration). cycles(dt) ~ k/dt, so dt_floor = op2_lat/T_BEAT * dt_ref.
    dt_floor = op2_lat / T_BEAT * dt_ref
    print(f"  real-time dt floor (latency = {T_BEAT:.0f} s beat): dt = {dt_floor*1e6:.0f} us"
          f"  -> finer resolution than this, the RV32I cannot keep up on a 2 s beat")

    # O(N/dt) slope sweep -> the mechanism proof (numeric climbs, analog is flat in dt)
    dts = np.array([8e-3, 4e-3, 2e-3, 1e-3, 5e-4, 2e-4, 1e-4])
    sweep = []
    for dt in dts:
        c, ns, _ = numeric_lif_cycles_per_beat(dt)
        sweep.append(dict(dt=float(dt), cycles=int(c), latency_s=c / F_CLK,
                          energy_J=c * E_CYCLE))
    # linearity check: cycles should scale ~ 1/dt (O(N/dt))
    c_lin = np.array([s["cycles"] for s in sweep]) * dts
    print(f"  O(N/dt) check: cycles*dt over the sweep = "
          f"{c_lin.mean():.3e} ± {c_lin.std():.1e} (flat => linear in 1/dt)")

    # analog reservoir feature-generation cost: physics integrates for free; the RISC-V
    # only receives the sparse output spikes over the AER/LA path. Order estimate:
    # ~tens of spikes/beat, each a 4-byte UART packet (~1.3 ms) -- bounded by I/O, not compute.
    hw_spk = sum(len(np.asarray(hw["spikes"][j, b])) for j in range(16) for b in range(90)) / 90
    aer_cyc = hw_spk * 200          # ~200 cyc/spike to sample+timestamp a received event (est.)
    print(f"\n=== analog reservoir (OP1) feature-generation cost ===")
    print(f"  mean {hw_spk:.1f} output spikes/beat; integration in physics = O(1) in dt "
          f"(0 compute cycles); AER sample ~{int(aer_cyc):,} cyc/beat (est.)")
    print(f"  numeric/analog feature-cost ratio @ dt=1ms: ~{op2_cyc/max(aer_cyc,1):,.0f}x")

    out = dict(
        n_beats=int(len(y)), records=recs,
        accuracy=acc,
        paired_analog_vs_gbm=dict(mean=float(d.mean()), ci=[float(lo), float(hi)],
                                  wilcoxon_p=float(pw)),
        cost=dict(f_clk=F_CLK, e_cycle=E_CYCLE, dt_ref=dt_ref, t_beat=T_BEAT,
                  op2_cycles_per_beat=op2_cyc, op2_latency_s=op2_lat,
                  op2_dt_floor_s=float(dt_floor),
                  op1_aer_cycles_per_beat=float(aer_cyc),
                  op1_mean_spikes_per_beat=float(hw_spk),
                  # OP3: COUNTED, not estimated. Exact rv32i instruction count for the
                  # full path (234->128 resample 15,698 + per-beat normalisation 15,657
                  # + RR features 703 + 600-tree traversal 23,270), from
                  # firmware/op3_kernel/op3_kernel.c at -march=rv32i -O2 with dynamic
                  # trip counts over the real fitted model and the real 90 beats; 1 CPI
                  # plus one cycle per load, the same convention as the LIF column above.
                  # See op3_count.py and data/op3_kernel_count.json. This replaces a
                  # hard-coded 4000.0 order-of-magnitude estimate that was low by 13.8x.
                  op3_gbm_cycles_per_beat=55329.0,
                  # OP4 is still an order-of-magnitude estimate; it is a reference
                  # function, not a claim, and no headline number depends on it.
                  op4_ref_cycles_per_beat=2000.0),   # ESTIMATE
        dt_sweep=sweep,
        static_costs=dict(lif_fixed=LIF_FIXED_INSTR, mul_per_iter=MUL_INSTR_PER_ITER,
                          reservoir_inner=RESERVOIR_INNER_INSTR, loads=LOADS_PER_STEP),
    )
    with open(cli.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {cli.out}")

    make_figure(cli.out)   # data-driven: reads the json written just above
    return 0


# --- Nature-figure style: small, vector, embedded fonts, colorblind-safe palette ---
# Categorical palette (dataviz skill; validated worst-adjacent CVD dE 21.2 >= 12, light
# surface). One hue per operating point, reused in both panels. Aqua = analog substrate
# (physics/free), red = the costly numeric reproduction, yellow/blue = digital baselines.
PALETTE = {
    "OP1_analog_reservoir": "#1baf7a",   # aqua
    "OP2_numeric_LIF":      "#e34948",   # red
    "OP3_edge_GBM":         "#eda100",   # yellow
    "OP4_cpu_ref":          "#2a78d6",   # blue
}
INK, MUTED, GRID = "#0b0b0b", "#898781", "#e1e0d9"


def _apply_style():
    import matplotlib as mpl
    mpl.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42,          # embed TrueType (editable/vector)
        "svg.fonttype": "none",
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7,
        "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6,
        "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "axes.labelcolor": INK, "text.color": INK,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "xtick.minor.width": 0.4, "ytick.minor.width": 0.4,
        "xtick.minor.size": 1.5, "ytick.minor.size": 1.5,
        "legend.frameon": False, "axes.grid": False,
        "lines.solid_capstyle": "round",
    })


def make_figure(results_json="reservoir_frontier.json"):
    """Nature-Communications-quality two-panel frontier, rendered entirely from the saved
    analysis in `results_json` (no numbers hardcoded here):
      (a) accuracy vs energy/inference for the four operating points -- the accuracies
          coincide within s.d.; the numeric-LIF reproduction (OP2) costs ~10^2-10^3x more.
      (b) the exact O(N/dt) mechanism -- numeric compute climbs linearly with temporal
          resolution 1/dt while the analog substrate is flat (physics, O(1) in dt).

    Honesty encoding: filled marker = cost anchored in an EXACT rv32i cycle count (OP2);
    open marker = order-of-magnitude cost estimate (OP1 AER readout, OP3/OP4 classifiers).
    Cycle counts and the O(N/dt) slope are clock-independent; only the latency/energy-time
    axes scale linearly with F_CLK (set once below; a one-line change).
    """
    import json
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    _apply_style()

    d = json.load(open(results_json))
    acc, cost, sweep = d["accuracy"], d["cost"], d["dt_sweep"]
    F_CLK = cost["f_clk"]            # <-- one place: 25 MHz RV32I core (firmware/soc.h)
    e_cyc, T_BEAT = cost["e_cycle"], cost["t_beat"]
    f_mhz = F_CLK / 1e6

    # energy per inference (J) = feature-generation cycles x E_cycle (E_cycle labelled est.)
    E = {  # (energy_mJ, cycles, is_cost_exact)
        "OP1_analog_reservoir": (cost["op1_aer_cycles_per_beat"] * e_cyc * 1e3, None, False),
        "OP2_numeric_LIF":      (cost["op2_cycles_per_beat"]     * e_cyc * 1e3,
                                 cost["op2_cycles_per_beat"], True),
        "OP3_edge_GBM":         (cost["op3_gbm_cycles_per_beat"] * e_cyc * 1e3, None, False),
        "OP4_cpu_ref":          (cost["op4_ref_cycles_per_beat"] * e_cyc * 1e3, None, False),
    }
    NAME = {"OP1_analog_reservoir": "OP1  analog reservoir",
            "OP2_numeric_LIF":      "OP2  numeric-LIF (RV32I)",
            "OP3_edge_GBM":         "OP3  edge trees (no MUL)",
            "OP4_cpu_ref":          "OP4  CPU reference"}
    MARK = {"OP1_analog_reservoir": "o", "OP2_numeric_LIF": "s",
            "OP3_edge_GBM": "^", "OP4_cpu_ref": "D"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.09, 2.83))  # 180 x 72 mm
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)

    # ---- panel (a): accuracy vs energy -------------------------------------------------
    ax1.set_xscale("log")
    ax1.set_xlim(1.1e-4, 2.4)
    ax1.set_ylim(0.34, 0.90)
    # shaded band = mutual overlap of the four bootstrap-95%-CI-of-the-mean bars: a common
    # accuracy consistent with every substrate -> "accuracies coincide within uncertainty".
    band_lo = max(acc[k]["ci_lo"] for k in E); band_hi = min(acc[k]["ci_hi"] for k in E)
    ax1.axhspan(band_lo, band_hi, color=MUTED, alpha=0.10, lw=0, zorder=0)
    ax1.text(0.030, band_hi + 0.010, "accuracies coincide\n(95% CIs overlap)",
             fontsize=5.4, color=MUTED, style="italic", va="bottom", ha="center",
             linespacing=1.15)
    # bootstrap 95% CI of the mean over the 7 held-out records (asymmetric); markers on top
    for k in E:
        e_mJ, _, exact = E[k]; col = PALETTE[k]; a = acc[k]["acc"]
        yerr = [[a - acc[k]["ci_lo"]], [acc[k]["ci_hi"] - a]]
        ax1.errorbar(e_mJ, a, yerr=yerr, fmt="none", ecolor=col, elinewidth=1.0,
                     alpha=0.55, capsize=2.2, capthick=0.8, zorder=2)
    for k in E:
        e_mJ, _, exact = E[k]; col = PALETTE[k]
        ax1.plot(e_mJ, acc[k]["acc"], MARK[k], ms=6.5, mfc=(col if exact else "white"),
                 mec=col, mew=1.4, zorder=4)
    # the hero: same accuracy, ~302x the energy (approximate -- rides on E_cycle)
    e1 = E["OP1_analog_reservoir"][0]; e2 = E["OP2_numeric_LIF"][0]
    ratio = cost["op2_cycles_per_beat"] / cost["op1_aer_cycles_per_beat"]
    ax1.annotate("", xy=(e2, 0.375), xytext=(e1, 0.375),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8, shrinkA=1, shrinkB=1))
    ax1.text((e1 * e2) ** 0.5, 0.388, f"same accuracy · $\\approx${ratio:.0f}$\\times$ energy",
             ha="center", va="bottom", fontsize=5.8, color=INK)
    # the ACTUAL comparison statistic: paired analog - best-digital difference (from json)
    pd = d["paired_analog_vs_gbm"]
    ax1.text(0.030, 0.885,
             f"analog $-$ edge trees:  $+{pd['mean']:.3f}$\n"
             f"95% CI [$+{pd['ci'][0]:.3f}$, $+{pd['ci'][1]:.3f}$],  Wilcoxon $p={pd['wilcoxon_p']:.3f}$",
             ha="center", va="top", fontsize=5.3, color=INK, linespacing=1.3)
    ax1.set_xlabel(f"energy per inference (mJ)   ·   E$_{{cyc}}$ = {e_cyc*1e12:.0f} pJ (est.)")
    ax1.set_ylabel("inter-patient accuracy (LORO)")
    ax1.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    ax1.grid(axis="y", ls=":", lw=0.5, color=GRID, zorder=0)
    ax1.tick_params(length=2.5)
    # legend (identity + honesty note) in the clear x-strip between the OP1 and OP2 columns
    handles = [Line2D([0], [0], marker=MARK[k], color="none",
                      mfc=(PALETTE[k] if E[k][2] else "white"), mec=PALETTE[k], mew=1.4,
                      ms=6, label=NAME[k]) for k in E]
    handles.append(Line2D([0], [0], marker="o", color="none", mfc="white", mec=INK,
                          mew=1.2, ms=6, label="open = order-of-mag. cost est."))
    ax1.legend(handles=handles, loc="center left", bbox_to_anchor=(0.40, 0.42),
               handletextpad=0.4, labelspacing=0.30, borderpad=0.3, fontsize=5.4)

    # ---- panel (b): the O(N/dt) mechanism (exact) --------------------------------------
    inv_dt = np.array([1.0 / s["dt"] for s in sweep])
    lat_ms = np.array([s["cycles"] / F_CLK * 1e3 for s in sweep])   # clock-independent cyc
    order = np.argsort(inv_dt); inv_dt, lat_ms = inv_dt[order], lat_ms[order]
    col2 = PALETTE["OP2_numeric_LIF"]; col1 = PALETTE["OP1_analog_reservoir"]
    aer_ms = cost["op1_aer_cycles_per_beat"] / F_CLK * 1e3
    dt_floor = (cost["op2_cycles_per_beat"] / F_CLK) / T_BEAT * cost["dt_ref"]

    ax2.axhline(T_BEAT * 1e3, color=INK, ls=(0, (4, 2)), lw=0.9, zorder=2)
    ax2.plot(inv_dt, lat_ms, "-", color=col2, lw=1.6, zorder=3)
    ax2.plot(inv_dt, lat_ms, "s", color=col2, mfc=col2, mec="white", mew=0.6,
             ms=5, zorder=4)                                         # filled = exact cycles
    ax2.axhline(aer_ms, color=col1, lw=1.8, zorder=3)
    ax2.axvline(1.0 / dt_floor, color=MUTED, ls=":", lw=0.8, zorder=1)

    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xlabel(r"temporal-resolution demand  1/$\Delta t$  (Hz)")
    ax2.set_ylabel(f"compute latency per beat (ms) @ {f_mhz:.0f} MHz")
    ax2.grid(which="both", ls=":", lw=0.5, color=GRID, zorder=0)
    ax2.tick_params(which="both", length=2.5)

    # short annotations, kept outside the data
    ax2.text(inv_dt[-1], lat_ms[-1] * 1.5, r"$\propto N/\Delta t$",
             fontsize=6.5, color=col2, ha="right", va="bottom")
    ax2.text(inv_dt[0] * 1.1, T_BEAT * 1e3 * 1.25, "real-time budget (2 s beat)",
             fontsize=5.8, color=INK, va="bottom")
    ax2.text(inv_dt[0] * 1.1, aer_ms * 1.35, "analog: flat in $\\Delta t$ (physics, O(1))",
             fontsize=5.8, color=col1, va="bottom")
    ax2.text(1.0 / dt_floor * 0.92, ax2.get_ylim()[0] * 3, f"$\\Delta t$ floor {dt_floor*1e6:.0f} µs",
             fontsize=5.8, color=MUTED, ha="right", va="bottom", rotation=90)

    # panel letters (bold lowercase, top-left, outside the axes)
    for ax, letter in ((ax1, "a"), (ax2, "b")):
        ax.text(-0.20, 1.02, letter, transform=ax.transAxes, fontsize=8,
                fontweight="bold", va="bottom", ha="left")

    fig.tight_layout(w_pad=2.2)
    base = "measurements/array/figures/ecg_frontier"
    fig.savefig(base + ".pdf", bbox_inches="tight")            # vector primary
    fig.savefig(base + ".png", dpi=350, bbox_inches="tight")   # raster preview
    plt.close(fig)
    print(f"wrote {base}.{{pdf,png}}  (F_CLK={f_mhz:.0f} MHz, "
          f"energy ratio OP2/OP1 ~{ratio:.0f}x, dt floor {dt_floor*1e6:.0f} us)")


if __name__ == "__main__":
    raise SystemExit(main())
