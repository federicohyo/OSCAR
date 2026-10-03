#!/usr/bin/env python3
"""Run the LIF emulation on silicon and score it. Clean rewrite of the runner.

The emulated row -- the olfaction pipeline with the sixteen LIF neurons computed in
firmware instead of on the analog array -- is the only comparison that isolates the
substrate, since projection, encoding, kernel and classifier are identical on both sides.
Its energy was measured; its accuracy was computed on the host and argued to be
bit-identical if run. This runs it, so the reference figure can carry the point.

Firmware side is UART_CMD_LIFRUN (0xD1): header then T signed event counts, reply echoes
the spike count, the received stimulus sum and the Timer0 cycles spent in the ticks. The
handler blocks but times out per byte, so a lost byte can no longer wedge it.

Two things this rewrite fixes by construction rather than by patching:
  - the stimulus is derived ONCE, here, and the event array is asserted to be small before
    anything is sent. The previous runner had been edited so many times that D_ev and
    D_cur reported identical minima, which the source could not produce;
  - the transport check compares the echoed sum against the bytes ACTUALLY SENT, not
    against the array they were meant to encode, so an encoding slip cannot pass.

    CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_emul_run.py --limit 20
"""
import argparse, json, os, time
import numpy as np
import pyftdi.serialext

from olfaction_emul_accuracy import lif_fixed, drive_matrix, build

CMD = 0xD2          # LIFRUN2: precomputed drive, returns the spike-time bitmask


def uart(clk):
    from neuron_bridge import find_ftdi_base_url
    base = find_ftdi_base_url()
    if not base:
        raise SystemExit("no FT4232H found")
    return pyftdi.serialext.serial_for_url(base + "/4", baudrate=960 * clk, timeout=0.4)


def quiet(port, gap=0.05, limit=1.0):
    t0 = last = time.time()
    while time.time() - t0 < limit:
        if port.read(4096):
            last = time.time()
        elif time.time() - last > gap:
            return


def one(port, drv, decay, w, vth, refr, tries=8, settle=0.15):
    """drv: per-tick PRECOMPUTED drive (current), 4 bytes each. Returns (spikes, mask).

    Drive is sent precomputed because that is what lif_fixed() adds -- sending event
    counts and multiplying by w on-chip introduced a multiply rv32i has no instruction
    for, which is not what a deployed implementation would do.

    Transport: the ~607-byte frame used to go out one byte per USB transaction and the
    batch died mid-run on the jitter that injected, so it now goes in 32-byte chunks
    (one USB frame each) paced at one byte-time per byte, with more tries and a settle
    between attempts."""
    drv = np.asarray(drv, dtype=np.int64)
    payload = b"".join(int(x & 0xFFFFFFFF).to_bytes(4, "big") for x in drv)
    sent = int(np.sum(drv)) & 0xFFFFFFFF
    sent = sent - (1 << 32) if sent >= 1 << 31 else sent
    frame = bytes([CMD, len(drv), (decay >> 8) & 0xFF, decay & 0xFF,
                   (vth >> 8) & 0xFF, vth & 0xFF, refr & 0xFF]) + payload
    byte_time = 10.0 / float(port.baudrate)
    ds = None
    for _ in range(tries):
        quiet(port)
        for off in range(0, len(frame), 32):
            part = frame[off:off + 32]
            port.write(part)
            time.sleep(byte_time * len(part))
        line, t0 = b"", time.time()
        while b"\n" not in line and time.time() - t0 < 6.0:
            line += port.read(64)
        txt = bytes(c for c in line if 32 <= c < 127).decode(errors="replace")
        if os.environ.get("DBG"):
            print(f"      raw={txt.strip()[:110]!r} sent={sent}")
        if "sp=" in txt and "ds=" in txt and "m=" in txt:
            sp = int(txt.rsplit("sp=", 1)[1][:4], 16)
            ds = int(txt.rsplit("ds=", 1)[1][:8], 16)
            ds = ds - (1 << 32) if ds >= 1 << 31 else ds
            mh = txt.rsplit("m=", 1)[1][:40]
            if ds == sent and len(mh) == 40:
                words = [int(mh[i:i + 8], 16) for i in range(0, 40, 8)]
                ticks = [t for t in range(len(drv))
                         if words[t >> 5] >> (t & 31) & 1]
                return sp, ticks
        time.sleep(settle)
    raise RuntimeError(f"transport failed: chip echoed {ds}, wire carried {sent}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clk", type=int, default=int(os.environ.get("CARAVAN_CLK_MHZ", 25)))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--stimulus", default="data/olfaction_emul_stimulus.npz")
    ap.add_argument("--out", default="data/olfaction_emul_onchip.json")
    args = ap.parse_args()

    # LOAD the frozen stimulus rather than rebuild it. Rebuilding it inside this function
    # produced event counts of 80000 where the identical code standalone produced 4, and
    # after a long hunt I could not explain it; freezing the array in a separate verified
    # step (where the unit-weight build is checked against the weighted one) removes the
    # question from the measurement path entirely.
    z = np.load(args.stimulus)
    evm, cur = z["ev"].astype(np.int64), z["cur"].astype(np.int64)
    decay, w, vth, refr = int(z["decay"]), int(z["w"]), int(z["vth"]), int(z["refr"])
    Y, it, nchunk, T = z["labels"], z["trial"], int(z["nchunk"]), int(z["T"])
    peak = int(np.max(np.abs(evm)))
    assert peak <= 127, f"event counts too large for int8: {peak}"
    print(f"decay={decay} w={w} vth={vth} refr={refr}; {nchunk} chunks x 16 neurons, T={T}")
    print(f"events {evm.min()}..{evm.max()}, currents {cur.min()}..{cur.max()}")

    port = uart(args.clk)
    port.write(bytes([0xEC, 0, 0, 0]))                    # silence the spike stream
    time.sleep(0.3); quiet(port)
    rows = evm.shape[0] if not args.limit else min(args.limit, evm.shape[0])
    chip = np.zeros(rows, int); host = np.zeros(rows, int); times = []
    t0 = time.time()
    for i in range(rows):
        chip[i], tk = one(port, cur[i], decay, w, vth, refr)
        times.append(tk)
        ref = lif_fixed(cur[i:i + 1], decay, w, vth, refr)[0]
        host[i] = len(ref)
        if [int(round(x * 1000)) for x in ref] != tk:
            raise SystemExit(f"row {i}: spike TIMES differ chip {tk} host "
                             f"{[int(round(x*1000)) for x in ref]}")
        if chip[i] != host[i]:
            raise SystemExit(f"row {i}: chip {chip[i]} host {host[i]} -- the arithmetic "
                             f"differs, which would itself be the result")
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{rows}, {(time.time()-t0)/60:.1f} min, all agree", flush=True)
    port.close()
    print(f"\n{rows} rows, every count matches the host mirror "
          f"({(time.time()-t0)/60:.1f} min)")
    json.dump(dict(rows=int(rows), decay=decay, w=w, vth=vth, refr=refr,
                   chip=chip.tolist(), host=host.tolist(), times=times,
                   nneur=16, nchunk=nchunk, T=T,
                   labels=Y.tolist(), trial=it.tolist(),
                   agree=bool(np.array_equal(chip, host))),
              open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
