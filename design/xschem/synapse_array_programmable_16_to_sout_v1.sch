v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 1060 -3850 0 0 0.4 0.4 {}
T {input spikes} 510 -3580 0 0 0.4 0.4 {}
T {synaptic weight} 780 -3860 0 0 0.4 0.4 {}
T {analog synapse current } 1350 -3850 0 0 0.4 0.4 {}
T {decoder } 160 -3680 0 0 0.4 0.4 {}
N 1230 -3540 1360 -3540 {
lab=sout}
N 110 -3620 140 -3620 {
lab=req}
N 440 -3620 470 -3620 {
lab=req_syn}
N 440 -3640 470 -3640 {
lab=D[0:15]}
N 800 -3520 930 -3520 {
lab=#net1}
N 790 -3420 820 -3420 {
lab=#net2}
N 820 -3440 820 -3420 {
lab=#net2}
N 820 -3460 820 -3440 {
lab=#net2}
N 820 -3460 930 -3460 {
lab=#net2}
C {devices/iopin.sym} 1090 -3670 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 1090 -3650 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 1160 -3770 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 700 -3790 0 0 {name=p90 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 890 -3800 0 0 {name=p70 lab=W[0:3]

}
C {devices/ipin.sym} 1150 -3800 0 0 {name=p100 lab=JExcWn[0:3]

}
C {devices/iopin.sym} 1430 -3800 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1360 -3540 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 1230 -3500 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1230 -3480 2 0 {name=p37 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 890 -3740 0 0 {name=p9 lab=setW

}
C {devices/ipin.sym} 890 -3770 0 0 {name=p10 lab=resetW

}
C {decoder_4_to_16.sym} 290 -3610 0 0 {name=x3}
C {devices/lab_pin.sym} 140 -3640 0 0 {name=p5 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 470 -3640 2 0 {name=p18 sig_type=std_logic lab=D[0:15]}
C {devices/lab_pin.sym} 680 -3500 0 0 {name=p11 sig_type=std_logic lab=D[0:15]}
C {devices/lab_pin.sym} 930 -3420 0 0 {name=p13 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 930 -3500 0 0 {name=p19 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 930 -3480 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {sky130_stdcells/and2_1.sym} 740 -3520 0 0 {name=x2[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 470 -3620 2 0 {name=p22 sig_type=std_logic lab=req_syn}
C {devices/lab_pin.sym} 680 -3540 0 0 {name=p23 sig_type=std_logic lab=req_syn}
C {devices/ipin.sym} 700 -3760 0 0 {name=p26 lab=req

}
C {devices/lab_pin.sym} 110 -3620 0 0 {name=p27 sig_type=std_logic lab=req}
C {synapse_4bit_memory_v1_norail.sym} 1080 -3470 0 0 {name=x1[0:15]}
C {devices/lab_pin.sym} 930 -3540 0 0 {name=p8 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/ipin.sym} 890 -3710 0 0 {name=p1 lab=vthrdn

}
C {devices/ipin.sym} 890 -3680 0 0 {name=p2 lab=vtaup

}
C {devices/lab_pin.sym} 930 -3440 0 0 {name=p6 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 930 -3400 0 0 {name=p7 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 670 -3400 0 0 {name=p12 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 670 -3440 0 0 {name=p14 sig_type=std_logic lab=D[0:15]}
C {sky130_stdcells/and2_1.sym} 730 -3420 0 0 {name=x3[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 440 -3580 2 0 {name=p16 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 440 -3600 2 0 {name=p17 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 1090 -3610 0 0 {name=p21 lab=aVDD}
C {devices/lab_pin.sym} 1230 -3520 2 0 {name=p30 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 1090 -3630 0 0 {name=p15 lab=aGND
}
C {devices/lab_pin.sym} 1230 -3460 2 0 {name=p20 sig_type=std_logic lab=aGND}
