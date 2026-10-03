# OSCAR architecture

This document gives the chip-level picture. It is deliberately short; the
authoritative sources are the design itself (`design/xschem/`, `design/verilog/`,
`design/gds/`) and the firmware (`firmware/neuron_handshake/neuron_handshake.c`).

## The die at a glance

A SkyWater 130-nm Caravel/Caravan chip. The analog *user* area holds the
chemosensing front-end and the neuromorphic array; the digital management core
is a VexRiscv RV32I with SRAM and boot flash. A memory-mapped bridge wires the
core to the analog array over a four-phase (req/ack) address-event interface.

```
        electrode pad (TiO2)                reference pad
              |                                   |
        +-----v------+                      +-----v------+
        |  pad LNA   |     +----------+     |  pin LNA   |
        +-----+------+     |          |     +-----+------+
              |            |  biases  |           |
              +------------>  (DACs)  <-----------+
                           +----+-----+
                                |
                    +-----------v------------+
                    |  16 x LIF neuron somas |
                    |  512 4-bit DPI synapses|
                    |  (16 exc + 16 inh each)|
                    +-----------+------------+
                                |
                     digital 4-phase AER (req/ack)
                                |
              +-----------------v------------------+
              |   VexRiscv RV32I + SRAM + flash    |
              |   timestamps, routes, recurrence   |
              +-----------------+------------------+
                                |
                          UART (spike stream)
                                |
                         host / FT4232H
```

## Analog domain

- **Front-end.** An exposed TiO₂-coated chemosensing electrode pad plus a
  reference pad. Two capacitively coupled low-noise amplifiers (one pad-coupled,
  one pin-driven) buffer the transduced signal into the array.
- **Neurons.** Sixteen analog leaky-integrate-and-fire somas. Firing rate is set
  by bias currents (`vleakn`, `ifdcp`, …), **not** by synapse weight.
- **Synapses.** 512 current-mode differential-pair-integrator (DPI) synapses:
  16 excitatory + 16 inhibitory per neuron, each with a 4-bit weight word. The
  weight is programmed over the digital bridge; it behaves as a cliff, not a
  smooth rate knob (see `HARDWARE_TRAPS.md`).
- **Biases.** The only analog input to the chip is a set of DAC-programmed bias
  voltages, driven bit-banged over FTDI. There are 23 DAC channels.

## Digital domain

- **Core.** VexRiscv RV32I (`rv32i_zicsr`), running from SRAM after boot from
  flash. The AER read-out drain is copied to SRAM at boot (`.ramtext` →
  `dff2`), so the handshake is not limited by XIP flash (`req/ack ≈ 250 ms` in
  flash vs `≈ 50 µs` from SRAM; only a couple of µs is CPU work, the rest is
  analog neuron reset dead time).
- **AER.** A four-phase req/ack handshake pulls one spike address at a time off
  the array. Spikes carry a 21-bit Timer0 timestamp. Over UART they are sent as
  self-synchronizing 4-byte packets: `byte0 = 0x80 | DROP | STALL | addr`, then
  a 21-bit timestamp in three 7-bit bytes (MSB=0).
- **Stimuli.** Stimuli are staged as address/sign words and emitted by the core;
  a Poisson mode and a regular-train mode let the chip pace itself. On-die
  recurrence can be wired with `SET_RECUR`, so spikes from one neuron inject `c`
  spikes into another via the dedicated recurrent synapse.

## Interfaces (FT4232H channel map)

| Channel | Use |
|---|---|
| A | SPI flash |
| B + C | DAC bit-bang (bias programming) |
| D | UART (spike stream + command bytes) |

The DLL/clock selection and CPU reset travel over the Caravel housekeeping SPI
(HK-SPI), a separate path.

## Firmware ↔ host contract

The firmware accepts one-byte UART commands (`PROGRAM_SYNC`, `SPIKE_SETUP`,
`SEND_SPIKE`, `POISSON`/`POISSONSTOP`, `SET_RECUR`, `RECUR_CTRL`, `SPIKE_MASK`,
`MONITOR_SYNC`, `REPORT_HS`, `CALRUN`, `SET_PULSE`, `BURST`, the Timer0
microbenchmarks, and the on-core LIF emulation opcodes). The host layer in
`host/` is the only owner of the FTDI device; it translates human/line commands
into these bytes and reconstructs absolute spike time from the 21-bit tick
delta plus the host clock. See `firmware/README.md` for the opcode table and
`docs/BRINGUP.md` for the flashing flow.
