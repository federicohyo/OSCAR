#include <defs.h>
#include <stub.h>

void configure_io()
{
    reg_mprj_io_0 = GPIO_MODE_MGMT_STD_ANALOG;

    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    reg_mprj_io_5 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;     // UART Rx
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;           // UART Tx

    // gpio_analog[0..6] = mprj_io[7..13] — analog bias pads
    reg_mprj_io_7 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_8 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_9 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_10 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_11 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_12 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_13 = GPIO_MODE_USER_STD_ANALOG;

    // io_analog[0..10] = mprj_io[14..24] — dedicated analog pads
    // Match via-programmed default (0x000a = USER_STD_ANALOG)
    reg_mprj_io_14 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_15 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_16 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_17 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_18 = GPIO_MODE_USER_STD_ANALOG;

    reg_mprj_io_19 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_20 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_21 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_22 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_23 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_24 = GPIO_MODE_USER_STD_ANALOG;

    // gpio_analog[7..17] = mprj_io[25..35] — analog bias pads
    reg_mprj_io_25 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_26 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_27 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_28 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_29 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_30 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_31 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_32 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_33 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_34 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_35 = GPIO_MODE_USER_STD_ANALOG;
    reg_mprj_io_36 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_37 = GPIO_MODE_MGMT_STD_OUTPUT;

    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);
}

// --- reg_la0_data (LA bits 0..31) ---
#define X3_SYN_REQ_BIT   (1 << 3) // la_data_in[3] = x3.syn_req
#define X3_EXC_BIT   (1 << 4) // la_data_in[4] = x3.exc
#define X3_SETW_BIT (1 << 5) // la_data_in[5] = x3.setw
#define X3_RESETW_BIT (1 << 6) // la_data_in[6] = x3.resetW
#define X3_SYN_ADDR_MASK (0xF << 7) // la_data_in[7:10] = x3.syn_addr[0:3]
#define X3_W_MASK (0xF << 11) // la_data_in[11:14] = x3.W[0:3]
#define X5_REQ_INP_BIT (1 << 15) // la_data_in[15]  = x5.req_inp
#define X5_NEU_ADDR_MASK (0xF << 16) // la_data_in[16:19] = x5.neu_addr[3:0]
#define X5_EXC_BIT   (1 << 20)   // la_data_in[20]  = x5.exc
#define X5_SETW_BIT  (1 << 21)   // la_data_in[21]  = x5.setW
#define X5_RESETW_BIT (1 << 22)  // la_data_in[22]  = x5.resetW
#define X5_SYN_ADDR_MASK (0xF << 23) // la_data_in[23:26] = x5.syn_addr[0:3]
#define X5_W_MASK (0xF << 27) // la_data_in[27:30] = x5.W[0:3]

// --- reg_la1_data (LA bits 32..63) ---
#define X5_ACK_BIT   (1 << 28)   // la_data_in[60]  = x5.ack
#define X5_REQ_BIT   (1 << 29)   // la_data_out[61] = x5.req_o
#define X5_AER0_BIT  (1 << 30)   // la_data_out[62] = x5.AER[0]
#define X5_AER1_BIT  (1 << 31)   // la_data_out[63] = x5.AER[1]

// --- reg_la2_data (LA bits 64..95) ---
#define X5_AER2_BIT  (1 << 0)    // la_data_out[64] = x5.AER[2]
#define X5_AER3_BIT  (1 << 1)    // la_data_out[65] = x5.AER[3]
#define X5_CLK_BIT   (1 << 2)    // la_data_in[66]  = x5.CLK
#define X5_DA_BIT    (1 << 3)    // la_data_in[67]  = x5.Da
#define NRES_BIT     (1 << 4)    // la_data_in[68]  = nRes (shared x3+x5)
#define X3_REQ_BIT   (1 << 5)    // la_data_out[69] = x3.req
#define X3_ACK_BIT   (1 << 6)    // la_data_in[70]  = x3.ack_out

// UART RX command framing
// Monitor select command frame: [0xD0, neuron(0..15)]
#define UART_CMD_MONITOR_SYNC 0xD0
// Program command frame: [0xF0, syn_addr(0..15), weight(0..15), synapse_type(0/1)]
#define UART_CMD_PROGRAM_SYNC 0xF0
// Spike setup command frame: [0xE0, syn_addr(0..15), neu_addr(0..15), synapse_type(0/1)]
#define UART_CMD_SPIKE_SETUP  0xE0
// Spike trigger command frame: [0xE1] -> send one spike using last spikesetup() route.
#define UART_CMD_SEND_SPIKE   0xE1
// Poisson start frame: [0xE2, mean_isi_ticks[23:16], [15:8], [7:0]] -> the RISC-V
//   generates Poisson-distributed spikes (exponential ISIs) on the last spikesetup()
//   route, with the given mean inter-spike interval in 10 MHz timer ticks.
#define UART_CMD_POISSON_START 0xE2
// Poisson stop frame: [0xE3] -> stop on-chip Poisson generation.
#define UART_CMD_POISSON_STOP  0xE3
// Synfire chain start: [0xE4, laps(6-bit)] -> RISC-V mediates spike chain
//   0->1->2->...->15->0 for 'laps' rounds. 0 = run until SYNFIRE_STOP.
#define UART_CMD_SYNFIRE_START 0xE4
// Synfire chain stop: [0xE5] -> stop synfire chain.
#define UART_CMD_SYNFIRE_STOP  0xE5
// Coincidence trial: [0xE6, synA, synB, neuron, dt_b3, dt_b2, dt_b1, dt_b0]
//   (synA/synB/neuron 6-bit; dt = 24-bit inter-input interval in 10 MHz ticks).
//   Fires input A on synA->neuron, waits dt, fires input B on synB->neuron. The
//   neuron fires only if the two EPSPs summate past threshold within the window.
#define UART_CMD_COINCIDENCE   0xE6
// Recurrent reservoir: sparse RISC-V-mediated recurrent connectivity.
//   SET_RECUR  [0xE9, src, dst, cw]: append connection src->dst; cw = count(bits0-3) | exc(bit4).
//   RECUR_CTRL [0xEA, mode]: 0=off, 1=on, 2=clear all connections.
#define UART_CMD_SET_RECUR     0xE9
#define UART_CMD_RECUR_CTRL    0xEA
// Timer0 numeric-LIF cost benchmark: [0xEB] -> times a calibration loop and K lif_step()
// iterations with the free-running Timer0, prints "BENCH ..." over UART. Validates the
// modeled 153 cyc/step on silicon. Benchmark fns are -O2 (match numeric_lif.lst) inside the
// -O0 firmware via __attribute__((optimize)).
#define UART_CMD_BENCH         0xEB
// Timer0 OLFACTION OP3 cost benchmark: [0xEE] (0xEC is SPIKE_MASK -- keep this opcode distinct) -> times K traversals of the counted
// gradient-boosted tree kernel (50 trees, 746 nodes, 160.3 node visits/decision).
// Counted at 4,126 cycles; this is the measured counterpart, the step the ECG OP3
// lacked. Node table and feature vector live in flash .rodata; the kernel touches
// locals only, because bench_cmd runs deep in main()'s -O0 frame with 1 KB of RAM.
#define UART_CMD_OLFBENCH      0xEE
#define UART_CMD_ARRAYBENCH    0xEF
#define UART_CMD_LIFRAM        0xE7
// LIFRUN [0xD1, T, decay_hi, decay_lo, w_hi, w_lo, vth_hi, vth_lo, refr, ev[0..T-1]]
//   -> prints "LIFRUN sp=<hex>".
// The functional counterpart of LIFRAM. LIFRAM drives ONE neuron with a constant jump and
// exists only to time the loop, so the emulated pipeline's ACCURACY ran host-side
// rather than on the die -- computed in this same arithmetic, and the
// figure had to withhold the point. This command takes the real per-tick stimulus (ev[t]
// is a SIGNED event count; drive = ev[t] * w, matching drive_matrix() in
// olfaction_emul_accuracy.py) and returns the spike count, so the number can be measured
// instead of argued. Same shift-add Q16 decay, int32 state, hard reset and refractory as
// lif_steps_ram(), because the point is to confirm THIS arithmetic on silicon.
#define UART_CMD_LIFRUN        0xD1
#define UART_CMD_LIFRUN2       0xD2
// LIFBENCH [0xD3] -> times K calls to lifrun_step() in a TIGHT loop with UART and
// per-tick timer reads off, and reports once. Per-tick instrumentation under-prices a ~50
// cycle operation: two Timer0 update/read pairs per tick swamped it and reported 1771.
// This times the SAME SRAM-resident function that produced the accuracy, in the SAME
// image, so the number and the energy come from one configuration.
#define UART_CMD_LIFBENCH      0xD3
#define LIFRUN_TMAX            255

// MEMPROBE [0xD4] -> existence/size probe of the DECLARED-but-unlinked SRAM
// (regions.ld: sram : ORIGIN = 0x01000000, LENGTH = 0x800). regions.ld declares
// it, sections.lds leaves it unlinked, so nothing on this tape-out has touched
// it -- this settles whether the RAM is real and whether it is 2 KB (wraps at
// 0x800) or 4 KB (wraps at 0x1000). Every write before the final sweep restores
// the old cell contents: if the decode aliases dff at 0x0, a plain write there
// would corrupt .data/.bss and take the main loop down mid-probe. Phase markers
// print BEFORE each access class, so a bus wedge still tells us where it died.
#define UART_CMD_MEMPROBE      0xD4

__attribute__((optimize("O2")))
static void memprobe_cmd(void)
{
    volatile uint32_t *p = (volatile uint32_t *)0x01000000u;
    uint32_t i, old;

    print("MEMP start\n");
    /* 1: does the base address behave like RAM at all (single cell, restored) */
    uint32_t fails = 0;
    static const uint32_t pat[4] = {0x00000000u, 0xFFFFFFFFu,
                                    0xA5A5A5A5u, 0x12345678u};
    old = p[0];
    for (i = 0; i < 4; i++) {
        p[0] = pat[i];
        if (p[0] != pat[i]) fails++;
    }
    p[0] = old;
    print("MEMP base_fail="); print_hex(fails, 2); print("\n");

    /* 2: aliasing markers across 8 KB, contents restored afterwards. Offsets
     * 0x000/0x800/0x1000/0x2000 all alias if the block is 2 KB; only the first
     * survives if it is 4 KB; all six distinct means >= 8 KB of real RAM. */
    static const uint32_t offs[6] = {0x000u, 0x400u, 0x800u,
                                     0xC00u, 0x1000u, 0x2000u};
    uint32_t saved[6];
    for (i = 0; i < 6; i++) saved[i] = p[offs[i] / 4];
    for (i = 0; i < 6; i++) p[offs[i] / 4] = 0xB0000000u | offs[i];
    for (i = 0; i < 6; i++) {
        print("MEMP +"); print_hex(offs[i], 4);
        print("=");        print_hex(p[offs[i] / 4], 8); print("\n");
    }
    for (i = 0; i < 6; i++) p[offs[i] / 4] = saved[i];
    /* The markers replace a bulk sweep: a 2048-word pass over this undecoded range wedged the bus
     * (chip needed a CPU reset toggle), and the markers above already answer the
     * existence and 2-vs-4 KB question. */
    print("MEMP done\n");
}


#define UART_CMD_ARRAYOPT      0xE8
// BURST [0xDD, n]: fire n spikes back-to-back on the STAGED route, paced by firmware.
// The point is the inter-spike interval. 'T n' from the bridge writes n separate 0xE1
// bytes, so the spikes are UART-paced at ~0.83 ms apart at 24000 baud -- far outside the
// membrane's ~3 ms integration window once you want more than three of them. sendspike()
// is ~1 us, so a firmware loop puts all n inside the window and lets the neuron actually
// integrate. With UART pacing the array can only be a 2-level comparator (olfaction.md 6.17).
#define UART_CMD_BURST         0xDD
// PULSEBENCH [0xDE]: Timer0-time K sendspike() calls at the CURRENT pulse_mult, so the
// input pulse width is MEASURED rather than taken from the "1 tick = 100 ns" comment,
// which predates the flash-fetch accounting and the F_CPU scaling. Width matters
// directly: charge per input event is I_syn x width, so pulse_mult is a LINEAR charge
// knob where JExcWn is exponential.
#define UART_CMD_PULSEBENCH    0xDE
// PULSEFINE [0xDF, n]: set the raw delay count used by sendspike(), bypassing the
// 10*pulse_mult granularity. Measured 2026-08-15, the pulse is 29.6 us at pulse_mult=1
// and grows 2.25 us per unit -- so the FLOOR comes from the count, since the
// smallest count the old path can request is 10 (x CLK_SCALE = 20 loop iterations, each
// ~1.35 us from XIP fetch). Charge per input event is I_syn x width, so that floor is a
// large fixed charge quantum: one spike saturates the membrane at every bias tried,
// which is what held back a graded spike-count comparator. n=0 restores the pulse_mult
// path exactly, so the default and the pinned exhibition behaviour are unchanged.
#define UART_CMD_PULSEFINE     0xDF

/* dff2 is 512 B and aer_drain fills nearly all of it, so the SRAM-resident LIF needs
 * more room than remains (link overflows by 132 B). Build with -DLIFRAM_BUILD to swap them: the
 * LIF gets dff2 and the drain falls back to flash. That image is for CYCLE COUNTING ONLY
 * -- it records zero spikes, so a flash-resident drain costs it nothing, and the drain's
 * SRAM cost is already measured separately (105 + 480/event). Keep it away from
 * acquisitions: the drain would be ~37.8x slower and the AER handshake would stall. */
#ifdef LIFRAM_BUILD
#define AER_SECTION ".text"
#define LIF_SECTION ".ramtext"
#else
#define AER_SECTION ".ramtext"
#define LIF_SECTION ".text"
#endif
#define UART_CMD_ADDR_SETTLE   0xDA   // sweep min address-sample settle (n14)
// Per-neuron stream filter: [0xEC, b0, b1, b2] -> mask = b0 | b1<<6 | (b2&0xF)<<12
// Bit i set = neuron i is streamed. Masked neurons are still ACKED (a neuron holds
// req until acked, so skipping the ack would stall the AER bus for everyone) and
// stay out of the ring, so they use zero buffer slots and zero UART bandwidth.
// Payload is carried 6 bits at a time to stay clear of the 0x8x..0xFx command range.
#define UART_CMD_SPIKE_MASK    0xEC
// Regular spike train: [0xED, b3, b2, b1, b0] -> period = 24-bit tick count, same
// framing as 0xE2. Stopped by 0xE3 (shared with Poisson). Paced on-chip by Timer0,
// because the HOST pace is unreliable: port.write() blocks for up to 182 ms behind the
// reader's port lock, so a host-threaded 200 Hz train delivered 24-121 Hz.
#define UART_CMD_TRAIN_START   0xED
// Runtime input-pulse width multiplier: [0xDC, mult(1..63)]. spikesetup()/sendspike()
// use delay_loop(10 * mult). EXPERIMENT: at 50 MHz the INHIBITORY synapse delivers
// almost zero charge (membrane dmean -0.25 mV vs -6.8 mV at 10 MHz) even though delay_loop is
// clock-scaled, so the req_inp pulse should already have the same real-time width.
// This knob tests whether widening it recovers inhibition.
#define UART_CMD_SET_PULSE     0xDC

// Compile-time spike streaming mode:
//   1 (default): deferred streaming -- SRAM drain captures a timestamp +
//     neuron ID into a ring buffer in dff2, then the main loop flushes the ring
//     to UART as 4-byte packets with raw 21-bit Timer0 ticks.  The timestamp
//     capture (~10 cyc) runs in the analog-reset dead time after ack deassert,
//     so the req/ack cycle keeps its pace.  Build: make hex
//     Packet byte 0 = 0x80 | SPIKE_DROP_FLAG(0x40) | neuron_id. The flag is set
//     when the ring overflowed since the previous packet; the host's rates are
//     then UNDERESTIMATES, and host-side arithmetic stays blind to it, because
//     dropping is what keeps the observed rate below the link ceiling.
//   0: fast reservoir mode -- skip per-spike UART + timestamp entirely, so the
//     AER drain loop runs from SRAM at full speed.  Used for 0xDB timing.
//     Build: make STREAM_SPIKES=0 hex
#ifndef STREAM_SPIKES
#define STREAM_SPIKES 1
#endif

// Core clock in MHz. Both Timer0 and delay_loop() are driven by the core clock,
// so every pulse width and tick constant below was hand-calibrated at 10 MHz and
// must be scaled when the DLL raises the core. Reachable cores are 100/N MHz for
// N=2..7, so 10 (crystal) and 20/25/50 divide evenly here.
//   Build: make F_CPU_MHZ=50 hex     (then engage the DLL before running)
#ifndef F_CPU_MHZ
#define F_CPU_MHZ 10
#endif
#define CLK_SCALE (F_CPU_MHZ / 10u)
// Phase-3 hang guard: max iterations spent waiting for req to fall after ack. req is a
// digital release, so it falls in ~us; this stops a wedged handshake from hanging
// the drain forever. Expressed in CPU iterations, so it scales with the core clock to
// stay a fixed REAL-TIME budget. Keep this at its value rather than shrinking it to "go faster": dropping ack before
// req falls breaks the 4-phase handshake and duplicates spikes.
#define REQ_LOW_MAX (2000u * CLK_SCALE)
// poisson_mean_ticks and coinc_dt arrive from the host ALREADY IN TICKS, so the
// host converts seconds->ticks with the real clock (neuron_bridge.py TIMER_HZ).
//   coinc_dt's clamp scales: it only bounds a duration (300 ms real time).
//   poisson_mean_ticks' clamp stays as-is and MUST: 5e6 is the overflow guard
//   that keeps umul32(mean, neglog_lut_max=799) inside 32 bits (5e6*799 = 3.995e9).
//   Consequence at 50 MHz: the slowest Poisson mean rate is 10 Hz rather than 2 Hz.

#define UART_CMD_REPORT_HS 0xDB   // print + reset handshake Timer0 timing & per-neuron counts
#define REC_SYN                1      // dedicated recurrent synapse index
#define MAXREC                 128    // max recurrent connections
// Max number of UART RX bytes to process per main loop iteration (non-blocking).
#define UART_RX_MAX_BYTES_PER_LOOP 8

// UART TX DEBUG packet tags (MSB clear so they stay clear of spike AER packets).
#define UART_DBG_PROGRAM_WEIGHT 0x71 //TODO DEBUG
#define UART_DBG_SPIKE_SETUP    0x72 //TODO DEBUG

// RX parser states
#define RX_STATE_IDLE              0
#define RX_STATE_MONITOR_NEURON    1
#define RX_STATE_PROG_SYN_ADDR     2
#define RX_STATE_PROG_WEIGHT       3
#define RX_STATE_PROG_EXC          4
#define RX_STATE_SPIKE_SYN_ADDR    5
#define RX_STATE_SPIKE_NEU_ADDR    6
#define RX_STATE_SPIKE_EXC         7
// Poisson mean-ISI is sent as four 6-bit bytes (each < 0x40) so every data byte stays
// clear of a command sync byte (0xD0/0xE0..0xE3/0xF0). 24-bit mean in ticks.
#define RX_STATE_BURST_N          28
#define RX_STATE_PULSEFINE        29
#define RX_STATE_CALRUN_MODE      39
#define RX_STATE_CALRUN_LVL       30
#define RX_STATE_CALRUN_REPS      31
#define RX_STATE_CALRUN_TICKS     32
#define RX_STATE_CALRUN_LADDER    33
#define RX_STATE_GAP_N1           34
#define RX_STATE_GAP_N2           35
#define RX_STATE_GAP_HI           36
#define RX_STATE_GAP_LO           37
#define RX_STATE_GAP_REPS         38
#define RX_STATE_POISSON_B3        8
#define RX_STATE_POISSON_B2        9
#define RX_STATE_POISSON_B1       10
#define RX_STATE_POISSON_B0       11
#define RX_STATE_SYNFIRE_LAPS     12
// Coincidence: synA, synB, neuron, then 24-bit dt as four 6-bit bytes.
#define RX_STATE_COINC_SYNA       13
#define RX_STATE_COINC_SYNB       14
#define RX_STATE_COINC_NEU        15
#define RX_STATE_COINC_DT3        16
#define RX_STATE_COINC_DT2        17
#define RX_STATE_COINC_DT1        18
#define RX_STATE_COINC_DT0        19
// Recurrent connectivity: src, dst, then cw = count(bits0-3) | exc(bit4).
#define RX_STATE_RECUR_SRC        20
#define RX_STATE_RECUR_DST        21
#define RX_STATE_RECUR_CW         22
#define RX_STATE_RECUR_MODE       23
#define RX_STATE_MASK_B0          24
#define RX_STATE_MASK_B1          25
#define RX_STATE_MASK_B2          26
#define RX_STATE_PULSE_MULT       27

// Input-pulse width multiplier (cmd 0xDC). In .ramnoinit (dff2, ABOVE _fstack) because
// .bss globals down at 0x104-0x120 get clobbered by the deep -O0 main() frame.
// Precomputed loop count for the SRAM sendspike(). Resolving
// `pulse_fine ? pulse_fine-1 : 10*pulse_mult*CLK_SCALE` inside the function cost two
// global loads, a multiply and a branch -- ~120 B of dff2, which overruns the space. Compute
// it once whenever either knob changes and the hot path loads a single word.
volatile uint32_t pulse_mult __attribute__((section(".ramnoinit")));
volatile uint32_t pulse_ticks __attribute__((section(".ramnoinit")));


void delay_loop(volatile uint32_t count)
{
    // Bounds CPU iterations rather than time, so a raised core shortens every pulse.
    // Scale once here and all ~16 call sites keep their calibrated real-time width.
    count *= CLK_SCALE;
    while (count > 0) count--;
}

void blink(int n)
{
    int i;
    for (i = 0; i < n; i++) {
        reg_gpio_out = 0;        // LED ON (active-LOW)
        delay_loop(200000);
        reg_gpio_out = 1;        // LED OFF (active-LOW)
        delay_loop(200000);
    }
}

void long_pause()
{
    delay_loop(2000000);
}

//DEBUG to see if weights and spike setup are being programmed corrrectly
static void uart_try_tx(uint32_t byte)
{
    if (reg_uart_txfull == 0) {
        reg_uart_data = byte & 0xFF;
    }
}

static void uart_dbg_program_weight(uint32_t exc, uint32_t w, uint32_t syn_addr)
{
    uart_try_tx(UART_DBG_PROGRAM_WEIGHT);
    uart_try_tx(syn_addr & 0x0F);
    uart_try_tx(w & 0x0F);
    uart_try_tx(exc & 0x01);
}

static void uart_dbg_spike_setup(uint32_t exc, uint32_t syn_addr, uint32_t neu_addr)
{
    uart_try_tx(UART_DBG_SPIKE_SETUP);
    uart_try_tx(syn_addr & 0x0F);
    uart_try_tx(neu_addr & 0x0F);
    uart_try_tx(exc & 0x01);
}
//end DEBUG

//set weight for a synapse by setting exc=1 for excitatory and exc=0 for inhibitory
// w[0:3] is data and setW is used as clock for shifting W[0:3] at the same time on the rising edge,
// syn_addr[0:3] is used to select the synapse address after a 4 to 16 bit decoder.
// reset should be 0 for normal operation.
void program_neuron_weight(uint32_t exc, uint32_t *la0_out, uint32_t w, uint32_t syn_addr)
{
    // uart_dbg_program_weight(exc, w, syn_addr); //DEBUG
    if (exc)
        *la0_out |= X5_EXC_BIT;
    else
        *la0_out &= ~X5_EXC_BIT;

    // Set synapse address bits
    *la0_out = (*la0_out & ~(X5_SYN_ADDR_MASK)) | ((syn_addr & 0xF) << 23);

    // Ensure SETW_BIT is LOW before setting weight data (setup phase)
    *la0_out &= ~X5_SETW_BIT;
    
    //first we need to latch the data: exc, syn_addr in the first flipflop outside the core
    //for that we use X5_REQ_INP_BIT as clock
    //neu_addr only has to be set for a spike!

    // CLK low setup data
    *la0_out &= ~X5_REQ_INP_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    // CLK high (rising edge latches data)
    *la0_out |= X5_REQ_INP_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    // CLK low
    *la0_out &= ~X5_REQ_INP_BIT;
    reg_la0_data = *la0_out;

    // data propagation delay
    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    // Set weight bits (while SETW_BIT is low)
    *la0_out = (*la0_out & ~(X5_W_MASK)) | ((w & 0xF) << 27);
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    // CLK high (rising edge latches data)
    *la0_out |= X5_SETW_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    // CLK low
    *la0_out &= ~X5_SETW_BIT;
    reg_la0_data = *la0_out;
}

void resetsynapse(uint32_t *la0_out, uint32_t syn_addr, uint32_t exc)
{
    //set exc bit for resetting excitatory or inhibitory synapse
    if (exc)
        *la0_out |= X5_EXC_BIT;
    else
        *la0_out &= ~X5_EXC_BIT;
    
    // Set synapse address bits
    *la0_out = (*la0_out & ~(X5_SYN_ADDR_MASK)) | ((syn_addr & 0xF) << 23);
    reg_la0_data = *la0_out;

    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    //resetW high for one cycle to reset data in latch
    *la0_out |= X5_RESETW_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); //1tick=100ns at mult=1
    *la0_out &= ~X5_RESETW_BIT;
    reg_la0_data = *la0_out;
}

// setup exc, syn_addr, neu_addr bits, pulse req_inp to latch into input flipflop, then pulse req_inp again to send spike (data should hold steady for both rising edges)
void spikesetup (uint32_t *la0_out, uint32_t exc, uint32_t syn_addr, uint32_t neu_addr)
{
    // uart_dbg_spike_setup(exc, syn_addr, neu_addr); //DEBUG

    if (exc)
        *la0_out |= X5_EXC_BIT;
    else
        *la0_out &= ~X5_EXC_BIT;

    // x5.neu_addr wiring is [3:0] on la_data_in[16:19], so reverse nibble bit order.
    uint32_t neu_addr_hw = ((neu_addr & 0x1) << 3)
                         | ((neu_addr & 0x2) << 1)
                         | ((neu_addr & 0x4) >> 1)
                         | ((neu_addr & 0x8) >> 3);

    // Set neuron/synapse address with req_inp held low before the setup pulse.
    *la0_out &= ~X5_REQ_INP_BIT;
    *la0_out = (*la0_out & ~(X5_NEU_ADDR_MASK | X5_SYN_ADDR_MASK))
             | ((neu_addr_hw & 0xF) << 16)
             | ((syn_addr & 0xF) << 23);

    // Pulse x5.req_inp to setup data in the input flipflop before the core
    *la0_out &= ~X5_REQ_INP_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); // req high
    *la0_out |= X5_REQ_INP_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); // req low
    *la0_out &= ~X5_REQ_INP_BIT;
    reg_la0_data = *la0_out;
    delay_loop(10 * pulse_mult); // delay after setup before sending spikes
}

/* SRAM-RESIDENT, and the delay is INLINED rather than calling delay_loop().
 *
 * Measured end to end (PULSEBENCH 0xDE), this call took 72 us at pulse_mult=1 and 69 us
 * with the delay zeroed -- so the pulse was almost entirely fixed cost: the two
 * reg_la0_data writes and the call itself, fetched from XIP flash at ~131 cycles per
 * instruction. Every bias stayed above it, and charge per input event is
 * I_syn x width, so every input spike carried a ~70 us quantum of synaptic current.
 * That is why one spike saturated the membrane at every operating point tried, and why
 * a graded spike-count comparator stayed out of reach.
 *
 * Putting the function in dff2 removes the fetch cost. Calling delay_loop() from here
 * would put it straight back, hence the inlined loop. Cost: SPIKE_RING_SIZE halved to
 * make room.
 */
void __attribute__((section(".ramtext"), noinline, optimize("Os")))
sendspike(uint32_t *la0_out)
{   // (data should already be setup via spikesetup)
    *la0_out |= X5_REQ_INP_BIT; // set HIGH to send spike
    reg_la0_data = *la0_out;
    uint32_t c = pulse_ticks;
    while (c) { c--; __asm__ volatile(""); }
    *la0_out &= ~X5_REQ_INP_BIT; // set LOW after spike is sent
    reg_la0_data = *la0_out;
}

/* ONE burst loop, shared by every caller.
 *
 * cal_probe() and the host's BURST command contained the same source line -- a loop
 * calling the SRAM-resident sendspike() -- but sat in functions compiled at different
 * optimisation levels (cal_probe -Os, the BURST handler inside main() at -O0). The pulse
 * each spike delivers was therefore identical while the GAP between spikes varied, and a
 * wider gap leaks more charge between spikes, so more spikes are needed to reach
 * threshold. That is the direction of the unexplained disagreement: the host read
 * switching counts 2-3 ABOVE the core.
 *
 * The gap is too fast to measure here -- the membrane monitor samples at 100 Hz and a burst
 * lasts about 1 ms -- so rather than measure it, make it identical by construction:
 * noinline, one optimisation level, one call site's worth of overhead for everybody.
 */
__attribute__((noinline, optimize("Os")))
static void burst_fire(uint32_t *la0, uint32_t n)
{
    for (uint32_t i = 0; i < n; i++) sendspike(la0);
}

// --- On-chip Poisson spike generation -----------------------------------
// xorshift32 PRNG (shifts/xor only -- rv32i friendly, libgcc-free).
static uint32_t prng_state = 0x1234567u;
static uint32_t prng_next(void)
{
    uint32_t x = prng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    prng_state = x;
    return x;
}

// Unsigned 32x32 -> 32 multiply. rv32i multiplies in software and we link -nostdlib
// (libgcc's __mulsi3 stays out), so shift-add it by hand.
static uint32_t umul32(uint32_t a, uint32_t b)
{
    uint32_t r = 0;
    while (b) {
        if (b & 1u) r += a;
        a <<= 1;
        b >>= 1;
    }
    return r;
}

// ---- Timer0 numeric-LIF cost benchmark (0xEB) -----------------------------------------
// Compiled -O2 (match numeric_lif.lst) inside the -O0 firmware. Times a calibration loop of
// known core-cycle length and K lif_step() iterations with the free-running Timer0, prints
// raw ticks; the host converts ticks->core cycles. bench_sink is volatile so -O2 keeps
// the timed loops (and the calibration loop stays out of closed-form folding).
volatile uint32_t bench_sink;

// The LIF step is INLINED here (lif_step/umul32 call frames omitted): the firmware RAM is only
// 1 KB (dff: data+bss+stack), and bench_cmd runs deep inside main()'s large -O0 frame, so
// extra call depth overflows the stack. Inlining also matches numeric_lif.lst, where at -O2
// umul32 is inlined into the step. Values are printed as 32-bit hex (the firmware's print_dec
// caps at 2000). bench_sink is volatile so -O2 keeps the timed loops.
#ifndef BENCH_K
#define BENCH_K 2000u
#endif
#ifndef BENCH_CAL_ITERS
#define BENCH_CAL_ITERS 20000u
#endif
__attribute__((optimize("O2")))
// [0xDA] Minimum AER address-sample settle. Uses ONLY locals (like bench_cmd) so
// it is stack-safe; leaves the main handshake untouched. Free-run a single neuron
// (e.g. n14 via its bias set); for each post-ack settle s = 0..12, over ~300
// firing events, read the address at delay_loop(s) and again after a long
// ground-truth settle, and count mismatches. The smallest s with 0 mismatches
// (and ref == expected neuron) is the shortest we can stall the array and still
// latch the right address -> a faster req/ack cycle for the whole array. Blocking;
// the main-loop spike emit is idle during it, so UART carries only the report.
void select_monitor_neuron(uint32_t neuron, uint32_t *la2_out);   // fwd decl (defined below)

static inline uint32_t read_aer(void)
{
    uint32_t la1_in = reg_la1_data_in;
    uint32_t la2_in = reg_la2_data_in;
    return (((la1_in >> 30) & 1) << 3)
         | (((la1_in >> 31) & 1) << 2)
         | ((la2_in & 1) << 1)
         | ((la2_in >> 1) & 1);
}

#define STIM_PERIOD_TICKS (100000u * CLK_SCALE)   // 10 ms = 100 Hz, any core clock

static void measure_addr_settle(void)
{
    // Full n14 setup (matches the manual sequence): monitor n14, program synapse
    // 0 -> weight 15 excitatory, route synapse 0 -> neuron 14 excitatory. Only n14
    // is responsive (its bias set), so its output address is the known truth = 14.
    // We stimulate at 100 Hz (well-separated spikes, so req gaps cleanly between
    // them) and read the output address at each candidate post-ack settle s.
    uint32_t la0_out = 0, la1_out = 0, la2_out = 0;
    select_monitor_neuron(14, &la2_out);
    program_neuron_weight(1, &la0_out, 15, 0);       // exc, weight 15, synapse 0
    spikesetup(&la0_out, 1, 0, 14);                  // exc, synapse 0, neuron 14
    print("ADDRSETTLE\n");
    for (uint32_t s = 0; s <= 12u; s++) {
        uint32_t mismatch = 0, trials = 0, last_ref = 0;
        reg_timer0_update = 1;
        uint32_t tcap = reg_timer0_value;
        while (trials < 64u) {
            reg_timer0_update = 1;
            if ((uint32_t)(tcap - reg_timer0_value) >= 20000000u * CLK_SCALE) break; // 2 s cap/settle
            reg_timer0_update = 1; uint32_t tstim = reg_timer0_value;
            for (uint32_t k = 0; k < 5u; k++) sendspike(&la0_out);      // 5 inputs -> 1 output
            uint32_t wr = 0;
            while (!(reg_la1_data_in & X5_REQ_BIT) && (wr < 200000u * CLK_SCALE)) wr++; // await n14 output
            if (reg_la1_data_in & X5_REQ_BIT) {                         // n14 fired
                la1_out |= X5_ACK_BIT;  reg_la1_data = la1_out;          // ack
                delay_loop(s);
                uint32_t a_test = read_aer();
                delay_loop(30);                                         // ground-truth settle
                uint32_t a_ref = read_aer();
                la1_out &= ~X5_ACK_BIT; reg_la1_data = la1_out;         // deassert
                uint32_t w = 0;
                while ((reg_la1_data_in & X5_REQ_BIT) && (w < 200u)) w++;
                if (a_test != a_ref) mismatch++;
                last_ref = a_ref;
                trials++;
            }
            // pace to 100 Hz: hold until 10 ms since this input
            do { reg_timer0_update = 1; }
            while ((uint32_t)(tstim - reg_timer0_value) < STIM_PERIOD_TICKS);
        }
        print(" s="); print_hex(s, 2);
        print(" mism="); print_hex(mismatch, 4);
        print("/"); print_hex(trials, 4);
        print(" ref="); print_hex(last_ref, 1); print("\n");
    }
}

#include "../olfaction_kernel/model.h"
#include "../olfaction_kernel/testvec.h"
#include "../olfaction_kernel/arraypipe.h"

// Thresholds are pre-scaled per trial, so the traversal compares the raw Q8.8 feature
// directly and per-decision normalisation stays outside the cost -- the cheapest honest OP3.
__attribute__((optimize("O2")))
static void olfbench_cmd(void)
{
    const uint32_t CAL_ITERS = BENCH_CAL_ITERS, K = 200u;
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL_ITERS; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;
    uint32_t ticks_cal = c0 - c1;

    int32_t sink = 0;
    reg_timer0_update = 1; uint32_t s0 = reg_timer0_value;
    for (uint32_t k = 0; k < K; k++) {
        int32_t score[N_CLASS];
        for (int c = 0; c < N_CLASS; c++) score[c] = 0;
        int cls = 0;
        for (int tix = 0; tix < N_TREES; tix++) {
            int i = tree_root[tix];
            while (!node_tab[i].leaf)
                i = (olf_feat[node_tab[i].feat] <= node_tab[i].thr)
                    ? node_tab[i].left : node_tab[i].right;
            score[cls] += node_tab[i].val;
            if (++cls == N_CLASS) cls = 0;
        }
        int best = 0;
        for (int c = 1; c < N_CLASS; c++) if (score[c] > score[best]) best = c;
        sink += best + score[best];
    }
    reg_timer0_update = 1; uint32_t s1 = reg_timer0_value;
    uint32_t ticks_step = s0 - s1;
    bench_sink += (uint32_t)sink;

    print("OLFBENCH ci="); print_hex(CAL_ITERS, 8);
    print(" tc=");         print_hex(ticks_cal, 8);
    print(" K=");          print_hex(K, 8);
    print(" ts=");         print_hex(ticks_step, 8);
    print("\n");
}

/* SRAM-RESIDENT numeric LIF, to settle whether the array's advantage is analog physics
 * or merely memory residency.
 *
 * The flash-resident LIF step measures 5,090 cycles and the analog block (rail + the
 * SRAM-resident AER drain) 104 uJ against its 4,544 uJ -- an apparent 44x for the array.
 * But that compares a flash-resident emulation against an SRAM-resident drain, so a large
 * part of it is the ~37.8x instruction-fetch penalty rather than anything about analog.
 * This puts the identical LIF loop in .ramtext (dff2) so both sides are SRAM-resident and
 * the comparison is honest. The hot loop moves; the timing wrapper stays in flash.
 */
uint32_t __attribute__((section(LIF_SECTION), noinline, optimize("O2")))
lif_steps_ram(uint32_t K)
{
    int32_t v = 0, refr = 0, spikes = 0;
    uint32_t decay = 60000; int32_t jump = 3000, vth = 65536;
    for (uint32_t i = 0; i < K; i++) {
        uint32_t neg = v < 0;
        uint32_t a = neg ? (uint32_t)(-v) : (uint32_t)v, b = decay, r = 0;
        while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; }
        int32_t vv = neg ? -(int32_t)(r >> 16) : (int32_t)(r >> 16);
        vv += jump;
        if (vv < 0) vv = 0;
        if (refr > 0) { refr--; vv = 0; }
        else if (vv >= vth) { spikes++; vv = 0; refr = 125; }
        v = vv;
    }
    return (uint32_t)spikes;
}

/* Functional LIF over a supplied stimulus. -O2 to match lif_steps_ram()'s codegen, and
 * the buffer is a file-scope static because main()'s -O0 frame has little room for it. */

/* Blocking, everything in LOCALS, and it is resilient to stalls.
 *
 * The state variables need care: a stimulus buffer overflowed dff by 88 bytes
 * and dff2 by 228, packed globals still overflowed dff2 by 40, and putting them in .bss
 * put them where main()'s deep -O0 frame clobbers them -- which is why the state-machine
 * version stopped replying at all. Locals sidestep the question entirely.
 *
 * The earlier blocking version could wait forever on a lost byte, taking
 * the whole main loop down with it and swallowing the next frame along with it. A
 * bounded wait fixes that at the source: give up on a byte after roughly 40 ms, report it,
 * and return. The host is spared from unsticking the chip.
 *
 * Reading reg_uart_data leaves the FIFO unchanged -- reg_uart_ev_pending = 2 must be written,
 * exactly as the main dispatch loop does. With that write every read returns the next head
 * byte. */
#define LIFRUN_SPIN 400000u

/* The TICK is what the energy number prices, so it must be measured in the configuration
 * a real implementation would ship: SRAM-resident, and adding a PRECOMPUTED drive rather
 * than multiplying. Two reasons the first version's cycle count overstated a deployable
 * cost -- it ran from flash at ~131 cyc/instr, and it computed ev*w, which rv32i
 * implements in software and which lif_fixed() keeps precomputed (its drive arrives ready).
 * Build with -DLIFRAM_BUILD so LIF_SECTION is .ramtext; the AER drain falls back to flash,
 * which costs this measurement nothing because it stays clear of the array. */
__attribute__((section(LIF_SECTION), noinline, optimize("O2")))
static void lifrun_step(int32_t drive, uint32_t decay, int32_t vth, int32_t refrn,
                        int32_t *v, int32_t *refr, int32_t *spikes)
{
    int32_t vv0 = *v;
    uint32_t neg = vv0 < 0;
    uint32_t a = neg ? (uint32_t)(-vv0) : (uint32_t)vv0, b = decay, r = 0;
    while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; }
    int32_t vv = neg ? -(int32_t)(r >> 16) : (int32_t)(r >> 16);
    vv += drive;                       /* precomputed, exactly as lif_fixed() does */
    if (vv < 0) vv = 0;
    if (*refr > 0) { (*refr)--; vv = 0; }
    else if (vv >= vth) { (*spikes)++; vv = 0; *refr = refrn; }
    *v = vv;
}

__attribute__((optimize("O2")))
static uint32_t lifrun_get(uint32_t *ok)
{
    uint32_t spin = 0;
    while (reg_uart_rxempty) {
        if (++spin > LIFRUN_SPIN) { *ok = 0; return 0; }
    }
    uint32_t b = reg_uart_data & 0xFF;
    reg_uart_ev_pending = 2;
    return b;
}

/* LIFRUN2 [0xD2, T, dc_hi, dc_lo, vt_hi, vt_lo, refr, then T x 4-byte signed drive]
 *   -> "LIFRUN2 sp=<4> ds=<8> cy=<8> T=<4>"
 * Drive arrives PRECOMPUTED so the tick is multiply-free, and the tick is SRAM-resident, so
 * cy is the cost a deployed implementation would pay. ds echoes the summed drive as the
 * transport check. */
__attribute__((optimize("O2")))
static void lifbench_cmd(void)
{
    const uint32_t CAL = BENCH_CAL_ITERS, K = 300u;
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;

    int32_t v = 0, refr = 0, spikes = 0;
    reg_timer0_update = 1; uint32_t s0 = reg_timer0_value;
    for (uint32_t i = 0; i < K; i++)
        lifrun_step(20000, 64000, 32768, 10, &v, &refr, &spikes);
    reg_timer0_update = 1; uint32_t s1 = reg_timer0_value;
    bench_sink += (uint32_t)spikes;

    print("LIFBENCH ci="); print_hex(CAL, 8);
    print(" tc=");         print_hex(c0 - c1, 8);
    print(" K=");          print_hex(K, 8);
    print(" ts=");         print_hex(s0 - s1, 8);
    print("\n");
}

__attribute__((optimize("O2")))
static void lifrun2_cmd(void)
{
    uint32_t ok = 1, h[6];
    for (uint32_t i = 0; i < 6; i++) {
        h[i] = lifrun_get(&ok);
        if (!ok) { print("LIFRUN2 to=hdr\n"); return; }
    }
    uint32_t T = h[0], decay = (h[1] << 8) | h[2];
    int32_t vth = (int32_t)((h[3] << 8) | h[4]);
    int32_t refrn = (int32_t)h[5];
    /* WHICH ticks spiked, rather than just how many. The reference scores spike TIMES through an
     * exponential kernel, so the comparison needs more than a count. 150 ticks fit in
     * five 32-bit words. */
    int32_t v = 0, refr = 0, spikes = 0, dsum = 0;
    uint32_t cyc = 0, mask[5] = {0, 0, 0, 0, 0};
    for (uint32_t i = 0; i < T; i++) {
        uint32_t b0 = lifrun_get(&ok), b1 = lifrun_get(&ok);
        uint32_t b2 = lifrun_get(&ok), b3 = lifrun_get(&ok);
        if (!ok) { print("LIFRUN2 to=ev\n"); return; }
        int32_t drive = (int32_t)((b0 << 24) | (b1 << 16) | (b2 << 8) | b3);
        dsum += drive;
        int32_t before = spikes;
        reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
        lifrun_step(drive, decay, vth, refrn, &v, &refr, &spikes);
        reg_timer0_update = 1; cyc += c0 - reg_timer0_value;
        if (spikes != before && i < 160) mask[i >> 5] |= 1u << (i & 31);
    }
    print("LIFRUN2 sp="); print_hex((uint32_t)spikes, 4);
    print(" ds=");        print_hex((uint32_t)dsum, 8);
    print(" cy=");        print_hex(cyc, 8);
    print(" T=");         print_hex(T, 4);
    print(" m=");
    for (uint32_t i = 0; i < 5; i++) print_hex(mask[i], 8);
    print("\n");
}

__attribute__((optimize("O2")))
static void lifrun_cmd(void)
{
    uint32_t ok = 1, h[8];
    for (uint32_t i = 0; i < 8; i++) {
        h[i] = lifrun_get(&ok);
        if (!ok) { print("LIFRUN to=hdr\n"); return; }
    }
    uint32_t T = h[0], decay = (h[1] << 8) | h[2];
    int32_t w = (int32_t)((h[3] << 8) | h[4]);
    int32_t vth = (int32_t)((h[5] << 8) | h[6]);
    int32_t refrn = (int32_t)h[7];

    int32_t v = 0, refr = 0, spikes = 0, esum = 0;
    uint32_t cyc = 0;
    for (uint32_t i = 0; i < T; i++) {
        int32_t ev = (int32_t)(int8_t)lifrun_get(&ok);
        if (!ok) { print("LIFRUN to=ev\n"); return; }
        esum += ev;
        reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
        uint32_t neg = v < 0;
        uint32_t a = neg ? (uint32_t)(-v) : (uint32_t)v, b = decay, r = 0;
        while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; }
        int32_t vv = neg ? -(int32_t)(r >> 16) : (int32_t)(r >> 16);
        vv += ev * w;
        if (vv < 0) vv = 0;
        if (refr > 0) { refr--; vv = 0; }
        else if (vv >= vth) { spikes++; vv = 0; refr = refrn; }
        v = vv;
        reg_timer0_update = 1; cyc += c0 - reg_timer0_value;   /* down-counter */
    }
    print("LIFRUN sp="); print_hex((uint32_t)spikes, 4);
    print(" es=");       print_hex((uint32_t)esum, 8);
    print(" cy=");       print_hex(cyc, 8);
    print(" T=");        print_hex(T, 4);
    print("\n");
}

__attribute__((optimize("O2")))
static void lifram_cmd(void)
{
    const uint32_t CAL_ITERS = BENCH_CAL_ITERS, K = BENCH_K;
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL_ITERS; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;
    uint32_t ticks_cal = c0 - c1;

    reg_timer0_update = 1; uint32_t s0 = reg_timer0_value;
    uint32_t sp_ = lif_steps_ram(K);
    reg_timer0_update = 1; uint32_t s1 = reg_timer0_value;
    bench_sink += sp_;

    print("LIFRAM ci="); print_hex(CAL_ITERS, 8);
    print(" tc=");       print_hex(ticks_cal, 8);
    print(" K=");        print_hex(K, 8);
    print(" ts=");       print_hex(s0 - s1, 8);
    print("\n");
}

/* rv32i multiplies in software and the build is -nostdlib, so gcc's calls to the
 * libgcc helper are satisfied here. Supplying it also makes the measurement honest:
 * every multiply gcc leaves un-strength-reduced is priced at this routine's real
 * cost, which is exactly what the optimisation is trying to avoid. */
int __mulsi3(int a, int b)
{
    unsigned int ua = (unsigned int)a, ub = (unsigned int)b, r = 0;
    while (ub) { if (ub & 1u) r += ua; ua <<= 1; ub >>= 1; }
    return (int)r;
}

static short ap_buf[AP_STEPS];
static int   ap_feat[AP_NFEAT];

/* OPTIMISED array pipeline, timed against the naive one in the same image.
 *
 * The naive stages cost 7.07 M cycles (projection) and 5.58 M (kernel features), which
 * together dwarf everything else including the neurons they serve. Both are dominated by
 * ap_mul, a 16-iteration software shift-add, because rv32i multiplies in software.
 * Two changes remove most of it:
 *
 *  P': weights are Q8 COMPILE-TIME constants (ap_projq8 / AP_PROJ_DOT). At Q16 the
 *      product overflows int32; at Q8 it fits, and a literal constant lets gcc
 *      strength-reduce each multiply into a few shifts and adds instead of calling the
 *      software routine.
 *  K': the recursive decay multiplies on EVERY tick -- 4,800 times -- but only 85 ticks
 *      carry a spike. With a precomputed decay^dt table each spike contributes a table
 *      LOOKUP to each sample point, so the stage becomes MULTIPLY-FREE and iterates over
 *      events (85) rather than ticks (2,400).
 *
 * K' is mathematically identical to the recursive form rather than an approximation: the
 * accumulator at sample s is exactly sum over spikes of decay^(s - t_spike).
 */
__attribute__((optimize("O2")))
static void pulsebench_cmd(void)
{
    const uint32_t CAL_ITERS = BENCH_CAL_ITERS, K = 300u;
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL_ITERS; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;
    uint32_t ticks_cal = c0 - c1;

    // Time the WHOLE sendspike(), which is what the array sees: REQ high, delay, REQ
    // low. Timing delay_loop() in a for-loop instead (the earlier version) charged the
    // pulse for the enclosing loop and call overhead -- 684 cycles of it, which is most
    // of what was reported as a 29.6 us pulse. g_la0 points at main()'s la0_out so this
    // drives the real path rather than a dummy that would clear the staged route.
    reg_timer0_update = 1; uint32_t d0 = reg_timer0_value;
    for (uint32_t i = 0; i < K; i++) delay_loop(pulse_ticks);
    reg_timer0_update = 1; uint32_t d1 = reg_timer0_value;
    uint32_t ticks_dly = d0 - d1;

    reg_timer0_update = 1; uint32_t e0 = reg_timer0_value;
    for (uint32_t i = 0; i < K; i++) bench_sink += i;      // same loop, no spike
    reg_timer0_update = 1; uint32_t e1 = reg_timer0_value;
    uint32_t ticks_emp = e0 - e1;

    print("PULSEBENCH ci="); print_hex(CAL_ITERS, 8);
    print(" tc=");   print_hex(ticks_cal, 8);
    print(" K=");    print_hex(K, 8);
    print(" td=");   print_hex(ticks_dly, 8);
    print(" pf=");   print_hex(pulse_ticks, 8);
    print(" te=");   print_hex(ticks_emp, 8);
    print("\n");
}

__attribute__((optimize("O2")))
static void arrayopt_cmd(void)
{
    print("AOSTART\n");
    const uint32_t CAL_ITERS = BENCH_CAL_ITERS;
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL_ITERS; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;
    uint32_t ticks_cal = c0 - c1;
    int sink = 0;

    /* P': constant-weight projection */
    reg_timer0_update = 1; uint32_t p0 = reg_timer0_value;
    for (int u = 0; u < AP_UNITS; u++)
        for (int t = 0; t < AP_STEPS; t++) {
            const int *x = &olf_feat[t * AP_CHAN];
            ap_buf[t] = (short)ap_proj_dot(x, u);
        }
    reg_timer0_update = 1; uint32_t p1 = reg_timer0_value;
    uint32_t t_proj = p0 - p1;
    print("AOPROJ\n");

    /* K': event-driven, multiply-free kernel features */
    reg_timer0_update = 1; uint32_t k0 = reg_timer0_value;
    int fi = 0;
    const int step = AP_TICKS / AP_NSAMP;
    for (int u = 0; u < AP_UNITS; u++) {
        int ns = ap_nspk[u];
        for (int q = 0; q < AP_NTAU; q++) {
            for (int si = 0; si < AP_NSAMP; si++) {
                int sp = (si + 1) * step - 1, a = 0;
                for (int e = 0; e < ns; e++) {
                    int ts = ap_spkt[u][e];
                    if (ts > sp) break;
                    a += ap_decaypow[q][sp - ts];
                }
                ap_feat[fi + si] = a;
            }
            fi += AP_NSAMP;
        }
    }
    reg_timer0_update = 1; uint32_t k1 = reg_timer0_value;
    uint32_t t_kern = k0 - k1;
    sink += ap_feat[0] + ap_buf[0];
    bench_sink += (uint32_t)sink;

    print("ARRAYOPT ci="); print_hex(CAL_ITERS, 8);
    print(" tc=");   print_hex(ticks_cal, 8);
    print(" tp=");   print_hex(t_proj, 8);
    print(" tk=");   print_hex(t_kern, 8);
    print("\n");
}

/* Time the ARRAY's digital pipeline on silicon, stage by stage.
 *
 * The array-vs-digital table had two measured rows (AER drain, OP3 kernel) and four
 * ESTIMATED ones -- and the estimates claimed the array's digital overhead was ~3.8x the
 * whole digital baseline. Too load-bearing to leave modelled, so each stage is timed here
 * with Timer0, in the SAME binary at the SAME optimisation as olfbench_cmd's OP3 kernel.
 *
 * THE optimize("O2") ATTRIBUTE BELOW IS LOAD-BEARING. Without it this function compiles
 * at the file's -O0 while olfbench_cmd (which carries the attribute) compiles at O2, and
 * the comparison is meaningless: the identical calibration loop took 6 register-only
 * instructions in olfbench_cmd and 14 stack-based ones here, a 49x difference in the
 * calibration alone. The first measured version of this table was published with that
 * error in it.
 *
 *   P  projection  16 units x 50 steps x 8 channels MAC  -- feeding the neurons
 *   E  encode      level-crossing on the projected signals
 *   K  kernel      16 units x 2 taus, recursive decay over 150 ticks of REAL spikes
 *   C  classify    128 features x 5 classes MAC
 * The AER drain is already measured (105 + 480/event), so it stays as-is.
 *
 * TWO THINGS THIS EXPOSED, both of which the estimate had off:
 * (1) rv32i multiplies in software and the firmware is -nostdlib, so the firmware
 *     supplies its own __mulsi3. Every product below goes through ap_mul(), a shift-add whose
 *     cost scales with the multiplier's bit width. That IS the real cost on this core
 *     and it is now measured rather than assumed at "16 cycles".
 * (2) a 16x50 projection buffer overflowed dff. The pipeline is therefore STREAMED one
 *     unit at a time (50 shorts), which is what a real implementation would do anyway.
 */
/* Shift-add multiply. UNSIGNED internally on purpose: `a <<= 1` on a signed int that
 * overflows is undefined behaviour, and it bit the first version of this benchmark --
 * the -O0 and -O2 builds computed DIFFERENT results from the same inputs (the encoder
 * counted 209 events at -O0 and 576 at -O2), which is the signature of UB rather than
 * optimisation. Unsigned shifts are defined and both builds now agree. */
__attribute__((optimize("O2")))
static int ap_mul(int a, int b)
{
    int neg = 0;
    unsigned int ua, ub_, r = 0;
    if (a < 0) { ua = (unsigned int)(-(long)a); neg = !neg; } else ua = (unsigned int)a;
    if (b < 0) { ub_ = (unsigned int)(-(long)b); neg = !neg; } else ub_ = (unsigned int)b;
    while (ub_) { if (ub_ & 1u) r += ua; ua <<= 1; ub_ >>= 1; }
    return neg ? -(int)r : (int)r;
}

__attribute__((optimize("O2")))
static void arraybench_cmd(void)
{
    const uint32_t CAL_ITERS = BENCH_CAL_ITERS;
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL_ITERS; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;
    uint32_t ticks_cal = c0 - c1;
    int sink = 0;

    /* P: random projection 8 -> 16 */
    reg_timer0_update = 1; uint32_t p0 = reg_timer0_value;
    for (int u = 0; u < AP_UNITS; u++)
        for (int t = 0; t < AP_STEPS; t++) {
            int a = 0;
            for (int c = 0; c < AP_CHAN; c++)
                a += ap_mul(olf_feat[t * AP_CHAN + c], ap_proj[u][c]) >> AP_Q;
            ap_buf[t] = (short)a;
        }
    reg_timer0_update = 1; uint32_t p1 = reg_timer0_value;
    uint32_t t_proj = p0 - p1;

    /* E: level-crossing encode (runs over the last unit's buffer, x16 for all units) */
    reg_timer0_update = 1; uint32_t e0 = reg_timer0_value;
    int nev = 0;
    for (int u = 0; u < AP_UNITS; u++) {
        int prev = ap_buf[0];
        for (int t = 1; t < AP_STEPS; t++) {
            int d = ap_buf[t] - prev;
            if (d > 4096 || d < -4096) { nev++; prev = ap_buf[t]; }
        }
    }
    reg_timer0_update = 1; uint32_t e1 = reg_timer0_value;
    uint32_t t_enc = e0 - e1;
    sink += nev;

    /* K: exponential kernel features over the REAL recorded spikes.
       Accumulator is Q8 (rather than Q16) so acc*decay stays inside int32 -- at Q16 the product
       reaches 2^34 and would need __muldi3, which -nostdlib leaves out. */
    reg_timer0_update = 1; uint32_t k0 = reg_timer0_value;
    int fi = 0;
    for (int u = 0; u < AP_UNITS; u++)
        for (int q = 0; q < AP_NTAU; q++) {
            int a = 0, step = AP_TICKS / AP_NSAMP, next = step, si = 0;
            for (int t = 0; t < AP_TICKS; t++) {
                a = (ap_mul(a, ap_decay[q]) >> AP_Q) + (ap_spk[u][t] << 8);
                if (t + 1 >= next && si < AP_NSAMP) {
                    ap_feat[fi + si] = a; si++; next += step;
                }
            }
            fi += AP_NSAMP;
        }
    reg_timer0_update = 1; uint32_t k1 = reg_timer0_value;
    uint32_t t_kern = k0 - k1;

    /* C: linear read-out, scaler folded into the weights */
    reg_timer0_update = 1; uint32_t l0 = reg_timer0_value;
    int best = 0, bs = 0;
    for (int c = 0; c < AP_NCLASS; c++) {
        int sc = ap_b[c];
        for (int f = 0; f < AP_NFEAT; f++)
            sc += ap_mul(ap_w[c][f], ap_feat[f]) >> AP_Q;
        if (c == 0 || sc > bs) { bs = sc; best = c; }
    }
    reg_timer0_update = 1; uint32_t l1 = reg_timer0_value;
    uint32_t t_clf = l0 - l1;
    bench_sink += (uint32_t)(sink + best + bs);

    print("ARRAYBENCH ci="); print_hex(CAL_ITERS, 8);
    print(" tc=");   print_hex(ticks_cal, 8);
    print(" tp=");   print_hex(t_proj, 8);
    print(" te=");   print_hex(t_enc, 8);
    print(" tk=");   print_hex(t_kern, 8);
    print(" tl=");   print_hex(t_clf, 8);
    print(" nev=");  print_hex((uint32_t)nev, 8);
    print("\n");
}

/* O2 like olfbench_cmd and arraybench_cmd. Without it this compiles at the file's -O0
 * and the numeric-LIF baseline is handicapped against the O2 tree kernel it is compared
 * with -- the same error that invalidated the first array-pipeline table. The digital
 * emulation must be the STRONGEST this core can do, rather than the laziest. */
__attribute__((optimize("O2")))
static void bench_cmd(void)
{
    const uint32_t CAL_ITERS = BENCH_CAL_ITERS, K = BENCH_K;

    // (1) calibration: REGISTER-ONLY loop of known instruction count (minimal per-iter memory,
    //     matching the LIF loop's profile so ticks scale with retired instructions). Result
    //     stored once so -O2 keeps it; data-dependent so it stays out of closed-form folding.
    uint32_t acc = 1;
    reg_timer0_update = 1; uint32_t c0 = reg_timer0_value;
    for (uint32_t i = 0; i < CAL_ITERS; i++) { acc = (acc << 1) | (acc >> 31); acc ^= i; }
    reg_timer0_update = 1; uint32_t c1 = reg_timer0_value;
    bench_sink = acc;
    uint32_t ticks_cal = c0 - c1;                                 // down-counter

    // (2) K inlined LIF steps, 16-bit decay (16 soft-mul iters), typical silent hot path
    int32_t v = 0, refr = 0, spikes = 0;
    uint32_t decay = 60000; int32_t jump = 3000, vth = 65536, vreset = 0;
    reg_timer0_update = 1; uint32_t s0 = reg_timer0_value;
    for (uint32_t i = 0; i < K; i++) {
        uint32_t neg = v < 0;
        uint32_t a = neg ? (uint32_t)(-v) : (uint32_t)v, b = decay, r = 0;
        while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; }        // shift-add multiply
        int32_t vv = neg ? -(int32_t)(r >> 16) : (int32_t)(r >> 16);
        vv += jump;
        if (vv < 0) vv = 0;
        if (refr > 0) { refr--; vv = vreset; }
        else if (vv >= vth) { spikes++; vv = vreset; refr = 125; }
        v = vv;
    }
    reg_timer0_update = 1; uint32_t s1 = reg_timer0_value;
    uint32_t ticks_step = s0 - s1;
    bench_sink += (uint32_t)spikes;

    print("BENCH ci="); print_hex(CAL_ITERS, 8);
    print(" tc=");      print_hex(ticks_cal, 8);
    print(" K=");       print_hex(K, 8);
    print(" ts=");      print_hex(ticks_step, 8);
    print("\n");
}

// -ln(U) lookup, U=(i+0.5)/256, scaled by 128 (value = round(-ln(U)*128)).
// With E[-ln U] = 1, drawing ISI = mean_ticks*(-ln U) gives E[ISI] = mean_ticks,
// i.e. a true Poisson process at rate 1/mean. Shift by 7 undoes the *128 scale.
static const uint16_t neglog_lut[256] = {
     799,  658,  592,  549,  517,  492,  470,  452,
     436,  422,  409,  397,  386,  377,  367,  359,
     351,  343,  336,  330,  323,  317,  311,  306,
     300,  295,  290,  286,  281,  277,  272,  268,
     264,  260,  257,  253,  249,  246,  242,  239,
     236,  233,  230,  227,  224,  221,  218,  216,
     213,  210,  208,  205,  203,  200,  198,  196,
     193,  191,  189,  187,  185,  183,  180,  178,
     176,  174,  173,  171,  169,  167,  165,  163,
     161,  160,  158,  156,  155,  153,  151,  150,
     148,  147,  145,  143,  142,  140,  139,  137,
     136,  135,  133,  132,  130,  129,  128,  126,
     125,  124,  122,  121,  120,  118,  117,  116,
     115,  113,  112,  111,  110,  109,  108,  106,
     105,  104,  103,  102,  101,  100,   99,   98,
      96,   95,   94,   93,   92,   91,   90,   89,
      88,   87,   86,   85,   84,   83,   82,   81,
      80,   80,   79,   78,   77,   76,   75,   74,
      73,   72,   71,   71,   70,   69,   68,   67,
      66,   65,   65,   64,   63,   62,   61,   61,
      60,   59,   58,   57,   57,   56,   55,   54,
      54,   53,   52,   51,   51,   50,   49,   48,
      48,   47,   46,   45,   45,   44,   43,   43,
      42,   41,   41,   40,   39,   39,   38,   37,
      36,   36,   35,   35,   34,   33,   33,   32,
      31,   31,   30,   29,   29,   28,   28,   27,
      26,   26,   25,   24,   24,   23,   23,   22,
      21,   21,   20,   20,   19,   19,   18,   17,
      17,   16,   16,   15,   15,   14,   13,   13,
      12,   12,   11,   11,   10,   10,    9,    9,
       8,    7,    7,    6,    6,    5,    5,    4,
       4,    3,    3,    2,    2,    1,    1,    1,
};

// Next exponential inter-spike interval (timer ticks) for the given mean.
static uint32_t poisson_next_isi(uint32_t mean_ticks)
{
    uint32_t u = prng_next() >> 24;                 // top 8 bits -> LUT index
    uint32_t isi = umul32(mean_ticks, neglog_lut[u]) >> 7;
    return isi ? isi : 1u;
}

// Shift 4-bit neuron address into monitor_select via Da/CLK
// MSB first: Da enters D[0], pushes toward D[3]. First bit shifted
// ends up at D[3] after 4 clocks, so send MSB (bit 3) first.
void select_monitor_neuron(uint32_t neuron, uint32_t *la2_out)
{
    int i;
    for (i = 3; i >= 0; i--) {
        // Set Da
        if (neuron & (1 << i))
            *la2_out |= X5_DA_BIT;
        else
            *la2_out &= ~X5_DA_BIT;

        // CLK LOW, setup Da
        *la2_out &= ~X5_CLK_BIT;
        reg_la2_data = *la2_out;
        delay_loop(10);

        // CLK HIGH (rising edge latches Da)
        *la2_out |= X5_CLK_BIT;
        reg_la2_data = *la2_out;
        delay_loop(10);

        // CLK LOW
        *la2_out &= ~X5_CLK_BIT;
        reg_la2_data = *la2_out;
        delay_loop(10);
    }

    // Clear Da
    *la2_out &= ~X5_DA_BIT;
    reg_la2_data = *la2_out;
}

// ---- SRAM-resident fast AER drain (fast reservoir mode, STREAM_SPIKES=0) ----
// This loop runs from dff2 (.ramtext) rather than XIP flash, so its instruction fetch
// avoids the XIP bound -- the cost that capped the readout. It acks each neuron ASAP
// (so it resets and re-fires instead of holding req) and tallies per-neuron
// spike counts into dff2 (.ramnoinit, above _fstack -> immune to the low-.bss
// stack-overflow bug). The body keeps all calls inlined, so nothing here is
// fetched from XIP (delay + address decode are inlined by hand).
// All dff2-resident drain state in one struct so aer_drain needs only ONE
// base-address register (rather than 7 separate globals -> 9 callee-saved saves).
// Mode 0 (benchmark): aer_counts + hs_* timing, ring and UART off.
// Mode 1 (stream): ring capture only, counts and timing off — the host
//   reconstructs per-neuron rates from the packet stream, and µs/handshake
//   is measured with mode 0 (0xDB) rather than while streaming.
#if STREAM_SPIKES
// 8 entries filled on ordinary bursts even well under the UART ceiling.
// 16 is the largest power of two that fits: dff2 is nearly full, and 32 exceeds
// .ramnoinit by 12 B. Doubles the burst headroom; the sustained ceiling is still
// the UART, so drops are reported rather than engineered away.
// 8 rather than 16: the ring is the bulk of .ramnoinit and dff2 has to also hold the
// SRAM-resident sendspike(). Halving it frees 32 B. Safe for how we acquire -- runs mask
// to one neuron, so spikes arrive far slower than the 1.67 ms it takes to flush one
// 4-byte packet at 24000 baud, and drops have measured 0 with wide margin. The unmasked
// AER bracket scan streams all 16 briefly; watch `drops` there.
#define SPIKE_RING_SIZE 2u
#define SPIKE_RING_MASK (SPIKE_RING_SIZE - 1)
// Sticky OR into byte 0 of the next packet (byte 0 is 0x80|id, so bits 4-6 are
// free). Tells the host "spikes were lost before this one" at zero bandwidth
// cost -- essential, because the rate alone hides loss:
// dropping is exactly what holds that rate below the link ceiling.
#define SPIKE_DROP_FLAG 0x40u
// Bit 5: the flush had to WAIT for the UART FIFO, i.e. the link is the bottleneck
// and the array is being back-pressured (a neuron holds req until it is acked).
// Rates are then real but throttled rather than free-running -- mask neurons to buy bandwidth.
#define SPIKE_STALL_FLAG 0x20u
// Write one byte, waiting for room. Writing into a full FIFO silently discards the byte,
// which corrupts the 4-byte packet, so every byte must be gated, rather than only the first.
#define UART_PUT(b) do {                                   \
        if (reg_uart_txfull) drain_ram.stalls = 1;         \
        while (reg_uart_txfull) { }                        \
        reg_uart_data = (b);                               \
    } while (0)
#endif
/* Field order and widths are chosen to fit dff2 alongside the SRAM-resident sendspike():
 * spike_ring first so it is naturally aligned, then the 16-bit and 8-bit fields packed
 * behind it. drops/stalls are uint8 because they are asserted ZERO -- saturating at 255
 * still reads as "nonzero: out of tolerance". */
/* Field widths and order are chosen so this fits dff2 alongside the SRAM-resident
 * sendspike(): spike_ring first so it stays naturally aligned, the 16-bit fields behind
 * it, then the bytes. drops/stalls are uint8 because they are asserted ZERO -- saturating
 * at 255 still reads as "nonzero: out of tolerance". */
struct drain_ram {
#if !STREAM_SPIKES
    // Mode 0: benchmark instrumentation only.
    volatile uint32_t last_aer;
    volatile uint16_t aer_counts[16];
    volatile uint32_t hs_ticks_sum;
    volatile uint32_t hs_count;
#else
    // Mode 1: ring buffer only.
    uint32_t spike_ring[SPIKE_RING_SIZE];
    volatile uint16_t last_aer;        // synfire/recurrent routing
    volatile uint16_t spike_mask;      // bit i = stream neuron i (0xFFFF = all)
    volatile uint8_t ring_head;
    volatile uint8_t ring_tail;
    volatile uint8_t drops;            // spikes overwritten before the host read them
    volatile uint8_t stalls;           // flush had to wait on the UART FIFO
#endif
} drain_ram __attribute__((section(".ramnoinit")));

uint32_t __attribute__((section(AER_SECTION), noinline, optimize("Os")))
aer_drain(uint32_t *la1_out_p, struct drain_ram *dr)
{
    uint32_t drained = 0;
#if STREAM_SPIKES
    uint32_t rh = dr->ring_head;
    uint32_t rt = dr->ring_tail;
#else
    reg_timer0_update = 1; uint32_t t0 = reg_timer0_value;
#endif
    while ((reg_la1_data_in & X5_REQ_BIT) && (drained < 64u)) {
        drained++;
        *la1_out_p |= X5_ACK_BIT;  reg_la1_data = *la1_out_p;   // Phase 1/2: ack
        volatile uint32_t s = 2; while (s) s--;                 // post-ack settle (inlined)
        uint32_t la1_in = reg_la1_data_in;
        uint32_t la2_in = reg_la2_data_in;
        uint32_t addr = (((la1_in >> 30) & 1) << 3)
                      | (((la1_in >> 31) & 1) << 2)
                      | ((la2_in & 1) << 1)
                      | ((la2_in >> 1) & 1);
        dr->last_aer = addr;
#if STREAM_SPIKES
        // Filtered-out neurons were already acked above (mandatory: req stays high
        // until acked). Skipping them here costs zero ring slots and zero UART bytes,
        // and a masked neuron stays out of the drop path for the ones we do want.
        if ((dr->spike_mask >> (addr & 0x0F)) & 1u) {
            reg_timer0_update = 1;
            // 21-bit timestamp: bytes 1..3 carry 7 bits each, so 16 bits leaves 5 of
            // them unused. 16 bits wraps every 1.31 ms at 50 MHz -- SHORTER than the FTDI's
            // 16 ms latency timer, so the host clock is too short to unwrap it. 21 bits wraps every
            // 41.9 ms, which the host clock resolves easily. Address moves to bit 21.
            dr->spike_ring[rh] = ((addr & 0x0F) << 21) | (reg_timer0_value & 0x1FFFFFu);
            rh = (rh + 1) & SPIKE_RING_MASK;
            if (rh == rt) {             // ring full: the OLDEST spike is overwritten
                rt = (rt + 1) & SPIKE_RING_MASK;
                dr->drops++;            // only on overflow, so the fast path is unchanged
            }
        }
#else
        dr->aer_counts[addr & 0x0F]++;
#endif
        // Phase 3: wait for req to fall, WITH ACK STILL ASSERTED. This is the half of
        // the 4-phase cycle the early version left out: ack used to drop here ("deassert ASAP")
        // while req was still high, so the outer loop re-entered, re-acked and re-read
        // the SAME still-asserted address. That emitted one spike as 2, 4, ... packets
        // (microseconds apart, far below the analog refractory), and the multiplicity
        // grew with the core clock and with how long a neuron holds req (its biases).
        // The bound is only a hang guard; it must be a real-time budget, so scale it.
        uint32_t rw = 0;
        while ((reg_la1_data_in & X5_REQ_BIT) && (rw < REQ_LOW_MAX)) rw++;
        // Phase 4: only now release ack. The neuron completes its reset dead time and
        // re-asserts req on its NEXT spike rather than this one.
        *la1_out_p &= ~X5_ACK_BIT; reg_la1_data = *la1_out_p;
    }
#if STREAM_SPIKES
    dr->ring_head = rh;
    dr->ring_tail = rt;
#else
    if (drained) {
        reg_timer0_update = 1; uint32_t t1 = reg_timer0_value;
        dr->hs_ticks_sum += (t0 - t1);
        dr->hs_count     += drained;
    }
#endif
    return drained;
}

// [0xDB] Report handshake timing + per-neuron counts over UART, then reset.
// Mode 0 only: the host measures µs/handshake = hs_ticks_sum / (10 * hs_count),
// per-neuron rate_i = c_i / T.  In mode 1 the host reconstructs rates from
// the spike packet stream instead.
#if !STREAM_SPIKES
static void report_hs(void)
{
    print("HS t="); print_hex(drain_ram.hs_ticks_sum, 8);
    print(" n=");   print_hex(drain_ram.hs_count, 8);
    for (uint32_t i = 0; i < 16; i++) { print(" "); print_hex(drain_ram.aer_counts[i], 4); }
    print("\n");
    drain_ram.hs_ticks_sum = 0; drain_ram.hs_count = 0;
    for (uint32_t i = 0; i < 16; i++) drain_ram.aer_counts[i] = 0;
}
#endif

// ===== CALRUN (0xD5) / CALSET (0xD6): on-die drift detect + recovery ========
//
// The demonstration this exists for: the die detects that a comparator threshold has
// moved and recovers it, with zero host traffic in the loop between the injection and the
// telemetry read. The host's only jobs are loading the level's biases (which inference
// on this die requires regardless -- a threshold IS a bias here) and storing what comes
// back.
//
// FLASH-RESIDENT ON PURPOSE. dff2 holds aer_drain with 4 bytes free, so this handler
// lives in flash. The cost is invisible: a cycle is paced by the ~31 ms membrane re-arm
// per burst, against which flash fetch (~131 cyc/instr) of a small control loop is
// noise. Two rules follow and are obeyed below: this handler keeps spikes off the stream (a
// flash-resident handler would fall behind the UART), so it masks to the probed neuron
// and consumes the ring itself; and every wait is Timer0-bounded, or a stalled handshake
// wedges the main loop.
//
// FIRING IS READ FROM THE RING rather than from a counter. STREAM_SPIKES=1 builds leave
// out aer_counts[]; adding one would grow .ramtext, which is already full. With the mask set
// to a single neuron, "did it fire" is just "did ring_head advance".
//
// PROBE ORDER IS zero, below, above, at -- with `at` LAST. Measured 2026-08-19: the
// first suprathreshold burst after a long idle can miss (cold-start, sub-count,
// DEFERRED.md sec.1). `above` fires deterministically even cold -- 13 hold rounds, zero
// flips -- so it doubles as warm-up for `at`. `zero` sends zero spikes and warms nothing,
// which keeps it out of the warm-up slot.
#define UART_CMD_CALRUN        0xD5

#define CAL_LEVELS   6
#define CAL_ORD      7      /* one ordinal per inter-threshold interval, not 33 */
#define CAL_NMAX     32
#define CAL_GMIN     1      /* encoding margin in counts; see DEFERRED.md sec.2 --
                             * should eventually come from measured edge half-width */
#define CAL_MINGAP   2      /* below this, midpoint encoding loses its margin */
#define CAL_SETTLE   40000u /* Timer0 ticks to wait for a spike after a burst */
/* RE-ARM between repetitions. The membrane time constant is ~10 ms and a node slot is
 * 31.2 ms, but the first version waited at most 4 ms and exited the instant a spike was
 * detected -- so after the neuron fired, the next burst began microseconds later, on a
 * membrane still returning to rest. Residual charge makes the neuron fire on fewer
 * spikes than it would from rest, which is why the core read thresholds ~2-3 counts BELOW
 * the host (which paces at 100 ms), why the width-repair loop chased a moving target, and
 * why re-verification came up short: each probe perturbed the next. One slot of quiet
 * between repetitions makes a threshold a property of the neuron again. */
#define CAL_REARM    1000000u /* Timer0 ticks (~100 ms) of quiet after every repetition.
                              * Matched to the host path, whose drain loop keeps it above ~60 ms,
                              * so 100 ms is the nearest
                              * value both sides can hold. Comfortably past the measured
                              * return to rest (bracket [12, 32] ms). */
#define CAL_MAXTICKS 254u   /* PULSEFINE raw count ceiling */
#define CAL_TPC      5u     /* ticks of width per count of threshold, from
                             * the measured width sweep (~3-7 near default) */

/* State avoids .bss. Measured 2026-08-19: main()'s -O0 frame is 720 B, so it spans
 * 0x130..0x400 while .bss ends at 0x388 -- anything persistent in .bss sits underneath
 * main's own frame and is clobbered between calls. (.ramnoinit, the reliable
 * region, has 4 bytes free -- short of the 20 needed.) So CALRUN follows this firmware's
 * existing idiom for handlers -- 0xDA: "Uses ONLY locals (like bench_cmd)". The
 * calibrated ladder arrives in the command payload and is held in main's own frame,
 * which is the one piece of stack that is unambiguously main's to use. */

/* Midpoint encoding, re-derived from a ladder. Floor midpoint of the bracketing
 * switching counts, with the lowest interval encoded as zero spikes -- the rule
 * recovered from the Sec. V run itself: {0,7,9,14,19,25,31} for N*={6,8,11,18,21,29}. */
__attribute__((optimize("Os")))
static void cal_encode(volatile uint8_t *nst, volatile uint8_t *out)
{
    out[0] = 0;
    for (uint32_t i = 1; i < CAL_ORD - 1; i++)
        out[i] = (uint8_t)((nst[i - 1] + nst[i]) >> 1);
    out[CAL_ORD - 1] = (uint8_t)((nst[CAL_LEVELS - 1] + CAL_NMAX + 1u) >> 1);
}

/* Every burst count must clear every switching count by >= CAL_GMIN. This is the
 * difference between "recovered" and "recovered silently onto the 13.3% boundary regime":
 * under the ladder measured 2026-08-19 the stale table put bursts 7 and 9
 * exactly ON switching counts, 11.1% of all comparisons. */
__attribute__((optimize("Os")))
static uint32_t cal_margin_ok(volatile uint8_t *nst, volatile uint8_t *bur, uint32_t *worst)
{
    uint32_t w = 255;
    for (uint32_t i = 0; i < CAL_ORD; i++) {
        if (bur[i] == 0) continue;              /* ordinal 0 sends nothing */
        for (uint32_t j = 0; j < CAL_LEVELS; j++) {
            int32_t d = (int32_t)bur[i] - (int32_t)nst[j];
            if (d < 0) d = -d;
            if ((uint32_t)d < w) w = (uint32_t)d;
        }
    }
    *worst = w;
    return w >= CAL_GMIN;
}

/* One probe: fire `n` spikes, then wait (bounded) for the neuron to answer. Returns the
 * number of repetitions that fired. Drains and consumes the ring itself. */
__attribute__((optimize("Os")))
static uint32_t cal_probe(uint32_t *la0, uint32_t *la1, uint32_t n, uint32_t reps)
{
    uint32_t fired = 0;
    for (uint32_t r = 0; r < reps; r++) {
        /* clear anything pending so the snapshot means what it says */
        for (uint32_t g = 0; g < 4; g++) (void)aer_drain(la1, &drain_ram);
        drain_ram.ring_tail = drain_ram.ring_head;

        burst_fire(la0, n);            /* shared loop: see burst_fire() */

        /* COUNT the events aer_drain services; skip the ring_head comparison. The ring holds
         * SPIKE_RING_SIZE=2 entries, so its head index toggles 0<->1 and any EVEN number
         * of spikes in the window returns it to where it started -- read as "silent".
         * A neuron above threshold often emits more than one spike, so that test
         * made the bisection walk past the true N* (measured: 23 against a host-measured
         * 16). aer_drain's return value is monotone and free of that ambiguity. */
        reg_timer0_update = 1;
        uint32_t t0 = reg_timer0_value;          /* down-counter */
        uint32_t hit = 0;
        for (;;) {
            if (aer_drain(la1, &drain_ram)) { hit = 1; break; }
            reg_timer0_update = 1;
            if ((uint32_t)(t0 - reg_timer0_value) > CAL_SETTLE) break;   /* timeout */
        }
        if (hit) fired++;
        drain_ram.ring_tail = drain_ram.ring_head;

        /* Let the membrane return to rest before the next repetition. Keep draining so a
         * stalled handshake keeps req from holding high across the gap. */
        reg_timer0_update = 1;
        uint32_t tq = reg_timer0_value;
        for (;;) {
            (void)aer_drain(la1, &drain_ram);
            reg_timer0_update = 1;
            if ((uint32_t)(tq - reg_timer0_value) > CAL_REARM) break;
        }
        drain_ram.ring_tail = drain_ram.ring_head;
    }
    return fired;
}

/* Smallest N that fires in every repetition, by bisection. 0 = outside the range. */
__attribute__((optimize("Os")))
static uint32_t cal_bisect(uint32_t *la0, uint32_t *la1, uint32_t reps)
{
    /* WARM-UP. The first suprathreshold burst after an idle can lose its first repetition
     * (cold-start, measured 2026-08-19: sub-count, deterministic, miss@[0]). A bracket
     * that walks UP from n=4 meets that miss at the first count that should fire, reads
     * it as "fired in fewer reps", and steps past -- so a cold bisection reports
     * N* one count HIGH. One discarded suprathreshold burst removes the whole effect;
     * N=CAL_NMAX fires whenever anything in range does. */
    (void)cal_probe(la0, la1, CAL_NMAX, 1);
    uint32_t lo = 0, hi = 0;
    for (uint32_t n = 4; n <= CAL_NMAX; n <<= 1) {
        if (cal_probe(la0, la1, n, reps) == reps) { hi = n; break; }
        lo = n;
    }
    if (!hi) return 0;
    while (hi - lo > 1) {
        uint32_t mid = (lo + hi) >> 1;
        if (cal_probe(la0, la1, mid, reps) == reps) hi = mid; else lo = mid;
    }
    return hi;
}

__attribute__((optimize("Os")))
/* CALRUN is TWO PHASES, and they stay separate.
 *
 * The first version validated after every single-level measurement, so it checked one
 * freshly measured count against five values that were still the stale written-down ones.
 * That mixture falls outside a single coherent ladder: raising level 0 from its recorded 6 to its measured 7 put
 * it one count from the stale 8, below the minimum gap, and the check refused. Four of six
 * levels refused that way and the refusals cascaded. The measurements themselves were
 * fine; the phase structure was the issue.
 *
 *   Phase A (mode 0), calrun_measure: probe ONE level, report where its threshold now is,
 *      and try to walk it back to its calibrated value with the pulse width. No validation
 *      and an empty encoding table -- validation waits on a complete ladder.
 *   Phase B (mode 1), calrun_derive: given all six counts, validate the ladder ONCE
 *      (range, order, gap) and derive the encoding ONCE, then print it.
 *
 * Both run on the core. The host carries the six counts from phase A into phase B because
 * this handler is stateless between calls -- main()'s -O0 frame spans .bss, so anything
 * persistent there is clobbered. That carry is transport: the host carries values, while
 * threshold, midpoint and verdict all stay on-chip.
 */
__attribute__((optimize("Os")))
static void calrun_measure(uint32_t *la0, uint32_t *la1, uint32_t lvl, uint32_t reps,
                           const uint8_t *cal_ref)
{
    if (lvl >= CAL_LEVELS || reps == 0 || reps > 32) { print("CAL err=arg\n"); return; }
    uint16_t save_mask = drain_ram.spike_mask;
    drain_ram.spike_mask = (uint16_t)(1u << 14);
    reg_timer0_update = 1;
    uint32_t tstart = reg_timer0_value;

    uint32_t nref = cal_ref[lvl];

    /* sentinel, `at` LAST: the first suprathreshold burst after an idle loses its first
     * repetition (cold start), and `above` fires even cold, so it doubles as warm-up. */
    uint32_t p0    = cal_probe(la0, la1, 0, reps);
    uint32_t below = (nref >= 2) ? cal_probe(la0, la1, nref - 2, reps) : 0;
    uint32_t above = cal_probe(la0, la1, nref + 1, reps);
    uint32_t at    = cal_probe(la0, la1, nref, reps);

    if (p0 * 20u > reps) {                      /* free-running: nothing here is a counter */
        print("CALM lvl="); print_hex(lvl, 2);
        print(" REJECT=freerun p0="); print_hex(p0, 2);
        print("/"); print_hex(reps, 2); print("\n");
        drain_ram.spike_mask = save_mask;
        return;
    }

    /* trip on the OUTER probes only; `at` is direction telemetry rather than a trip condition */
    uint32_t tripped = (below > 1u) || ((reps - above) > 1u);

    uint32_t meas = nref, now = nref, path = 0, ticks_used = pulse_ticks;
    if (tripped) {
        meas = cal_bisect(la0, la1, reps);
        now  = meas;
        if (meas == 0) {
            reg_timer0_update = 1;
            print("CALM lvl="); print_hex(lvl, 2);
            print(" ref=");  print_hex(nref, 2);
            print(" meas=00 now=ff trip=1 path=0 oor=1 p0="); print_hex(p0, 2);
            print(" ticks0="); print_hex(tstart - reg_timer0_value, 8);
            print("\n");
            drain_ram.spike_mask = save_mask;
            return;                              /* out of range: phase B decides */
        }
        /* WIDTH CORRECTION. Charge per input event is I_syn x pulse width and the core
         * writes that width directly -- DAC-free -- so walking the threshold back to its
         * calibrated value leaves the ORIGINAL encoding valid. Try this first.
         *
         * The error is in COUNTS and the actuator is in TICKS, and they are different
         * units: one count of threshold costs roughly CAL_TPC ticks of width. The first
         * version added the count error straight onto the ticks, so a one-count miss
         * produced a one-tick step -- about a fifth of what is needed -- and the guard ran
         * out before the threshold moved. Levels 6 and 12 came up short for exactly that reason,
         * with 234 ticks of unused headroom in the direction they needed to go.
         *
         * Step proportionally until the error changes sign, then bisect the bracket. N* is
         * monotone decreasing in width, so the bracket is well defined: t_lo is a width
         * known to leave N* too HIGH, t_hi one that leaves it too LOW. */
        uint32_t t = pulse_ticks, got = meas, guard = 0;
        uint32_t t_lo = 0, t_hi = 0, have_lo = 0, have_hi = 0;
        while (got != nref && guard++ < 24u) {
            if (got > nref) { t_lo = t; have_lo = 1; }   /* threshold too high -> widen */
            else            { t_hi = t; have_hi = 1; }   /* threshold too low  -> narrow */

            if (have_lo && have_hi) {                    /* bracketed: bisect on width */
                if (t_hi > t_lo + 1u || t_lo > t_hi + 1u)
                    t = (t_lo > t_hi) ? ((t_lo + t_hi) >> 1) : ((t_lo + t_hi) >> 1);
                else break;                              /* adjacent widths: the closest the widths allow */
            } else if (got > nref) {
                uint32_t d = (got - nref) * CAL_TPC;
                if (t >= CAL_MAXTICKS) break;
                t = (t + d > CAL_MAXTICKS) ? CAL_MAXTICKS : t + d;
            } else {
                uint32_t d = (nref - got) * CAL_TPC;
                if (t == 0) break;
                t = (t > d) ? t - d : 0;
            }
            pulse_ticks = t;
            got = cal_bisect(la0, la1, reps);
            if (got == 0) break;
        }
        if (got == nref) {
            path = 1; now = nref; ticks_used = t;
        } else {
            /* Repair came up short. THE WIDTH LEFT IN PLACE IS THE WIDTH REPORTED: restore the
             * default and re-measure there, so `now` describes the operating point the
             * chip is actually left at. Reporting `got` here would report a threshold
             * measured at a width that has been superseded. */
            pulse_ticks = 10u * pulse_mult * CLK_SCALE;
            ticks_used = pulse_ticks;
            now = cal_bisect(la0, la1, reps);
            if (now == 0) now = meas;                    /* search empty: fall back */
        }
    }

    reg_timer0_update = 1;
    print("CALM lvl=");  print_hex(lvl, 2);
    print(" ref=");      print_hex(nref, 2);
    print(" meas=");     print_hex(meas, 2);
    print(" now=");      print_hex(now, 2);
    print(" trip=");     print_hex(tripped, 1);
    print(" path=");     print_hex(path, 1);
    print(" ticks=");    print_hex(ticks_used, 2);
    print(" oor=0 p0="); print_hex(p0, 2);
    print(" below=");    print_hex(below, 2);
    print(" above=");    print_hex(above, 2);
    print(" at=");       print_hex(at, 2);
    print(" ticks0=");   print_hex(tstart - reg_timer0_value, 8);
    print("\n");
    drain_ram.spike_mask = save_mask;
}

__attribute__((optimize("Os")))
static void calrun_derive(const uint8_t *lad)
{
    volatile uint8_t now[CAL_LEVELS], burst[CAL_ORD];
    for (uint32_t i = 0; i < CAL_LEVELS; i++) now[i] = lad[i];

    /* Validate ONCE, over the whole measured ladder. A level above the representable
     * range is reported separately from the others. */
    uint32_t oor = 0, bad_order = 0, bad_gap = 0, prev = 0, nvalid = 0;
    for (uint32_t i = 0; i < CAL_LEVELS; i++) {
        if (now[i] == 0 || now[i] > CAL_NMAX) { oor++; continue; }
        if (nvalid && now[i] <= prev)                 bad_order++;
        else if (nvalid && (now[i] - prev) < CAL_MINGAP) bad_gap++;
        prev = now[i]; nvalid++;
    }
    if (bad_order || bad_gap || nvalid < 2) {
        print("CALD REFUSE=validity order="); print_hex(bad_order, 2);
        print(" gap=");  print_hex(bad_gap, 2);
        print(" oor=");  print_hex(oor, 2);
        print(" nval="); print_hex(nvalid, 2);
        print("\n");
        return;
    }

    /* Midpoint encoding over the VALID levels only: burst[i] < N*_i <= burst[i+1], with
     * the interval above the highest valid threshold bounded by the range end. */
    volatile uint8_t v[CAL_LEVELS];
    uint32_t nv = 0;
    for (uint32_t i = 0; i < CAL_LEVELS; i++)
        if (now[i] && now[i] <= CAL_NMAX) v[nv++] = now[i];
    burst[0] = 0;
    for (uint32_t i = 1; i < nv; i++) burst[i] = (uint8_t)((v[i - 1] + v[i]) >> 1);
    burst[nv] = (uint8_t)((v[nv - 1] + CAL_NMAX + 1u) >> 1);
    for (uint32_t i = nv + 1; i < CAL_ORD; i++) burst[i] = CAL_NMAX;

    /* Margin: every burst at least CAL_GMIN counts from every switching count. This is
     * what separates "recovered" from "recovered onto a threshold boundary". */
    uint32_t worst = 255;
    for (uint32_t i = 0; i < CAL_ORD; i++) {
        if (burst[i] == 0) continue;
        for (uint32_t j = 0; j < nv; j++) {
            int32_t d = (int32_t)burst[i] - (int32_t)v[j];
            if (d < 0) d = -d;
            if ((uint32_t)d < worst) worst = (uint32_t)d;
        }
    }
    uint32_t gap = 255;
    for (uint32_t i = 1; i < nv; i++) { uint32_t g = v[i] - v[i - 1]; if (g < gap) gap = g; }

    if (worst < CAL_GMIN) {
        print("CALD REFUSE=margin worst="); print_hex(worst, 2); print("\n");
        return;
    }
    print("CALD ok nval="); print_hex(nv, 2);
    print(" oor=");    print_hex(oor, 2);
    print(" gap=");    print_hex(gap, 2);
    print(" head=");   print_hex(CAL_NMAX - v[nv - 1], 2);
    print(" margin="); print_hex(worst, 2);
    print(" enc=");
    for (uint32_t i = 0; i < CAL_ORD; i++) print_hex(burst[i], 2);
    print(" lad=");
    for (uint32_t i = 0; i < CAL_LEVELS; i++) print_hex(now[i], 2);
    print("\n");
}


// ===== GAPPROBE (0xD7): how long does the membrane actually need to re-arm? ==========
//
// The published slot is 31.2 ms = 3.13 tau, and 97% of the 13.8 uJ per node visit is that
// re-arm rather than the burst (0.42 uJ). So both the 26.0 s per decision and the energy scale
// almost linearly with the slot -- and 3.13 tau was a CHOICE about how far the membrane
// should return to rest rather than a measurement of what the comparator needs.
//
// This measures the requirement directly. A conditioning burst of n1 spikes drives the
// neuron (typically past threshold, so it fires and enters its reset); after a programmed
// gap, a probe burst of n2 asks whether the comparator still answers correctly. Sweeping
// the gap down finds the point where the answer changes -- and it has to be checked in
// BOTH directions, because too short a gap breaks two different ways:
//   n2 = N*   must still FIRE      -- too short and the neuron is still in reset
//   n2 = N*-2 must still stay silent -- too short and the membrane is still recovering,
//                                     so the effective threshold has moved down
// The floor is the shortest gap where both hold. The host runs it twice, once per n2.
//
// The gap is too short for the host to produce: pf() spends a fixed 3 x 20 ms draining after
// every burst, so the host's inter-burst period floors near 60 ms -- already above the
// 31.2 ms slot it is supposed to probe. It has to be timed on-chip.
#define UART_CMD_GAPPROBE      0xD7

#define GAP_UNIT     100u      /* payload is in units of 100 Timer0 ticks */
#define GAP_RESOLVE  40000u    /* ticks to wait for a burst to produce its spike */
#define GAP_REST     600000u   /* ticks of quiet before each rep, so it starts from rest */

__attribute__((optimize("Os")))
static void gapprobe_cmd(uint32_t *la0, uint32_t *la1,
                         uint32_t n1, uint32_t n2, uint32_t gap100, uint32_t reps)
{
    if (reps == 0 || reps > 32) { print("GAP err=arg\n"); return; }
    uint16_t save = drain_ram.spike_mask;
    drain_ram.spike_mask = (uint16_t)(1u << 14);
    uint32_t gap = gap100 * GAP_UNIT;
    uint32_t f1 = 0, f2 = 0, gmeas = 0;

    for (uint32_t r = 0; r < reps; r++) {
        /* Start every repetition from rest, so the gap under test is the ONLY thing
         * that differs between them. */
        reg_timer0_update = 1;
        uint32_t q0 = reg_timer0_value;
        for (;;) {
            (void)aer_drain(la1, &drain_ram);
            reg_timer0_update = 1;
            if ((uint32_t)(q0 - reg_timer0_value) > GAP_REST) break;
        }
        drain_ram.ring_tail = drain_ram.ring_head;

        /* --- conditioning burst ------------------------------------------------- */
        for (uint32_t s = 0; s < n1; s++) sendspike(la0);
        reg_timer0_update = 1;
        uint32_t t0 = reg_timer0_value;
        for (;;) {
            if (aer_drain(la1, &drain_ram)) { f1++; break; }
            reg_timer0_update = 1;
            if ((uint32_t)(t0 - reg_timer0_value) > GAP_RESOLVE) break;
        }
        drain_ram.ring_tail = drain_ram.ring_head;

        /* --- the gap under test. Keep draining (a stalled handshake would hold req
         * high and change what the next burst sees), but time it exactly. ---------- */
        reg_timer0_update = 1;
        uint32_t g0 = reg_timer0_value;
        for (;;) {
            (void)aer_drain(la1, &drain_ram);
            reg_timer0_update = 1;
            if ((uint32_t)(g0 - reg_timer0_value) >= gap) break;
        }
        reg_timer0_update = 1;
        gmeas = (uint32_t)(g0 - reg_timer0_value);
        drain_ram.ring_tail = drain_ram.ring_head;

        /* --- probe burst: this is the comparison whose correctness is in question -- */
        for (uint32_t s = 0; s < n2; s++) sendspike(la0);
        reg_timer0_update = 1;
        uint32_t t1 = reg_timer0_value;
        for (;;) {
            if (aer_drain(la1, &drain_ram)) { f2++; break; }
            reg_timer0_update = 1;
            if ((uint32_t)(t1 - reg_timer0_value) > GAP_RESOLVE) break;
        }
        drain_ram.ring_tail = drain_ram.ring_head;
    }

    print("GAP n1=");   print_hex(n1, 2);
    print(" n2=");      print_hex(n2, 2);
    print(" gap=");     print_hex(gap, 8);
    print(" meas=");    print_hex(gmeas, 8);
    print(" f1=");      print_hex(f1, 2);
    print(" f2=");      print_hex(f2, 2);
    print(" reps=");    print_hex(reps, 2);
    print("\n");
    drain_ram.spike_mask = save;
}

void main()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // LED OFF (active-LOW)

    // Power-cycle the user project, don't just enable it. A CPU reset leaves the
    // analog area powered, so x5's AER address encoder can latch (all four address
    // lines stuck high -> every spike decodes as neuron 15) and survive a reflash,
    // a CPU reset, and a 100 us nRes pulse. Only removing power clears it. This is
    // the software equivalent of unplugging the board.
    reg_mprj_pwr = 0;
    delay_loop(20000);          // ~2 ms with power off, clock-scaled
    reg_mprj_pwr = 1;
    delay_loop(20000);          // let the analog rails settle before driving IO

    configure_io();

    // LA configuration — CORRECTED polarity
    // reg_la*_oenb: despite "bar" naming, 1 = CPU output ENABLED (active-HIGH)
    // Gate-level proof: la_data_in[N] = la_oe[N] & la_out[N] & power_good (AND3)
    // Previously inverted: bits for user-driven signals were set to 1 (enabling
    // CPU output on req/AER) while CPU-driven signals (ack, CLK, Da, nRes) were 0
    // (CPU output held low). This held ack away from the neuron.
    reg_la0_oenb = 0x7FFFFFF8;    // bits 3-30: CPU drives la_data_in[3:30]
    reg_la1_oenb = 0x10000000;    // bit 28: CPU drives x5.ack
    reg_la2_oenb = 0x0000005C;    // bits 2,3,4,6: CPU drives CLK, Da, nRes, x3.ack
    reg_la3_oenb = 0x00000000;

    // reg_la*_iena: 0 = input ENABLED (AND2B inverts: ~la_ien & power_good)
    reg_la0_iena = 0x00000000;
    reg_la1_iena = 0x00000000;
    reg_la2_iena = 0x00000000;
    reg_la3_iena = 0x00000000;

    // Initialize outputs: all LOW
    // ack=0 (idle), nRes=0 (held in reset), CLK=0, Da=0
    uint32_t la0_out = 0;
    uint32_t la1_out = 0;
    uint32_t la2_out = 0;

    reg_la0_data = la0_out;
    reg_la1_data = la1_out;
    reg_la2_data = la2_out;

    // Hold the analog reset LOW long enough for x3/x5 to actually reset. The store
    // above and the release below are a few instructions apart, so nRes was pulsed
    // for only ~100 ns at 50 MHz. (Measured: lengthening it to ~100 us does NOT by
    // itself fix an AER encoder stuck reading all-ones -- that survives this reset.)
    delay_loop(1000);                  // ~100 us, clock-scaled by delay_loop()

    // Release nRes: drive HIGH to release active-low reset
    la2_out |= NRES_BIT;
    reg_la2_data = la2_out;
    delay_loop(1000);                  // let x3/x5 come out of reset before use

    // LiteX UART: baud divider fixed at synthesis (9600 @ 10 MHz).
    reg_uart_enable = 1;

    // Signal start: 3 fast blinks then go straight to handshake loop
    blink(3);

    // Start Timer0 as free-running down-counter (10 MHz = 1 tick per 100 ns)
    reg_timer0_config = 0;                    // disable
    reg_timer0_data = 0xFFFFFFFF;             // load max
    reg_timer0_data_periodic = 0xFFFFFFFF;    // reload max
    reg_timer0_config = 1;                    // enable

    // Read initial timer value (unused in deferred mode; kept for Timer0 setup)
    reg_timer0_update = 1;
    (void)reg_timer0_value;
    drain_ram.last_aer = 0;
    pulse_mult = 1;
    pulse_ticks = 10u * 1u * CLK_SCALE;
#if STREAM_SPIKES
    drain_ram.ring_head = 0;
    drain_ram.ring_tail = 0;
    drain_ram.drops = 0;
    drain_ram.stalls = 0;
    drain_ram.spike_mask = 0xFFFF;     // default: stream every neuron
#endif

    // Select monitor neuron 14
    select_monitor_neuron(14, &la2_out);

    // program excitatory synapse 0 with max weight
    // program_neuron_weight(1, &la0_out, 15, 0); // Set excitatory synapse 0 to max weight (15)

    uint32_t rx_state = RX_STATE_IDLE;
    uint32_t prog_syn_addr = 0;
    uint32_t prog_weight = 0;
    uint32_t mask_tmp = 0;          // accumulates the 3 payload bytes of 0xEC
    uint32_t cal_arg = 0, cal_reps = 0, cal_tick = 0, cal_n = 0;
    uint8_t  cal_lad[CAL_LEVELS];   // calibrated ladder, in main's OWN frame
    uint32_t gap_n1 = 0, gap_n2 = 0, gap_hi = 0, gap_lo = 0;
    uint32_t cal_mode = 0;          // 0 = measure one level, 1 = derive once

    //reset all synapses to clear any junk data after configuration
    int i;
    for (i = 0; i < 16; i++) {
        resetsynapse(&la0_out, i, 1); // Reset excitatory synapse i
        resetsynapse(&la0_out, i, 0); // Reset inhibitory synapse i
    }
    
    uint32_t spike_syn_addr = 14;
    uint32_t spike_neu_addr = 14;
    uint32_t spike_exc = 1;
    spikesetup(&la0_out, spike_exc, spike_syn_addr, spike_neu_addr); // Initial spike source

    // On-chip Poisson generator state.
    uint32_t poisson_active = 0;
    uint32_t poisson_regular = 0;   // 1 = fixed ISI (0xED), 0 = exponential (0xE2)
    uint32_t poisson_mean_ticks = 0;   // reassembled from four 6-bit RX bytes
    uint32_t poisson_deadline = 0;      // Timer0 (down-counter) value at next spike

    // Synfire chain state: RISC-V re-routes each output spike to the next neuron.
    uint32_t synfire_active = 0;
    uint32_t synfire_hops = 0;          // total hops completed
    uint32_t synfire_max_hops = 0;      // 0 = unlimited

    // Coincidence trial state.
    uint32_t coinc_synA = 0, coinc_synB = 0, coinc_neu = 0, coinc_dt = 0;
    // Recurrent reservoir connectivity (sparse src->dst list, weight = spike count)
    uint8_t rec_src[MAXREC], rec_dst[MAXREC], rec_cnt[MAXREC], rec_exc[MAXREC];
    uint32_t rec_n = 0, recur_active = 0, rec_src_tmp = 0, rec_dst_tmp = 0;

    while (1) {
        // Handle RX commands from PC (non-blocking, bounded work per iteration)
        uint32_t rx_processed = 0;
        while ((reg_uart_rxempty == 0) && (rx_processed < UART_RX_MAX_BYTES_PER_LOOP)) {
            uint32_t rx = reg_uart_data & 0xFF;
            reg_uart_ev_pending = 2;  // Ack RX event (bit 1) to pop FIFO
            rx_processed++;

            // Allow re-sync if a command-sync byte arrives mid-frame.
            if (rx == UART_CMD_PROGRAM_SYNC) {
                rx_state = RX_STATE_PROG_SYN_ADDR;
                continue;
            }
            if (rx == UART_CMD_SPIKE_SETUP) {
                rx_state = RX_STATE_SPIKE_SYN_ADDR;
                continue;
            }
            if (rx == UART_CMD_BURST) {
                rx_state = RX_STATE_BURST_N;
                continue;
            }
            if (rx == UART_CMD_SEND_SPIKE) {
                // Explicit spike injection from bridge.
                sendspike(&la0_out);
                continue;
            }
            if (rx == UART_CMD_REPORT_HS) {
#if !STREAM_SPIKES
                report_hs();
#endif
                continue;
            }
            if (rx == UART_CMD_POISSON_START) {
                poisson_regular = 0;
                rx_state = RX_STATE_POISSON_B3;
                poisson_mean_ticks = 0;
                continue;
            }
            if (rx == UART_CMD_POISSON_STOP) {
                poisson_active = 0;
                continue;
            }
            if (rx == UART_CMD_SYNFIRE_START) {
                rx_state = RX_STATE_SYNFIRE_LAPS;
                continue;
            }
            if (rx == UART_CMD_SYNFIRE_STOP) {
                synfire_active = 0;
                continue;
            }
            if (rx == UART_CMD_COINCIDENCE) {
                rx_state = RX_STATE_COINC_SYNA;
                continue;
            }
            if (rx == UART_CMD_SET_RECUR) {
                rx_state = RX_STATE_RECUR_SRC;
                continue;
            }
            if (rx == UART_CMD_RECUR_CTRL) {
                rx_state = RX_STATE_RECUR_MODE;
                continue;
            }
            if (rx == UART_CMD_SPIKE_MASK) {
                rx_state = RX_STATE_MASK_B0;
                continue;
            }
            if (rx == UART_CMD_SET_PULSE) {
                rx_state = RX_STATE_PULSE_MULT;
                continue;
            }
            if (rx == UART_CMD_TRAIN_START) {
                poisson_regular = 1;            // fixed ISI; same payload framing as 0xE2
                rx_state = RX_STATE_POISSON_B3;
                continue;
            }
            if (rx == UART_CMD_ADDR_SETTLE) {
                measure_addr_settle();
                continue;
            }
            if (rx == UART_CMD_OLFBENCH) { olfbench_cmd(); continue; }
            if (rx == UART_CMD_ARRAYBENCH) { arraybench_cmd(); continue; }
            if (rx == UART_CMD_LIFRAM) { lifram_cmd(); continue; }
            if (rx == UART_CMD_LIFRUN) { lifrun_cmd(); continue; }
            if (rx == UART_CMD_LIFRUN2) { lifrun2_cmd(); continue; }
            if (rx == UART_CMD_LIFBENCH) { lifbench_cmd(); continue; }
            if (rx == UART_CMD_MEMPROBE) { memprobe_cmd(); continue; }
            if (rx == UART_CMD_ARRAYOPT) { arrayopt_cmd(); continue; }
            if (rx == UART_CMD_PULSEBENCH) { pulsebench_cmd(); continue; }
            if (rx == UART_CMD_PULSEFINE) { rx_state = RX_STATE_PULSEFINE; continue; }
            if (rx == UART_CMD_CALRUN)    { rx_state = RX_STATE_CALRUN_MODE; continue; }
            if (rx == UART_CMD_GAPPROBE)  { rx_state = RX_STATE_GAP_N1; continue; }
            if (rx == UART_CMD_BENCH) {
                bench_cmd();
                continue;
            }
            if (rx == UART_CMD_MONITOR_SYNC) {
                rx_state = RX_STATE_MONITOR_NEURON;
                continue;
            }

            if (rx_state == RX_STATE_IDLE) {
                // Ignore unframed bytes while idle.
                continue;
            } else if (rx_state == RX_STATE_PULSEFINE) {
                // 0 restores the pulse_mult default; otherwise rx-1 is the raw count
                pulse_ticks = rx ? ((uint32_t)rx - 1u)
                                 : (10u * pulse_mult * CLK_SCALE);
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_CALRUN_MODE) {
                cal_mode = rx; rx_state = RX_STATE_CALRUN_LVL;
            } else if (rx_state == RX_STATE_CALRUN_LVL) {
                cal_arg = rx; rx_state = RX_STATE_CALRUN_REPS;
            } else if (rx_state == RX_STATE_CALRUN_REPS) {
                cal_reps = rx; rx_state = RX_STATE_CALRUN_TICKS;
            } else if (rx_state == RX_STATE_CALRUN_TICKS) {
                cal_tick = rx; cal_n = 0; rx_state = RX_STATE_CALRUN_LADDER;
            } else if (rx_state == RX_STATE_CALRUN_LADDER) {
                // The calibrated ladder is CALIBRATION DATA carried by the cycle's own
                // opening command, rather than host control inside the loop: once these bytes
                // land, detection, recovery and re-verification run to completion with
                // zero further host traffic.
                cal_lad[cal_n++] = rx;
                if (cal_n >= CAL_LEVELS) {
                    // mode 0 = measure this level; mode 1 = validate + derive from the
                    // six counts just carried in. One mode per call.
                    if (cal_mode == 0)
                        calrun_measure(&la0_out, &la1_out, cal_arg, cal_reps, cal_lad);
                    else
                        calrun_derive(cal_lad);
                    rx_state = RX_STATE_IDLE;
                }
            } else if (rx_state == RX_STATE_GAP_N1) {
                gap_n1 = rx; rx_state = RX_STATE_GAP_N2;
            } else if (rx_state == RX_STATE_GAP_N2) {
                gap_n2 = rx; rx_state = RX_STATE_GAP_HI;
            } else if (rx_state == RX_STATE_GAP_HI) {
                gap_hi = rx; rx_state = RX_STATE_GAP_LO;
            } else if (rx_state == RX_STATE_GAP_LO) {
                gap_lo = rx; rx_state = RX_STATE_GAP_REPS;
            } else if (rx_state == RX_STATE_GAP_REPS) {
                gapprobe_cmd(&la0_out, &la1_out, gap_n1, gap_n2,
                             (gap_hi << 8) | gap_lo, rx);
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_BURST_N) {
                burst_fire(&la0_out, (uint32_t)rx);   /* same loop the core uses */
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_MONITOR_NEURON) {
                select_monitor_neuron(rx & 0x0F, &la2_out);
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_PROG_SYN_ADDR) {
                prog_syn_addr = rx & 0x0F;
                rx_state = RX_STATE_PROG_WEIGHT;
            } else if (rx_state == RX_STATE_PROG_WEIGHT) {
                prog_weight = rx & 0x0F;
                rx_state = RX_STATE_PROG_EXC;
            } else if (rx_state == RX_STATE_PROG_EXC) {
                uint32_t exc = rx & 0x01;
                program_neuron_weight(exc, &la0_out, prog_weight, prog_syn_addr);
                // Weight programming toggles LA0 bits, so restore spike routing setup.
                spikesetup(&la0_out, spike_exc, spike_syn_addr, spike_neu_addr);
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_SPIKE_SYN_ADDR) {
                spike_syn_addr = rx & 0x0F;
                rx_state = RX_STATE_SPIKE_NEU_ADDR;
            } else if (rx_state == RX_STATE_SPIKE_NEU_ADDR) {
                spike_neu_addr = rx & 0x0F;
                rx_state = RX_STATE_SPIKE_EXC;
            } else if (rx_state == RX_STATE_POISSON_B3) {
                poisson_mean_ticks = (rx & 0x3F) << 18;
                rx_state = RX_STATE_POISSON_B2;
            } else if (rx_state == RX_STATE_POISSON_B2) {
                poisson_mean_ticks |= (rx & 0x3F) << 12;
                rx_state = RX_STATE_POISSON_B1;
            } else if (rx_state == RX_STATE_POISSON_B1) {
                poisson_mean_ticks |= (rx & 0x3F) << 6;
                rx_state = RX_STATE_POISSON_B0;
            } else if (rx_state == RX_STATE_POISSON_B0) {
                poisson_mean_ticks |= (rx & 0x3F);
                // Clamp so umul32(mean, max_lut=799) stays within 32 bits and the
                // rate is sane: mean in [2000, 5e6] ticks = [2 Hz, 5 kHz] at 10 MHz.
                if (poisson_mean_ticks < 2000u) poisson_mean_ticks = 2000u;
                // 5e6 is the OVERFLOW GUARD on umul32(mean, neglog_lut_max=799) < 2**32.
                // The regular train leaves umul32 unused, so the clamp stays off it and it
                // can use the full 24-bit wire range (slower rates).
                if (!poisson_regular && poisson_mean_ticks > 5000000u)
                    poisson_mean_ticks = 5000000u;
                // Schedule the first spike one exponential ISI from now.
                reg_timer0_update = 1;
                poisson_deadline = reg_timer0_value - poisson_next_isi(poisson_mean_ticks);
                poisson_active = 1;
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_SYNFIRE_LAPS) {
                uint32_t laps = rx & 0x3F;
                if (laps == 0) laps = 5;  // default 5 laps
                synfire_max_hops = laps * 16;
                synfire_hops = 0;
                synfire_active = 1;
                // Seed: route to neuron 0 and fire the first spike
                spike_neu_addr = 0;
                spike_exc = 1;
                spikesetup(&la0_out, spike_exc, spike_syn_addr, spike_neu_addr);
                sendspike(&la0_out);
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_RECUR_SRC) {
                rec_src_tmp = rx & 0x0F;
                rx_state = RX_STATE_RECUR_DST;
            } else if (rx_state == RX_STATE_RECUR_DST) {
                rec_dst_tmp = rx & 0x0F;
                rx_state = RX_STATE_RECUR_CW;
            } else if (rx_state == RX_STATE_RECUR_CW) {
                if (rec_n < MAXREC) {
                    rec_src[rec_n] = rec_src_tmp;
                    rec_dst[rec_n] = rec_dst_tmp;
                    rec_cnt[rec_n] = rx & 0x0F;
                    rec_exc[rec_n] = (rx >> 4) & 1;
                    rec_n++;
                }
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_RECUR_MODE) {
                uint32_t rm = rx & 0x0F;
                if (rm == 2) rec_n = 0;          // clear connections
                else recur_active = rm;          // 0=off, 1=on
                rx_state = RX_STATE_IDLE;
#if STREAM_SPIKES
            } else if (rx_state == RX_STATE_MASK_B0) {
                mask_tmp = (rx & 0x3F);
                rx_state = RX_STATE_MASK_B1;
            } else if (rx_state == RX_STATE_MASK_B1) {
                mask_tmp |= (uint32_t)(rx & 0x3F) << 6;
                rx_state = RX_STATE_MASK_B2;
            } else if (rx_state == RX_STATE_MASK_B2) {
                mask_tmp |= (uint32_t)(rx & 0x0F) << 12;
                drain_ram.spike_mask = (uint16_t)(mask_tmp & 0xFFFF);
                rx_state = RX_STATE_IDLE;
#endif
            } else if (rx_state == RX_STATE_PULSE_MULT) {
                uint32_t m = rx & 0x3F;
                pulse_mult = m ? m : 1u;
                pulse_ticks = 10u * pulse_mult * CLK_SCALE;
                rx_state = RX_STATE_IDLE;
            } else if (rx_state == RX_STATE_COINC_SYNA) {
                coinc_synA = rx & 0x0F;
                rx_state = RX_STATE_COINC_SYNB;
            } else if (rx_state == RX_STATE_COINC_SYNB) {
                coinc_synB = rx & 0x0F;
                rx_state = RX_STATE_COINC_NEU;
            } else if (rx_state == RX_STATE_COINC_NEU) {
                coinc_neu = rx & 0x0F;
                rx_state = RX_STATE_COINC_DT3;
            } else if (rx_state == RX_STATE_COINC_DT3) {
                coinc_dt = (rx & 0x3F) << 18;
                rx_state = RX_STATE_COINC_DT2;
            } else if (rx_state == RX_STATE_COINC_DT2) {
                coinc_dt |= (rx & 0x3F) << 12;
                rx_state = RX_STATE_COINC_DT1;
            } else if (rx_state == RX_STATE_COINC_DT1) {
                coinc_dt |= (rx & 0x3F) << 6;
                rx_state = RX_STATE_COINC_DT0;
            } else if (rx_state == RX_STATE_COINC_DT0) {
                coinc_dt |= (rx & 0x3F);
                // 300 ms of REAL time at any core clock. Unlike the Poisson clamp this
                // one bounds duration only, so it scales. 3e6*5 = 15e6 still fits
                // the 24-bit wire format (max 16777215).
                if (coinc_dt > 3000000u * CLK_SCALE) coinc_dt = 3000000u * CLK_SCALE;

                // === Clean coincidence primitive: ONE req_inp edge per input (rather than a doublet),
                //     all slow delay_loop work OUTSIDE the timed A->B window. Only the two
                //     fast fire edges bracket the coinc_dt wait, so A->B = coinc_dt + a
                //     fixed ~1 ms XIP floor (measured; reg writes + timer reads over 10 MHz
                //     SPI flash). ISOLATED here -- spikesetup()/sendspike() (and thus
                //     SPIKE/SYNFIRE/Poisson, which still doublet) are untouched. ===
                uint32_t neu_hw = ((coinc_neu & 0x1) << 3) | ((coinc_neu & 0x2) << 1)
                                | ((coinc_neu & 0x4) >> 1) | ((coinc_neu & 0x8) >> 3);

                // PRE-STAGE (slow OK, before timed window): exc=1, neuron, syn_a, req LOW
                la0_out &= ~X5_REQ_INP_BIT;
                la0_out |= X5_EXC_BIT;
                la0_out = (la0_out & ~(X5_NEU_ADDR_MASK | X5_SYN_ADDR_MASK))
                        | ((neu_hw & 0xF) << 16) | ((coinc_synA & 0xF) << 23);
                reg_la0_data = la0_out;
                delay_loop(10);                    // settle A (outside A->B interval)

                // FIRE A: single rising edge
                la0_out |=  X5_REQ_INP_BIT; reg_la0_data = la0_out;   // A edge
                la0_out &= ~X5_REQ_INP_BIT; reg_la0_data = la0_out;

                // Swap address to syn_b now (req LOW -> edge-free); absorbed into the wait
                la0_out = (la0_out & ~X5_SYN_ADDR_MASK) | ((coinc_synB & 0xF) << 23);
                reg_la0_data = la0_out;

                // WAIT coinc_dt (proven-correct block, unchanged)
                reg_timer0_update = 1;
                uint32_t coinc_target = reg_timer0_value - coinc_dt;  // down-counter
                do {
                    reg_timer0_update = 1;
                } while ((int32_t)(reg_timer0_value - coinc_target) > 0);

                // FIRE B: single rising edge
                la0_out |=  X5_REQ_INP_BIT; reg_la0_data = la0_out;   // B edge
                la0_out &= ~X5_REQ_INP_BIT; reg_la0_data = la0_out;
                rx_state = RX_STATE_IDLE;
            } else {
                spike_exc = rx & 0x01;
                spikesetup(&la0_out, spike_exc, spike_syn_addr, spike_neu_addr);
                rx_state = RX_STATE_IDLE;
            }
        }

        // On-chip Poisson generator: fire on the staged route when Timer0
        // (down-counter) reaches the scheduled deadline, then draw the next
        // exponential ISI. Signed compare tolerates the counter wrap (ISI < 2^31).
        if (poisson_active) {
            reg_timer0_update = 1;
            uint32_t now = reg_timer0_value;
            if ((int32_t)(poisson_deadline - now) >= 0) {   // now has counted down past deadline
                sendspike(&la0_out);
                uint32_t isi = poisson_regular ? poisson_mean_ticks
                                               : poisson_next_isi(poisson_mean_ticks);
                poisson_deadline = now - (isi ? isi : 1u);
            }
        }

                // uncomment if you want to keep sending spikes in idle when req is LOW, otherwise req has to be pulsed from the PC to send a spike
        // if ((rx_state == RX_STATE_IDLE) && !(reg_la1_data_in & X5_REQ_BIT)) {
        //     int i;
        //     for (i = 0; i < 1; i++) {
        //         sendspike(&la0_out);
        //     }
        //     // delay_loop(1000); // delay of 1ms
        // }

        // SRAM-resident AER drain for both modes.  Returns # of spikes drained.
        uint32_t drained = aer_drain(&la1_out, &drain_ram);
#if STREAM_SPIKES
        // Deferred streaming: flush the ring buffer to UART from XIP (off the
        // critical path).  4-byte self-synchronizing packets with raw 16-bit
        // Timer0 ticks (host converts to us: ticks / 10 at 10 MHz):
        //   byte0 = 0x80 | addr         (MSB=1, 4-bit neuron ID)
        //   byte1 = (ts >> 14) & 0x7F   (top 2 bits of 16-bit ts)
        //   byte2 = (ts >>  7) & 0x7F   (middle 7 bits)
        //   byte3 =  ts        & 0x7F   (low 7 bits)
        // Host: ts = (b1<<14)|(b2<<7)|b3; delta = prev_ts - ts (mod 65536).
        // Non-blocking: stops if UART FIFO full, drains on the next iteration.
        while (drain_ram.ring_tail != drain_ram.ring_head) {
            if (reg_uart_txfull) break;
            uint32_t entry = drain_ram.spike_ring[drain_ram.ring_tail];
            uint32_t s_addr = (entry >> 21) & 0x0F;
            uint32_t s_ts   = entry & 0x1FFFFFu;   // 21 bits
            // Carry any overflow since the last packet, then clear. aer_drain runs
            // from this same loop (ISR-free), so read-then-clear stays race-free.
            uint32_t s_flag = 0;
            if (drain_ram.drops)  s_flag |= SPIKE_DROP_FLAG;
            if (drain_ram.stalls) s_flag |= SPIKE_STALL_FLAG;
            drain_ram.drops = 0; drain_ram.stalls = 0;
            // A packet must be ATOMIC. txfull was checked once above, but the FIFO
            // can fill after byte 0, and a write into a full LiteX FIFO is SILENTLY
            // DISCARDED -- that shredded packets near the link ceiling and lost
            // spikes while the ring stayed clear, so `drops` stayed 0 and the
            // host saw corrupt frames it resynced away. Gate every byte instead.
            // This back-pressures the array (a neuron holds req until acked) rather
            // than losing data silently, and STALL says so.
            UART_PUT(0x80 | s_flag | s_addr);
            UART_PUT((s_ts >> 14) & 0x7F);
            UART_PUT((s_ts >>  7) & 0x7F);
            UART_PUT( s_ts        & 0x7F);
            drain_ram.ring_tail = (drain_ram.ring_tail + 1) & SPIKE_RING_MASK;
        }
#endif
        // Synfire chain + recurrent reservoir: re-route the last drained spike.
        // These run from XIP (call spikesetup/sendspike) so they must be outside
        // the SRAM drain.  Only fires if aer_drain serviced at least one spike.
        if (drained) {
            if (synfire_active) {
                uint32_t next = (drain_ram.last_aer + 1) & 0x0F;
                spike_neu_addr = next;
                spikesetup(&la0_out, spike_exc, spike_syn_addr, spike_neu_addr);
                delay_loop(20);
                sendspike(&la0_out);
                synfire_hops++;
                if (synfire_max_hops > 0 && synfire_hops >= synfire_max_hops) {
                    synfire_active = 0;
                }
            }
            if (recur_active) {
                for (uint32_t k = 0; k < rec_n; k++) {
                    if (rec_src[k] == drain_ram.last_aer) {
                        spikesetup(&la0_out, rec_exc[k], REC_SYN, rec_dst[k]);
                        delay_loop(20);
                        for (uint32_t s = 0; s < rec_cnt[k]; s++) {
                            sendspike(&la0_out);
                        }
                    }
                }
                spikesetup(&la0_out, spike_exc, spike_syn_addr, spike_neu_addr);
            }
        }

    }
}
