v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 1030 -3140 0 0 0.4 0.4 {}
T {input spikes} 540 -3140 0 0 0.4 0.4 {}
T {synaptic weight} 750 -3145 0 0 0.4 0.4 {}
T {analog synapse current } 1320 -3140 0 0 0.4 0.4 {}
N 1200 -2830 1330 -2830 {
lab=sout}
N 1330 -2830 1460 -2830 {
lab=sout}
N 100 -2810 130 -2810 {
lab=req}
N 430 -2810 460 -2810 {
lab=req_syn}
N 430 -2830 460 -2830 {
lab=D[15:0]}
N 860 -2690 900 -2690 {
lab=vpulseextp}
N 770 -2810 900 -2810 {
lab=#net1}
C {devices/iopin.sym} 1060 -2960 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 1060 -2940 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 1130 -3000 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 670 -3080 0 0 {name=p46 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 860 -3085 0 0 {name=p15 lab=W[0:3]

}
C {devices/ipin.sym} 1130 -3060 0 0 {name=p381 lab=vthrdpip

}
C {devices/ipin.sym} 1130 -3030 0 0 {name=p382 lab=vtaudpin

}
C {devices/ipin.sym} 1130 -3090 0 0 {name=p383 lab=vstddpip

}
C {devices/iopin.sym} 1400 -3090 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1460 -2830 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 1200 -2810 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1200 -2790 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 900 -2730 0 0 {name=p44 sig_type=std_logic lab=vtaudpin
}
C {devices/lab_pin.sym} 900 -2770 0 0 {name=p45 sig_type=std_logic lab=vthrdpip}
C {devices/lab_pin.sym} 900 -2830 0 0 {name=p43 sig_type=std_logic lab=vstddpip}
C {devices/ipin.sym} 860 -3025 0 0 {name=p9 lab=setW

}
C {devices/ipin.sym} 860 -3055 0 0 {name=p10 lab=resetW

}
C {decoder_4_to_16.sym} 280 -2800 0 0 {name=x3}
C {devices/lab_pin.sym} 130 -2830 0 0 {name=p5 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 460 -2830 1 0 {name=p18 sig_type=std_logic lab=D[15:0]}
C {devices/lab_pin.sym} 650 -2830 0 0 {name=p11 sig_type=std_logic lab=D[0:15]}
C {devices/lab_pin.sym} 900 -2710 0 0 {name=p13 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 900 -2750 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 900 -2790 0 0 {name=p19 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 860 -2690 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {sky130_stdcells/and2_1.sym} 710 -2810 0 0 {name=x4[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 460 -2810 2 0 {name=p22 sig_type=std_logic lab=req_syn}
C {devices/lab_pin.sym} 650 -2790 0 0 {name=p23 sig_type=std_logic lab=req_syn}
C {devices/ipin.sym} 670 -3050 0 0 {name=p26 lab=req

}
C {devices/lab_pin.sym} 100 -2810 0 0 {name=p27 sig_type=std_logic lab=req}
C {synapse_4bit_memory_inh.sym} 1050 -2760 0 0 {name=x1[0:15]}
C {devices/lab_pin.sym} 430 -2770 2 0 {name=p1 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 430 -2790 2 0 {name=p2 sig_type=std_logic lab=VDD}
