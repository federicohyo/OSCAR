#!/usr/bin/env python3
"""Agilent DSO-X 2002A over raw USBTMC, for captures the 1 kHz stream cannot make.

    from agilent_scope import Agilent
    with Agilent() as sc:
        sc.setup_single(chan=2, span_s=0.04, level=0.9, points=50000)
        t, v = sc.capture(timeout_s=30)

WHY THIS EXISTS. The pixhack streams both channels continuously at 1 kHz, which
is the right instrument for the event, the envelope and the alignment -- it runs
for the whole 16 s stimulus. It is the wrong instrument for a burst: the chip's
own timestamps put the within-burst interspike interval at 1.368 ms, so 1 kHz
samples it 1.4 times per spike and returns an alias (1000-731 = 269 Hz beat, an
apparent spike every 3.7 ms). This scope reaches 50 kpts, which over a 40 ms
window is 1.25 MSa/s -- roughly 1700 samples per interspike interval.

No pyvisa: the device is readable as /dev/usbtmc<N> by anyone in `plugdev`, and
one open file plus SCPI strings is the whole driver.

PROBE ATTENUATION IS THE INSTRUMENT'S BELIEF, NOT A MEASUREMENT. `:CHANn:PROB`
was found at 10x on both channels; if the probe actually fitted is 1x, every
volt reported here is ten times too large and nothing in the data will say so.
Check it against a known level before trusting an absolute voltage.
"""
import fcntl
import time
import numpy as np

DEV = "/dev/usbtmc2"


class Agilent:
    # _IO('[', 2) from linux/usb/tmc.h -- the USBTMC "device clear".
    USBTMC_IOCTL_CLEAR = (91 << 8) | 2
    # _IOW('[', 10, __u32): the driver's per-read timeout, in ms. The default is
    # short enough that a 50 kpt block transfer can outlast it.
    USBTMC_IOCTL_SET_TIMEOUT = (1 << 30) | (4 << 16) | (91 << 8) | 10

    def _set_timeout_ms(self, ms):
        try:
            import struct
            fcntl.ioctl(self.f.fileno(), self.USBTMC_IOCTL_SET_TIMEOUT,
                        struct.pack("I", int(ms)))
        except OSError:
            pass        # this call is optional on older kernels; the default still works

    def __init__(self, dev=DEV):
        self.f = open(dev, "r+b", buffering=0)
        self._set_timeout_ms(10000)
        # An interrupted session leaves an unread response queued, and every
        # later query then returns ETIMEDOUT until the interface is cleared --
        # including *IDN?. Clear on open so one aborted run leaves the link clean for the
        # next; the first query after a clear can still come back empty, which
        # is why q() retries.
        self.clear()

    def clear(self):
        try:
            fcntl.ioctl(self.f.fileno(), self.USBTMC_IOCTL_CLEAR)
        except OSError:
            pass
        self._set_timeout_ms(10000)
        # Nothing else. A read() here to "drain leftovers" is what makes this
        # worse: the clear has already discarded the queued response, so the read
        # blocks for the driver's full timeout and leaves the interface returning
        # zero-length reads to every query afterwards -- which looks exactly like
        # a dead instrument. Clear, wait, then let q() re-issue.
        time.sleep(0.5)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        try:
            self.f.close()
        except OSError:
            pass

    # -- io ---------------------------------------------------------------
    def w(self, cmd, settle=0.06, tries=3):
        for k in range(tries):
            try:
                self.f.write((cmd + "\n").encode())
                time.sleep(settle)
                return
            except (TimeoutError, OSError):
                # Even a WRITE times out once the interface is wedged (seen right
                # after a single-shot trigger). Clearing is the only way back.
                self.clear()
        raise TimeoutError(f"cannot send {cmd!r}")

    def q(self, cmd, n=65536, tries=6, settle=0.15):
        """Write the query ONCE, then read until it answers.

        Re-sending a query while its response is still pending is what puts
        "query unterminated" on the instrument's front panel and leaves it
        stopped -- the scope discards the first answer, and the two sides are
        then permanently one response out of step. A read that times out has not
        lost anything, so the fix for a slow answer is another read, never
        another write. Only when the instrument has genuinely dropped the request
        (after a device clear) is re-issuing correct, and that is the last resort
        at the bottom.
        """
        self.f.write((cmd + "\n").encode())
        time.sleep(settle)
        for _ in range(tries):
            try:
                out = self.f.read(n)
            except (TimeoutError, OSError):
                continue
            if out:
                return out.decode(errors="replace").strip()
            time.sleep(settle)
        raise TimeoutError(f"no answer to {cmd!r}")

    def qf(self, cmd):
        return float(self.q(cmd))

    def idn(self):
        return self.q("*IDN?")

    # -- acquisition ------------------------------------------------------
    def setup_single(self, chan=2, span_s=0.04, level=None, slope="POS",
                     points=50000, delay_frac=0.4):
        """Arm one single-shot acquisition triggered on `chan`.

        span_s is the whole screen (10 divisions). delay_frac puts the trigger
        that far into the screen, so the burst that fires the trigger is captured
        with some of the membrane before it, not only after.
        """
        self.w(":STOP")
        self.w(f":TIM:SCAL {span_s/10.0:.9f}")
        self.w(f":TIM:POS {(0.5 - delay_frac) * span_s:.9f}")
        self.w(":ACQ:TYPE NORM")
        self.w(f":ACQ:POIN {int(points)}")
        self.w(f":TRIG:SOUR CHAN{chan}")
        self.w(f":TRIG:SLOP {slope}")
        if level is not None:
            self.w(f":TRIG:LEV {level:.6f}")
        self.w(":TRIG:SWE NORM")     # NORM rather than AUTO: wait for a real edge
        self.w(":SING")
        self.chan = chan

    def triggered(self):
        """:TER? -- the Trigger Event Register, which CLEARS ON READ, so one
        `1` is the whole event and polling it twice loses it.

        Not :AST?: that is an Infiniium command and the 2000 X-series answers it
        with nothing at all, which surfaces as a query timeout rather than an
        error.
        """
        return self.q(":TER?").strip() in ("1", "+1")

    def wait(self, timeout_s=30.0, poll=0.2):
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if self.triggered():
                return True
            time.sleep(poll)
        return False

    def capture(self, chan=None, timeout_s=30.0):
        """Wait for the armed acquisition, then read it back as (t, volts)."""
        if not self.wait(timeout_s):
            raise TimeoutError("scope did not trigger")
        return self.read_waveform(chan if chan is not None else self.chan)

    def read_waveform(self, chan, _retry=True):
        """Read the acquisition currently in memory.

        NEVER "recover" a stalled read with :RUN/:STOP. That answers again, but
        it answers about a NEW acquisition -- it overwrites the single shot you
        were trying to read, and the preamble still describes the old timebase,
        so the loss is silent. A device clear is safe (the acquisition survives
        it); re-running is not.
        """
        try:
            return self._read_waveform(chan)
        except (TimeoutError, OSError):
            if not _retry:
                raise
            self.clear()
            return self._read_waveform(chan)

    def _read_waveform(self, chan):
        self.w(f":WAV:SOUR CHAN{chan}")
        self.w(":WAV:POIN:MODE RAW")
        self.w(":WAV:FORM BYTE")
        pre = [float(x) for x in self.q(":WAV:PRE?", settle=0.4).split(",")]
        _fmt, _typ, npts, _cnt, xinc, xorig, xref, yinc, yorig, yref = pre[:10]
        npts = int(npts)
        self.f.write(b":WAV:DATA?\n")
        time.sleep(0.4)
        raw = b""
        # IEEE 488.2 definite-length block: '#', one digit giving the header
        # width, then that many digits of byte count, then the payload.
        t0 = time.time()
        while len(raw) < 2:
            try:
                raw += self.f.read(64)
            except (TimeoutError, OSError):
                if time.time() - t0 > 10:
                    raise
                time.sleep(0.2)
        ndig = int(raw[1:2])
        while len(raw) < 2 + ndig:
            raw += self.f.read(64)
        nbytes = int(raw[2:2 + ndig])
        head = 2 + ndig
        while len(raw) < head + nbytes:
            chunk = self.f.read(min(65536, head + nbytes - len(raw)))
            if not chunk:
                break
            raw += chunk
        data = np.frombuffer(raw[head:head + nbytes], dtype=np.uint8).astype(float)
        v = (data - yref) * yinc + yorig
        t = (np.arange(len(v)) - xref) * xinc + xorig
        return t, v

    def snapshot(self, chan):
        """Cheap 'is anything on this probe' reading."""
        return dict(vpp=self.qf(f":MEAS:VPP? CHAN{chan}"),
                    vavg=self.qf(f":MEAS:VAV? CHAN{chan}"),
                    vmax=self.qf(f":MEAS:VMAX? CHAN{chan}"),
                    probe=self.qf(f":CHAN{chan}:PROB?"))


if __name__ == "__main__":
    with Agilent() as sc:
        print(sc.idn())
        for ch in (1, 2):
            print(f"CH{ch}: {sc.snapshot(ch)}")
        # read whatever is on screen right now -- validates the block transfer
        sc.w(":TIM:SCAL 20E-3"); sc.w(":TRIG:SWE AUTO"); sc.w(":RUN")
        time.sleep(1.0); sc.w(":STOP")
        for ch in (1, 2):
            t, v = sc.read_waveform(ch)
            print(f"CH{ch}: {len(v)} pts, {1.0/np.median(np.diff(t))/1e3:.1f} kSa/s, "
                  f"span {(t[-1]-t[0])*1e3:.1f} ms, {v.min():.3f}..{v.max():.3f} V")
        sc.w(":RUN")
