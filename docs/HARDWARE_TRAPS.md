# Hardware traps

These cost real bench time to rediscover. Read before touching the hardware.

## Clock, baud and the DLL

- **Baud is welded to the core clock: `baud = 960 × f_MHz`; the spike-stream
  ceiling is ≈ `24 × f_MHz` spk/s.**
- Reachable core clocks are `100/N` MHz (N = 2..7): **50, 33, 25, 20 MHz**, plus
  **10 MHz** (bare crystal, DLL disengaged).
- `F_CPU_MHZ` (a compile-time flag scaling `delay_loop` pulse widths and Timer0
  constants) **must match in three places**: the firmware build, the
  `neuron_bridge.py` clock (`CARAVAN_CLK_MHZ`, default 50), and
  `run_neuron_test.py --clock`. Match it in all three so the bytes reach the
  chip.
- **The on-die DLL setting resets on a power cycle.** After power-up the chip
  runs on the 10 MHz crystal. Re-engage the DLL for 20/25/33/50 MHz.
- **Flash only on the crystal.** Flash SCK scales with the core clock, so
  flashing at 50 MHz is unsafe; every HK-SPI sequence must be followed by a CPU
  reset toggle.
- **Synaptic efficacy is clock-dependent — retune biases at the clock you run.**
  Delivered charge (excitatory *and* inhibitory) falls as the core clock rises.
  It is a gain shift: a 10 MHz bias point at 50 MHz leaves excitation ~5.5×
  weaker and inhibition under the noise floor, which can masquerade as inactive
  inhibition. **Always fire an excitatory positive control before concluding
  anything about inhibition.**

## Spikes, masking and the AER encoder

- **The AER encoder can latch — in more than one way.** Every spike may read
  as neuron 15, *or* every response may come back **one address low** (stim 2→1,
  …, stim 0→15 wrapping, half the array apparently silent). Both survive reset,
  reflash and bias reprogramming at every clock; **a physical power cycle clears
  them.**
- **Run an unmasked 16-neuron addressing scan (`MASK 65535`, stimulate k, check
  the reported address is k) BEFORE and AFTER every long acquisition.** This
  makes a latched encoder visible: a per-neuron mask keyed to the intended
  address can turn a mislabelled array into an apparently dead one, or a
  plausible recording of the *shifted* neurons. Free post-hoc check: if a masked
  run returned healthy counts for all 16, addressing was correct throughout (a
  shifted encoder + mask = zero spikes).

## Biases, weights and polarity

- **The weight word is a cliff.** w=15 → ~28 Hz median, w=7 → 15/16 silent,
  w=3 / w=1 → all silent, w=15 restores all 16. Set firing rate with the biases
  (`vleakn`/`ifdcp`).
- **Load `.biases` files through `neuron_bridge.apply_bias_dict` / the bridge's
  per-channel `B` command.** The single `VREF=1.78` path in `run_neuron_test`
  halves the 7 NMOS biases (NMOS channels clamp to `VREFN=0.89`) and neurons
  fire far too fast.
- **Bias polarity:** NMOS (`vleakn`, `vtaun`, `vrefn`, `JExcWn*`) higher V = more
  current (OFF = 0 V); PMOS (everything else, incl. `ifdcp`, `JInhWp*`) lower V =
  more current (OFF = VDD ≈ 1.78 V).
- **Tune biases in a step separate from reflashing** — `run_neuron_test` resets
  all 23 DACs. Bench scripts reload biases per neuron, so reflashing between
  *runs* is fine; DACs persist across CPU reset.

## Process / ownership

- **One process owns the FTDI at a time.** Kill stray `neuron_bridge.py` / scope
  clients / the GUI before starting a bench script:
  `pkill -f "[n]euron_bridge.py"` (the bracket avoids matching your own shell).
- **Reservoir accuracy and D_eff are strongly operating-point dependent.**
  Re-acquiring the same 60 beats at 2.7× drive moved inter-patient accuracy
   0.913→0.700 and D_eff 18.1→14.9. Any reservoir comparison must hold the
   *firing rate* fixed alongside the bias file.
- Every long acquisition should be bracketed by an **unmasked AER addressing
  scan** and should assert `drops == stalls == 0`; each check catches a silent
  condition otherwise. Run long acquisitions in `screen`.

## chip0 specifics

- On one board (chip0) the **on-die flash passthrough reads back as ESD-damaged**
  (`JEDEC = ffffff`, `status = 0xff`, while HK-SPI and XIP boot still work — the
  `0xC4` passthrough mux is the affected part). Its flash is frozen with a pinned
  25 MHz image. Rules: use the 25 MHz bring-up on it and always
  `CARAVAN_CLK_MHZ=25`. Reflash path is an external Raspberry Pi wired to the
  motherboard J15 header. This is a board-level detail rather than a
  chip-architecture fact.
