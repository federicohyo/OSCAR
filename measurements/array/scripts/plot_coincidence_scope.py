#!/usr/bin/env python3
"""Plot the two coincidence-detection membrane traces captured on the DSO-X 2002A.

Two inputs are delivered to one neuron separated by dt; the membrane is read out on
the analog monitor pin. At dt=5 ms the two EPSPs summate past threshold and the
neuron spikes; at dt=8 ms they summate to a subthreshold peak and it does not fire.
The captures are aligned on the first-EPSP onset and overlaid.
"""

import os
import numpy as np

DATA = "data/array"
FILES = [
    ("scope_12_coincidence5ms.csv", 5, "tab:red"),
    ("scope_11_coincidence8ms.csv", 8, "tab:blue"),
]
OUT = "measurements/array/figures/coincidence_membrane.pdf"


def load(path):
    d = np.genfromtxt(path, delimiter=",", skip_header=2)
    return d[:, 0] * 1e3, d[:, 1] * 1e3  # ms, mV


def onset_time(t, v, thresh_mv=60.0):
    """Time of the first rise > baseline+thresh (the first EPSP onset)."""
    base = np.median(v[:200])
    above = np.where(v > base + thresh_mv)[0]
    return t[above[0]] if above.size else 0.0


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"pdf.fonttype": 42})

    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    for fname, dt, color in FILES:
        t, v = load(os.path.join(DATA, fname))
        t0 = onset_time(t, v)
        tt = t - t0
        m = (tt >= -3) & (tt <= 30)
        ax.plot(tt[m], v[m], color=color, linewidth=1.2,
                label=rf"$\Delta t$ = {dt} ms")
    ax.set_xlabel("Time (ms)", fontsize=11)
    ax.set_ylabel("Membrane potential (mV)", fontsize=11)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=9, frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    fig.savefig(os.path.splitext(OUT)[0] + ".png", dpi=150, bbox_inches="tight")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
