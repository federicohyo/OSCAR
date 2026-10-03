/* OP3 edge-classifier kernel, written to be COUNTED.
 *
 * Task I. reservoir_frontier.py:231 costs OP3 at a hard-coded 4000 cycles/beat,
 * labelled in its own comment as an order-of-magnitude estimate. That figure
 * produces the 588x headline in the abstract and the conclusion. This file is the
 * actual computation, in rv32i, so it can be counted the same way the 153-cycle
 * numeric-LIF column was: exact instruction counts from the disassembly, 1 CPI,
 * plus one extra cycle per load (VexRiscv load = 2 cycles).
 *
 * The path reproduced here is exactly reservoir_data.py::get_beats plus
 * _rr_features plus HistGradientBoostingClassifier traversal:
 *
 *   1. resample   234-sample window (win=(-90,144) @ 360 Hz) -> 128 points,
 *                 linear interpolation (np.interp)
 *   2. normalise  min/max over the 128, then (v - lo) / (hi - lo)
 *   3. rr         prev_rr, next_rr, prev/local_avg, local_avg over +/-10 beats
 *   4. traverse   600 trees (200 boosting stages x 3 classes), 671.5 internal-node
 *                 visits per beat measured on the real fitted model and the real
 *                 90 beats, 600 leaf accumulations
 *
 * FIXED POINT: Q16.16 in int32. The core has neither a hardware multiplier nor a
 * hardware divider, so both are software routines here and are counted as such.
 *
 * FAVOURABLE CHOICES, all made in OP3's favour so the resulting ratio remains an
 * upper bound on the analog substrate's disadvantage:
 *   - normalisation computes ONE reciprocal and then multiplies, rather than
 *     doing 128 divisions. The naive version costs ~128 divisions instead.
 *   - the tree node table is assumed resident and indexed directly; no bounds
 *     checks, no bagging, no per-class softmax.
 *   - R-peak detection is charged to nobody (Section 8.4): it is shared with OP1
 *     and OP2, which consume an R-peak-aligned window.
 *
 * Build (counting only -- this never runs on the die in this form):
 *   riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -O2 -ffreestanding -nostdlib \
 *     -c op3_kernel.c -o op3_kernel.o && riscv64-unknown-elf-objdump -d op3_kernel.o
 */

typedef signed char        int8_t;
typedef short              int16_t;
typedef int                int32_t;
typedef unsigned int       uint32_t;

#define N_SRC   234        /* window length: win=(-90,144) at fs=360 */
#define N_DST   128        /* resample target: get_beats(length=128)  */
#define RR_WIN  10         /* _rr_features(win=10) -> up to 21 samples */
#define N_TREES 600        /* 200 boosting stages x 3 classes         */

/* ---------------------------------------------------------------- soft mul */
/* Shift-and-add, same shape as the umul32 loop counted for the LIF step
 * (7 instructions per iteration, one iteration per bit of the multiplier). */
static int32_t soft_mul(int32_t a, int32_t b)
{
    uint32_t x = (uint32_t)a, r = 0;
    uint32_t m = (uint32_t)b;
    while (m) {
        if (m & 1u) r += x;
        x <<= 1;
        m >>= 1;
    }
    return (int32_t)r;
}

/* ---------------------------------------------------------------- soft div */
/* Restoring division, 32 iterations, no early exit. */
static int32_t soft_div(int32_t num, int32_t den)
{
    uint32_t n = (uint32_t)num, d = (uint32_t)den, q = 0, rem = 0;
    int i;
    for (i = 31; i >= 0; i--) {
        rem = (rem << 1) | ((n >> i) & 1u);
        if (rem >= d) { rem -= d; q |= (1u << i); }
    }
    return (int32_t)q;
}

/* ------------------------------------------------------- 1. resample 234->128 */
/* np.interp onto a uniform grid: position advances by a constant Q16.16 step,
 * so each output point costs one integer part, one fractional part, one
 * multiply and one add. */
int32_t op3_resample(const int16_t *src, int32_t *dst)
{
    /* step = (N_SRC-1)/(N_DST-1) in Q16.16, hoisted out of the loop */
    const int32_t step = (int32_t)(((N_SRC - 1) << 16) / (N_DST - 1));
    int32_t pos = 0;
    int k;
    for (k = 0; k < N_DST; k++) {
        int32_t i = pos >> 16;
        int32_t frac = pos & 0xffff;
        int32_t a = (int32_t)src[i];
        int32_t b = (int32_t)src[i + 1];
        dst[k] = (a << 16) + soft_mul(b - a, frac);
        pos += step;
    }
    return dst[0];
}

/* ------------------------------------------------------- 2. per-beat normalise */
/* min/max scan, then ONE reciprocal and 128 multiplies. */
void op3_normalise(int32_t *v)
{
    int32_t lo = v[0], hi = v[0];
    int k;
    for (k = 1; k < N_DST; k++) {
        if (v[k] < lo) lo = v[k];
        if (v[k] > hi) hi = v[k];
    }
    {
        int32_t span = hi - lo;
        int32_t recip = soft_div((int32_t)1 << 30, span ? span : 1);
        for (k = 0; k < N_DST; k++)
            v[k] = soft_mul(v[k] - lo, recip) >> 14;
    }
}

/* ------------------------------------------------------- 3. RR features */
/* prev_rr, next_rr, prev/local_avg, local_avg over the +/-10-beat window. */
void op3_rr(const int32_t *rpk, int32_t idx, int32_t *out)
{
    int32_t prev = rpk[idx]     - rpk[idx - 1];
    int32_t next = rpk[idx + 1] - rpk[idx];
    int32_t sum = 0;
    int j;
    for (j = -RR_WIN; j <= RR_WIN; j++)
        sum += rpk[idx + j] - rpk[idx + j - 1];
    {
        int32_t loc = soft_div(sum, 2 * RR_WIN + 1);
        out[0] = prev;
        out[1] = next;
        out[2] = soft_div(prev << 16, loc ? loc : 1);
        out[3] = loc;
    }
}

/* ------------------------------------------------------- 4. tree traversal */
/* Flat node table. A node is a leaf when feature_idx < 0, in which case `value`
 * is the leaf contribution; otherwise `value` is the split threshold and
 * left/right are node indices. */
struct op3_node {
    int16_t feature_idx;   /* <0 -> leaf */
    int16_t left;
    int16_t right;
    int16_t pad;
    int32_t value;         /* threshold, or leaf contribution */
};

int32_t op3_trees(const int32_t *feat, const struct op3_node *nodes,
                  const int16_t *roots, int32_t *class_acc)
{
    int t, c = 0;
    for (t = 0; t < N_TREES; t++) {
        const struct op3_node *nd = &nodes[roots[t]];
        while (nd->feature_idx >= 0)
            nd = &nodes[(feat[nd->feature_idx] <= nd->value) ? nd->left : nd->right];
        class_acc[c] += nd->value;          /* cycling 0,1,2 -- no modulo: the core
                                               has no divider and a counter is what
                                               an embedded implementation would use */
        if (++c == 3) c = 0;
    }
    return class_acc[0];
}
