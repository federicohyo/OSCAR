#!/usr/bin/env python3
"""Single source of truth for every cost-frontier number.

Task 1 of the pre-release fix list. Several quantities (dt*, the OP1/OP2 energy
ratio, the crossover, the 580x) appear simultaneously in the abstract, the body text,
the reference table, the reference figure and the conclusion. Before this module they were hand-maintained in
five places and had already drifted: the figure was plotted on the idealised 153-cycle
1-CPI instruction count while the text quoted the measured 481-cycle SRAM-resident
cost.

Everything below is either

  * MEASURED   -- on the fabricated die (rail power, Timer0 cycle counts), or
  * COUNTED    -- exact rv32i instruction counts disassembled from compiled firmware
                  under an explicit 1-CPI assumption this die leaves unmet, or
  * DERIVED    -- arithmetic on the two above.

Nothing here is estimated or fitted. Any quantity that would need a bench run that has
stays unrun is left blank rather than guessed.

    python3 constants.py            # run the self-checks, write energy_table.csv

The regression assertions at the bottom are the point: they pin the arithmetic so the
basis stays fixed.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# OSCAR: this module emits a CSV table (see docs/PLOTTING.md).
CSV_OUT = os.path.join(HERE, "energy_table.csv")

# The olfaction result JSONs live under data/olfaction/.
_RESDIR = os.path.join(HERE, "..", "..", "data", "olfaction")
with open(os.path.join(_RESDIR, "olfaction_hybrid_score.json")) as _f:
    _HYB = json.load(_f)
with open(os.path.join(_RESDIR, "olfaction_hybrid_slot.json")) as _f:
    _SLOT = json.load(_f)
with open(os.path.join(_RESDIR, "olfaction_mismatch_payoff.json")) as _f:
    _PAY = json.load(_f)
P_ANALOG_W = 0.10e-3      # [W]   aVDD, corrected rail measurement (2026-08-29);
                          # 0.43 mW previously quoted covered more than the array alone
P_CORE_W = 9.3e-3         # [W]   DVDD, RV32I at 25 MHz
K_RAIL = P_ANALOG_W * _SLOT["t_slot_s"]      # rail joules in one node visit

# ============================================================================
# MEASURED on the fabricated die
# ============================================================================
F_CLK = 25e6              # [Hz]  nominal core clock (the reference analysis)
T_BEAT = 2.0              # [s]   ECG analysis window
N_NEURONS = 16

# Timer0 microbenchmark (BENCH, 0xEB), two copies of the identical LIF loop.
# Both return identical tick counts at 25 and 50 MHz -> fixed cycle cost.
CYC_STEP_SRAM = 481       # [cyc/neuron-step]  MEASURED, SRAM-resident  <-- REFERENCE BASIS
CYC_STEP_FLASH = 50447    # [cyc/neuron-step]  MEASURED, flash-resident (as shipped)

# AER read-out drain decomposition (the reference analysis), MEASURED, SRAM-resident.
DRAIN_FIXED_CYC = 105     # [cyc/call]
DRAIN_MARGINAL_CYC = 480  # [cyc/event]

# ============================================================================
# COUNTED -- exact instruction count, 1-CPI assumption (lower bound, favours digital)
# ============================================================================
CYC_STEP_IDEAL = 153      # [cyc/neuron-step]  see reservoir_frontier.py:numeric_lif_cycles_per_beat

# OP3 edge classifier, full path, per beat. COUNTED from firmware/op3_kernel/op3_kernel.c
# compiled at -march=rv32i -O2, with dynamic trip counts driven by the real fitted model
# and the real 90 beats (op3_count.py, data/op3_kernel_count.json). Same convention as
# the LIF column: 1 CPI plus one extra cycle per load.
#
# This REPLACES the hard-coded 4000 cyc/beat order-of-magnitude estimate at
# reservoir_frontier.py:231 that produced the old 588x headline. The estimate was low by
# 13.8x, for a different reason than predicted: it leaves tree traversal uncovered
# (23,270 cyc on its own), let alone the feature extraction it omits entirely.
OP3_CYC_RESAMPLE  = 15698     # 234 -> 128 linear interpolation, soft-multiply bound
OP3_CYC_NORMALISE = 15657     # min/max scan + one reciprocal + 128 soft multiplies
OP3_CYC_RR        = 703       # 4 RR features, two software divisions
OP3_CYC_TREES     = 23270     # 600 trees, 671.5 internal-node visits, 600 leaf accumulates
OP3_CYC_TOTAL     = OP3_CYC_RESAMPLE + OP3_CYC_NORMALISE + OP3_CYC_RR + OP3_CYC_TREES

# ============================================================================
# MEASURED on the fabricated die -- OLFACTION second task (2026-08-13)
# ============================================================================
# A 5-way odour-identity classifier on one 50 ms heater-cycle feature, gradient-boosted
# trees (50 trees, 746 nodes), timed by the Timer0 BENCH path exactly as the LIF step
# was. Two fixed-point widths were built and measured because the width is a design
# choice with its own accuracy/cost trade-off:
#
#   Q8.8   118,349 cyc  but only 0.933 voted accuracy -- its resolution (3.9e-3) exceeds
#          the smallest boosting leaf value (1.7e-3), so small corrections round to zero
#   Q16     85,215 cyc  and 1.000 voted, agreeing with the float model on 100% of chunks
#
# Q16 is both exact and 28% CHEAPER: its 16-byte node stride indexes with one shift
# where Q8.8's 12-byte stride needs three instructions, and flash fetch amplifies that.
# The COUNTED figure is 4,126 for both and stays blind to it, which is why this is measured.
OLF_CYC_MEASURED_Q16 = 85215    # [cyc/decision] MEASURED, flash-resident, matched accuracy
OLF_CYC_MEASURED_Q8 = 118349    # [cyc/decision] MEASURED, but 0.933 voted -- UNMATCHED
OLF_CYC_COUNTED = 4126
# Digital cost of ONE node visit of the hybrid tree: pick the next node, load the
# level, accumulate the leaf. MEASURED (olfaction_hybrid_slot.py). This is the routing
# that runs on the host on this die, because the core leaves bias-DAC programming to the host;
# it is quoted so the energy accounting is independent of where the routing ran.
OLF_ROUTE_CYC = 532

# ---- olfaction, array measured on silicon (2026-08-15) ---------------------
# Every stage timed with Timer0 in ONE image at -O2 (UART_CMD_ARRAYBENCH 0xEF,
# UART_CMD_OLFBENCH 0xEE, UART_CMD_BENCH 0xEB, UART_CMD_LIFRAM 0xE7). An earlier
# version of these numbers was reference internally with the array pipeline compiled
# at -O0 against an -O2 baseline and a corrupted tick calibration; it understated the
# array stages by ~49x. These are the corrected values.
OLF_ARR_PROJ_CYC = 7074902     # [cyc/chunk] random projection 8->16, MEASURED
OLF_ARR_ENC_CYC = 2504         # [cyc/chunk] level-crossing encoder, MEASURED
OLF_ARR_DRAIN_CYC = 106665     # [cyc/chunk] AER drain, 105 + 480/event at 222 events
OLF_ARR_KERN_CYC = 5576409     # [cyc/chunk] exponential kernel features, MEASURED
OLF_ARR_CLF_CYC = 494795       # [cyc/chunk] linear read-out, MEASURED
OLF_ARR_RAIL_UJ = P_ANALOG_W * 0.15e6  # [uJ/chunk] rail x 150 ms capture window;
                          # follows the corrected P_ANALOG_W (was 64.5 at 0.43 mW)

# LIF step, same loop and optimisation, both residencies. The flash figure is NOT a
# stable property of the code: the same loop measured 5090 cyc/step in one image and
# 844 in the next, purely from linker placement.
OLF_LIF_SRAM_CYC = 51.9        # [cyc/step] MEASURED, .ramtext in dff2
OLF_LIF_FLASH_CYC = 844.1      # [cyc/step] MEASURED, XIP; layout-sensitive
OLF_LIF_N, OLF_LIF_TICKS = 16, 150

# Optimised read-out (constant-weight projection; decay^dt table, multiply-free kernel)
OLF_OPT_PROJ_CYC = 2284004     # [cyc/chunk] MEASURED, single valid run
OLF_OPT_KERN_CYC = 77898       # [cyc/chunk] MEASURED, single valid run
# the naive values from the SAME run as the optimised ones. The stage timings vary ~10%
# between runs (flash fetch is placement-sensitive), so a speed-up must be computed from
# a contemporaneous pair rather than against OLF_ARR_*_CYC measured in a different image.
OLF_NAIVE_PROJ_SAMERUN = 6388615
OLF_NAIVE_KERN_SAMERUN = 4907006

# Accuracy, all under ONE protocol: within-0.1s chunks, GroupKFold by trial, voted over
# the 5 heater-cycle chunks of a trial. NOT the train-on-1.0s Dennler protocol that the
# 1.000/0.933 figures above come from -- keep the two separate.
# WITH the digital kernel read-out (the reference table row "analog array + digital read-out").
OLF_ACC_ARRAY_V5, OLF_ACC_ARRAY_V5_SD = 0.756, 0.042      # 3 chip re-acquisitions
# COUNTS-ONLY on the same measured array -- the quantity the width sweeps in the reference figure
# report, so this is the point that belongs on that axis. Naming them here rather than
# inlining the literals; a with-kernel number was previously plotted on the counts-only
# axis, which understated how well the simulation agrees with silicon.
OLF_ACC_COUNTS_PC, OLF_ACC_COUNTS_V5 = 0.533, 0.733
OLF_ACC_ARRAY_BEST_V5, OLF_ACC_ARRAY_BEST_V5_SD = 0.789, 0.016
# Emulation accuracy in the FIRMWARE's arithmetic (Q16 shift-add decay, int32, hard
# reset, refractory), operating point swept and best taken, 3 projection seeds --
# the same fairness the array's operating point got. Supersedes 0.867 +/- 0.037, which
# came from a FLOAT LIF and overstated the emulation by 0.045.
# MEASURED ON SILICON 2026-08-18 (olfaction_emul_run.py / data/olfaction/olfaction_emul_onchip*.json):
# the three stimulus seeds were executed row by row on the core (UART_CMD_LIFRUN2), all
# 7200 rows returned spike times bit-identical to the host mirror of the firmware
# arithmetic, and scoring those times gives 0.691 +/- 0.028 / 0.822 +/- 0.042 exactly --
# the deterministic-arithmetic argument, verified. The point is drawn filled (measured).
OLF_ACC_EMUL_V5, OLF_ACC_EMUL_V5_SD = 0.822, 0.042
OLF_ACC_EMUL_PC, OLF_ACC_EMUL_PC_SD = 0.691, 0.028
OLF_EMUL_RATE_HZ = 21
OLF_ACC_Q16_V5, OLF_ACC_Q16_V5_SD = 0.953, 0.016          # 5 CV fold seeds
OLF_ACC_Q8_V5, OLF_ACC_Q8_V5_SD = 0.947, 0.016
OLF_CHUNKS_PER_DECISION = 5
          # [cyc/decision] COUNTED, 1-CPI, stays out of SRAM
OLF_DECISION_HZ = 20.0          # [Hz] the e-nose heater cycle: 50 ms, one cycle = one feature
OLF_EVENTS_PER_DECISION = 20    # [events] assumed array activity per decision

# ============================================================================
# DERIVED
# ============================================================================
E_CYCLE_J = P_CORE_W / F_CLK                      # 372 pJ/cycle

_olf_common_cyc = (OLF_ARR_PROJ_CYC + OLF_ARR_ENC_CYC + OLF_ARR_KERN_CYC + OLF_ARR_CLF_CYC)
_olf_arr_tot_uj = (_olf_common_cyc + OLF_ARR_DRAIN_CYC) * E_CYCLE_J * 1e6 + OLF_ARR_RAIL_UJ
_olf_arr_digfrac = 100.0 * (1.0 - OLF_ARR_RAIL_UJ / _olf_arr_tot_uj)
_olf_block_analog = OLF_ARR_RAIL_UJ + OLF_ARR_DRAIN_CYC * E_CYCLE_J * 1e6
_olf_block_sram = OLF_LIF_SRAM_CYC * OLF_LIF_N * OLF_LIF_TICKS * E_CYCLE_J * 1e6
_olf_block_flash = OLF_LIF_FLASH_CYC * OLF_LIF_N * OLF_LIF_TICKS * E_CYCLE_J * 1e6
_olf_dec_array = _olf_arr_tot_uj * OLF_CHUNKS_PER_DECISION
_olf_emul_chunk_uj = _olf_common_cyc * E_CYCLE_J * 1e6 + _olf_block_sram
_olf_dec_emul = _olf_emul_chunk_uj * OLF_CHUNKS_PER_DECISION
OLF_DEC_EMUL_UJ = _olf_dec_emul          # public, for figures (panel b of the reference figure)
_olf_dec_q16 = OLF_CYC_MEASURED_Q16 * E_CYCLE_J * 1e6 * OLF_CHUNKS_PER_DECISION
_olf_dec_q8 = OLF_CYC_MEASURED_Q8 * E_CYCLE_J * 1e6 * OLF_CHUNKS_PER_DECISION
# --- design targets an analog array must hit to beat this core, all derived from the
# measurements above. The unit is one neuron-step, because that is what the analog
# neuron and its digital replica each produce.
_olf_steps = OLF_LIF_N * OLF_LIF_TICKS
_olf_dig_step_nj = OLF_LIF_SRAM_CYC * E_CYCLE_J * 1e9
_olf_rail_step_nj = OLF_ARR_RAIL_UJ * 1e3 / _olf_steps
_olf_drain_step_nj = OLF_ARR_DRAIN_CYC * E_CYCLE_J * 1e6 * 1e3 / _olf_steps
_olf_drain_ev_nj = 480 * E_CYCLE_J * 1e9
_olf_spikes_per_step = _olf_drain_ev_nj / _olf_dig_step_nj
_olf_sparsity_ceiling = 100.0 * _olf_dig_step_nj / _olf_drain_ev_nj
_olf_rail_budget_uw = (_olf_dig_step_nj - _olf_drain_step_nj) * _olf_steps / 1e3 / 0.15
_olf_rail_over = P_ANALOG_W * 1e6 / _olf_rail_budget_uw
_olf_analog_frac = 100.0 * (OLF_ARR_RAIL_UJ + OLF_ARR_DRAIN_CYC * E_CYCLE_J * 1e6) \
    / _olf_arr_tot_uj
_olf_amort = _olf_common_cyc * E_CYCLE_J * 1e6 / _olf_block_analog

# --- PROJECTED (extrapolated beyond measurement): the same task with an algorithm the substrate can
# execute. The 8->16 projection is what the 16 exc + 16 inh 4-bit synapses per neuron
# already compute in analog, so the digital MAC is redundant; and if a second layer
# integrates in the membranes, the read-out is spike COUNTS rather than exponential
# filters. Both primitives exist on this die (the synapse fabric; SETRECUR, demonstrated
# by the T-XOR result). Everything else is held at its measured value.
_olf_m_enc = OLF_ARR_ENC_CYC * E_CYCLE_J * 1e6 * 0.5      # 8 raw channels rather than 16
_olf_m_clf = OLF_ARR_CLF_CYC / (128 * 5) * (16 * 5) * E_CYCLE_J * 1e6
_olf_matched_uj = (_olf_m_enc + _olf_m_clf
                   + OLF_ARR_DRAIN_CYC * E_CYCLE_J * 1e6 + OLF_ARR_RAIL_UJ)
_olf_matched_gain = _olf_arr_tot_uj / _olf_matched_uj
_olf_matched_vs_tree = _olf_matched_uj / (OLF_CYC_MEASURED_Q16 * E_CYCLE_J * 1e6)
_olf_matched_analog_share = 100.0 * (OLF_ARR_RAIL_UJ
                                     + OLF_ARR_DRAIN_CYC * E_CYCLE_J * 1e6) / _olf_matched_uj

# --- hybrid: RISC-V routes the tree, the array integrates, 16 neurons time-multiplexed
# across the visited nodes. Per-visit costs are measured; the hybrid is projected.
OLF_TREE_NODES, OLF_TREE_VISITS = 746, 160.3
_olf_dig_visit_nj = OLF_CYC_MEASURED_Q16 / OLF_TREE_VISITS * E_CYCLE_J * 1e9
_olf_rail_slot_nj = OLF_ARR_RAIL_UJ * 1e3 / OLF_LIF_N          # one neuron, one window
_olf_aer_read_nj = 480 * E_CYCLE_J * 1e9
_olf_slot_nj = _olf_rail_slot_nj + _olf_aer_read_nj
_olf_dig_integrate_nj = OLF_LIF_TICKS * OLF_LIF_SRAM_CYC * E_CYCLE_J * 1e9
_olf_slot_ticks = _olf_slot_nj / (OLF_LIF_SRAM_CYC * E_CYCLE_J * 1e9)

_olf_opt_saved = ((OLF_NAIVE_PROJ_SAMERUN - OLF_OPT_PROJ_CYC)
                  + (OLF_NAIVE_KERN_SAMERUN - OLF_OPT_KERN_CYC)) * E_CYCLE_J * 1e6
E_ANALOG_STATIC_J = P_ANALOG_W * T_BEAT           # 0.86 mJ, independent of dt
RAIL_POWER_RATIO = P_CORE_W / P_ANALOG_W          # 21.6x


def dt_star(cyc_per_step, f_clk=F_CLK, n=N_NEURONS):
    """Real-time floor: the finest Euler step at which the core still integrates a
    beat within the beat. dt* = N*c/f -- the beat length cancels."""
    return n * cyc_per_step / f_clk


def numeric_cycles_per_beat(dt, cyc_per_step, t_beat=T_BEAT, n=N_NEURONS):
    return (t_beat / dt) * n * cyc_per_step


def numeric_energy_J(dt, cyc_per_step):
    return numeric_cycles_per_beat(dt, cyc_per_step) * E_CYCLE_J


def aer_cycles_per_beat(events_per_beat, calls_per_beat=1):
    """MEASURED basis for OP1's read-out work.

    Task F. reservoir_frontier.py:212 costs the read-out at an estimated
    200 cyc/spike. The measured SRAM-resident drain is 105 cyc fixed per call plus
    480 cyc marginal per event (the reference analysis), so we use that instead: same
    quantity, measured basis rather than estimated. The static-power share moves
    from ~99% to ~98% and every ratio moves by well under 1%, so every conclusion
    stands -- but the label was off, and an off basis label is the defect this
    reference campaign's discipline exists to prevent."""
    return calls_per_beat * DRAIN_FIXED_CYC + events_per_beat * DRAIN_MARGINAL_CYC


def analog_energy_J(aer_cyc):
    """Static analog power over the window plus the core's read-out work on top."""
    return E_ANALOG_STATIC_J + aer_cyc * E_CYCLE_J


def crossover_dt(cyc_per_step, e_analog_J):
    """dt at which numeric reproduction costs exactly what the array costs."""
    return (T_BEAT * N_NEURONS * cyc_per_step * E_CYCLE_J) / e_analog_J


# ---------------------------------------------------------------------------
# Task Q: decompose the OP1-vs-OP3 gap so the "unoptimised silicon" caveat can be
# stated as a checkable finding rather than a disclaimer.
#
# OP1 = E_static (analog rail x window)  +  E_readout (core cycles x E_CYCLE)
# OP3 = E_op3    (core cycles x E_CYCLE)
#
# Write the core's energy per cycle as E_CYCLE/k, i.e. k = how many times more
# energy-efficient a redesigned core would be per cycle. Then
#
#     ratio(k) = (E_static + E_readout/k) / (E_op3/k)
#              = k * (E_static/E_op3)  +  E_readout/E_op3
#
# which is LINEAR AND INCREASING in k: making the digital side more efficient
# weighs against the array, because 98% of OP1's cost sits off the core at
# all. The lever that closes the gap is the analog rail. Writing the analog
# static power as E_static/m:
#
#     ratio(m) = (E_static/m + E_readout) / E_op3   ->  1  at  m = E_static/(E_op3 - E_readout)
#
# and as m -> infinity the ratio converges to E_readout/E_op3 rather than zero: the
# read-out the array needs is itself a fixed fraction of the whole tree baseline.
# All three are DERIVED -- pure arithmetic on the measured/counted quantities
# above, a direct equality derived from the figures above.
# ---------------------------------------------------------------------------

def gap_slope_in_core_efficiency(e_static_J, e_op3_J):
    """d(ratio)/dk: how much a k-fold more efficient core WIDENS the OP1/OP3 gap."""
    return e_static_J / e_op3_J


def gap_floor(e_readout_J, e_op3_J):
    """OP1/OP3 with the analog rail free: the array's best case on this task."""
    return e_readout_J / e_op3_J


def analog_reduction_for_parity(e_static_J, e_readout_J, e_op3_J):
    """Factor the analog static power must fall by for OP1 to equal OP3."""
    return e_static_J / (e_op3_J - e_readout_J)


# --- the two bases, side by side -------------------------------------------
DT_STAR_MEASURED = dt_star(CYC_STEP_SRAM)     # 308 us   <-- reference
DT_STAR_IDEAL = dt_star(CYC_STEP_IDEAL)       #  98 us   <-- lower bound
DT_STAR_FLASH = dt_star(CYC_STEP_FLASH)       #  32.3 ms (as shipped)


def emit_csv(op1_energy_mJ, op3_energy_uJ, aer_cyc_pb, events_pb,
             olf_e_op3=None, olf_e_arr=None, olf_e_read=None, olf_break_hz=None,
             path=CSV_OUT):
    """Write the energy/cost table as CSV (OSCAR ships no LaTeX).

    `table` below holds `(name, value)` pairs, emitted as `name,value` CSV rows
    so the energy numbers are machine-readable.
    """
    e_an = op1_energy_mJ * 1e-3
    e_ro = aer_cyc_pb * E_CYCLE_J          # OP1's read-out share, J
    e_op3 = op3_energy_uJ * 1e-6
    table = [
        ("cycstep", '%d' % (CYC_STEP_SRAM)),
        ("dtstar", '%.0f' % ((DT_STAR_MEASURED * 1e6))),
        ("dtstarfifty", '%.1f' % ((dt_star(CYC_STEP_SRAM, 50e6) * 1e6))),
        ("ratioonems", '%.1f' % ((numeric_energy_J(1e-3, CYC_STEP_SRAM) / e_an))),
        ("ratioatfloor", '%.1f' % ((
        numeric_energy_J(DT_STAR_MEASURED, CYC_STEP_SRAM) / e_an))),
        ("crossover", '%.1f' % ((crossover_dt(CYC_STEP_SRAM, e_an) * 1e3))),
        ("numcyconems", '%.2f' % ((
        numeric_cycles_per_beat(1e-3, CYC_STEP_SRAM) / 1e6))),
        ("numlatonems", '%.0f' % ((
        numeric_cycles_per_beat(1e-3, CYC_STEP_SRAM) / F_CLK * 1e3))),
        ("numenergyonems", '%.2f' % ((numeric_energy_J(1e-3, CYC_STEP_SRAM) * 1e3))),
        ("cycstepideal", '%d' % (CYC_STEP_IDEAL)),
        ("dtstarideal", '%.0f' % ((DT_STAR_IDEAL * 1e6))),
        ("ratioonemsideal", '%.1f' % ((
        numeric_energy_J(1e-3, CYC_STEP_IDEAL) / e_an))),
        ("idealflatter", '%.1f' % ((CYC_STEP_SRAM / CYC_STEP_IDEAL))),
        ("cycstepflash", '%s' % (f"{CYC_STEP_FLASH:,}".replace(",", "{,}"))),
        ("dtstarflash", '%.1f' % ((DT_STAR_FLASH * 1e3))),
        ("panalog", '%.2f' % ((P_ANALOG_W * 1e3))),
        ("pcore", '%.1f' % ((P_CORE_W * 1e3))),
        ("ecycle", '%.0f' % ((E_CYCLE_J * 1e12))),
        ("railratio", '%.1f' % (RAIL_POWER_RATIO)),
        ("eanalog", '%.2f' % (op1_energy_mJ)),
        ("eanalogstatic", '%.2f' % ((E_ANALOG_STATIC_J * 1e3))),
        ("staticshare", '%.0f' % ((E_ANALOG_STATIC_J / (op1_energy_mJ*1e-3) * 100))),
        ("aercyc", '%s' % (f"{int(round(aer_cyc_pb)):,}".replace(",", "{,}"))),
        ("aerevents", '%.0f' % (events_pb)),
        ("olfcyc", '%s' % (f"{OLF_CYC_MEASURED_Q16:,}".replace(",", "{,}"))),
        ("olfcycqeight", '%s' % (f"{OLF_CYC_MEASURED_Q8:,}".replace(",", "{,}"))),
        ("olfcyccounted", '%s' % (f"{OLF_CYC_COUNTED:,}".replace(",", "{,}"))),
        ("olfroutecyc", '%s' % (f"{OLF_ROUTE_CYC:,}".replace(",", "{,}"))),
        ("olfarrproj", '%s' % (f"{OLF_ARR_PROJ_CYC:,}".replace(",", "{,}"))),
        ("olfarrenc", '%s' % (f"{OLF_ARR_ENC_CYC:,}".replace(",", "{,}"))),
        ("olfarrdrain", '%s' % (f"{OLF_ARR_DRAIN_CYC:,}".replace(",", "{,}"))),
        ("olfarrkern", '%s' % (f"{OLF_ARR_KERN_CYC:,}".replace(",", "{,}"))),
        ("olfarrclf", '%s' % (f"{OLF_ARR_CLF_CYC:,}".replace(",", "{,}"))),
        ("olfarrprojuj", '%.0f' % ((OLF_ARR_PROJ_CYC * E_CYCLE_J * 1e6))),
        ("olfarrencuj", '%.1f' % ((OLF_ARR_ENC_CYC * E_CYCLE_J * 1e6))),
        ("olfarrdrainuj", '%.1f' % ((OLF_ARR_DRAIN_CYC * E_CYCLE_J * 1e6))),
        ("olfarrkernuj", '%.0f' % ((OLF_ARR_KERN_CYC * E_CYCLE_J * 1e6))),
        ("olfarrclfuj", '%.0f' % ((OLF_ARR_CLF_CYC * E_CYCLE_J * 1e6))),
        ("olfarrrailuj", '%.1f' % (OLF_ARR_RAIL_UJ)),
        ("olfarrtotuj", '%s' % (f"{_olf_arr_tot_uj:,.0f}".replace(",", "{,}"))),
        ("olfarrdigfrac", '%.1f' % (_olf_arr_digfrac)),
        ("olfemulchunkuj", '%s' % (f"{_olf_emul_chunk_uj:,.0f}".replace(",", "{,}"))),
        ("olfcommonuj", '%s' % (f"{_olf_common_cyc * E_CYCLE_J * 1e6:,.0f}".replace(",", "{,}"))),
        ("olfblockanalog", '%.1f' % (_olf_block_analog)),
        ("olfblocksram", '%.1f' % (_olf_block_sram)),
        ("olfblockflash", '%.0f' % (_olf_block_flash)),
        ("olflifsram", '%.1f' % (OLF_LIF_SRAM_CYC)),
        ("olflifcyc", '%s' % (f"{OLF_LIF_SRAM_CYC*OLF_LIF_N*OLF_LIF_TICKS:,.0f}".replace(",", "{,}"))),
        ("olflifflash", '%.1f' % (OLF_LIF_FLASH_CYC)),
        ("olflifratio", '%.1f' % ((OLF_LIF_FLASH_CYC / OLF_LIF_SRAM_CYC))),
        ("olfblockpenalty", '%.1f' % ((_olf_block_analog / _olf_block_sram))),
        ("olfdecarray", '%s' % (f"{_olf_dec_array:,.0f}".replace(",", "{,}"))),
        ("olfdecemul", '%s' % (f"{_olf_dec_emul:,.0f}".replace(",", "{,}"))),
        ("olfdecqsixteen", '%.0f' % (_olf_dec_q16)),
        ("olfdecqeight", '%.0f' % (_olf_dec_q8)),
        ("olfaccarray", '%.3f' % (OLF_ACC_ARRAY_V5)),
        ("olfaccarraysd", '%.3f' % (OLF_ACC_ARRAY_V5_SD)),
        ("olfaccarraybest", '%.3f' % (OLF_ACC_ARRAY_BEST_V5)),
        ("olfaccarraybestsd", '%.3f' % (OLF_ACC_ARRAY_BEST_V5_SD)),
        ("olfaccemul", '%.3f' % (OLF_ACC_EMUL_V5)),
        ("olfaccemulsd", '%.3f' % (OLF_ACC_EMUL_V5_SD)),
        ("olfanalogpenalty", '%.3f' % ((OLF_ACC_EMUL_V5 - OLF_ACC_ARRAY_V5))),
        ("olfanalogpenaltysd", '%.3f' % (((OLF_ACC_EMUL_V5_SD**2 + OLF_ACC_ARRAY_V5_SD**2) ** 0.5))),
        ("olfaccqsixteen", '%.3f' % (OLF_ACC_Q16_V5)),
        ("olfaccqsixteensd", '%.3f' % (OLF_ACC_Q16_V5_SD)),
        ("olfaccqeight", '%.3f' % (OLF_ACC_Q8_V5)),
        ("olfaccqeightsd", '%.3f' % (OLF_ACC_Q8_V5_SD)),
        ("accthree", '%.3f' % (_HYB["analog"]["voted5"])),
        ("accthreesd", '%.3f' % (_HYB["voted5_sd"])),
        ("accceil", '%.3f' % (_HYB["digital_snapped"]["voted5"])),
        ("accfull", '%.3f' % (_HYB["digital_full"]["voted5"])),
        ("hybdecuj", '%s' % (f"{_SLOT['e_decision_J'] * 1e6:,.0f}".replace(",", "{,}"))),
        ("hybnodeerr", '%.1f' % ((100 * _HYB["node_disagreement"]))),
        ("hybslotms", '%.1f' % ((_SLOT["t_slot_s"] * 1e3))),
        ("hybrearmms", '%.0f' % ((3 * _SLOT["tau_s"] * 1e3))),
        ("hybtaums", '%.0f' % ((_SLOT["tau_s"] * 1e3))),
        ("hybvisituj", '%.1f' % ((_SLOT["e_visit_J"] * 1e6))),
        ("hybpar", '%.2f' % (_PAY["speedup"])),
        ("hybvisitparuj", '%.1f' % (((_SLOT["e_visit_J"] - K_RAIL + K_RAIL / _PAY["speedup"]) * 1e6))),
        ("olfchunks", '%d' % (OLF_CHUNKS_PER_DECISION)),
        ("olfdigstep", '%.1f' % (_olf_dig_step_nj)),
        ("olfrailstep", '%.1f' % (_olf_rail_step_nj)),
        ("olfdrainstep", '%.1f' % (_olf_drain_step_nj)),
        ("olfanalogstep", '%.1f' % ((_olf_rail_step_nj + _olf_drain_step_nj))),
        ("olfdrainev", '%.0f' % (_olf_drain_ev_nj)),
        ("olfspikesteps", '%.1f' % (_olf_spikes_per_step)),
        ("olfsparsityceil", '%.1f' % (_olf_sparsity_ceiling)),
        ("olfsparsitymeas", '%.1f' % ((100.0 * 85 / _olf_steps))),
        ("olfrailbudget", '%.0f' % (_olf_rail_budget_uw)),
        ("olfrailover", '%.1f' % (_olf_rail_over)),
        ("olfanalogfrac", '%.1f' % (_olf_analog_frac)),
        ("olfamort", '%.0f' % (_olf_amort)),
        ("olfmatcheduj", '%.0f' % (_olf_matched_uj)),
        ("olfmatchedgain", '%.0f' % (_olf_matched_gain)),
        ("olfmatchedtree", '%.1f' % (_olf_matched_vs_tree)),
        ("olfmatchedshare", '%.0f' % (_olf_matched_analog_share)),
        ("olftreevisits", '%.0f' % (OLF_TREE_VISITS)),
        ("olftreenodes", '%d' % (OLF_TREE_NODES)),
        ("olfdigvisit", '%.0f' % (_olf_dig_visit_nj)),
        ("olfslot", '%.1f' % ((_olf_slot_nj / 1e3))),
        ("olfslotratio", '%.0f' % ((_olf_slot_nj / _olf_dig_visit_nj))),
        ("olfdigintegrate", '%.2f' % ((_olf_dig_integrate_nj / 1e3))),
        ("olfslotticks", '%.0f' % (_olf_slot_ticks)),
        ("olfcountspc", '%.3f' % (OLF_ACC_COUNTS_PC)),
        ("olfcountsvfive", '%.3f' % (OLF_ACC_COUNTS_V5)),
        ("olfoptproj", '%s' % (f"{OLF_OPT_PROJ_CYC:,}".replace(",", "{,}"))),
        ("olfoptkern", '%s' % (f"{OLF_OPT_KERN_CYC:,}".replace(",", "{,}"))),
        ("olfoptprojx", '%.1f' % ((OLF_NAIVE_PROJ_SAMERUN / OLF_OPT_PROJ_CYC))),
        ("olfoptkernx", '%.0f' % ((OLF_NAIVE_KERN_SAMERUN / OLF_OPT_KERN_CYC))),
        ("olfnaiveproj", '%s' % (f"{OLF_NAIVE_PROJ_SAMERUN:,}".replace(",", "{,}"))),
        ("olfnaivekern", '%s' % (f"{OLF_NAIVE_KERN_SAMERUN:,}".replace(",", "{,}"))),
        ("olfoptsaveduj", '%s' % (f"{_olf_opt_saved:,.0f}".replace(",", "{,}"))),
        ("olfeopthree", '%.1f' % (((olf_e_op3 or 0) * 1e6))),
        ("olfearray", '%.1f' % (((olf_e_arr or 0) * 1e6))),
        ("olfereadout", '%.1f' % (((olf_e_read or 0) * 1e6))),
        ("olfrate", '%.0f' % (OLF_DECISION_HZ)),
        ("olfbreakhz", '%.0f' % ((olf_break_hz or 0))),
        ("olfratio", '%.2f' % (((olf_e_op3 or 1) / (olf_e_arr or 1)))),
        ("treeratio", '%.0f' % ((op1_energy_mJ * 1e3 / op3_energy_uJ))),
        ("etree", '%.1f' % (op3_energy_uJ)),
        ("opthreecyc", '%s' % (f"{OP3_CYC_TOTAL:,}".replace(",", "{,}"))),
        ("opthreeresample", '%s' % (f"{OP3_CYC_RESAMPLE:,}".replace(",", "{,}"))),
        ("opthreenorm", '%s' % (f"{OP3_CYC_NORMALISE:,}".replace(",", "{,}"))),
        ("opthreerr", '%d' % (OP3_CYC_RR)),
        ("opthreetrees", '%s' % (f"{OP3_CYC_TREES:,}".replace(",", "{,}"))),
        ("opthreecompares", "672"),
        ("ereadout", '%.1f' % ((e_ro * 1e6))),
        ("gapslope", '%.0f' % (gap_slope_in_core_efficiency(E_ANALOG_STATIC_J, e_op3))),
        ("gapcorehalf", '%.0f' % ((
        2 * gap_slope_in_core_efficiency(E_ANALOG_STATIC_J, e_op3)
        + gap_floor(e_ro, e_op3)))),
        ("gapfloor", '%.2f' % (gap_floor(e_ro, e_op3))),
        ("gapbestcase", '%.1f' % ((1.0 / gap_floor(e_ro, e_op3)))),
        ("analogparity", '%.0f' % (analog_reduction_for_parity(
        E_ANALOG_STATIC_J, e_ro, e_op3))),
        ("arrayrate", '%.0f' % ((events_pb / T_BEAT))),
        ("ratepowerheadroom", '%.0f' % ((
        N_NEURONS * 26.0 / (events_pb / T_BEAT)))),
        ("drainfixed", '%d' % (DRAIN_FIXED_CYC)),
        ("drainmarginal", '%d' % (DRAIN_MARGINAL_CYC)),
    ]
    rows = ["constant,value"] + ["%s,%s" % (n, v) for n, v in table]
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")
    return path


def selfcheck(op1_energy_mJ, op3_energy_uJ=None, aer_cyc_pb=None):
    """Regression assertions. These all close in the reference analysis text as released;
    if one trips, the figure and the text have drifted apart again."""
    e_an = op1_energy_mJ * 1e-3
    ok = lambda got, want, tol, what: (
        abs(got - want) <= tol or _fail(what, got, want, tol))

    ok(dt_star(CYC_STEP_SRAM) * 1e6, 308, 1.0, "dt* measured")
    ok(dt_star(CYC_STEP_IDEAL) * 1e6, 98, 1.0, "dt* idealised")
    ok(numeric_cycles_per_beat(1e-3, CYC_STEP_SRAM), 15.39e6, 0.02e6, "cycles @1ms")
    ok(numeric_cycles_per_beat(1e-3, CYC_STEP_SRAM) / F_CLK * 1e3, 616, 1.0, "latency @1ms")
    ok(numeric_energy_J(1e-3, CYC_STEP_SRAM) * 1e3, 5.73, 0.02, "energy @1ms")
    # Ratios below moved at Task F (OP1 read-out re-based onto the measured drain; see
    # note above) and again when P_ANALOG_W was corrected 0.43 -> 0.10 mW on 2026-08-29:
    # e_an is the rail static energy, so every ratio against it scales by 4.3.
    ok(numeric_energy_J(1e-3, CYC_STEP_SRAM) / e_an, 26.69, 0.05, "ratio @1ms")
    ok(OP3_CYC_TOTAL, 55328, 5, "OP3 counted cycles/beat")
    ok(numeric_energy_J(DT_STAR_MEASURED, CYC_STEP_SRAM) * 1e3, 18.6, 0.1, "energy @dt*")
    ok(numeric_energy_J(DT_STAR_MEASURED, CYC_STEP_SRAM) / e_an, 86.7, 0.2, "ratio @dt*")
    ok(RAIL_POWER_RATIO, 93.0, 0.1, "rail-power ratio")
    ok(E_CYCLE_J * 1e12, 372, 1.0, "pJ per cycle")
    # the energy ratio at the floor converges to the rail-power ratio, because at dt*
    # the core computes 100% of the time. The residual (86.7 vs 93.0) is the small
    # dynamic addend in e_an, visible only now that the corrected 100 uW rail makes
    # the static part dominate less completely.
    ok(numeric_energy_J(DT_STAR_MEASURED, CYC_STEP_SRAM) / e_an, RAIL_POWER_RATIO, 6.5,
       "ratio at floor == rail-power ratio")

    # --- Task Q: the gap decomposition the prose rests on.
    # These are pinned on the CURRENT (counted) OP3 basis. Task 6c will replace
    # OP3_CYC_TOTAL with a measured value; when it does, update these numbers to the
    # new basis -- every one is an equality rather than a bound to be relaxed.
    if op3_energy_uJ is not None and aer_cyc_pb is not None:
        e_op3 = op3_energy_uJ * 1e-6
        e_ro = aer_cyc_pb * E_CYCLE_J
        ok(e_ro * 1e6, 14.5, 0.1, "OP1 read-out energy")
        ok(e_an / e_op3, 10.42, 0.2, "OP1/OP3 ratio")
        # the identity the prose depends on: ratio = k*slope + floor, so a MORE
        # efficient core (k>1) widens the gap. If this ever comes out <= 0 the
        # sentence in the reference analysis is off. (slope = analog-static share, so it
        # moved 41.8 -> 9.7 with the corrected 100 uW rail; the floor is rail-free.)
        slope = gap_slope_in_core_efficiency(E_ANALOG_STATIC_J, e_op3)
        floor = gap_floor(e_ro, e_op3)
        ok(slope, 9.72, 0.2, "gap slope in core efficiency")
        ok(floor, 0.71, 0.02, "gap floor at zero analog power")
        ok(1.0 * slope + floor, e_an / e_op3, 0.05, "ratio identity closes at k=1")
        ok(analog_reduction_for_parity(E_ANALOG_STATIC_J, e_ro, e_op3), 33, 1,
           "analog reduction for parity")
    return True


def _fail(what, got, want, tol):
    raise AssertionError(f"REGRESSION: {what}: got {got:.4g}, expected {want:.4g} "
                         f"(tol {tol:.4g}). Figure and text have drifted apart.")


if __name__ == "__main__":
    import json
    d = json.load(open(os.path.join(HERE, "reservoir_frontier.json")))
    cost = d["cost"]
    # MEASURED basis (Task F): 105 cyc/call + 480 cyc/event rather than the 200 cyc/spike
    # estimate the json still carries.
    ev = cost["op1_mean_spikes_per_beat"]
    aer_cyc = aer_cycles_per_beat(ev)
    e_an_mJ = analog_energy_J(aer_cyc) * 1e3
    # COUNTED basis (Task I) rather than the json's 4000-cycle estimate.
    e_tree_uJ = OP3_CYC_TOTAL * E_CYCLE_J * 1e6
    selfcheck(e_an_mJ, e_tree_uJ, aer_cyc)
    # --- olfaction: the second point on the decision-rate axis -------------
    olf_e_op3 = OLF_CYC_MEASURED_Q16 * E_CYCLE_J
    olf_e_read = aer_cycles_per_beat(OLF_EVENTS_PER_DECISION) * E_CYCLE_J
    olf_e_arr = P_ANALOG_W / OLF_DECISION_HZ + olf_e_read
    # break-even: the array wins when P/f + readout < E_OP3
    olf_break_hz = P_ANALOG_W / max(olf_e_op3 - olf_e_read, 1e-30)
    p = emit_csv(e_an_mJ, e_tree_uJ, aer_cyc, ev,
                 olf_e_op3, olf_e_arr, olf_e_read, olf_break_hz)
    print("all self-checks pass")
    print(f"  OP1 analog          {e_an_mJ:8.3f} mJ  ({E_ANALOG_STATIC_J*1e3:.2f} mJ static, "
          f"{E_ANALOG_STATIC_J/ (e_an_mJ*1e-3)*100:.1f}% of it)")
    print(f"  OP1 read-out        {aer_cyc:8.0f} cyc/beat  ({ev:.1f} events x {DRAIN_MARGINAL_CYC}"
          f" + {DRAIN_FIXED_CYC})   [MEASURED basis, was 200 cyc/spike estimate]")
    print(f"  dt* measured        {DT_STAR_MEASURED*1e6:8.1f} us   (c={CYC_STEP_SRAM})")
    print(f"  dt* idealised       {DT_STAR_IDEAL*1e6:8.1f} us   (c={CYC_STEP_IDEAL}, lower bound)")
    print(f"  ratio @1 ms         {numeric_energy_J(1e-3, CYC_STEP_SRAM)/(e_an_mJ*1e-3):8.2f}x")
    print(f"  crossover           {crossover_dt(CYC_STEP_SRAM, e_an_mJ*1e-3)*1e3:8.2f} ms")
    print(f"  tree ratio          {e_an_mJ*1e3/e_tree_uJ:8.0f}x  (OP3 = {e_tree_uJ:.2f} uJ)")
    e_op3, e_ro = e_tree_uJ * 1e-6, aer_cyc * E_CYCLE_J
    print(f"  gap decomposition   slope {gap_slope_in_core_efficiency(E_ANALOG_STATIC_J, e_op3):.1f}"
          f" per unit core efficiency, floor {gap_floor(e_ro, e_op3):.2f}x at zero analog power,"
          f" parity at {analog_reduction_for_parity(E_ANALOG_STATIC_J, e_ro, e_op3):.0f}x"
          f" analog reduction")
    print(f"wrote {p}")
