v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 1110 -1240 0 0 0.4 0.4 {}
T {input spikes} 560 -970 0 0 0.4 0.4 {}
T {synaptic weight} 830 -1250 0 0 0.4 0.4 {}
T {analog synapse current } 1400 -1240 0 0 0.4 0.4 {}
N 350 -1030 380 -1030 {
lab=syn_addr[0:1]}
N 1340 -920 1470 -920 {
lab=sout}
N 1470 -920 1600 -920 {
lab=sout}
N 1000 -860 1040 -860 {
lab=vpulseextp}
N 910 -900 1040 -900 {
lab=#net1}
N 910 -820 940 -820 {
lab=#net2}
N 940 -840 940 -820 {
lab=#net2}
N 940 -840 1040 -840 {
lab=#net2}
C {devices/iopin.sym} 1140 -1060 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 1140 -1040 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 1210 -1100 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 750 -1180 0 0 {name=p46 lab=syn_addr[0:1]

}
C {devices/ipin.sym} 940 -1190 0 0 {name=p15 lab=W[0:3]

}
C {devices/ipin.sym} 1210 -1190 0 0 {name=p383 lab=JExcWn[0:3]

}
C {devices/iopin.sym} 1480 -1190 0 0 {name=p28 lab=sout
}
C {devices/ipin.sym} 940 -1130 0 0 {name=p9 lab=setW

}
C {devices/ipin.sym} 940 -1160 0 0 {name=p10 lab=resetW

}
C {devices/lab_pin.sym} 350 -1030 0 0 {name=p5 sig_type=std_logic lab=syn_addr[0:1]}
C {devices/lab_pin.sym} 680 -990 2 0 {name=p18 sig_type=std_logic lab=D[3:0]}
C {devices/lab_pin.sym} 680 -1010 2 0 {name=p22 sig_type=std_logic lab=req_syn}
C {devices/ipin.sym} 750 -1150 0 0 {name=p26 lab=req

}
C {devices/lab_pin.sym} 380 -1050 0 0 {name=p27 sig_type=std_logic lab=req}
C {decoder_2_to_4.sym} 530 -1020 0 0 {name=x6}
C {devices/lab_pin.sym} 1600 -920 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 1340 -900 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1340 -880 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 790 -920 0 0 {name=p11 sig_type=std_logic lab=D[0:3]}
C {devices/lab_pin.sym} 1040 -800 0 0 {name=p13 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 790 -800 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1040 -880 0 0 {name=p19 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1000 -860 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {sky130_stdcells/and2_1.sym} 850 -900 0 0 {name=x4[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 790 -880 0 0 {name=p23 sig_type=std_logic lab=req_syn}
C {synapse_4bit_memory_v1.sym} 1190 -850 0 0 {name=x1[0:3]}
C {devices/ipin.sym} 1210 -1170 0 0 {name=p1 lab=vthrdn

}
C {devices/ipin.sym} 1210 -1150 0 0 {name=p2 lab=vtaup

}
C {devices/lab_pin.sym} 1040 -820 0 0 {name=p6 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1040 -780 0 0 {name=p7 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1040 -920 0 0 {name=p8 sig_type=std_logic lab=JExcWn[0:3]
}
C {devices/lab_pin.sym} 790 -840 0 0 {name=p12 sig_type=std_logic lab=D[0:3]}
C {sky130_stdcells/and2_1.sym} 850 -820 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 680 -1030 2 0 {name=p14 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 680 -1050 2 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 1140 -1020 0 0 {name=p20 lab=aVDD}
C {devices/lab_pin.sym} 1340 -860 2 0 {name=p21 sig_type=std_logic lab=aVDD}
