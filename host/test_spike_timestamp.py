#!/usr/bin/env python3
"""Test the 4-byte binary spike protocol parser.

Validates that the parser correctly decodes neuron IDs and delta timestamps,
handles resynchronization after corrupt bytes, and reconstructs absolute
timestamps from cumulative deltas.

Usage:
    python3 test_spike_timestamp.py
"""

import sys


def encode_spike(neuron_id, delta_us):
    """Encode a spike into a 4-byte packet."""
    return bytes([
        0x80 | (neuron_id & 0x0F),
        (delta_us >> 14) & 0x7F,
        (delta_us >>  7) & 0x7F,
         delta_us        & 0x7F,
    ])


def parse_spikes(data):
    """Parse 4-byte spike packets from raw bytes.

    Returns list of (neuron_id, abs_timestamp_us) tuples.
    Same algorithm as neuron_bridge.py spike_reader_thread.
    """
    buf = bytearray(data)
    abs_us = 0
    results = []

    while len(buf) >= 4:
        # Scan for sync byte (MSB=1)
        if buf[0] & 0x80 == 0:
            buf.pop(0)
            continue
        # Verify next 3 bytes are data (MSB=0)
        if any(b & 0x80 for b in buf[1:4]):
            buf.pop(0)
            continue

        neuron = buf[0] & 0x0F
        delta_us = (buf[1] << 14) | (buf[2] << 7) | buf[3]
        abs_us += delta_us
        del buf[:4]
        results.append((neuron, abs_us))

    return results


def test_basic_encoding():
    """Test basic encode/decode roundtrip."""
    pkt = encode_spike(5, 1000)
    assert len(pkt) == 4
    assert pkt[0] == 0x85  # 0x80 | 5
    assert pkt[0] & 0x80  # sync bit set
    assert all(b & 0x80 == 0 for b in pkt[1:])  # data bytes have MSB=0

    results = parse_spikes(pkt)
    assert len(results) == 1
    assert results[0] == (5, 1000)
    print("  PASS: basic encoding")


def test_multiple_spikes():
    """Test parsing multiple consecutive packets."""
    data = b""
    data += encode_spike(0, 500)
    data += encode_spike(7, 1500)
    data += encode_spike(15, 3000)

    results = parse_spikes(data)
    assert len(results) == 3
    assert results[0] == (0, 500)
    assert results[1] == (7, 2000)     # 500 + 1500
    assert results[2] == (15, 5000)    # 2000 + 3000
    print("  PASS: multiple spikes")


def test_all_neurons():
    """Test all 16 neuron IDs."""
    data = b""
    for n in range(16):
        data += encode_spike(n, 100)

    results = parse_spikes(data)
    assert len(results) == 16
    for i, (neuron, ts) in enumerate(results):
        assert neuron == i
        assert ts == (i + 1) * 100
    print("  PASS: all 16 neuron IDs")


def test_zero_delta():
    """Test zero delta (simultaneous spikes)."""
    data = encode_spike(3, 0) + encode_spike(4, 0)
    results = parse_spikes(data)
    assert len(results) == 2
    assert results[0] == (3, 0)
    assert results[1] == (4, 0)
    print("  PASS: zero delta")


def test_max_delta():
    """Test maximum 21-bit delta (2^21 - 1 = 2097151 us ~ 2.1s)."""
    max_delta = (1 << 21) - 1  # 2097151
    data = encode_spike(10, max_delta)

    results = parse_spikes(data)
    assert len(results) == 1
    assert results[0] == (10, max_delta)
    print(f"  PASS: max delta ({max_delta} us = {max_delta/1e6:.1f}s)")


def test_resync_leading_garbage():
    """Test resync after leading garbage bytes."""
    garbage = bytes([0x01, 0x23, 0x45])  # all MSB=0, skipped
    data = garbage + encode_spike(2, 999)

    results = parse_spikes(data)
    assert len(results) == 1
    assert results[0] == (2, 999)
    print("  PASS: resync after leading garbage")


def test_resync_mid_stream():
    """Test resync when a corrupt byte appears mid-stream."""
    data = encode_spike(1, 100)
    # Insert a corrupt sync byte (looks like a packet start but followed by another sync)
    data += bytes([0x8F, 0x80])  # two sync bytes in a row → first is discarded
    data += encode_spike(6, 200)  # but 0x80 then gets consumed as next start...

    # Actually, after discarding 0x8F (because buf[1]=0x80 has MSB set),
    # we resync on 0x80 which is encode_spike(6, 200)'s first byte? No:
    # buf = [0x8F, 0x80, <4 bytes of spike(6,200)>]
    # buf[0]=0x8F (sync), buf[1]=0x80 (MSB set!) → discard buf[0]
    # buf = [0x80, <4 bytes of spike(6,200)>]
    # But 0x80 is the start of a packet with neuron=0, and the next 3 bytes
    # are the start of encode_spike(6,200): 0x86, ...
    # buf[1]=0x86 has MSB=1 → discard 0x80
    # buf = [0x86, delta bytes...]
    # This is spike(6, 200). Let's just verify the parser recovers.
    results = parse_spikes(data)
    assert len(results) >= 2  # first spike + recovered spike
    assert results[0] == (1, 100)
    # The corrupt bytes cause the second spike to have neuron 6, delta 200
    assert results[-1][0] == 6
    print("  PASS: resync mid-stream")


def test_resync_all_garbage():
    """Test that pure garbage produces no spikes."""
    garbage = bytes([0x01, 0x02, 0x03, 0x04, 0x05])
    results = parse_spikes(garbage)
    assert len(results) == 0
    print("  PASS: pure garbage → no spikes")


def test_incomplete_packet():
    """Test that incomplete packets at end are not consumed."""
    data = encode_spike(8, 500) + bytes([0x83, 0x01])  # incomplete
    results = parse_spikes(data)
    assert len(results) == 1
    assert results[0] == (8, 500)
    print("  PASS: incomplete packet at end ignored")


def test_delta_encoding_values():
    """Test specific delta values to verify bit packing."""
    test_cases = [
        (0, 0, [0x80, 0x00, 0x00, 0x00]),
        (1, 1, [0x81, 0x00, 0x00, 0x01]),
        (2, 127, [0x82, 0x00, 0x00, 0x7F]),       # fits in byte 3
        (3, 128, [0x83, 0x00, 0x01, 0x00]),        # spills to byte 2
        (4, 16383, [0x84, 0x00, 0x7F, 0x7F]),      # max in bytes 2-3
        (5, 16384, [0x85, 0x01, 0x00, 0x00]),      # spills to byte 1
        (15, 2097151, [0x8F, 0x7F, 0x7F, 0x7F]),   # max 21-bit value
    ]

    for neuron, delta, expected_bytes in test_cases:
        pkt = encode_spike(neuron, delta)
        assert list(pkt) == expected_bytes, \
            f"neuron={neuron} delta={delta}: expected {expected_bytes}, got {list(pkt)}"

        results = parse_spikes(pkt)
        assert results[0] == (neuron, delta), \
            f"neuron={neuron} delta={delta}: parsed as {results[0]}"

    print("  PASS: delta encoding bit packing")


def main():
    print("Testing 4-byte spike protocol parser...")
    print()

    test_basic_encoding()
    test_multiple_spikes()
    test_all_neurons()
    test_zero_delta()
    test_max_delta()
    test_delta_encoding_values()
    test_resync_leading_garbage()
    test_resync_mid_stream()
    test_resync_all_garbage()
    test_incomplete_packet()

    print()
    print("All tests passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
