#!/usr/bin/env python3
"""The three ECG recordings, named once.

Task M. Four separate acquisitions of the array underlie the reservoir results,
they differ in encoder, beat set and evoked activity by more than a factor of
five, and for four rounds of reference analysis review they were confused with one
another -- a rate dispersion from one was quoted against another, and a dead-time
exclusion computed on one was applied to all three. Every analysis script should
name which of these it is reading, and every number the reference analysis quotes should
be traceable to one of them.

    from reservoir_datasets import ACC, DIM, NSV, REF25, describe
    sp, y, T = load(DIM.path)          # the D_eff recording, 282 events/window

All three predate two firmware changes: they were taken on the 10 MHz crystal
with the FLASH-resident read-out and HOST-ARRIVAL timestamps (before commit
905c46c, 2026-07-10). The consequence is measured, not assumed: every
inter-event interval in all three lies on an 11.986 ms lattice with a two-period
floor (deff_refractory_ablation.py).

    python3 reservoir_datasets.py      # verify the recorded properties on disk
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Recording:
    tag: str
    path: str
    beats: int
    records: tuple
    classes: str
    coding: str
    events_per_window: float
    rate_cv: float
    used_for: str
    notes: str = ""
    _fields: tuple = field(default=(), repr=False)


ACC = Recording(
    tag="ACC",
    path="reservoir_spikes_nv_delta.npz",
    beats=60,
    records=("106", "119", "208", "221", "233"),
    classes="NV",
    coding="delta",                       # one shared level-crossing stream
    events_per_window=49.2,
    rate_cv=0.641,
    used_for="the reference table (binary N/PVC accuracy, 0.987 +/- 0.027 inter-patient) and "
             "the random-projection control in the reference analysis.",
)

DIM = Recording(
    tag="DIM",
    path="reservoir_spikes_nv_randproj.npz",
    beats=60,
    records=("106", "119", "208", "221", "233"),
    classes="NV",
    coding="delta_randproj",              # per-neuron projected level-crossing
    events_per_window=281.8,
    rate_cv=0.495,
    used_for="the reference analysis in full: the reference table, the reference figure, every D_eff number in the "
             "reference, the operating-point dispersion match, and the acquisition "
             "lattice measurement.",
    notes="The per-neuron input projection is what makes the comparison against a "
          "projected software LIF like-for-like; it is also why this recording "
          "carries 5.7x the events of ACC on the same beats. The 282 events/window "
          "figure that excludes a 250 ms per-event dead time is THIS recording's.",
)

NSV = Recording(
    tag="NSV",
    path="reservoir_spikes_nsv_structured_hw.npz",
    beats=90,
    records=("200", "208", "209", "222", "223", "232", "233"),
    classes="NSV",
    coding="structured_hw",
    events_per_window=81.1,
    rate_cv=0.262,
    used_for="the reference analysis, the cost frontier: OP1's accuracy in the reference figure, its 81.1 "
             "events/beat in the energy accounting (constants.py reads this via "
             "reservoir_frontier.json), and the rate dispersion OP2 is matched to.",
)

REF25 = Recording(
    tag="REF25",
    path="reservoir_spikes_ref25_2026-08-12.npz",
    beats=60,
    records=("106", "119", "208", "221", "233"),
    classes="NV",
    coding="delta_randproj",              # same encoder as DIM, so directly comparable
    events_per_window=1249.3,
    rate_cv=0.482,                        # all 16, the registry convention; 0.394 over the 15 live
    used_for="the reference analysis. The reference acquisition: the first recording taken at an "
             "operating point selected in advance for margin and then SHOWN to "
             "reproduce (1.4% on a fixed 10-beat subset across the acquisition, "
             "against a tolerance fixed beforehand).",
    notes="The first recording on the corrected read-out AND at a characterised "
          "operating point. No 11.99 ms lattice: 0% of intervals on an integer "
          "multiple, per-trial phase concentration 0.092, min ISI 1.2-4.6 ms. "
          "15/16 neurons live -- n14 is dark under every bias set on disk and is "
          "excluded rather than revived, because reviving it needs a hand-edited "
          "per-neuron value sitting near an edge, which is the fragility that made "
          "the earlier operating point unreproducible. Hot at 39 Hz: this is the "
          "point the die can HOLD, not the quietest one it can reach.",
)

ALL = (ACC, DIM, NSV, REF25)
BY_PATH = {r.path: r for r in ALL}


def describe(path):
    """Recording for an npz path, or None if it is not one of the four."""
    return BY_PATH.get(path.split("/")[-1])


def _verify():
    import numpy as np
    ok = True
    for r in ALL:
        d = np.load(r.path, allow_pickle=True)
        sp = d["spikes"]
        n, nb = sp.shape
        ev = sum(len(np.asarray(sp[j, b])) for j in range(n) for b in range(nb)) / nb
        rates = np.array([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb
                          for j in range(n)])
        cv = rates.std() / rates.mean()
        recs = tuple(sorted(set(map(str, d["records"]))))
        checks = [
            ("beats", nb, r.beats),
            ("records", recs, r.records),
            ("coding", str(d["coding"]), r.coding),
            ("events/window", round(ev, 1), r.events_per_window),
            ("rate CV", round(float(cv), 3), r.rate_cv),
        ]
        bad = [c for c in checks if c[1] != c[2]]
        print(f"{r.tag:4s} {r.path:42s} {'OK' if not bad else 'MISMATCH'}")
        for name, got, want in bad:
            print(f"       {name}: on disk {got!r}, declared {want!r}")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_verify())
