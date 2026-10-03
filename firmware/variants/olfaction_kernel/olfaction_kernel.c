/* OP3 olfaction kernel, written to be COUNTED and then MEASURED on the die.
 *
 * The task-matched digital baseline for 5-way odour identity from one 50 ms
 * heater-cycle feature (50 samples x 8 MOx channels = 400 values). Counting this is
 * what makes the olfaction cost comparison quotable: the first estimate for it was
 * 19,200 cycles and was wrong by more than 2x in the array's favour, which is exactly
 * the estimate-standing-in-for-a-count error that produced the retracted 580x.
 *
 * MODEL CHOICE. Gradient-boosted trees, matching the ECG baseline's "strong
 * multiply-free edge classifier". Deliberately the SMALLEST model that still reaches
 * 1.000 voted accuracy: max_iter=10, max_leaf_nodes=8 -> 50 trees, 746 nodes, 8.9 KB
 * of table. The 500-tree variant needs 148 KB and cannot run on this die at all, so
 * quoting its cost would be quoting a baseline that does not exist. Smaller is also
 * the array-UNFAVOURABLE choice, which is the right way to pick it.
 *
 * Logistic regression was the alternative and is rejected on cost, not accuracy: it
 * scores 0.967 per-chunk against the trees' 0.900, but 2000 MACs on a core with no
 * hardware multiplier is ~112,000 instructions in shift-add loops alone.
 *
 * FAVOURABLE CHOICES, all made in OP3's favour so the ratio stays an upper bound on
 * the array's disadvantage:
 *   - normalisation is LAZY: only the 94 of 400 features the trees ever read are
 *     normalised, not all 400.
 *   - one reciprocal per channel (8), then multiplies -- not 94 divisions.
 *   - the node table is assumed resident and indexed directly; no bounds checks.
 *   - the per-channel baseline is computed once per trial and amortised over the
 *     decisions in it, so it is not charged here.
 *
 * FIXED POINT: Q8.8 in int32, thresholds and leaf values pre-scaled by the exporter.
 *
 * Build (counting):
 *   riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -O2 -ffreestanding -nostdlib \
 *     -c olfaction_kernel.c -o olfaction_kernel.o && riscv64-unknown-elf-objdump -d ...
 */
typedef signed char  int8_t;
typedef short        int16_t;
typedef int          int32_t;
typedef unsigned int uint32_t;

#include "model.h"

#define N_FEAT   400
#define N_USED    94          /* distinct features the trees ever read */

/* ---------------------------------------------------------------- soft mul */
/* Shift-and-add, same shape as the umul32 loop counted for the LIF step:
 * 7 instructions per iteration, one iteration per set bit position of b. */
static int32_t smul(int32_t a, int32_t b)
{
    uint32_t neg = 0, ua, ub, r = 0;
    if (a < 0) { a = -a; neg ^= 1u; }
    if (b < 0) { b = -b; neg ^= 1u; }
    ua = (uint32_t)a; ub = (uint32_t)b;
    while (ub) { if (ub & 1u) r += ua; ua <<= 1; ub >>= 1; }
    return neg ? -(int32_t)r : (int32_t)r;
}

/* Feature normalisation: (x - base) * recip_base, Q8.8. Lazy -- the caller passes
 * only the indices the trees read. */
static void normalise_used(const int32_t *raw, const int32_t *recip,
                           const int16_t *used, int32_t *out, int n_used)
{
    for (int i = 0; i < n_used; i++) {
        int16_t f = used[i];
        int32_t ch = f & 7;                        /* 8 channels interleaved */
        int32_t d = raw[f] - (recip[ch + 8]);      /* recip[8..15] holds the base */
        out[f] = smul(d, recip[ch]) >> QSHIFT;
    }
}

/* Traverse all trees, accumulate per-class scores, return argmax. Multiply-free. */
int olfaction_classify(const int32_t *feat)
{
    int32_t score[N_CLASS];
    for (int c = 0; c < N_CLASS; c++) score[c] = 0;
    /* Boosting emits trees class-major, so the class index is a wrapping counter.
     * Writing it as `tix % N_CLASS` costs a __modsi3 CALL per tree on a core with no
     * divider -- 50 library calls -- which no embedded programmer would ship. */
    int cls = 0;
    for (int tix = 0; tix < N_TREES; tix++) {
        int i = tree_root[tix];
        while (!node_tab[i].leaf)
            i = (feat[node_tab[i].feat] <= node_tab[i].thr)
                ? node_tab[i].left : node_tab[i].right;
        score[cls] += node_tab[i].val;
        if (++cls == N_CLASS) cls = 0;
    }
    int best = 0;
    for (int c = 1; c < N_CLASS; c++) if (score[c] > score[best]) best = c;
    return best;
}

/* Full per-decision path, the thing that gets counted. */
int olfaction_decision(const int32_t *raw, const int32_t *recip,
                       const int16_t *used, int32_t *scratch)
{
    normalise_used(raw, recip, used, scratch, N_USED);
    return olfaction_classify(scratch);
}
