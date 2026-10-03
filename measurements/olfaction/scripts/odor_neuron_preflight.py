#!/usr/bin/env python3
"""Pre-flight for the odor -> neuron leg. Run once the GUI is closed and the
neuron channels are applied.

    ../.venv-meas/bin/python3 LNA/odor_neuron_preflight.py

WRITES NO BIASES. That is deliberate: the array and the amplifier share one DAC
bank, and the per-neuron bias files used by the general bring-up gate set
`lna_iref`/`VB1`/`VB2`/`TUNEp`/`VREF` to values that switch the amplifier off.
Whatever is loaded stays loaded; this only stimulates and listens.

It also never opens /dev/ttyACM0 -- the scope server owns that port.

Three checks, in order, each gating the next:

  1. UNMASKED 16-NEURON ADDRESSING SCAN. Stimulate neuron k, confirm the address
     that comes back is k. The AER encoder can latch so that every spike reads as
     one address, or so that every address comes back one low -- both survive
     reset, reflash and rebiasing, and only a power cycle clears them. Without
     this the failure is silent: a per-neuron mask keyed to the intended address
     turns a mislabelled array into an apparently dead one.
  2. NEURON 9 POSITIVE CONTROL. It must spike to a plain BURST before any loop is
     wired, otherwise a null result later is uninterpretable.
  3. DROP/STALL check on the UART stream.
"""
import os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from meas_common import BridgeSession

TARGET = 9
WEIGHT = 15
SYN_CANDIDATES = [0, 15]        # 0 confirmed at the bench (1 spike in -> 1 spike out)


def stim(br, syn, neuron, n=8, exc=True, settle=0.35):
    """Program, route, burst, tally. program_weight MUST precede route."""
    br.drain()
    br.program_weight(syn, WEIGHT, exc=exc)
    time.sleep(0.05)
    br.route(syn, neuron, exc=exc)
    time.sleep(0.05)
    br.send(f"BURST {n}")
    time.sleep(settle)
    return br.drain()


def main():
    with BridgeSession() as br:
        br.send("MASK 65535")          # unmasked: we must see WHATEVER address comes back
        time.sleep(0.2); br.drain()

        syn = None
        for s in SYN_CANDIDATES:
            c = stim(br, s, TARGET, n=8)
            print(f"synapse {s:2d} -> neuron {TARGET}: {sum(c)} spikes  "
                  f"{'(addresses: ' + ','.join(str(i) for i,x in enumerate(c) if x) + ')' if sum(c) else ''}")
            if sum(c):
                syn = s; break
        if syn is None:
            print("\nNo response on either candidate synapse.")
            print("Neuron 9 did not fire -- do not proceed. Either the neuron biases are")
            print("not in, the synapse index is neither 15 nor 0, or the array is wedged.")
            return 1
        print(f"\nusing synapse {syn}\n")

        print("=== 1. unmasked 16-neuron addressing scan ===")
        seen, bad = {}, []
        for k in range(16):
            c = stim(br, syn, k, n=8)
            hits = [i for i, x in enumerate(c) if x]
            seen[k] = hits
            ok = hits == [k]
            if not ok: bad.append(k)
            print(f"  stim {k:2d} -> {('addr ' + ','.join(map(str, hits))) if hits else 'silent':<22s}"
                  f" {sum(c):3d} spikes  {'OK' if ok else '<-- MISMATCH'}")

        allhits = [h for v in seen.values() for h in v]
        if allhits and len(set(allhits)) == 1:
            print(f"\n*** AER ADDRESS LATCH: every stimulus reports address {allhits[0]}.")
            print("    Only a POWER CYCLE clears this. Reset/reflash/rebias will not.")
            return 2
        shifted = sum(1 for k, v in seen.items() if v == [(k - 1) % 16])
        if shifted >= 8:
            print(f"\n*** AER OFF-BY-ONE LATCH: {shifted}/16 report one address low.")
            print("    Only a POWER CYCLE clears this.")
            return 2
        if not allhits:
            print("\n*** No neuron responded at all -- array wedged or biases not applied.")
            return 2
        print(f"\n  {16-len(bad)}/16 addresses correct"
              + (f"; mismatched: {bad}" if bad else ""))

        print(f"\n=== 2. neuron {TARGET} positive control ===")
        for n in (1, 4, 16):
            c = stim(br, syn, TARGET, n=n, settle=0.5)
            print(f"  BURST {n:2d} -> {c[TARGET]:3d} spikes on neuron {TARGET}"
                  f"   (others: {sum(c)-c[TARGET]})")
        print("\n  BURST is firmware-paced (~1 us). `T` is UART-paced (~0.83 ms) and does")
        print("  not let the neuron integrate -- use BURST for the loop.")

        print("\n=== 3. stream health ===")
        br.send("STATS"); time.sleep(0.3)
        for _ in range(200):
            try: print("  " + br.out_q.get_nowait().rstrip())
            except Exception: break
    return 0


if __name__ == "__main__":
    sys.exit(main())
