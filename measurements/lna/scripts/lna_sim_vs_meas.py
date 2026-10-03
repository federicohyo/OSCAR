#!/usr/bin/env python3
"""Simulated vs measured LNA gain.

    ../.venv-meas/bin/python3 lna_sim_vs_meas.py            # plot from saved CSV
    ../.venv-meas/bin/python3 lna_sim_vs_meas.py --run-spice  # re-run ngspice first

The simulation is Federico's own testbench, run unmodified except for the
`.control` block, which is replaced by an AC sweep that writes data instead of
opening plot windows. Nothing about the circuit or its bias sources is touched,
so this is "the design as simulated" against "the chip as measured" -- not a
re-tuned simulation made to agree.

  testbench: aVLSI-SkyWater130-2024/netlists/low_noise_amp_fc_v3_loopgain_tb.spice
  measured : lna_transfer_final.csv (drive path divided out)

The closed-loop gain is set by the capacitor ratio inside the subcircuit:

    XC1 vin input  cap_mim_m3_1 W=132 L=70   -> C1 ~ 9240 um^2
    XC6 vin vout   cap_mim_m3_1 W=5   L=5    -> C2 ~   25 um^2
    C1/C2 = 369.6 = 51.35 dB   (the design intent)

so any gain shortfall on silicon is a statement about that ratio as fabricated,
not about the OTA -- which is the useful thing for the draft to say.
"""

import argparse
import csv
import math
import os
import subprocess
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
TB = ("/storage/tue/aVLSI-SkyWater130-2024/netlists/"
      "low_noise_amp_fc_v3_loopgain_tb.spice")
SIM_CSV = os.path.join(HERE, "lna_sim_ac.csv")
C1_UM2, C2_UM2 = 132 * 70, 5 * 5


def run_spice(workdir):
    """Run the testbench's AC analysis in batch, keeping the circuit untouched."""
    s = open(TB).read()
    i, j = s.index(".control"), s.index(".endc") + len(".endc")
    out = os.path.join(workdir, "sim_ac.txt")
    ctrl = f""".control
  ac dec 50 0.01 1e7
  let gdb = vdb(vout)
  let ph  = vp(vout)*180/PI
  set wr_singlescale
  wrdata {out} gdb ph
  meas ac DCG find vdb(vout) at=10
.endc"""
    net = os.path.join(workdir, "tb_ac.spice")
    open(net, "w").write(s[:i] + ctrl + s[j:])
    r = subprocess.run(["ngspice", "-b", net], capture_output=True, text=True, timeout=900)
    if not os.path.exists(out):
        sys.exit("ngspice produced no data:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    rows = []
    for ln in open(out):
        p = ln.split()
        if len(p) >= 3:
            try:
                rows.append((float(p[0]), float(p[1]), float(p[2])))
            except ValueError:
                pass
    with open(SIM_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["freq_hz", "gain_db", "phase_deg"])
        w.writerows([[f"{a:.6g}", f"{b:.6f}", f"{c:.4f}"] for a, b, c in rows])
    print(f"ngspice: {len(rows)} points -> {os.path.basename(SIM_CSV)}")


def corner(f, g, level):
    """Lowest frequency where the curve rises through `level` (dB)."""
    for i in range(1, len(f)):
        if g[i - 1] < level <= g[i]:
            t = (level - g[i - 1]) / (g[i] - g[i - 1])
            return 10 ** (math.log10(f[i - 1]) + t * (math.log10(f[i]) - math.log10(f[i - 1])))
    return float("nan")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run-spice", action="store_true")
    ap.add_argument("--png", default=os.path.join(FIG, "lna_sim_vs_meas.png"))
    args = ap.parse_args()

    os.makedirs(FIG, exist_ok=True)
    if args.run_spice or not os.path.exists(SIM_CSV):
        import tempfile
        with tempfile.TemporaryDirectory(prefix="lnaac_") as wd:
            run_spice(wd)

    sim = list(csv.DictReader(open(SIM_CSV)))
    sf = np.array([float(r["freq_hz"]) for r in sim])
    sg = np.array([float(r["gain_db"]) for r in sim])
    mea = list(csv.DictReader(open(os.path.join(HERE, "lna_transfer_final.csv"))))
    mf = np.array([float(r["freq_hz"]) for r in mea])
    mg = np.array([float(r["gain_db"]) for r in mea])

    Gs = sg[(sf >= 4) & (sf <= 280)].mean()
    Gm = mg[(mf >= 4) & (mf <= 280)].mean()
    ideal = 20 * math.log10(C1_UM2 / C2_UM2)
    fcs, fcm = corner(sf, sg, Gs - 3), corner(mf, mg, Gm - 3)

    print(f"  design intent C1/C2      : {ideal:6.2f} dB ({C1_UM2/C2_UM2:.1f}x)")
    print(f"  simulated  passband      : {Gs:6.2f} dB ({10**(Gs/20):.1f}x),  -3 dB at {fcs:.3f} Hz")
    print(f"  measured   passband      : {Gm:6.2f} dB ({10**(Gm/20):.1f}x),  -3 dB at {fcm:.3f} Hz")
    print(f"  shortfall  sim -> silicon: {Gs-Gm:6.2f} dB ({10**((Gs-Gm)/20):.2f}x)")
    print(f"  implied C2 on silicon    : {C1_UM2/10**(Gm/20):.1f} um^2 vs {C2_UM2} drawn "
          f"({C1_UM2/10**(Gm/20)/C2_UM2:.1f}x)")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogx(sf, sg, "-", lw=1.8, color="C1", label=f"simulated ({Gs:.1f} dB)")
    ax.semilogx(mf, mg, "o-", ms=5, lw=1.6, color="C0", label=f"measured ({Gm:.1f} dB)")
    ax.axhline(ideal, ls="--", lw=1, color="0.6")
    ax.text(sf.min() * 1.5, ideal + 0.8, f"$C_1/C_2$ = {ideal:.1f} dB", color="0.45", fontsize=8)
    ax.annotate("", xy=(30, Gm), xytext=(30, Gs),
                arrowprops=dict(arrowstyle="<->", color="C3", lw=1.3))
    ax.text(34, (Gs + Gm) / 2, f"{Gs-Gm:.1f} dB", color="C3", fontsize=10, va="center")
    ax.set_xlim(0.05, 1e6); ax.set_ylim(0, ideal + 6)
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("gain [dB]")
    ax.grid(True, which="both", alpha=.3); ax.legend(loc="lower center", fontsize=9)
    ax.set_title("LNA gain: simulation vs silicon")
    fig.tight_layout(); fig.savefig(args.png, dpi=150)
    print(f"\nplot: {args.png}")


if __name__ == "__main__":
    sys.exit(main())
