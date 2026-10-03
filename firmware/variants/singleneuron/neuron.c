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

void delay_loop(volatile uint32_t count) // Wait ~10 us (25 MHz clock → 1 tick per 40 ns → 250 ticks = 10 us)
{
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

void main()
{
	int i, j, k;

    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // LED OFF (active-LOW)
    
    // Enable User Project power
    reg_mprj_pwr = 1;

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

    // Release nRes: drive HIGH to release active-low reset
    la2_out |= NRES_BIT;
    reg_la2_data = la2_out;

    // Signal start: 3 fast blinks then go straight to handshake loop
    blink(3);
    
    print("Hello World !!\n");


	while (1) {


        blink(1);
        long_pause();
        blink(5);


    }
}

