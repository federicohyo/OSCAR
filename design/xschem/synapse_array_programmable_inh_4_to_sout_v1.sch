v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 1060 -1240 0 0 0.4 0.4 {}
T {synaptic weight} 780 -1250 0 0 0.4 0.4 {}
T {analog synapse current } 1350 -1240 0 0 0.4 0.4 {}
N 1230 -950 1360 -950 {
lab=sout}
N 1360 -930 1490 -930 {
lab=sout}
N 1360 -950 1360 -930 {
lab=sout}
N 130 -970 160 -970 {
lab=syn_addr[0:1]}
N 800 -930 810 -930 {
lab=#net1}
N 920 -930 930 -930 {
lab=#net1}
N 800 -850 840 -850 {
lab=#net2}
N 840 -870 840 -850 {
lab=#net2}
N 840 -870 930 -870 {
lab=#net2}
N 810 -930 920 -930 {
lab=#net1}
C {devices/iopin.sym} 1090 -1060 0 0 {name=p3 lab=GND
}
C {devices/ipin.sym} 1160 -1100 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 700 -1180 0 0 {name=p46 lab=syn_addr[0:1]

}
C {devices/ipin.sym} 890 -1190 0 0 {name=p15 lab=W[0:3]

}
C {devices/ipin.sym} 1160 -1190 0 0 {name=p383 lab=JInhWp[0:3]

}
C {devices/iopin.sym} 1430 -1190 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1490 -930 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 1230 -930 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1230 -910 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/ipin.sym} 890 -1130 0 0 {name=p9 lab=setW

}
C {devices/ipin.sym} 890 -1160 0 0 {name=p10 lab=resetW

}
C {devices/lab_pin.sym} 680 -950 0 0 {name=p11 sig_type=std_logic lab=D[0:3]}
C {devices/lab_pin.sym} 930 -830 0 0 {name=p13 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 680 -830 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 930 -910 0 0 {name=p19 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 930 -890 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {sky130_stdcells/and2_1.sym} 740 -930 0 0 {name=x4[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 680 -910 0 0 {name=p23 sig_type=std_logic lab=req_syn}
C {devices/ipin.sym} 700 -1150 0 0 {name=p26 lab=req

}
C {devices/ipin.sym} 1160 -1130 0 0 {name=p6 lab=vtaun

}
C {devices/lab_pin.sym} 930 -950 0 0 {name=p14 sig_type=std_logic lab=JInhWp[0:3]}
C {synapse_4bit_memory_inh_v1.sym} 1080 -880 0 0 {name=x1[0:3]}
C {devices/lab_pin.sym} 130 -970 0 0 {name=p64 sig_type=std_logic lab=syn_addr[0:1]}
C {devices/lab_pin.sym} 460 -930 2 0 {name=p65 sig_type=std_logic lab=D[3:0]}
C {devices/lab_pin.sym} 460 -950 2 0 {name=p66 sig_type=std_logic lab=req_syn}
C {devices/lab_pin.sym} 160 -990 0 0 {name=p67 sig_type=std_logic lab=req}
C {decoder_2_to_4.sym} 310 -960 0 0 {name=x10}
C {devices/iopin.sym} 1090 -1040 0 0 {name=p5 lab=VDD
}
C {devices/lab_pin.sym} 930 -850 0 0 {name=p4 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 930 -810 0 0 {name=p7 sig_type=std_logic lab=vtaun}
C {devices/ipin.sym} 1160 -1160 0 0 {name=p1 lab=vthrdp

}
C {devices/lab_pin.sym} 680 -870 0 0 {name=p2 sig_type=std_logic lab=D[0:3]}
C {sky130_stdcells/and2_1.sym} 740 -850 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 460 -970 2 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 460 -990 2 0 {name=p12 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1230 -890 2 0 {name=p16 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 1090 -1020 0 0 {name=p18 lab=aVDD
}
