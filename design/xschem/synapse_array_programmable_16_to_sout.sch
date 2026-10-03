v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 1010 -3190 0 0 0.4 0.4 {}
T {input spikes} 520 -3190 0 0 0.4 0.4 {}
T {synaptic weight} 730 -3195 0 0 0.4 0.4 {}
T {analog synapse current } 1300 -3190 0 0 0.4 0.4 {}
N 1180 -2880 1310 -2880 {
lab=sout}
N 1310 -2880 1440 -2880 {
lab=sout}
N 80 -2860 110 -2860 {
lab=req}
N 410 -2860 440 -2860 {
lab=req_syn}
N 410 -2880 440 -2880 {
lab=D[15:0]}
N 750 -2860 880 -2860 {
lab=#net1}
C {devices/iopin.sym} 1040 -3010 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 1040 -2990 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 1110 -3050 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 650 -3130 0 0 {name=p46 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 840 -3135 0 0 {name=p15 lab=W[0:3]

}
C {devices/ipin.sym} 1110 -3110 0 0 {name=p381 lab=vthrdpin

}
C {devices/ipin.sym} 1110 -3080 0 0 {name=p382 lab=vtaudpip

}
C {devices/ipin.sym} 1110 -3140 0 0 {name=p383 lab=vstddpin

}
C {synapse_4bit_memory.sym} 1030 -2810 0 0 {name=x1[0:15]}
C {devices/iopin.sym} 1380 -3140 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1440 -2880 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 1180 -2860 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1180 -2840 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 880 -2780 0 0 {name=p44 sig_type=std_logic lab=vtaudpip
}
C {devices/lab_pin.sym} 880 -2820 0 0 {name=p45 sig_type=std_logic lab=vthrdpin}
C {devices/lab_pin.sym} 880 -2880 0 0 {name=p43 sig_type=std_logic lab=vstddpin}
C {devices/ipin.sym} 840 -3075 0 0 {name=p9 lab=setW

}
C {devices/ipin.sym} 840 -3105 0 0 {name=p10 lab=resetW

}
C {decoder_4_to_16.sym} 260 -2850 0 0 {name=x3}
C {devices/lab_pin.sym} 110 -2880 0 0 {name=p5 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 440 -2880 1 0 {name=p18 sig_type=std_logic lab=D[15:0]}
C {devices/lab_pin.sym} 630 -2880 0 0 {name=p11 sig_type=std_logic lab=D[0:15]}
C {devices/lab_pin.sym} 880 -2760 0 0 {name=p13 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 880 -2800 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 880 -2840 0 0 {name=p19 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 880 -2740 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {sky130_stdcells/and2_1.sym} 690 -2860 0 0 {name=x4[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 440 -2860 2 0 {name=p22 sig_type=std_logic lab=req_syn}
C {devices/lab_pin.sym} 630 -2840 0 0 {name=p23 sig_type=std_logic lab=req_syn}
C {devices/ipin.sym} 650 -3100 0 0 {name=p26 lab=req

}
C {devices/lab_pin.sym} 80 -2860 0 0 {name=p27 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 410 -2820 2 0 {name=p1 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 410 -2840 2 0 {name=p2 sig_type=std_logic lab=VDD}
