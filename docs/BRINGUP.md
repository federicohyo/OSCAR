# Bring-up and flashing

## Toolchain

Ubuntu's `gcc-riscv64-unknown-elf` (multilib). The firmware Makefile builds
`rv32i` via `-march=rv32i_zicsr -mabi=ilp32` with
`TOOLCHAIN_PREFIX=riscv64-unknown-elf`. (`zicsr` is needed because
`crt0_vex.S` uses CSR instructions.)

## Build the firmware

```bash
cd firmware/neuron_handshake
make clean hex                  # default F_CPU_MHZ=50, STREAM_SPIKES=1
make clean hex F_CPU_MHZ=25     # 25 MHz DLL image
make clean hex F_CPU_MHZ=10     # bare-crystal image
make STREAM_SPIKES=0 hex        # counts-only / max-throughput build
```

This produces `neuron_handshake.hex` and `neuron_handshake.lst`. Prebuilt
per-clock images live in `firmware/neuron_handshake/binaries/`
(`*_10MHz.hex`, `*_20MHz.hex`, `*_25MHz.hex`, `*_33MHz.hex`, `*_50MHz.hex`, plus
functional variants such as `_lifram`, `_lifrun`, `_olfQ16`, `_olfQ8`,
`_ramsendspike`, `_prePulseFix`, `_arraybench`).

> **Clock caveat.** `F_CPU_MHZ` must match in three places: the firmware build,
> `neuron_bridge.py` (`CARAVAN_CLK_MHZ`, default 50), and
> `run_neuron_test.py --clock`. Match it in all three so the bytes reach the
> chip (`baud = 960 × f_MHz`). See `docs/HARDWARE_TRAPS.md`.

## Flashing — the real path

```bash
# After a power cycle: flash the 50 MHz image + engage the DLL
./host/bringup_50.sh

# Or the general bring-up driver
./.venv-meas/bin/python3 host/run_neuron_test.py            # --clock 50 default
./.venv-meas/bin/python3 host/run_neuron_test.py --clock 10 --skip-dac  # crystal

# Flash a prebuilt per-clock image and launch
./host/test_at_clock.sh 25
```

The underlying implementation is **`host/riscvprog.py`** (`class HKSPI`, plus
`AD5664RBitBang` and `Config`) over the Caravel housekeeping SPI. It is imported
by `run_neuron_test.py` as `from riscvprog import HKSPI, AD5664RBitBang, Config`.
Every HK-SPI sequence must be followed by a CPU reset toggle. The firmware
read-out drain runs from SRAM (`.ramtext` copied to `dff2` at boot).

> **Legacy Makefile target.** `firmware/neuron_handshake/Makefile`'s `flash:`
> target references `python3 ../util/caravel_hkflash.py`; use
> `host/run_neuron_test.py` / `host/riscvprog.py` for the working flash path
> (the target reports a message pointing to the host tools).

## Host bridge

`host/neuron_bridge.py` is the single owner of the FT4232H. It speaks line
commands, e.g.:

```
B <name> <value>       # program a bias DAC
M <neuron>             # select monitor neuron
P <syn> <w> exc|nexc   # program a 4-bit synapse weight
S <syn> <n> exc|nexc   # stage a spike route
TRIGRUN <hz>           # paced stimulus
MASK <hex>             # 16-bit per-neuron streaming mask
RECORD / ECGRUN
SETRECUR s d c e       # on-die recurrence: s fires -> c spikes to d
RECURCTRL 0|1
POISSON <b3..b0> / POISSONSTOP
CALRUN <10 bytes>
QUIT
```

`host/meas_common.py` wraps it as `BridgeSession` for bench/reservoir scripts.

## Sanity checks

```bash
# UART 4-byte packet codec unit tests
./.venv-meas/bin/python3 host/test_spike_timestamp.py
```

Before and after every long acquisition, run the unmasked 16-neuron addressing
scan (see `docs/HARDWARE_TRAPS.md`) and confirm `drops == stalls == 0`.
