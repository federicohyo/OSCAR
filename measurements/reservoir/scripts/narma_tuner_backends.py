#!/usr/bin/env python3
"""Measurement backends for the NARMA bias tuner. Both return an `Observation` (stream spike counts
+ u + membrane impulse traces), so `narma_tuner.analyze()`/`objective()` treat them identically.

  SimBackend  -- software validation. Maps bias VOLTS -> spiking-reservoir knobs through an
                 EXPONENTIAL (weak-inversion) transfer I ~ exp(V/UT), so the optimiser faces the same
                 stiff, narrow-ridge landscape (dead <-> edge-of-chaos <-> railed over a few tens of
                 mV) it will face on silicon. Reuses narma_chipsim.run_reservoir.
  ChipBackend -- the real thing (drop-in for the bench): applies biases via the bridge `B` command,
                 runs the on-die `NARMACOLLECT` stream, and captures membrane impulse traces on a few
                 neurons with scope_usb. Written to be run at the bench under the safety protocol;
                 exercised on hardware.
"""
import time
import numpy as np
from narma_tuner import Observation, WEAK_INV_UT
from narma_chipsim import run_reservoir


# ============================================================================ SIM
class SimBackend:
    """Volts -> knobs via weak-inversion exponentials, then the spiking chip-sim. The map is
    monotone and physically-flavoured (uncalibrated to the chip): its job is to reproduce the CHARACTER
    of the tuning landscape (exponential sensitivity, a narrow feasible ridge), so the optimiser +
    objective loop is validated end-to-end before the chip."""

    # nominal operating point (V) the exponentials are referenced to (near the saved narma point)
    V0 = {"vleakn": 0.268, "JExcWn": 0.62, "vtaun": 0.60, "vthrdn": 0.70, "JInhWp": 0.90}

    def __init__(self, N: int = 16, M: int = 800, frame_steps: int = 20, seed: int = 1,
                 tstep: float = 0.1, n_scope: int = 4):
        self.N, self.M, self.frame_steps, self.seed, self.tstep = N, M, frame_steps, seed, tstep
        self.n_scope = n_scope
        self.rng = np.random.default_rng(seed)
        self.u = self.rng.uniform(0, 0.5, M)

    def _knobs(self, theta):
        """Map bias volts to (tau_m, in_gain, rho, vth, bias_drive). Higher exc current -> higher
        recurrence rho AND input gain (toward chaos); more leak -> shorter tau_m; higher threshold
        -> fewer spikes. Exponential in V (weak inversion) except the threshold (a voltage compare)."""
        def I(name, v):                                  # weak-inversion current relative to nominal
            return np.exp((v - self.V0[name]) / WEAK_INV_UT)
        i_exc = I("JExcWn", theta.get("JExcWn", self.V0["JExcWn"]))
        i_leak = I("vleakn", theta.get("vleakn", self.V0["vleakn"]))
        i_tau = I("vtaun", theta.get("vtaun", self.V0["vtaun"]))
        i_inh = I("JInhWp", theta.get("JInhWp", self.V0["JInhWp"]))
        # threshold: ~linear in volts around nominal (a comparator level rather than a WI current)
        vth = 1.0 * (1.0 + 6.0 * (theta.get("vthrdn", self.V0["vthrdn"]) - self.V0["vthrdn"]))
        vth = float(np.clip(vth, 0.4, 3.0))
        tau_m = float(np.clip(40.0 / i_leak, 4.0, 400.0))         # more leak current -> shorter tau
        tau_syn_boost = float(np.clip(i_tau, 0.3, 3.0))          # longer synapse tau -> more integration
        in_gain = float(np.clip(0.4 * i_exc, 0.02, 8.0))
        rho = float(np.clip(1.4 * i_exc / (0.5 + i_inh), 0.0, 1.6))   # nominal ~0.93 (edge); exc->chaos, inh tempers
        bias_drive = float(np.clip(0.015 * i_exc, 0.0, 0.6))
        return tau_m * tau_syn_boost, in_gain, rho, vth, bias_drive

    def _run_counts(self, theta, u, recur=True):
        TAU, in_gain, rho, vth, bias_drive = self._knobs(theta)
        if not recur:
            rho = 0.0                                    # feedforward: neuron-neuron coupling off
        # DPI input-synapse low-pass (the chip's real fading-memory mechanism the bare chipsim omits):
        # tau_syn set by vtaun (i_tau). Filtering the input injects u(t-1),u(t-2)... into frame t, so
        # the per-frame count carries lagged input -> MC1/MC2 > 0, TUNABLE by vtaun. Too much smoothing
        # trades MC0 for MCk (the optimiser must find the balance) -> a genuine memory ridge.
        i_tau = np.exp((theta.get("vtaun", self.V0["vtaun"]) - self.V0["vtaun"]) / WEAK_INV_UT)
        tau_syn = float(np.clip(1.5 * i_tau, 0.2, 12.0))          # frames
        alpha = float(np.exp(-1.0 / tau_syn))
        u_f = np.empty_like(u); acc = 0.0
        for t in range(len(u)):
            acc = alpha * acc + (1.0 - alpha) * u[t]
            u_f[t] = acc
        return run_reservoir(u_f, self.N, TAU, vth, 2.0, in_gain, rho, 0.3,
                             self.frame_steps, seed=self.seed, bias=bias_drive)

    def _membrane_impulse(self, theta):
        """Sub-threshold impulse response on a few neurons: ONE input frame, then free leaky decay
        (NO resting bias, so the impulse component is what we fit -> tau_eff = the membrane time
        constant in FRAMES). If the impulse drive pins v at the rail the trace is flat -> fit_tau_eff
        returns inf -> flagged as railed/saturated (the mechanism spike-counts hide)."""
        TAU, in_gain, rho, vth, bias_drive = self._knobs(theta)
        tau_frames = TAU / self.frame_steps                      # dt-units -> frames (consistent readout)
        n_imp = 60
        u_imp = np.zeros(n_imp); u_imp[5] = 0.5                   # single impulse at frame 5
        rng = np.random.default_rng(self.seed)
        gains = in_gain * (0.5 + rng.random(self.N))
        decay = np.exp(-1.0 / max(tau_frames, 1e-3))
        traces = []
        v = np.zeros(self.N)
        V = np.zeros((n_imp, self.N))
        for t in range(n_imp):
            v = v * decay + gains * u_imp[t]                     # impulse-only drive
            v = np.clip(v, 0.0, 2.0)                              # rail at 2.0 (saturation ceiling)
            V[t] = v
        tsc = np.arange(n_imp, dtype=float)
        for k in range(min(self.n_scope, self.N)):
            traces.append((tsc, V[:, k].copy()))
        return traces

    def measure(self, theta: dict) -> Observation:
        counts = self._run_counts(theta, self.u, recur=True)
        counts_ff = self._run_counts(theta, self.u, recur=False)
        membrane = self._membrane_impulse(theta)
        return Observation(counts=counts, u=self.u, tstep=self.tstep,
                           counts_ff=counts_ff, membrane=membrane)


# ============================================================================ CHIP
class ChipBackend:
    """Real bench backend: bridge NARMACOLLECT (AER stream) + scope_usb membrane capture. Applies
    the candidate biases on top of a loaded base operating point. Run only with the chip up at
    50 MHz and biases loaded; obeys the safety protocol (positive-control canary is the caller's
    responsibility; on a wedge, stop and flag)."""

    def __init__(self, bridge, base_biases: dict, dens: int, rec_w: int, in_w: int = 15,
                 M: int = 120, tstep: float = 0.1, kmax: int = 8, scope_neurons=(5, 7, 13, 14),
                 impulse_burst: int = 200, impulse_rate: float = 200.0, use_scope: bool = True,
                 monitor_neuron=None, verbose: bool = True):
        self.b = bridge                                  # a live meas_common.BridgeSession
        self.base = dict(base_biases)
        self.dens, self.rec_w, self.in_w = dens, rec_w, in_w
        self.M, self.tstep, self.kmax = M, tstep, kmax
        self.scope_neurons = list(scope_neurons)
        self.impulse_burst, self.impulse_rate = impulse_burst, impulse_rate
        self.use_scope = use_scope
        self.monitor_neuron = monitor_neuron             # route this neuron's membrane to the scope pin
        self.inh_frac = 0.2                              # fraction of recurrent conns inhibitory (runaway lever)
        self.verbose = verbose
        self._scope = None

    def _log(self, *a):
        if self.verbose:
            print(*a, flush=True)

    @staticmethod
    def _find_usbtmc():
        import glob
        devs = sorted(glob.glob("/dev/usbtmc*"))
        return devs[0] if devs else "/dev/usbtmc0"

    def _scope_open(self):
        import os, fcntl, sys
        dev = self._find_usbtmc()
        try:
            fd = os.open(dev, os.O_RDWR)
            try: fcntl.ioctl(fd, (91 << 8) | 2)          # clear any stuck transaction
            except OSError: pass
            os.close(fd)
        except OSError as e:
            self._log(f"  scope device-clear on {dev} failed: {e}")
        sys.path.insert(0, ".")
        from scope_usb import Scope
        sc = Scope(); sc.connect()
        sc.channel(1, scale=0.3, offset=0.9, coupling="DC")
        sc.timebase(scale=1e-2, position=0.0)
        sc.trigger_edge(source=1, level=1.05, slope="POS", sweep="AUTO")
        sc.run()
        self._scope = sc
        self._log(f"  scope open on {dev}")

    def _apply(self, theta: dict):
        merged = dict(self.base); merged.update(theta)
        for name, v in theta.items():                    # only push the tuned channels (fast)
            self.b.bias(name, float(v))
        if self.monitor_neuron is not None:              # drive the scope monitor pin (live human view)
            self.b.monitor(int(self.monitor_neuron))
        time.sleep(0.4)

    def _collect_stream(self, recur: int):
        M = self.M; tstep_ms = int(round(self.tstep * 1000))
        inh_pct = int(round(self.inh_frac * 100))
        self.b.send(f"NARMACOLLECT {recur} {M} {tstep_ms} {self.kmax} {self.dens} {self.rec_w} "
                    f"{self.in_w} {inh_pct}")
        state = np.zeros((M, 16), int); u = np.zeros(M); seen = np.zeros(M, bool)
        deadline = time.time() + M * self.tstep + 60
        cond = "rec" if recur else "ff "
        nxt = max(1, M // 4)
        done_line = None
        while time.time() < deadline:
            try:
                line = self.b.out_q.get(timeout=1.0)
            except Exception:
                continue
            if line.startswith("NARMAROW "):
                p = line.split(); t = int(p[1])
                if 0 <= t < M:
                    u[t] = float(p[2]); state[t] = [int(x) for x in p[3:19]]; seen[t] = True
                    if int(seen.sum()) >= nxt:
                        self._log(f"    [{cond}] streaming {int(seen.sum())}/{M} frames...")
                        nxt += max(1, M // 4)
            elif line.startswith("NARMACOLLECTDONE"):
                done_line = line; break
            elif line.startswith("ERROR"):
                raise RuntimeError(f"bridge: {line}")
        if done_line:
            self._log(f"    [{cond}] {done_line.strip()}")
        elif int(seen.sum()) < M:
            self._log(f"    [{cond}] WARNING: only {int(seen.sum())}/{M} frames before timeout")
        return state, u

    def _membrane_impulse(self):
        """Capture the membrane on a few neurons under a short excitatory burst -> decay, fit tau_eff
        (and detect railing) offline. Uses the scope_diag_neuron.py pattern."""
        import threading
        if self._scope is None:
            self._scope_open()
        self._log(f"    scope: capturing membrane on neurons {self.scope_neurons}...")
        traces = []
        for k in self.scope_neurons:
            self.b.send("RECURCTRL 0")                    # isolate a single neuron's own membrane
            self.b.monitor(k); time.sleep(0.2)
            self.b.program_weight(0, 15, exc=True); self.b.route(0, k, exc=True); time.sleep(0.03)
            self.b.drain(max_lines=200000)
            stop = threading.Event()
            def stim():
                per = 1.0 / self.impulse_rate
                for _ in range(self.impulse_burst):
                    if stop.is_set(): break
                    self.b.fire(1); time.sleep(per)
            th = threading.Thread(target=stim); th.start()
            time.sleep(0.15)
            try:
                t, v = self._scope.read_waveform(1, points=2000)
                traces.append((np.asarray(t, float), np.asarray(v, float)))
            except Exception as e:
                traces.append((np.arange(2), np.zeros(2)))   # off read -> flat -> flagged railed/dead
                print(f"  scope read n{k} failed: {e}")
            stop.set(); th.join()
        return traces

    def measure(self, theta: dict) -> Observation:
        self._apply(theta)
        # BOTH conditions on the SAME fixed-seed u -> the rec-ff memory gap the objective rewards
        state_rec, u = self._collect_stream(recur=1)
        state_ff, _ = self._collect_stream(recur=0)
        membrane = self._membrane_impulse() if self.use_scope else None
        return Observation(counts=state_rec, counts_ff=state_ff, u=u, tstep=self.tstep,
                           membrane=membrane)

    def close(self):
        try:
            if self._scope is not None: self._scope.close()
        except Exception:
            pass
