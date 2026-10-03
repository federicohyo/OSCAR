v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 940 -3960 0 0 0.4 0.4 {}
T {synaptic weight} 660 -3970 0 0 0.4 0.4 {}
T {analog synapse current } 1230 -3960 0 0 0.4 0.4 {}
T {decoder (MSB XXX LSB)} 70 -3810 0 0 0.4 0.4 {}
N -10 -3730 20 -3730 {
lab=req}
N 320 -3730 350 -3730 {
lab=req_syn}
N 320 -3750 350 -3750 {
lab=D[0:15]}
N 680 -3630 810 -3630 {
lab=#net1}
N 690 -3590 810 -3590 {
lab=#net2}
N 670 -3550 690 -3550 {
lab=#net2}
N 690 -3590 690 -3550 {
lab=#net2}
C {devices/ipin.sym} 1040 -3880 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 580 -3900 0 0 {name=p60 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 770 -3910 0 0 {name=p80 lab=W[0:3]

}
C {devices/ipin.sym} 1040 -3910 0 0 {name=p90 lab=JInhWp[0:3]

}
C {devices/iopin.sym} 1310 -3910 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1110 -3670 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/ipin.sym} 770 -3850 0 0 {name=p9 lab=setW

}
C {devices/ipin.sym} 770 -3880 0 0 {name=p10 lab=resetW

}
C {decoder_4_to_16.sym} 170 -3720 0 0 {name=x3}
C {devices/lab_pin.sym} 20 -3750 0 0 {name=p5 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 350 -3750 2 0 {name=p18 sig_type=std_logic lab=D[0:15]}
C {devices/lab_pin.sym} 560 -3650 0 0 {name=p11 sig_type=std_logic lab=D[0:15]}
C {devices/lab_pin.sym} 810 -3550 0 0 {name=p13 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 550 -3530 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 810 -3650 0 0 {name=p19 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 810 -3610 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {sky130_stdcells/and2_1.sym} 620 -3630 2 1 {name=x2[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 350 -3730 2 0 {name=p22 sig_type=std_logic lab=req_syn}
C {devices/lab_pin.sym} 560 -3610 0 0 {name=p23 sig_type=std_logic lab=req_syn}
C {devices/ipin.sym} 580 -3870 0 0 {name=p26 lab=req

}
C {devices/lab_pin.sym} -10 -3730 0 0 {name=p27 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 810 -3670 0 0 {name=p7 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/ipin.sym} 1030 -3860 0 0 {name=p1 lab=vthrdp

}
C {devices/ipin.sym} 1030 -3840 0 0 {name=p2 lab=vtaun

}
C {devices/lab_pin.sym} 810 -3570 0 0 {name=p4 sig_type=std_logic lab=vthrdp
}
C {devices/lab_pin.sym} 810 -3530 0 0 {name=p6 sig_type=std_logic lab=vtaun
}
C {devices/lab_pin.sym} 550 -3570 0 0 {name=p8 sig_type=std_logic lab=D[0:15]}
C {sky130_stdcells/and2_1.sym} 610 -3550 0 0 {name=x3[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 320 -3690 2 0 {name=p12 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 320 -3710 2 0 {name=p14 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 910 -3800 0 0 {name=p16 lab=GND
}
C {devices/iopin.sym} 910 -3780 0 0 {name=p20 lab=VDD}
C {devices/iopin.sym} 910 -3740 0 0 {name=p24 lab=aVDD}
C {devices/lab_pin.sym} 1110 -3650 2 0 {name=p3 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1110 -3610 2 0 {name=p30 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1110 -3630 2 0 {name=p32 sig_type=std_logic lab=VDD}
C {synapse_4bit_memory_inh_v1_norail.sym} 960 -3600 0 0 {name=x1[0:15]}
C {devices/iopin.sym} 910 -3710 0 0 {name=p15 lab=aGND}
C {devices/lab_pin.sym} 1110 -3590 2 0 {name=p21 sig_type=std_logic lab=aGND}
