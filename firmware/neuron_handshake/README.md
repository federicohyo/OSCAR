# Neuron Handshake Firmware

RISC-V firmware for the Caravan SoC that implements a 4-phase AER (Address Event Representation) handshake to capture spikes from the analog neuron array (x5 block, 16 neurons).

## Status: Working

The 4-phase handshake is functional. The firmware runs a diagnostic verification sequence, then enters a continuous handshake loop where the LED blinks on each neuron spike.

## Readout modes (`STREAM_SPIKES`)

Both modes use the same SRAM-resident `aer_drain()` for the req/ack cycle. The
compile-time `STREAM_SPIKES` flag (Makefile, default 1) controls UART output:

| | `STREAM_SPIKES=1` (default, deferred streaming) | `STREAM_SPIKES=0` (fast reservoir) |
|---|---|---|
| Build | `make hex` | `make STREAM_SPIKES=0 hex` |
| Readout drain | `aer_drain()` from **SRAM** (`.ramtext`, dff2) + ring buffer | `aer_drain()` from **SRAM** (same) |
| req/ack servicing (measured) | **~50 µs** (SRAM, `handshake_result.json`) | **~50 µs** (same) |
| Per-spike UART stream | **yes** (deferred: ring buffer flushed in main loop) | **counts-only** |
| Spike packet format | 4-byte: `0x80\|addr`, raw 16-bit Timer0 ticks (3×7-bit) | — |
| Spike-rate readout | UART stream **and** `aer_counts[16]` (0xDB) | `aer_counts[16]` (0xDB) † |
| Use it for | **timestamped spike stream at full array speed** | max throughput / 0xDB timing / reservoir |

† `aer_counts` is read back via command `0xDB` (`report_hs`): sends
`HS t=<ticks> n=<count> c0..c15` and resets accumulators.

### How the SRAM readout works (fast build)

- `sections.lds` adds a `.ramtext` section that **loads from flash but runs from
  dff2** (0x400–0x600), with a **page-aligned LMA** (`AT(ALIGN(...,256))`). If the
  LMA shares a 256 B flash page with `.data`, the page-oriented flasher writes
  overlapping pages and **verify flags a mismatch**. `.ramnoinit` (NOLOAD, dff2)
  holds `aer_counts`.
- `crt0_vex.S` copies `.ramtext` from flash to dff2 at boot (mirrors the `.data` copy).
- `aer_drain()` is marked `section(".ramtext"), noinline` and keeps **all calls
  inlined** (post-ack settle + AER address decode are inlined by hand) — any `jal`
  would fetch from XIP and defeat the point. Verify with `objdump` that
  `<aer_drain>` is at a dff2 address with every `jal`/`call` inlined.
- dff2 is **above** `_fstack` (0x400), so `.ramtext` and `aer_counts` are immune to
  the 1 KB-RAM stack-overflow trap that clobbers low `.bss`.

_AER handshake speedup (measured 2026-07-08), in order of impact: (1) **SRAM
execution** — the drain was XIP-instruction-fetch bound; running it from SRAM took
req/ack ~10 ms → ~0.4 ms. (2) post-ack settle `delay_loop(10)`→`2`. (3) Phase-3
req-low bound `100000`→`8`. The bound alone barely helped (31→48 spk/s); the real
cost was XIP fetch, hence (1)._

### How deferred streaming works (`STREAM_SPIKES=1`)

The SRAM drain and the UART output are **decoupled** by a ring buffer:

1. **Capture (in `aer_drain`, SRAM, ~10 cycles):** after ack deassert, in the
   ~48 µs analog-reset dead time while the neuron resets and can't re-assert
   req, the drain pushes a packed entry into a ring buffer in dff2:
   ```
   spike_ring[head] = (neuron_id << 16) | (timer0_ticks & 0xFFFF);
   head = (head + 1) & 7;
   ```
   This adds <1% to the 50.3 µs/handshake cycle and leaves the critical
   ack→deassert path untouched.

2. **Flush (in `main` loop, XIP, off the critical path):** the main loop drains
   the ring to UART as 4-byte packets with raw 16-bit Timer0 ticks. Division
   happens host-side — the host converts ticks to µs (ticks / 10 at 10 MHz).

3. **Ring buffer:** 8 slots in `.ramnoinit` (dff2). At 1133 spikes/s that's
   ~7 ms of buffering. When full, the oldest unflushed spike is replaced so the
   newest lands in the ring. `aer_counts[16]` still tallies exact per-neuron
   totals — the ring is purely for the timestamped stream.

4. **Memory:** `.ramtext` grows by ~40 B (timestamp instructions inlined into
   `aer_drain`), `.ramnoinit` grows by 38 B (8×4 B ring + 2 B head/tail + 4 B
   last_aer). Total dff2 usage fits within 512 B.

### Membrane potential captured from the analog neuron array

![Membrane potential on scope](../../pics/20260307_162733.jpg)

Scope capture showing the membrane potential of a neuron via the x5 monout_array monitor output (pin 50). The characteristic integrate-and-fire waveform is clearly visible: slow integration ramp followed by a sharp spike and reset.

#### Bias values used for this capture

| Bias | Voltage | Type | Function |
|------|---------|------|----------|
| ifdcp | 1.72V | PMOS | Current source |
| vleakn | 0.302V | NMOS | Leak current |
| vtaun | 0.3V | NMOS | Membrane time constant (N) |
| vtaup | 1.78V | PMOS | Membrane time constant (P) — OFF |
| vthrdp | 1.78V | PMOS | Threshold (P) — OFF |
| vthrdn | 0.3V | NMOS | Threshold (N) |
| vrefn | 0.2V | NMOS | Reference |
| buffermonp | 0.2V | PMOS | Monitor buffer bias |
| vepulseextp | 1.78V | PMOS | Excitatory pulse — OFF |
| vipulseextp | 1.78V | PMOS | Inhibitory pulse — OFF |
| JExcWn[0:3] | 0.1V | NMOS | Excitatory weights |
| JInhWp[0:3] | 1.78V | PMOS | Inhibitory weights — OFF |

### Verified diagnostic output

```
5  — start
1  — Phase 1: ack asserted
2  — Phase 1: ack deasserted
1  — Phase 2: req = 1 (neuron has pending spike)
1  — Phase 3: ack asserted
3  — Phase 3a: req dropped after ack (HANDSHAKE SUCCESS)
4  — Phase 3b: req returned HIGH (full 4-phase cycle complete)
1  — Phase 4: la1_oenb readback = 0x1 (correct)
5  — Phase 4: la2_oenb readback = 0x5 (correct)
5  — entering handshake loop
... fast blinking = neurons firing continuously
```

### Root cause of the earlier handshake issue: `reg_la*_oenb` polarity

The `reg_la*_oenb` register name suggests active-LOW ("output enable bar"), but the gate-level netlist (`caravan_core.v`) proves it is **active-HIGH**:

```verilog
// CPU output path: AND3 gate
la_data_in_core[N] = la_oe_storage[N] & la_out_storage[N] & power_good
```

`la_oe_storage[N] = 1` → CPU output **ENABLED**. The earlier firmware had the polarity inverted: it set bits to 1 for user-driven signals and 0 for CPU-driven signals (ack, CLK, Da, nRes), which held ack at 0 at the AND3 gate so it stayed off the neuron. The corrected polarity below enables the CPU outputs.

Similarly, `reg_la*_iena` is counterintuitive: the AND2B gate inverts `la_ien_storage`, so `iena = 0` → input **ENABLED**. Setting all iena registers to 0 enables all inputs.

| Register        | Wire name      | Polarity                                    |
|-----------------|----------------|---------------------------------------------|
| `reg_la*_oenb`  | la_oe_storage  | **1 = CPU output ENABLED** (active-HIGH)    |
| `reg_la*_iena`  | la_ien_storage | **0 = input ENABLED** (inverted by AND2B)   |

#### Corrected values

```c
reg_la0_oenb = 0x007F8000;  // bits 15-22: req_inp, neu_addr[0:3], exc, setW, resetW
reg_la1_oenb = 0x10000000;  // bit 28: x5.ack
reg_la2_oenb = 0x0000005C;  // bits 2,3,4,6: CLK, Da, nRes, x3.ack
```

### LED polarity

The management GPIO LED is **active-LOW**: `reg_gpio_out = 0` → LED ON, `reg_gpio_out = 1` → LED OFF.

### Diagnostic blink reference

| Phase | Test | Success blinks | Alert blinks |
|-------|------|---------------|----------------|
| Start | — | 5 | — |
| 1 | CPU→user: drive ack HIGH/LOW | 1 (asserted), 2 (deasserted) | — |
| 2 | user→CPU: read req after nRes release | 1 (req=1) | 3 fast (req=0) |
| 3a | Handshake: assert ack, check req drops | 3 (req dropped) | 6 (req held HIGH) |
| 3b | Handshake: deassert ack, check req returns | 4 (req returned) | 7 (req held LOW) |
| 3 (timeout) | req stayed LOW | 10 (error) | — |
| 4 | Readback la1_oenb top nibble | N = nibble (expect 1) | 15 (if zero) |
| 4 | Readback la2_oenb nibble 1 | N = nibble (expect 5) | 15 (if zero) |
| Loop start | — | 5 | — |

## Building

```bash
cd firmware/neuron_handshake
make clean hex
```

Requires RISC-V toolchain at `/opt/riscv32i/bin/` (symlinks to riscv64 multilib).

## Running

```bash
# Full test: flash firmware + program DACs + reset CPU
python run_neuron_test.py

# Skip DAC programming
python run_neuron_test.py --skip-dac

# Skip firmware flash
python run_neuron_test.py --skip-flash

# Override a single bias
python run_neuron_test.py --override vtaup 0.85

# Sweep a bias (observe LED rate)
python run_neuron_test.py --sweep ifdcp 1.68 1.28 -0.1
```

**Important ordering**: Flash firmware first, then program DACs, then reset CPU so firmware starts with biases already set. The script handles this automatically.

## Architecture

### Signal mapping (LA bus)

| Signal | Direction | Register | Bit |
|--------|-----------|----------|-----|
| x5.req_o | chip -> CPU | reg_la1_data_in | 29 |
| x5.ack | CPU -> chip | reg_la1_data | 28 |
| x5.aer_o[0:1] | chip -> CPU | reg_la1_data_in | 30,31 |
| x5.aer_o[2:3] | chip -> CPU | reg_la2_data_in | 0,1 |
| x5.CLK | CPU -> chip | reg_la2_data | 2 |
| x5.Da | CPU -> chip | reg_la2_data | 3 |
| nRes (shared) | CPU -> chip | reg_la2_data | 4 |
| x3.req | chip -> CPU | reg_la2_data_in | 5 |
| x3.ack_out | CPU -> chip | reg_la2_data | 6 |

### Bias pads (gpio_analog)

See `run_neuron_test.py` DEFAULT_BIASES table. Key conventions:
- PMOS biases: OFF = VDD (1.78V)
- NMOS biases: OFF = 0.0V
- All bias pads configured as `GPIO_MODE_USER_STD_ANALOG` (0x000a)

### Monitor select (x8 block)

4-bit shift register (dfrtp_1 flip-flops) controlled by Da/CLK, feeds decoder_4_to_16, selects one of 16 neurons via analog mux to monout (io_analog[0], mprj_io[14]).
- nRes resets flip-flops (active-low async reset)
- buffermonp bias must be LOW for output buffer to work

### 4-phase handshake protocol

```
1. CPU polls req (bit 29 of reg_la1_data_in)
2. When req goes HIGH: CPU asserts ack (bit 28 of reg_la1_data)
3. CPU waits for req to go LOW (handshake complete)
4. CPU deasserts ack
5. Repeat
```

### UART binary protocol (4-byte self-synchronizing packets)

Each spike is transmitted as a 4-byte packet over UART:

```
Byte 0: 0x80 | (neuron_id & 0x0F)   ← MSB=1 marks packet start
Byte 1: (ts >> 14) & 0x7F           ← MSB=0, top 2 bits of 16-bit Timer0 ticks
Byte 2: (ts >>  7) & 0x7F           ← MSB=0, middle 7 bits
Byte 3: (ts      ) & 0x7F           ← MSB=0, low 7 bits
```

- **16-bit raw Timer0 ticks**: host reassembles `ts = (b1<<14)|(b2<<7)|b3`,
  computes `delta = prev_ts - ts` (mod 65536), then `delta_us = delta / 10`
  (Timer0 = 10 MHz). Max delta before wrap = 65536 ticks = 6.55 ms.
- **Self-synchronizing**: any byte with MSB=1 is always a packet start; MSB=0 is always data. If sync is lost, the parser discards bytes until the next 0x80+ byte.
- **Division is host-side**: the rv32i divides in software, so sending raw ticks keeps the software `div10` loop off the hot path.
- **Throughput**: at 9600 baud, ~240 packets/s (4 bytes × ~0.42 ms/byte). Spikes beyond the ring buffer or UART FIFO capacity give way to the newest entry; `aer_counts[16]` (0xDB) retains exact per-neuron totals.
