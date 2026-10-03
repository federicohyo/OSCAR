v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {An array of 4 neurons with 32 synapses each (16E/16I)} 230 -650 0 0 0.4 0.4 {}
T {Input neuron address } 1080 -830 0 0 0.4 0.4 {}
T {Ouput interface address events are encoded 
and an arbiter is taking care of req/ack cycles} 1090 -660 0 0 0.4 0.4 {}
T {neuron biases} 80 -1160 0 0 0.4 0.4 {}
T {excitatory and inhibitory syn} 290 -1150 0 0 0.4 0.4 {}
T {Output Spikes (AER)} 1220 -1140 0 0 0.4 0.4 {}
T {Digital Logic / Input Spikes (AER)} 800 -1150 0 0 0.4 0.4 {}
T {Monitors Vmem} 1500 -1150 0 0 0.4 0.4 {}
T {Synaptic Weights} 1720 -1150 0 0 0.4 0.4 {}
T {analog synapse} 310 -1100 0 0 0.4 0.4 {}
T {analog synapse} 540 -1100 0 0 0.4 0.4 {}
T {neuron address encoder } 1120 -500 0 0 0.4 0.4 {}
T {Latch the inputs} 190 -840 0 0 0.4 0.4 {}
T {Monitor one neuron at the time (Analog Output)} 1030 -390 0 0 0.4 0.4 {}
N 900 -1090 940 -1090 {
lab=nRes}
N 900 -1060 940 -1060 {
lab=ack}
N 920 -740 940 -740 {
lab=neu_addr_latched[0:1]}
N 910 -760 940 -760 {
lab=req_array}
N 1260 -700 1280 -700 {
lab=#net1}
N 1260 -720 1260 -700 {
lab=#net1}
N 1240 -720 1260 -720 {
lab=#net1}
N 1240 -700 1250 -700 {
lab=#net2}
N 1250 -710 1250 -700 {
lab=#net2}
N 1250 -710 1270 -710 {
lab=#net2}
N 1270 -720 1270 -710 {
lab=#net2}
N 1270 -720 1280 -720 {
lab=#net2}
N 1120 -320 1160 -320 {
lab=CLK}
N 1120 -340 1160 -340 {
lab=Da}
C {devices/lab_pin.sym} 390 -370 0 0 {name=p1 sig_type=std_logic lab=neu_req[0:3]}
C {devices/lab_pin.sym} 150 -770 0 0 {name=p2 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 690 -570 2 0 {name=p13 sig_type=std_logic lab=req_o[0:3]}
C {devices/lab_pin.sym} 690 -590 2 0 {name=p52 sig_type=std_logic lab=monout[0:3]}
C {devices/lab_pin.sym} 1580 -720 2 0 {name=p3 sig_type=std_logic lab=neu_req[0:3]}
C {devices/lab_pin.sym} 390 -530 0 0 {name=p388 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 390 -350 0 0 {name=p10 sig_type=std_logic lab=vrefn

}
C {devices/lab_pin.sym} 390 -570 0 0 {name=p51 sig_type=std_logic lab=bufmonp

}
C {devices/lab_pin.sym} 390 -210 0 0 {name=p11 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 390 -450 0 0 {name=p9 sig_type=std_logic lab=vleakn
}
C {devices/lab_pin.sym} 390 -410 0 0 {name=p41 sig_type=std_logic lab=vepulseextp
}
C {devices/lab_pin.sym} 390 -430 0 0 {name=p5 sig_type=std_logic lab=vipulseextp
}
C {devices/lab_pin.sym} 390 -510 0 0 {name=p12 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 390 -390 0 0 {name=p16 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 390 -290 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 150 -710 0 0 {name=p18 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 690 -510 2 0 {name=p23 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 690 -530 2 0 {name=p24 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 690 -550 2 0 {name=p25 sig_type=std_logic lab=dGND}
C {devices/ipin.sym} 160 -1040 0 0 {name=p234 lab=vleakn
}
C {devices/ipin.sym} 160 -1010 0 0 {name=p372 lab=vrefn

}
C {devices/ipin.sym} 160 -1070 0 0 {name=p377 lab=ifdcp
}
C {devices/ipin.sym} 1640 -1050 0 0 {name=p50 lab=bufmonp}
C {devices/opin.sym} 1300 -1080 0 0 {name=p28 lab=req_o}
C {devices/opin.sym} 1300 -1050 0 0 {name=p42 lab=aer_o[0:1]}
C {devices/iopin.sym} 1130 -920 0 0 {name=p29 lab=dGND
}
C {devices/iopin.sym} 1130 -900 0 0 {name=p30 lab=dVDD}
C {devices/ipin.sym} 900 -1090 0 0 {name=p31 lab=nRes}
C {devices/lab_pin.sym} 940 -1090 2 0 {name=p32 sig_type=std_logic lab=nRes}
C {devices/ipin.sym} 900 -1060 0 0 {name=p37 lab=ack}
C {devices/ipin.sym} 980 -1000 0 0 {name=p46 lab=neu_addr[0:1]

}
C {devices/ipin.sym} 920 -970 0 0 {name=p49 lab=req_inp

}
C {devices/ipin.sym} 980 -1030 0 0 {name=p45 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 910 -940 0 0 {name=p47 lab=exc

}
C {devices/iopin.sym} 1230 -900 0 0 {name=p54 lab=aVDD}
C {devices/iopin.sym} 1540 -1080 0 0 {name=p55 lab=monout}
C {devices/ipin.sym} 1900 -1090 0 0 {name=p56 lab=W[0:3]

}
C {devices/ipin.sym} 1900 -1060 0 0 {name=p57 lab=resetW

}
C {devices/ipin.sym} 1900 -1030 0 0 {name=p58 lab=setW

}
C {devices/ipin.sym} 450 -1020 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 670 -1020 0 0 {name=p74 lab=vipulseextp

}
C {devices/ipin.sym} 450 -1050 0 0 {name=p27 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 670 -1050 0 0 {name=p383 lab=JInhWp[0:3]

}
C {devices/lab_pin.sym} 390 -550 0 0 {name=p19 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 390 -590 0 0 {name=p43 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 1180 -590 0 0 {name=p65 sig_type=std_logic lab=req_o[0:3]}
C {devices/lab_pin.sym} 1480 -590 2 0 {name=p66 sig_type=std_logic lab=req_o}
C {devices/lab_pin.sym} 1470 -450 2 0 {name=p67 sig_type=std_logic lab=aer_o[0:1]}
C {devices/lab_pin.sym} 1180 -570 0 0 {name=p68 sig_type=std_logic lab=ack}
C {devices/lab_pin.sym} 1480 -570 0 1 {name=p33 sig_type=std_logic lab=ack_neu[0:3]}
C {devices/lab_pin.sym} 390 -490 2 1 {name=p14 sig_type=std_logic lab=ack_neu[0:3]}
C {devices/ipin.sym} 700 -990 0 0 {name=p4 lab=vthrdp

}
C {devices/ipin.sym} 700 -960 0 0 {name=p7 lab=vtaun

}
C {devices/ipin.sym} 420 -990 0 0 {name=p15 lab=vthrdn

}
C {devices/ipin.sym} 420 -960 0 0 {name=p20 lab=vtaup

}
C {devices/lab_pin.sym} 390 -330 0 0 {name=p21 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 390 -310 0 0 {name=p34 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 390 -230 0 0 {name=p35 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 390 -250 0 0 {name=p36 sig_type=std_logic lab=vtaup}
C {neuro_synaptic_core_4neu_32syn_v1.sym} 540 -400 0 0 {name=x1}
C {decoder_2_to_4.sym} 1090 -730 0 0 {name=x3}
C {devices/lab_pin.sym} 150 -730 0 0 {name=p38 sig_type=std_logic lab=neu_addr[0:1]}
C {devices/lab_pin.sym} 450 -730 0 1 {name=p39 sig_type=std_logic lab=req_array}
C {request_logic_delay_small.sym} 1430 -700 0 0 {name=x2}
C {arbiter_tree_four_bits.sym} 1330 -560 0 0 {name=x4}
C {encoder_4_to_2.sym} 1320 -430 0 0 {name=x5}
C {inputs_latch_4neu.sym} 300 -740 0 0 {name=x6}
C {devices/lab_pin.sym} 150 -790 0 0 {name=p6 sig_type=std_logic lab=req_inp}
C {devices/lab_pin.sym} 150 -750 0 0 {name=p8 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 450 -750 0 1 {name=p44 sig_type=std_logic lab=exc_latched}
C {devices/lab_pin.sym} 390 -270 0 0 {name=p53 sig_type=std_logic lab=exc_latched}
C {devices/lab_pin.sym} 910 -760 0 0 {name=p59 sig_type=std_logic lab=req_array}
C {devices/lab_pin.sym} 450 -770 0 1 {name=p60 sig_type=std_logic lab=neu_addr_latched[0:1]}
C {devices/lab_pin.sym} 920 -740 0 0 {name=p61 sig_type=std_logic lab=neu_addr_latched[0:1]}
C {devices/lab_pin.sym} 450 -790 0 1 {name=p62 sig_type=std_logic lab=syn_addr_latched[0:3]}
C {devices/lab_pin.sym} 390 -470 0 0 {name=p63 sig_type=std_logic lab=syn_addr_latched[0:3]}
C {devices/ipin.sym} 1620 -1010 0 0 {name=p71 lab=Da


}
C {devices/ipin.sym} 1620 -980 0 0 {name=p72 lab=CLK


}
C {devices/lab_pin.sym} 1460 -300 2 0 {name=p75 sig_type=std_logic lab=monout}
C {monitor_select_4.sym} 1310 -310 0 0 {name=x8}
C {devices/lab_pin.sym} 1460 -320 2 0 {name=p76 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1460 -340 2 0 {name=p77 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1130 -320 0 0 {name=p78 sig_type=std_logic lab=CLK}
C {devices/lab_pin.sym} 1120 -340 0 0 {name=p79 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 1160 -300 0 0 {name=p80 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1460 -280 2 0 {name=p82 sig_type=std_logic lab=monout[0:3]}
C {devices/lab_pin.sym} 1170 -450 0 0 {name=p26 sig_type=std_logic lab=ack_neu[0:3]}
C {devices/lab_pin.sym} 1240 -760 2 0 {name=p64 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1240 -740 2 0 {name=p69 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1580 -700 2 0 {name=p70 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1580 -680 2 0 {name=p73 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1470 -430 2 0 {name=p81 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1470 -410 2 0 {name=p83 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 450 -710 2 0 {name=p84 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 450 -690 2 0 {name=p85 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1480 -550 2 0 {name=p86 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1480 -530 2 0 {name=p87 sig_type=std_logic lab=dGND}
