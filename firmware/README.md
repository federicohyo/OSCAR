# OSCAR firmware

The RISC-V management firmware runs on the VexRiscv RV32I core and is the only
thing that talks to the analog array's four-phase AER interface. It programs
synapse weights, stages and fires stimuli, masks neurons, wires on-die
recurrence, timestamps output spikes, and streams them over UART.

## Layout

| Path | Contents |
|---|---|
| `neuron_handshake/` | Main firmware: `neuron_handshake.c`, `Makefile`, `README.md`, and prebuilt `binaries/*.hex`. |
| `neuron_handshake/binaries/` | Pinned prebuilt images: per-clock (`_10/20/25/33/50MHz`) plus functional variants (`_arraybench`, `_lifram`, `_lifrun`, `_olfQ16`, `_olfQ8`, `_ramsendspike`, `_prePulseFix`). |
| `common/` | Shared boot/SoC files: `crt0_vex.S`, `sections.lds`, `isr.c`, `stub.c`, headers (`csr.h`, `defs.h`, `soc.h`, …), and `generated/`. |
| `variants/` | Optional alternative builds: `numeric_lif`, `olfaction_kernel`, `op3_kernel`, `blink`, `singleneuron`. |

## Toolchain

Ubuntu `gcc-riscv64-unknown-elf` (multilib). The Makefile builds `rv32i` via
`-march=rv32i_zicsr -mabi=ilp32` with `TOOLCHAIN_PREFIX=riscv64-unknown-elf`.
(`zicsr` is needed because `crt0_vex.S` uses CSR instructions.)

## Build

```bash
cd firmware/neuron_handshake
make clean hex                      # default F_CPU_MHZ=50, STREAM_SPIKES=1
make clean hex F_CPU_MHZ=25         # 25 MHz DLL image
make clean hex F_CPU_MHZ=10         # bare-crystal image
make STREAM_SPIKES=0 hex            # counts-only / max-throughput build
```

Produces `neuron_handshake.hex` and `neuron_handshake.lst` (build outputs; not
committed). The checked-in `binaries/` retain the per-clock images the chip
ships with, because the DLL/clock pairing matters.

## Clock caveat

- `F_CPU_MHZ` must match in three places: the firmware build, the
  `neuron_bridge.py` clock (`CARAVAN_CLK_MHZ`), and `run_neuron_test.py --clock`.
  A mismatch is a silent comms failure (`baud = 960 × f_MHz`).
- Reachable clocks are `100/N` MHz (N = 2..7) → 50/33/25/20 MHz, plus 10 MHz
  (crystal).
- **The DLL does not survive a power cycle.** After power-up, flash on the
  crystal then engage the DLL (`host/bringup_50.sh`). Stream ceiling ≈
  `24 × f_MHz` spk/s.
- The read-out drain runs from SRAM (`.ramtext` copied to `dff2` at boot).

## Flashing — the real path

`host/run_neuron_test.py` / `host/bringup_50.sh` / `host/test_at_clock.sh`, built
on **`host/riscvprog.py`** (`class HKSPI`, plus `AD5664RBitBang`, `Config`) over
the Caravel housekeeping SPI. Every HK-SPI sequence must be followed by a CPU
reset toggle.

> **Stale upstream target.** The `flash:` target in
> `neuron_handshake/Makefile` still references `../util/caravel_hkflash.py`,
> which **does not exist**. It is intentionally a no-op that errors out; use the
> host tools instead. See `docs/BRINGUP.md`.

## UART command set (one-byte opcodes)

| opcode | name | function |
|---|---|---|
| `0xF0` | PROGRAM_SYNC | set 4-bit weight of synapse `s`, sign `exc/nexc` |
| `0xE0` | SPIKE_SETUP | stage route (`s → d`, sign) of next stimulus |
| `0xE1` | SEND_SPIKE | emit one (or `n`) staged stimulus spike(s) |
| `0xE2` / `0xE3` | POISSON start/stop | on-chip Poisson train, programmable rate |
| `0xE4` / `0xE5` | SYNFIRE start/stop | synfire-chain pacing |
| `0xE6` | COINCIDENCE | coincidence/facilitation bench path |
| `0xE9` | SET_RECUR | append recurrence `s → d`, `c` spikes, sign `e` (≤128) |
| `0xEA` | RECUR_CTRL | recurrence off / on / clear |
| `0xED` | TRAIN_START | regular train, 24-bit tick period |
| `0xEC` | SPIKE_MASK | 16-bit per-neuron streaming mask |
| `0xD0` | MONITOR_SYNC | select neuron for spike counts |
| `0xDB` | REPORT_HS | handshake timing + per-neuron counts (resets) |
| `0xD5` | CALRUN | on-chip burst-count calibration (opcode + 10 operands) |
| `0xDC` | SET_PULSE | scale stimulus pulse width (charge per event) |
| `0xDD` | BURST | paced burst for calibration |
| `0xEB` / `0xEE` / `0xEF` | BENCH / OLFBENCH / ARRAYBENCH | Timer0 cycle-count microbenchmarks |
| `0xD1` / `0xD2` | LIFRUN / LIFRUN2 | on-core LIF emulation |
| `0xE7` | LIFRAM | SRAM-resident LIF timing |

Spike packets over UART are 4 bytes: header `0x80 | DROP | STALL | addr`, then a
21-bit timestamp in three 7-bit bytes.

The host-side line commands (`B`, `M`, `P`, `S`, `TRIGRUN`, `MASK`, `RECORD`,
`ECGRUN`, `SETRECUR`, `RECURCTRL`, `POISSON`, `CALRUN`, `QUIT`, …) are
translated to these bytes by `host/neuron_bridge.py`.
