# Hardware traps

These cost real bench time to rediscover. Read before touching the hardware.

## Clock, baud and the DLL

- **Baud is welded to the core clock: `baud = 960 × f_MHz`; the spike-stream
  ceiling is ≈ `24 × f_MHz` spk/s.**
- Reachable core clocks are `100/N` MHz (N = 2..7): **50, 33, 25, 20 MHz**, plus
  **10 MHz** (bare crystal, no DLL).
- `F_CPU_MHZ` (a compile-time flag scaling `delay_loop` pulse widths and Timer0
  constants) **must match in three places**: the firmware build, the
  `neuron_bridge.py` clock (`CARAVAN_CLK_MHZ`, default 50), and
  `run_neuron_test.py --clock`. A mismatch is a **silent comms failure** — bytes
  talk past the chip.
- **The on-die DLL does NOT survive a power cycle.** After power-up the chip is
  back on the 10 MHz crystal. Re-engage the DLL for 20/25/33/50 MHz.
- **Flash only on the crystal.** Flash SCK scales with the core clock, so
  flashing at 50 MHz is unsafe; every HK-SPI sequence must be followed by a CPU
  reset toggle.
- **Synaptic efficacy is clock-dependent — retune biases at the clock you run.**
  Delivered charge (excitatory *and* inhibitory) falls as the core clock rises.
  It is a gain shift, not a kill: a 10 MHz bias point at 50 MHz leaves excitation
  ~5.5× weaker and inhibition under the noise floor, which looks exactly like
  "inhibition is broken". **Always fire an excitatory positive control before
  concluding anything about inhibition.**

## Spikes, masking and the AER encoder

- **The AER encoder can latch — and not only as all-ones.** Every spike may read
  as neuron 15, *or* every response may come back **one address low** (stim 2→1,
  …, stim 0→15 wrapping, half the array apparently silent). Both survive reset,
  reflash and bias reprogramming at every clock; **only a physical power cycle
  clears them.**
- **Run an unmasked 16-neuron addressing scan (`MASK 65535`, stimulate k, check
  the reported address is k) BEFORE and AFTER every long acquisition.** Without
  it the failure is silent: a per-neuron mask keyed to the intended address turns
  a mislabelled array into an apparently dead one, or a plausible recording of
  the *wrong* neurons. Free post-hoc check: if a masked run returned healthy
  counts for all 16, addressing was correct throughout (a shifted encoder + mask
  = zero spikes).

## Biases, weights and polarity

- **The weight word is not a rate knob — it is a cliff.** w=15 → ~28 Hz median,
  w=7 → 15/16 silent, w=3 / w=1 → all silent, w=15 restores all 16. Set firing
  rate with the biases (`vleakn`/`ifdcp`), never with the synapse weight.
- **Load `.biases` files through `neuron_bridge.apply_bias_dict` / the bridge's
  per-channel `B` command**, never `run_neuron_test`'s single `VREF=1.78` path —
  that halves the 7 NMOS biases (NMOS channels clamp to `VREFN=0.89`) and neurons
  fire far too fast.
- **Bias polarity:** NMOS (`vleakn`, `vtaun`, `vrefn`, `JExcWn*`) higher V = more
  current (OFF = 0 V); PMOS (everything else, incl. `ifdcp`, `JInhWp*`) lower V =
  more current (OFF = VDD ≈ 1.78 V).
- **Don't reflash while tuning biases** — `run_neuron_test` resets all 23 DACs.
  Bench scripts reload biases per neuron, so reflashing between *runs* is fine;
  DACs persist across CPU reset.

## Process / ownership

- **Only one process may own the FTDI.** Kill stray `neuron_bridge.py` / scope
  clients / the GUI before starting a bench script:
  `pkill -f "[n]euron_bridge.py"` (the bracket avoids matching your own shell).
- **Reservoir accuracy and D_eff are strongly operating-point dependent.**
  Re-acquiring the same 60 beats at 2.7× drive moved inter-patient accuracy
  0.913→0.700 and D_eff 18.1→14.9. Any reservoir comparison must hold the
  *firing rate* fixed, not just the bias file.
- Every long acquisition should be bracketed by an **unmasked AER addressing
  scan** and should assert `drops == stalls == 0`; both failure modes are silent
  otherwise. Run long acquisitions in `screen`.

## chip0 specifics

- On one board (chip0) the **on-die flash passthrough is dead** (ESD; `JEDEC =
  ffffff`, `status = 0xff`, while HK-SPI and XIP boot still work — the `0xC4`
  passthrough mux is the broken part). Its flash is frozen with a pinned 25 MHz
  image. Rules: never run the 50 MHz bring-up on it; always
  `CARAVAN_CLK_MHZ=25`. Reflash path is an external Raspberry Pi wired to the
  motherboard J15 header. This is board-specific, not a chip-architecture fact.

## Large files (available on request)

Three oversized design files are intentionally omitted to stay under GitHub's
file/size limits (no Git LFS is configured):

| Omitted file | Size |
|---|---|
| `design/gds/RF_block.gds` | ~140 MB |
| `design/mag/RF_block.mag` | ~137 MB |
| `design/mag/neuron_synapse_array_with_input_output_logic_v2_flat.mag` | ~104 MB |

They are one-off test structures / a flattened layout, not needed to open or
understand the DUT wrapper. Request them from the authors.

## GUI note

The C++ `ofxCaravanViewer` GUI and the `ofxXORtuning` / `ofxNARMATuning` forks
are **not shipped**. They need openFrameworks and are excluded. The bench and
reservoir workflows in this repository are the headless Python path
(`host/neuron_bridge.py` + `host/meas_common.py` + the `measurements/` scripts).
