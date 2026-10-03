#!/usr/bin/env python3
"""Autonomous NARMA-reservoir bias tuner -- shared core (analysis + objective + constrained BO).

The reservoir operating point lives on a narrow edge-of-chaos ridge and depends jointly on ~5-6
bias channels that are mostly in weak inversion (I ~ exp(V/UT): tiny dV -> large dI). Two design
consequences drive this whole module:

  1. SEARCH IN VOLTS. The DAC's voltage axis is the log-current axis, so working in volts
     linearises the exponential -> a smooth landscape a GP surrogate can fit. Steps are small and
     BOUNDED (a narrow window around a known-good point), always narrow.
  2. TWO SENSING CHANNELS. Spike counts (AER) give the task memory (MC0/1/2, rate, drift); the
     scope membrane gives the mechanism (tau_eff, and railing that spike-counts hide -- a "silent"
     neuron can be saturated-high, needing the OPPOSITE correction to a dead one).

This file is backend-agnostic: `analyze()` and `objective()` operate on a raw `Observation`
(stream spike counts + u + optional membrane traces) produced by either the SimBackend (validation)
or the ChipBackend (bridge NARMACOLLECT + scope). Both exercise the identical analysis, so the
objective validated on the sim is the objective the chip runs.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Callable
import numpy as np

WEAK_INV_UT = 0.033          # effective weak-inversion voltage scale (V per e-fold) used by the sim map


# ----------------------------------------------------------------------------- data containers
@dataclass
class Observation:
    """Raw signals from a backend for one bias vector."""
    counts: np.ndarray                       # (M, 16) per-frame per-neuron spike counts (RECURRENT stream)
    u: np.ndarray                            # (M,) the input stream
    tstep: float                             # frame duration (s)
    counts_ff: Optional[np.ndarray] = None   # (M, 16) FEEDFORWARD stream (recurrence off), SAME u -> rec-ff gap
    membrane: Optional[List[Tuple[np.ndarray, np.ndarray]]] = None  # per sampled neuron: (t, v) impulse trace


@dataclass
class Diagnostics:
    mc0: float; mc1: float; mc2: float       # CV memory capacity at lags 0,1,2 (RECURRENT reservoir)
    rate: float                              # mean spikes/frame/neuron on the 2nd half
    drift: float                             # (rate_2ndhalf - rate_1sthalf)/rate_1sthalf ; ~0 = saturation-free
    n_live: int                              # neurons with non-trivial activity
    tau_eff: float = float("nan")            # membrane decay time constant (frames), from scope/impulse
    railed_frac: float = 0.0                 # fraction of sampled neurons stuck-high (saturated)
    mc1_ff: float = float("nan")             # FEEDFORWARD MC at lag 1 (recurrence off) -> rec-ff gap
    mc2_ff: float = float("nan")             # FEEDFORWARD MC at lag 2
    raw: Dict = field(default_factory=dict)


# ----------------------------------------------------------------------------- analysis
def cv_mc(X: np.ndarray, u: np.ndarray, lag: int, wash: int, n_splits: int = 3,
         lam: float = 1e-2) -> float:
    """Cross-validated memory capacity at `lag`: corr^2 between the OUT-OF-FOLD ridge-readout
    predictions of u(t-lag) and the truth, over all frames >= wash. K-fold CV (out-of-fold preds)
    makes this robust to the single-split noise a BO would otherwise exploit -- the whole reason the
    M=120 objective overfit. This is the capacity that predicts NARMA (full linear readout)."""
    M = len(u)
    tgt = np.zeros(M); tgt[lag:] = u[:M - lag] if lag > 0 else u
    idx = np.arange(max(wash, lag), M)
    Xv, yv = X[idx], tgt[idx]
    n = len(idx); d = X.shape[1]
    if n < d + 2 * n_splits + 5:
        return 0.0
    fold = n // n_splits
    preds = np.zeros(n)
    for s in range(n_splits):
        te = np.zeros(n, bool)
        te[s * fold:(n if s == n_splits - 1 else (s + 1) * fold)] = True
        tr = ~te
        A = np.hstack([Xv[tr], np.ones((tr.sum(), 1))])
        W = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ yv[tr])
        preds[te] = np.hstack([Xv[te], np.ones((te.sum(), 1))]) @ W
    if preds.std() < 1e-9 or yv.std() < 1e-9:
        return 0.0
    c = np.corrcoef(preds, yv)[0, 1]
    return 0.0 if np.isnan(c) else float(c ** 2)


def fit_tau_eff(t: np.ndarray, v: np.ndarray) -> float:
    """Fit an exponential decay v(t) ~ A*exp(-t/tau)+c to the membrane trace after an input impulse;
    return tau in the same time units as t. Shared by the sim and the real scope trace. Robust to a
    baseline offset and to a railed (flat-high) trace (returns inf-ish -> caught as saturation)."""
    v = np.asarray(v, float); t = np.asarray(t, float)
    if v.ptp() < 1e-6:                                   # flat -> railed or dead; nothing to fit
        return float("inf") if v.mean() > 0.5 * (v.max() + 1e-9) else 0.0
    c = v.min()
    a = v - c
    peak = int(np.argmax(a))
    tt, aa = t[peak:], a[peak:]
    aa = np.maximum(aa, 1e-9)
    mask = aa > 0.05 * aa[0]                             # fit the decaying portion above 5% of peak
    if mask.sum() < 3:
        return 0.0
    try:
        slope = np.polyfit(tt[mask] - tt[0], np.log(aa[mask]), 1)[0]
    except Exception:
        return 0.0
    if slope >= -1e-6:                                   # ~flat or rising -> decay flat = railed/latched
        return float("inf")
    tau = -1.0 / slope
    return float(tau) if tau < 10.0 * len(t) else float("inf")   # absurdly long = effectively railed


def analyze(obs: Observation, wash: int = 100) -> Diagnostics:
    counts, u = obs.counts, obs.u
    M = len(u)
    wash = min(wash, max(5, M // 4))                     # clamp washout to stream length (short tuning streams)
    cut = (M + wash) // 2
    live = [k for k in range(counts.shape[1]) if counts[wash:, k].std() > 1e-6]
    X = counts[:, live] if live else counts
    mc = [cv_mc(X, u, lag, wash) for lag in (0, 1, 2)]
    h1 = counts[wash:cut].mean(); h2 = counts[cut:].mean()
    rate = float(h2)
    # symmetric relative drift, BOUNDED in [-2,2] (stays finite when the first half is ~empty,
    # e.g. a saturation runaway where all spikes land in the second half)
    drift = float((h2 - h1) / (0.5 * (h1 + h2) + 1e-6))
    # feedforward MC on the SAME live neurons + input -> the rec-ff gap the objective rewards
    mc1_ff = mc2_ff = float("nan")
    if obs.counts_ff is not None:
        Xf = obs.counts_ff[:, live] if live else obs.counts_ff
        mc1_ff = cv_mc(Xf, u, 1, wash)
        mc2_ff = cv_mc(Xf, u, 2, wash)
    # scope-derived mechanism signals
    tau_eff = float("nan"); railed = 0.0
    if obs.membrane:
        taus = [fit_tau_eff(t, v) for (t, v) in obs.membrane]
        finite = [x for x in taus if np.isfinite(x) and x > 0]
        tau_eff = float(np.median(finite)) if finite else float("inf")
        railed = float(np.mean([not (np.isfinite(x) and x > 0) for x in taus]))
    return Diagnostics(mc[0], mc[1], mc[2], rate, drift, len(live), tau_eff, railed,
                       mc1_ff, mc2_ff, raw={"mc": mc, "live": live})


# ----------------------------------------------------------------------------- objective
@dataclass
class ObjectiveCfg:
    # Reward RECURRENCE-SPECIFIC fading memory (the whole point of NARMA) over generic memory:
    #  - the rec-ff GAP (recurrent MC minus feedforward MC at lag>=1) is weighted highest, so a point
    #    where recurrence does nothing (rec~=ff) scores near zero.
    #  - absolute rec MC1/MC2 kept as a smaller term (need real memory above the noise floor).
    #  - MC0 capped (encoding is necessary, with an instant-echo kept from winning); n_live = dimensionality.
    w_gap1: float = 1.5; w_gap2: float = 1.0             # rec-ff memory gap (recurrence must contribute)
    w_mc0: float = 0.20; mc0_cap: float = 0.40           # capped encoding credit
    w_mc1: float = 0.5; w_mc2: float = 0.3               # absolute rec memory (secondary)
    w_nlive: float = 0.30                                # dimensionality reward (n_live/16)
    rate_lo: float = 0.30; rate_hi: float = 3.0          # spikes/frame/neuron band (bounded activity)
    drift_max: float = 0.35                              # |drift| beyond this = saturating/runaway (tightened)
    railed_max: float = 0.25                             # fraction of neurons stuck-high tolerated
    n_live_min: int = 4                                  # diversity floor (few neurons drive at the start point)
    tau_lo: float = 0.8; tau_hi: float = 4.0             # tau_eff band (frames): fading memory horizon
    penalty: float = 2.0                                 # weight on each constraint violation


def objective(diag: Diagnostics, cfg: ObjectiveCfg = ObjectiveCfg()) -> Tuple[float, bool, Dict]:
    """Penalised scalar (maximise): memory reward minus soft constraint violations. Returns
    (J, feasible, breakdown). Feasible = all hard constraints satisfied; BO still gets a smooth
    penalised signal off-feasible so it can climb back onto the ridge."""
    gap1 = (diag.mc1 - diag.mc1_ff) if np.isfinite(diag.mc1_ff) else 0.0   # recurrence-specific memory
    gap2 = (diag.mc2 - diag.mc2_ff) if np.isfinite(diag.mc2_ff) else 0.0
    reward = (cfg.w_gap1 * gap1 + cfg.w_gap2 * gap2
              + cfg.w_mc0 * min(diag.mc0, cfg.mc0_cap) + cfg.w_mc1 * diag.mc1 + cfg.w_mc2 * diag.mc2
              + cfg.w_nlive * (diag.n_live / 16.0))
    v = {}
    v["rate_lo"] = max(0.0, cfg.rate_lo - diag.rate)
    v["rate_hi"] = max(0.0, diag.rate - cfg.rate_hi)
    v["drift"] = max(0.0, abs(diag.drift) - cfg.drift_max)
    v["railed"] = max(0.0, diag.railed_frac - cfg.railed_max)
    v["n_live"] = max(0.0, cfg.n_live_min - diag.n_live) / max(1, cfg.n_live_min)
    if np.isnan(diag.tau_eff):
        pass                                             # scope unused -> tau constraints left to the scope pass
    elif np.isfinite(diag.tau_eff):
        v["tau_lo"] = max(0.0, cfg.tau_lo - diag.tau_eff) / cfg.tau_lo
        v["tau_hi"] = max(0.0, diag.tau_eff - cfg.tau_hi) / cfg.tau_hi
    else:
        v["tau_hi"] = 1.0                                # inf tau_eff = railed/latched -> penalise
    total_viol = sum(v.values())
    feasible = total_viol < 1e-9
    # clip J to a floor: a catastrophic point (e.g. saturation runaway) is just "bad" -- feeding a
    # huge negative outlier to the GP surrogate destroys its normalisation and blinds the BO.
    J = max(reward - cfg.penalty * total_viol, -3.0)
    return float(J), bool(feasible), {"reward": reward, "viol": v, "total_viol": total_viol}


# ----------------------------------------------------------------------------- constrained BO
@dataclass
class Channel:
    name: str
    center: float          # known-good operating point (V)
    half_span: float       # +/- window (V); small (weak inversion!), e.g. 0.03-0.06


class ConstrainedBO:
    """Compact Bayesian optimisation over a bounded box in VOLT space, warm-started at the channel
    centres, with a trust region that shrinks on stalls. Penalised-scalar objective (constraints
    folded into `objective`), single GP surrogate, Expected-Improvement acquisition sampled on a
    Sobol-ish random cloud inside the current trust region. Deliberately dependency-light
    (sklearn GP only) and robust to noisy evaluations (GP alpha)."""

    def __init__(self, channels: List[Channel], seed: int = 0, tr_init: float = 1.0,
                 alpha: float = 1e-3, n_cand: int = 512):
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import Matern, ConstantKernel, WhiteKernel
        self.ch = channels
        self.d = len(channels)
        self.lo = np.array([c.center - c.half_span for c in channels])
        self.hi = np.array([c.center + c.half_span for c in channels])
        self.center = np.array([c.center for c in channels])
        self.rng = np.random.default_rng(seed)
        self.tr = tr_init                                # trust-region fraction of the full box
        self.n_cand = n_cand
        self.X: List[np.ndarray] = []
        self.Y: List[float] = []
        kern = (ConstantKernel(1.0) * Matern(length_scale=np.ones(self.d), nu=2.5)
                + WhiteKernel(noise_level=alpha))
        self.gp = GaussianProcessRegressor(kernel=kern, normalize_y=True, n_restarts_optimizer=2,
                                           random_state=seed)
        self._since_improve = 0

    def _unit(self, x):    # volts -> [0,1]^d for the GP (scale-free)
        return (x - self.lo) / (self.hi - self.lo + 1e-12)

    def ask(self) -> np.ndarray:
        """Next bias vector (volts) to evaluate."""
        if len(self.X) < max(4, self.d + 1):            # initial design: Latin-ish random in full box
            return self.lo + self.rng.random(self.d) * (self.hi - self.lo)
        self.gp.fit(np.array([self._unit(x) for x in self.X]), np.array(self.Y))
        best = max(self.Y)
        # candidate cloud inside the trust region around the incumbent best
        xbest = self.X[int(np.argmax(self.Y))]
        span = (self.hi - self.lo) * self.tr
        cand = xbest + (self.rng.random((self.n_cand, self.d)) - 0.5) * span
        cand = np.clip(cand, self.lo, self.hi)
        mu, sd = self.gp.predict(np.array([self._unit(c) for c in cand]), return_std=True)
        sd = np.maximum(sd, 1e-9)
        z = (mu - best) / sd
        from scipy.stats import norm
        ei = (mu - best) * norm.cdf(z) + sd * norm.pdf(z)
        return cand[int(np.argmax(ei))]

    def tell(self, x: np.ndarray, y: float) -> None:
        improved = (len(self.Y) == 0) or (y > max(self.Y) + 1e-6)
        self.X.append(np.asarray(x, float)); self.Y.append(float(y))
        if improved:
            self._since_improve = 0
            self.tr = min(1.0, self.tr * 1.3)           # expand on progress
        else:
            self._since_improve += 1
            if self._since_improve >= 3:
                self.tr = max(0.08, self.tr * 0.6)      # shrink on stall (focus the ridge)
                self._since_improve = 0

    def best(self) -> Tuple[np.ndarray, float]:
        i = int(np.argmax(self.Y))
        return self.X[i], self.Y[i]


def channels_to_dict(channels: List[Channel], x: np.ndarray) -> Dict[str, float]:
    return {c.name: float(v) for c, v in zip(channels, x)}
