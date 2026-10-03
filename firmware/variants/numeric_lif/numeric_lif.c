// Numeric-LIF reservoir cost microbenchmark for the RISC-V (RV32I @ 25 MHz, using software
// multiply/divide). This is the DIGITAL SAME-ALGORITHM baseline (OP2 of the
// ECG frontier): the co-integrated core must reproduce the analog reservoir by Euler-
// integrating 16 heterogeneous LIF ODEs. It is compiled to rv32i and disassembled to
// count the instruction path; the dynamic per-beat cost is O(N_neurons * T/dt) and is
// dominated by the software multiply used for the membrane decay (rv32i multiplies in software).
//
// Fixed-point Q16 state, matching the codebase's -nostdlib convention (hand shift-add
// multiply, libgcc-free). One inner step per neuron:
//     v = (v * decay) >> 16 + jump[i];   // leak (soft-mul) + synaptic input
//     if (v < 0) v = 0;                  // rectify
//     if (v >= vth && !refractory) { spike; v = vreset; }
//
// The membrane decay `decay = round(exp(-dt/tau) * 65536)` is a per-neuron constant
// (the measured heterogeneous time constants), so the ONLY substrate difference vs the
// analog array is dt / precision / energy -- the fairness requirement of the brief.

#include <stdint.h>

#define N 16          // neurons
#define NSTEP 2000    // T/dt steps per beat (T=2 s, dt=1 ms shown; swept offline)

// Unsigned 32x32 -> 32 shift-add multiply. Identical to neuron_handshake.c:umul32 --
// rv32i multiplies in software and we link -nostdlib, so multiply by hand. Loop count = bit-length
// of the multiplier b, which is why the decay multiply dominates the per-step cost.
uint32_t umul32(uint32_t a, uint32_t b)
{
    uint32_t r = 0;
    while (b) {
        if (b & 1u) r += a;
        a <<= 1;
        b >>= 1;
    }
    return r;
}

// One Euler LIF step for one neuron. Returns 1 if the neuron spiked this step.
// v, decay in Q16; jump already in Q16; vth, vreset in Q16; refr counts down.
int lif_step(int32_t *v, uint32_t decay, int32_t jump,
             int32_t vth, int32_t vreset, int32_t *refr)
{
    // leak: v = (v * decay) >> 16   (soft multiply -- the expensive op)
    int32_t vv = *v;
    uint32_t neg = vv < 0;
    uint32_t mag = neg ? (uint32_t)(-vv) : (uint32_t)vv;
    uint32_t prod = umul32(mag, decay) >> 16;
    vv = neg ? -(int32_t)prod : (int32_t)prod;
    // synaptic input
    vv += jump;
    if (vv < 0) vv = 0;              // rectify
    int spiked = 0;
    if (*refr > 0) {
        (*refr)--;
        vv = vreset;
    } else if (vv >= vth) {
        spiked = 1;
        vv = vreset;
        *refr = 125;                 // refractory steps (5 ms / dt at dt=1 ms shown)
    }
    *v = vv;
    return spiked;
}

// Integrate the whole 16-neuron reservoir for one beat. `jumps` is the per-neuron,
// per-step synaptic input (Q16); in the real run this is the delta-encoded ECG feature
// stream binned onto the dt grid. Returns total output spikes (kept so the compiler
// keeps the loop live).
int reservoir_beat(int32_t *v, uint32_t *decay, int32_t *vth,
                   int32_t *vreset, int32_t *refr, const int32_t *jumps)
{
    int total = 0;
    for (int i = 0; i < NSTEP; i++) {
        for (int k = 0; k < N; k++) {
            total += lif_step(&v[k], decay[k], jumps[i * N + k],
                              vth[k], vreset[k], &refr[k]);
        }
    }
    return total;
}
