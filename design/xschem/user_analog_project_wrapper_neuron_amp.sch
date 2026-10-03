v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 3240 -470 0 0 {name=p1 lab=vdda1}
C {devices/iopin.sym} 3240 -440 0 0 {name=p2 lab=vdda2}
C {devices/iopin.sym} 3240 -410 0 0 {name=p3 lab=vssa1}
C {devices/iopin.sym} 3240 -380 0 0 {name=p4 lab=vssa2}
C {devices/iopin.sym} 3240 -350 0 0 {name=p5 lab=vccd1}
C {devices/iopin.sym} 3240 -320 0 0 {name=p6 lab=vccd2}
C {devices/iopin.sym} 3240 -290 0 0 {name=p7 lab=vssd1}
C {devices/iopin.sym} 3240 -260 0 0 {name=p8 lab=vssd2}
C {devices/ipin.sym} 3290 -190 0 0 {name=p9 lab=wb_clk_i}
C {devices/ipin.sym} 3290 -160 0 0 {name=p10 lab=wb_rst_i}
C {devices/ipin.sym} 3290 -130 0 0 {name=p11 lab=wbs_stb_i}
C {devices/ipin.sym} 3290 -100 0 0 {name=p12 lab=wbs_cyc_i}
C {devices/ipin.sym} 3290 -70 0 0 {name=p13 lab=wbs_we_i}
C {devices/ipin.sym} 3290 -40 0 0 {name=p14 lab=wbs_sel_i[3:0]}
C {devices/ipin.sym} 3290 -10 0 0 {name=p15 lab=wbs_dat_i[31:0]}
C {devices/ipin.sym} 3290 20 0 0 {name=p16 lab=wbs_adr_i[31:0]}
C {devices/opin.sym} 3280 80 0 0 {name=p17 lab=wbs_ack_o}
C {devices/opin.sym} 3280 110 0 0 {name=p18 lab=wbs_dat_o[31:0]}
C {devices/ipin.sym} 3290 150 0 0 {name=p19 lab=la_data_in[127:0]}
C {devices/opin.sym} 3280 180 0 0 {name=p20 lab=la_data_out[127:0]}
C {devices/ipin.sym} 3290 260 0 0 {name=p21 lab=io_in[26:0]}
C {devices/ipin.sym} 3290 290 0 0 {name=p22 lab=io_in_3v3[26:0]}
C {devices/ipin.sym} 3280 570 0 0 {name=p23 lab=user_clock2}
C {devices/opin.sym} 3280 320 0 0 {name=p24 lab=io_out[26:0]}
C {devices/opin.sym} 3280 350 0 0 {name=p25 lab=io_oeb[26:0]}
C {devices/iopin.sym} 3250 410 0 0 {name=p26 lab=gpio_analog[17:0]}
C {devices/iopin.sym} 3250 440 0 0 {name=p27 lab=gpio_noesd[17:0]}
C {devices/iopin.sym} 3250 470 0 0 {name=p29 lab=io_analog[10:0]}
C {devices/iopin.sym} 3250 500 0 0 {name=p30 lab=io_clamp_high[2:0]}
C {devices/iopin.sym} 3250 530 0 0 {name=p31 lab=io_clamp_low[2:0]}
C {devices/opin.sym} 3270 600 0 0 {name=p32 lab=user_irq[2:0]}
C {devices/ipin.sym} 3290 210 0 0 {name=p28 lab=la_oenb[127:0]}
C {devices/lab_pin.sym} 3840 560 0 0 {name=l36 sig_type=std_logic lab=io_analog[2]}
C {devices/lab_pin.sym} 3840 300 0 0 {name=l37 sig_type=std_logic lab=io_analog[3]}
C {devices/lab_pin.sym} 3840 420 0 0 {name=l38 sig_type=std_logic lab=io_analog[1]}
C {devices/lab_pin.sym} 3840 180 0 0 {name=l39 sig_type=std_logic lab=io_analog[0]}
C {devices/lab_pin.sym} 4140 220 2 0 {name=l2 sig_type=std_logic lab=vccd2}
C {devices/lab_pin.sym} 4140 200 0 1 {name=l3 sig_type=std_logic lab=vssd1}
C {devices/lab_pin.sym} 3840 200 0 0 {name=l4 sig_type=std_logic lab=io_analog[4]}
C {devices/lab_pin.sym} 3840 240 2 1 {name=l5 sig_type=std_logic lab=gpio_analog[13:16]}
C {neuron_32syn_v1.sym} 3990 370 0 0 {name=x3}
C {devices/lab_pin.sym} 4140 240 2 0 {name=l9 sig_type=std_logic lab=vdda2}
C {devices/lab_pin.sym} 3840 260 0 0 {name=l10 sig_type=std_logic lab=io_analog[7:10]}
C {devices/lab_pin.sym} 3840 340 2 1 {name=l1 sig_type=std_logic lab=gpio_analog[4]}
C {devices/lab_pin.sym} 3840 520 2 1 {name=l6 sig_type=std_logic lab=gpio_analog[8]}
C {devices/lab_pin.sym} 3840 320 2 1 {name=l7 sig_type=std_logic lab=gpio_analog[9]}
C {devices/lab_pin.sym} 3840 480 2 1 {name=l8 sig_type=std_logic lab=gpio_analog[10]}
C {devices/lab_pin.sym} 3840 460 2 1 {name=l11 sig_type=std_logic lab=gpio_analog[11]}
C {devices/lab_pin.sym} 3840 400 2 1 {name=l12 sig_type=std_logic lab=gpio_analog[12]}
C {devices/lab_pin.sym} 3840 380 2 1 {name=l13 sig_type=std_logic lab=la_data_in[1]}
C {devices/lab_pin.sym} 3840 500 2 1 {name=l14 sig_type=std_logic lab=la_data_in[2]}
C {devices/lab_pin.sym} 3840 440 2 1 {name=l15 sig_type=std_logic lab=la_data_in[3]}
C {devices/lab_pin.sym} 3840 360 2 1 {name=l16 sig_type=std_logic lab=la_data_in[4]}
C {devices/lab_pin.sym} 3840 280 2 1 {name=l17 sig_type=std_logic lab=la_data_in[5:8]}
C {devices/lab_pin.sym} 3840 220 2 1 {name=l18 sig_type=std_logic lab=la_data_in[9:12]}
C {devices/lab_pin.sym} 3840 540 2 1 {name=l19 sig_type=std_logic lab=la_data_in[39]}
C {devices/lab_pin.sym} 4140 260 2 0 {name=l20 sig_type=std_logic lab=la_data_out[38]}
C {devices/lab_pin.sym} 4140 180 2 0 {name=l21 sig_type=std_logic lab=la_data_out[40]}
C {low_noise_amp_fc_v3.sym} 3910 -120 0 0 {name=x1}
C {devices/lab_pin.sym} 3980 -220 2 0 {name=l23 sig_type=std_logic lab=vdda1}
C {devices/lab_pin.sym} 4030 -120 0 1 {name=l24 sig_type=std_logic lab=gpio_analog[5]}
C {devices/lab_pin.sym} 3860 -290 2 1 {name=l25 sig_type=std_logic lab=gpio_analog[0]}
C {devices/lab_pin.sym} 3860 -270 2 1 {name=l26 sig_type=std_logic lab=gpio_analog[1]}
C {devices/lab_pin.sym} 3860 -250 2 1 {name=l27 sig_type=std_logic lab=gpio_analog[2]}
C {devices/lab_pin.sym} 3860 -230 2 1 {name=l28 sig_type=std_logic lab=gpio_analog[3]}
C {devices/lab_pin.sym} 3810 -160 2 1 {name=l29 sig_type=std_logic lab=io_analog[5]}
C {devices/lab_pin.sym} 3810 -80 2 1 {name=l30 sig_type=std_logic lab=io_analog[6]}
C {devices/lab_pin.sym} 3980 -200 0 1 {name=l22 sig_type=std_logic lab=vssd1}
