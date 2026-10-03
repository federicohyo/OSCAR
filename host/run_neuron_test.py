#!/usr/bin/env python3
"""Neuron circuit test: program DAC biases and flash handshake firmware.

Usage:
    python run_neuron_test.py              # Program DACs + flash firmware
    python run_neuron_test.py --skip-dac   # Skip DAC programming
    python run_neuron_test.py --skip-flash # Skip firmware flash
    python run_neuron_test.py --override Vtaup 0.85  # Override a single bias

Prerequisites:
    - FTDI 4232H connected via USB
    - Board powered, Pi Zero providing 25 MHz clock
    - pyftdi installed (pip install pyftdi)
    - For flashing: neuron_handshake.hex built
      (cd firmware/neuron_handshake && make clean hex)
"""

import argparse
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_DIR = os.path.join(SCRIPT_DIR, "firmware")
sys.path.insert(0, FIRMWARE_DIR)

from riscvprog import HKSPI, AD5664RBitBang, Config

# Default bias table: (dac_id, address, name, voltage)
# All use vref=1.78, half_period_s=2e-6
DEFAULT_BIASES = [
    (1, 0b000, "free",         0.3),
    (1, 0b001, "vtaup",        1.78),     # PMOS → OFF = VDD
    (1, 0b010, "vthrdp",       1.78),     # PMOS → OFF = VDD
    (1, 0b011, "vepulseextp",  1.78),     # PMOS → OFF = VDD

    (2, 0b000, "vleakn",       0.2478),      # NMOS → OFF = 0
    (2, 0b001, "vtaun",        0.3),      # NMOS → OFF = 0
    (2, 0b010, "vipulseextp",  1.78),     # PMOS → OFF = VDD
    (2, 0b011, "JInhWp0",      1.78),     # PMOS → OFF = VDD

    # DAC3 ch A (lna_iref) NOT programmed here — powered down to high-Z below.
    # Pin 54 shared with monout_single; tri-state keeps monitor working.
    # Set lna_iref from the GUI slider when LNA characterisation is needed.
    (3, 0b001, "JInhWp1",      1.78),     # PMOS → OFF = VDD
    (3, 0b010, "JInhWp2",      1.78),     # PMOS → OFF = VDD
    (3, 0b011, "JInhWp3",      1.78),     # PMOS → OFF = VDD

    (4, 0b000, "JExcWn0",      0.0),      # NMOS → OFF = 0
    (4, 0b001, "JExcWn1",      0.0),      # NMOS → OFF = 0
    (4, 0b010, "JExcWn2",      0.0),      # NMOS → OFF = 0
    (4, 0b011, "JExcWn3",      0.0),      # NMOS → OFF = 0

    # LNA biases driven to OFF (dedicated pins rather than high-Z, and separate)
    # Original values: VREF=0.8, VB1=0.79, VB2=0.645, TUNEp=1.1
    (5, 0b000, "VREF",         0.0),      # LNA OFF (NMOS → 0V)
    (5, 0b001, "VB1",          0.0),      # LNA OFF (NMOS → 0V)
    (5, 0b010, "VB2",          0.0),      # LNA OFF (NMOS → 0V)
    (5, 0b011, "TUNEp",        1.78),     # LNA OFF (PMOS → VDD)

    (6, 0b000, "buffermonp",   0.2),     # PMOS → OFF = VDD
    (6, 0b001, "vrefn",        0.25),      # NMOS → OFF = 0
    (6, 0b010, "vthrdn",       0.3),      # NMOS → OFF = 0
    (6, 0b011, "ifdcp",        1.63),     # PMOS → OFF = VDD
]

VREF = 1.78
HALF_PERIOD_S = 2e-6


# --- Step 1: Program DAC biases ---

def program_dac_biases(overrides=None):
    print("=" * 50)
    print("STEP 1: Programming DAC biases")
    print("=" * 50)

    biases = list(DEFAULT_BIASES)

    if overrides:
        for name, voltage in overrides.items():
            found = False
            for i, (dac_id, addr, bname, _) in enumerate(biases):
                if bname == name:
                    biases[i] = (dac_id, addr, bname, voltage)
                    print(f"  Override: {name} = {voltage}V")
                    found = True
                    break
            if not found:
                print(f"  WARNING: Unknown bias name '{name}', ignoring")

    dac = AD5664RBitBang(
        Config.FTDI_B,
        Config.FTDI_C,
        frequency=200_000,
        cs_active_low=True,
    )

    try:
        for dac_id, addr, name, voltage in biases:
            dac.set_dac_voltage(
                dac_id=dac_id,
                voltage=voltage,
                vref=VREF,
                half_period_s=HALF_PERIOD_S,
                address=addr,
            )
            print(f"  DAC{dac_id} addr={addr:#05b} {name:16s} = {voltage:.3f}V")

        print(f"\n  All {len(biases)} DAC channels programmed.")

        # Power down DAC3 ch A (lna_iref) to high-Z — pin 54 shared with monout_single.
        # Moving the lna_iref slider in the GUI will wake the DAC when LNA tuning is needed.
        dac.power_down_dac(dac_id=3, address=0b000, mode=0b11, half_period_s=HALF_PERIOD_S)

        print("  UART uses FTDI channel D (DDBUS0/1); no UART gate pin control needed.")
    finally:
        dac.close()

    print()


# --- Step 2: Flash handshake firmware ---

def flash_handshake_firmware(hex_path=None):
    print("=" * 50)
    print("STEP 2: Flash firmware")
    print("=" * 50)

    if hex_path is None:
        hex_path = os.path.join(FIRMWARE_DIR, "neuron_handshake", "neuron_handshake.hex")
    if not os.path.isfile(hex_path):
        print(f"  ERROR: {hex_path} not found!")
        print("  Build it first:  cd firmware/neuron_handshake && make clean hex")
        return False

    print(f"  Hex file: {hex_path}")

    with HKSPI() as hk:
        hk.cpu_reset_hold()
        print("  CPU held in reset.")

        print("  Resetting flash...")
        hk.flash_reset()
        hk.flash_identify()

        print("  Erasing flash...")
        hk.flash_erase()

        # --- Program ---
        buf = bytearray()
        addr = 0
        nbytes = 0
        total_bytes = 0

        with open(hex_path, 'r') as f:
            x = f.readline()
            while x != '':
                if x[0] == '@':
                    addr = int(x[1:], 16)
                else:
                    values = bytearray.fromhex(x.rstrip())
                    buf[nbytes:nbytes] = values
                    nbytes += len(values)

                x = f.readline()

                if nbytes >= 256 or (x != '' and x[0] == '@' and nbytes > 0):
                    total_bytes += nbytes
                    hk.flash_write_enable()
                    wcmd = bytearray((
                        Config.CARAVEL_PASSTHRU, Config.CMD_PROGRAM_PAGE,
                        (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff,
                    ))
                    wcmd.extend(buf)
                    hk.slave.exchange(wcmd)
                    while hk.is_busy():
                        time.sleep(0.1)
                    print(f"    Wrote page at 0x{addr:06x}")

                    if nbytes > 256:
                        buf = buf[255:]
                        addr += 256
                        nbytes -= 256
                    else:
                        buf = bytearray()
                        addr += 256
                        nbytes = 0

            # Flush remaining bytes
            if nbytes > 0:
                total_bytes += nbytes
                hk.flash_write_enable()
                wcmd = bytearray((
                    Config.CARAVEL_PASSTHRU, Config.CMD_PROGRAM_PAGE,
                    (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff,
                ))
                wcmd.extend(buf)
                hk.slave.exchange(wcmd)
                while hk.is_busy():
                    time.sleep(0.1)
                print(f"    Wrote page at 0x{addr:06x}")

        print(f"  Flashed {total_bytes} bytes total.")

        # --- Verify ---
        print("  Verifying...")
        buf = bytearray()
        addr = 0
        nbytes = 0
        errors = 0

        with open(hex_path, 'r') as f:
            x = f.readline()
            while x != '':
                if x[0] == '@':
                    addr = int(x[1:], 16)
                else:
                    values = bytearray.fromhex(x.rstrip())
                    buf[nbytes:nbytes] = values
                    nbytes += len(values)

                x = f.readline()

                if nbytes >= 256 or (x != '' and x[0] == '@' and nbytes > 0):
                    read_cmd = bytearray((
                        Config.CARAVEL_PASSTHRU, Config.CMD_READ_LO_SPEED,
                        (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff,
                    ))
                    buf2 = hk.slave.exchange(read_cmd, nbytes)
                    if buf == buf2:
                        print(f"    Verify OK at 0x{addr:06x}")
                    else:
                        print(f"    VERIFY FAILED at 0x{addr:06x}")
                        errors += 1

                    if nbytes > 256:
                        buf = buf[255:]
                        addr += 256
                        nbytes -= 256
                    else:
                        buf = bytearray()
                        addr += 256
                        nbytes = 0

            if nbytes > 0:
                read_cmd = bytearray((
                    Config.CARAVEL_PASSTHRU, Config.CMD_READ_LO_SPEED,
                    (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff,
                ))
                buf2 = hk.slave.exchange(read_cmd, nbytes)
                if buf == buf2:
                    print(f"    Verify OK at 0x{addr:06x}")
                else:
                    print(f"    VERIFY FAILED at 0x{addr:06x}")
                    errors += 1

        if errors:
            print(f"  VERIFICATION FAILED ({errors} page(s))")
            return False

        print("  Verification passed.")
        print("  Releasing CPU from reset...")
        hk.cpu_reset_release()

    print()
    print("  RISC-V is now running neuron handshake firmware!")
    # (The LED does NOT blink per spike: reg_gpio_out is written only by blink() at
    # boot and then held off. Claiming otherwise sends people hunting a dead LED.)
    print()
    return True


# --- Main ---

# --- Core clock ---------------------------------------------------------------
# The firmware is built for F_CPU_MHZ (default 10) and its delay_loop pulse widths
# and Timer0 tick constants are scaled to it. The DLL does NOT survive a power
# cycle, so the clock must be engaged after every flash so the pulses match.
# Default is 10 MHz (crystal) because 50 MHz kills the inhibitory synapse; the fast
# readout is clock-independent so 10 MHz loses nothing but the excitatory-only speed.
# Reachable cores are 100/N MHz, N=2..7; fb MUST be 10 so the loop locks.
R_ENA, R_BYP, R_OUT, R_FB = 0x08, 0x09, 0x11, 0x12
FB_LOCK = 10
OUT_DIV = {50: 0x12, 33: 0x1B, 25: 0x24, 20: 0x2D}


def _hk_write(hk, addr, val):
    hk.slave.write([Config.CARAVEL_REG_WRITE, addr, val])


def set_core_clock(mhz):
    """Engage the DLL for `mhz` (or restore the crystal for 10). Resets the CPU."""
    with HKSPI() as hk:
        if mhz == 10:
            _hk_write(hk, R_BYP, 0x01); time.sleep(0.1)
            _hk_write(hk, R_ENA, 0x02)
            _hk_write(hk, R_OUT, 0x12); _hk_write(hk, R_FB, 0x04)
        else:
            _hk_write(hk, R_ENA, 0x00)
            _hk_write(hk, R_FB, FB_LOCK)          # VCO ~100 MHz; fb=4 kills the CPU
            _hk_write(hk, R_OUT, OUT_DIV[mhz])
            _hk_write(hk, R_ENA, 0x01); time.sleep(0.4)
            _hk_write(hk, R_BYP, 0x00); time.sleep(0.1)
        hk.cpu_reset_hold(); time.sleep(0.15); hk.cpu_reset_release()
    time.sleep(0.6)


def main():
    parser = argparse.ArgumentParser(description="Neuron circuit test: DAC biases + handshake firmware")
    parser.add_argument("--clock", type=int, default=50, choices=[10, 20, 25, 33, 50],
                        help="Core clock in MHz after flashing (default 50; must match "
                             "the firmware's F_CPU_MHZ). 10 = stay on the crystal. 50 MHz is "
                             "the reservoir/vowel operating point (all 16 neurons live); "
                             "synaptic efficacy is clock-dependent so retune biases per clock.")
    parser.add_argument("--skip-dac", action="store_true",
                        help="Skip DAC bias programming")
    parser.add_argument("--skip-flash", action="store_true",
                        help="Skip firmware flash")
    parser.add_argument("--hex", default=None,
                        help="Flash this image instead of firmware/neuron_handshake/"
                             "neuron_handshake.hex. Used to pin a known image (e.g. the "
                             "1959 installation) without disturbing the build tree.")
    parser.add_argument("--override", nargs=2, action="append", metavar=("NAME", "VOLTAGE"),
                        help="Override a bias voltage (e.g. --override Vtaup 0.85)")
    parser.add_argument("--sweep", nargs=4, metavar=("NAME", "START", "STOP", "STEP"),
                        help="Sweep a bias voltage (e.g. --sweep ifdcp 1.68 1.28 -0.1)")
    args = parser.parse_args()

    overrides = {}
    if args.override:
        for name, voltage in args.override:
            overrides[name] = float(voltage)

    print()
    print("  Neuron Circuit Test")
    print("  -------------------")
    print()

    # Step 1: Flash firmware (before DACs, since HKSPI may reset FTDI).
    # Always flash ON THE CRYSTAL: flash_phy_clk_divisor is left unwritten by the
    # firmware, so SPI-flash SCK scales with the core and a 50 MHz core would clock
    # the flash 5x. A prior session may have left the DLL engaged, so force it back.
    if not args.skip_flash:
        try:
            set_core_clock(10)
            ok = flash_handshake_firmware(args.hex)
        except Exception as e:
            print(f"  Flash FAILED: {e}")
            return 1
        if not ok:
            return 1
    else:
        print("Skipping firmware flash (--skip-flash).\n")

    # Step 2: DAC biases (after flash, so FTDI channels B/C aren't disturbed)
    if not args.skip_dac:
        try:
            program_dac_biases(overrides=overrides or None)
        except Exception as e:
            print(f"  DAC programming FAILED: {e}")
            return 1
    else:
        print("Skipping DAC programming (--skip-dac).\n")

    # Step 3: Reset CPU so firmware restarts with DAC biases already set
    if not args.skip_dac:
        print("=" * 50)
        print("STEP 3: Resetting CPU (firmware restarts with biases set)")
        print("=" * 50)
        with HKSPI() as hk:
            hk.cpu_reset_hold()
            time.sleep(0.1)
            hk.cpu_reset_release()
        print("  CPU reset done. Firmware now releases nRes after biases.\n")

    # Step 4: Engage the core clock the firmware was built for. Skipping this leaves
    # a 50 MHz image running at 10 MHz: every delay_loop pulse is 5x too long and
    # every Timer0 constant 5x too large, which looks exactly like a bias problem.
    print("=" * 50)
    print(f"STEP 4: Core clock -> {args.clock} MHz")
    print("=" * 50)
    set_core_clock(args.clock)
    baud = 960 * args.clock
    print(f"  Core {args.clock} MHz. UART baud is welded to it: {baud}.")
    print(f"  Streamed spike ceiling: {baud // 40} spk/s.")
    if args.clock != 10:
        print("  NOTE: the DLL does NOT survive a power cycle; the chip returns to")
        print("        the 10 MHz crystal (9600 baud) when power is removed.\n")
    else:
        print()

    # Optional: sweep a single bias
    if args.sweep:
        name, start, stop, step = args.sweep
        start, stop, step = float(start), float(stop), float(step)
        print("=" * 50)
        print(f"SWEEP: {name} from {start:.3f}V to {stop:.3f}V, step {step:.3f}V")
        print("=" * 50)
        print("  Watch LED blink rate — faster = more spikes")
        print("  Press Ctrl+C to stop\n")

        dac = AD5664RBitBang(
            Config.FTDI_B,
            Config.FTDI_C,
            frequency=200_000,
            cs_active_low=True,
        )

        try:
            # Find the DAC channel for this bias name
            dac_id = None
            addr = None
            for d, a, n, _ in DEFAULT_BIASES:
                if n == name:
                    dac_id, addr = d, a
                    break
            if dac_id is None:
                print(f"  ERROR: Unknown bias '{name}'")
                return 1

            v = start
            while (step > 0 and v <= stop + 0.001) or (step < 0 and v >= stop - 0.001):
                dac.set_dac_voltage(
                    dac_id=dac_id,
                    voltage=v,
                    vref=VREF,
                    half_period_s=HALF_PERIOD_S,
                    address=addr,
                )
                print(f"  {name} = {v:.3f}V  — observe LED for 10s ...")
                time.sleep(10)
                v += step
        except KeyboardInterrupt:
            print("\n  Sweep interrupted.")
        finally:
            dac.close()
        print()

    print("=" * 50)
    print("Neuron test setup complete!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
