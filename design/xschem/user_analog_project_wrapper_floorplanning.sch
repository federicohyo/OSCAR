v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 760 -520 800 -520 {
lab=gpio_analog[7:4]}
C {devices/iopin.sym} 200 -1230 0 0 {name=p1 lab=vdda1}
C {devices/iopin.sym} 200 -1200 0 0 {name=p2 lab=vdda2}
C {devices/iopin.sym} 200 -1170 0 0 {name=p3 lab=vssa1}
C {devices/iopin.sym} 200 -1140 0 0 {name=p4 lab=vssa2}
C {devices/iopin.sym} 200 -1110 0 0 {name=p5 lab=vccd1}
C {devices/iopin.sym} 200 -1080 0 0 {name=p6 lab=vccd2}
C {devices/iopin.sym} 200 -1050 0 0 {name=p7 lab=vssd1}
C {devices/iopin.sym} 200 -1020 0 0 {name=p8 lab=vssd2}
C {devices/ipin.sym} 250 -950 0 0 {name=p9 lab=wb_clk_i}
C {devices/ipin.sym} 250 -920 0 0 {name=p10 lab=wb_rst_i}
C {devices/ipin.sym} 250 -890 0 0 {name=p11 lab=wbs_stb_i}
C {devices/ipin.sym} 250 -860 0 0 {name=p12 lab=wbs_cyc_i}
C {devices/ipin.sym} 250 -830 0 0 {name=p13 lab=wbs_we_i}
C {devices/ipin.sym} 250 -800 0 0 {name=p14 lab=wbs_sel_i[3:0]}
C {devices/ipin.sym} 250 -770 0 0 {name=p15 lab=wbs_dat_i[31:0]}
C {devices/ipin.sym} 250 -740 0 0 {name=p16 lab=wbs_adr_i[31:0]}
C {devices/opin.sym} 240 -680 0 0 {name=p17 lab=wbs_ack_o}
C {devices/opin.sym} 240 -650 0 0 {name=p18 lab=wbs_dat_o[31:0]}
C {devices/ipin.sym} 250 -610 0 0 {name=p19 lab=la_data_in[127:0]}
C {devices/opin.sym} 240 -580 0 0 {name=p20 lab=la_data_out[127:0]}
C {devices/ipin.sym} 250 -500 0 0 {name=p21 lab=io_in[26:0]}
C {devices/ipin.sym} 250 -470 0 0 {name=p22 lab=io_in_3v3[26:0]}
C {devices/ipin.sym} 240 -190 0 0 {name=p23 lab=user_clock2}
C {devices/opin.sym} 240 -440 0 0 {name=p24 lab=io_out[26:0]}
C {devices/opin.sym} 240 -410 0 0 {name=p25 lab=io_oeb[26:0]}
C {devices/iopin.sym} 210 -350 0 0 {name=p26 lab=gpio_analog[17:0]}
C {devices/iopin.sym} 210 -320 0 0 {name=p27 lab=gpio_noesd[17:0]}
C {devices/iopin.sym} 210 -290 0 0 {name=p29 lab=io_analog[10:0]}
C {devices/iopin.sym} 210 -260 0 0 {name=p30 lab=io_clamp_high[2:0]}
C {devices/iopin.sym} 210 -230 0 0 {name=p31 lab=io_clamp_low[2:0]}
C {devices/opin.sym} 230 -160 0 0 {name=p32 lab=user_irq[2:0]}
C {devices/ipin.sym} 250 -550 0 0 {name=p28 lab=la_oenb[127:0]}
C {neuron_32syn_v1.sym} 950 -390 0 0 {name=x3}
C {neuron_synapse_array_with_input_output_logic_v1.sym} 1600 -390 0 0 {name=x5}
C {low_noise_amp_fc_v3.sym} 1520 -790 0 0 {name=x4}
C {low_noise_amp_fc_v3_withpad.sym} 950 -800 0 0 {name=x6}
C {devices/lab_pin.sym} 800 -830 2 1 {name=l50 sig_type=std_logic lab=io_analog[7]}
C {devices/lab_pin.sym} 1470 -960 2 1 {name=l22 sig_type=std_logic lab=io_analog[7]}
C {devices/lab_pin.sym} 800 -810 2 1 {name=l23 sig_type=std_logic lab=io_analog[5]}
C {devices/lab_pin.sym} 1470 -920 2 1 {name=l24 sig_type=std_logic lab=io_analog[5]}
C {devices/lab_pin.sym} 800 -790 2 1 {name=l25 sig_type=std_logic lab=io_analog[3]}
C {devices/lab_pin.sym} 1470 -900 2 1 {name=l26 sig_type=std_logic lab=io_analog[3]}
C {devices/lab_pin.sym} 800 -770 2 1 {name=l27 sig_type=std_logic lab=io_analog[6]}
C {devices/lab_pin.sym} 1470 -940 2 1 {name=l28 sig_type=std_logic lab=io_analog[6]}
C {devices/lab_pin.sym} 1100 -790 2 0 {name=l29 sig_type=std_logic lab=io_analog[4]}
C {devices/lab_pin.sym} 1420 -830 2 1 {name=l30 sig_type=std_logic lab=io_analog[9]}
C {devices/lab_pin.sym} 1420 -750 2 1 {name=l31 sig_type=std_logic lab=io_analog[10]}
C {devices/lab_pin.sym} 1640 -790 2 0 {name=l32 sig_type=std_logic lab=io_analog[8]}
C {devices/lab_pin.sym} 1100 -830 2 0 {name=l1 sig_type=std_logic lab=io_analog[1]}
C {devices/lab_pin.sym} 1100 -810 2 0 {name=l2 sig_type=std_logic lab=io_analog[2]}
C {devices/lab_pin.sym} 1590 -890 2 0 {name=l3 sig_type=std_logic lab=io_analog[1]}
C {devices/lab_pin.sym} 1590 -870 2 0 {name=l4 sig_type=std_logic lab=io_analog[2]}
C {devices/lab_pin.sym} 1450 -290 2 1 {name=l8 sig_type=std_logic lab=gpio_analog[2]}
C {devices/lab_pin.sym} 800 -340 2 1 {name=l9 sig_type=std_logic lab=gpio_analog[2]}
C {devices/lab_pin.sym} 1450 -570 2 1 {name=l10 sig_type=std_logic lab=gpio_analog[0]}
C {devices/lab_pin.sym} 800 -560 2 1 {name=l11 sig_type=std_logic lab=gpio_analog[0]}
C {devices/lab_pin.sym} 800 -500 2 1 {name=l12 sig_type=std_logic lab=gpio_analog[3]}
C {devices/lab_pin.sym} 1450 -490 2 1 {name=l13 sig_type=std_logic lab=gpio_analog[3]}
C {devices/lab_pin.sym} 1450 -190 2 1 {name=l14 sig_type=std_logic lab=gpio_analog[9]}
C {devices/lab_pin.sym} 1450 -210 2 1 {name=l15 sig_type=std_logic lab=gpio_analog[17]}
C {devices/lab_pin.sym} 800 -360 2 1 {name=l16 sig_type=std_logic lab=gpio_analog[9]}
C {devices/lab_pin.sym} 800 -300 2 1 {name=l17 sig_type=std_logic lab=gpio_analog[17]}
C {devices/lab_pin.sym} 800 -580 2 1 {name=l20 sig_type=std_logic lab=gpio_analog[14:11]}
C {devices/lab_pin.sym} 1450 -510 2 1 {name=l21 sig_type=std_logic lab=gpio_analog[14:11]}
C {devices/lab_pin.sym} 800 -420 2 1 {name=l33 sig_type=std_logic lab=gpio_analog[15]}
C {devices/lab_pin.sym} 1450 -390 2 1 {name=l34 sig_type=std_logic lab=gpio_analog[15]}
C {devices/lab_pin.sym} 1450 -410 2 1 {name=l35 sig_type=std_logic lab=gpio_analog[8]}
C {devices/lab_pin.sym} 800 -440 2 1 {name=l36 sig_type=std_logic lab=gpio_analog[8]}
C {devices/lab_pin.sym} 1450 -310 2 1 {name=l37 sig_type=std_logic lab=gpio_analog[16]}
C {devices/lab_pin.sym} 800 -240 2 1 {name=l38 sig_type=std_logic lab=gpio_analog[16]}
C {devices/lab_pin.sym} 1750 -590 2 0 {name=l48 sig_type=std_logic lab=io_analog[0]}
C {devices/lab_pin.sym} 1100 -580 2 0 {name=l49 sig_type=std_logic lab=io_analog[3]}
C {devices/lab_pin.sym} 1450 -610 2 1 {name=l51 sig_type=std_logic lab=la_data_in[27:30]}
C {devices/lab_pin.sym} 1450 -430 2 1 {name=l52 sig_type=std_logic lab=la_data_in[23:26]}
C {devices/lab_pin.sym} 1450 -550 2 1 {name=l53 sig_type=std_logic lab=la_data_in[22]}
C {devices/lab_pin.sym} 1450 -350 2 1 {name=l54 sig_type=std_logic lab=la_data_in[21]}
C {devices/lab_pin.sym} 1450 -170 2 1 {name=l55 sig_type=std_logic lab=la_data_in[20]}
C {devices/lab_pin.sym} 1750 -570 2 0 {name=l56 sig_type=std_logic lab=la_data_out[65:62]}
C {devices/lab_pin.sym} 1450 -330 2 1 {name=l57 sig_type=std_logic lab=la_data_in[66]}
C {devices/lab_pin.sym} 1450 -370 2 1 {name=l58 sig_type=std_logic lab=la_data_in[67]}
C {devices/lab_pin.sym} 1450 -590 2 1 {name=l59 sig_type=std_logic lab=la_data_in[68]}
C {devices/lab_pin.sym} 1100 -480 2 0 {name=l60 sig_type=std_logic lab=la_data_out[69]}
C {devices/lab_pin.sym} 800 -220 2 1 {name=l61 sig_type=std_logic lab=la_data_in[70]}
C {devices/lab_pin.sym} 1450 -270 2 1 {name=l62 sig_type=std_logic lab=la_data_in[19:16]}
C {devices/lab_pin.sym} 1450 -230 2 1 {name=l63 sig_type=std_logic lab=la_data_in[15]}
C {devices/lab_pin.sym} 800 -200 2 1 {name=l64 sig_type=std_logic lab=la_data_in[68]}
C {devices/lab_pin.sym} 800 -540 2 1 {name=l65 sig_type=std_logic lab=la_data_in[11:14]}
C {devices/lab_pin.sym} 800 -480 2 1 {name=l66 sig_type=std_logic lab=la_data_in[7:10]}
C {devices/lab_pin.sym} 800 -400 2 1 {name=l67 sig_type=std_logic lab=la_data_in[6]}
C {devices/lab_pin.sym} 800 -320 2 1 {name=l68 sig_type=std_logic lab=la_data_in[5]}
C {devices/lab_pin.sym} 800 -260 2 1 {name=l69 sig_type=std_logic lab=la_data_in[4]}
C {devices/lab_pin.sym} 800 -380 2 1 {name=l70 sig_type=std_logic lab=la_data_in[3]}
C {devices/lab_pin.sym} 1750 -610 2 0 {name=l71 sig_type=std_logic lab=la_data_out[61]}
C {devices/lab_pin.sym} 1450 -530 2 1 {name=l72 sig_type=std_logic lab=la_data_in[60]}
C {devices/lab_pin.sym} 1100 -520 2 0 {name=l73 sig_type=std_logic lab=vccd1}
C {devices/lab_pin.sym} 1750 -510 2 0 {name=l74 sig_type=std_logic lab=vccd1}
C {devices/lab_pin.sym} 1100 -500 2 0 {name=l75 sig_type=std_logic lab=vssd1}
C {devices/lab_pin.sym} 1750 -550 2 0 {name=l76 sig_type=std_logic lab=vssd1}
C {devices/lab_pin.sym} 1750 -490 2 0 {name=l77 sig_type=std_logic lab=vccd2}
C {devices/lab_pin.sym} 1100 -540 2 0 {name=l78 sig_type=std_logic lab=vccd2}
C {devices/lab_pin.sym} 1100 -560 2 0 {name=l79 sig_type=std_logic lab=vssd2}
C {devices/lab_pin.sym} 1750 -530 2 0 {name=l80 sig_type=std_logic lab=vssd2}
C {devices/lab_pin.sym} 760 -520 2 1 {name=l5 sig_type=std_logic lab=gpio_analog[7:4]}
C {devices/lab_pin.sym} 800 -460 2 1 {name=l7 sig_type=std_logic lab=gpio_analog[10]}
C {devices/lab_pin.sym} 1450 -470 2 1 {name=l6 sig_type=std_logic lab=gpio_analog[7:4]}
C {devices/lab_pin.sym} 1450 -450 2 1 {name=l39 sig_type=std_logic lab=gpio_analog[10]}
C {devices/lab_pin.sym} 800 -280 2 1 {name=l18 sig_type=std_logic lab=gpio_analog[1]}
C {devices/lab_pin.sym} 1450 -250 2 1 {name=l19 sig_type=std_logic lab=gpio_analog[1]}
