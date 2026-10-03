v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 800 -860 0 0 0.4 0.4 {}
T {synaptic weights} 500 -860 0 0 0.4 0.4 {}
T {store synaptic weight (4 bits)} 610 -350 0 0 0.4 0.4 {}
T {analog synapse current } 1110 -860 0 0 0.4 0.4 {}
T {input spikes} 260 -860 0 0 0.4 0.4 {}
N 600 -380 690 -380 {
lab=#net1}
N 490 -380 520 -380 {
lab=resetW}
N 1000 -540 1000 -440 {
lab=spke}
N 870 -420 1000 -420 {
lab=#net2}
N 890 -540 1000 -540 {
lab=spke}
C {devices/iopin.sym} 860 -660 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 860 -680 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 940 -780 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 360 -800 0 0 {name=p46 lab=spk

}
C {devices/ipin.sym} 600 -760 0 0 {name=p17 lab=setW

}
C {devices/ipin.sym} 600 -790 0 0 {name=p5 lab=resetW

}
C {devices/lab_pin.sym} 1300 -340 2 0 {name=p37 sig_type=std_logic lab=aVDD}
C {sky130_stdcells/dfrtp_1.sym} 780 -400 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 690 -400 0 0 {name=p7 sig_type=std_logic lab=W[0:3]}
C {devices/iopin.sym} 1190 -810 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1300 -420 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 1000 -500 2 0 {name=p26 sig_type=std_logic lab=spke}
C {sky130_stdcells/inv_1.sym} 560 -380 0 0 {name=x4 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 490 -380 0 0 {name=p1 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 690 -420 0 0 {name=p12 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1300 -380 2 0 {name=p19 sig_type=std_logic lab=JExcWn[0:3]
}
C {devices/lab_pin.sym} 1000 -440 0 0 {name=p20 sig_type=std_logic lab=spke}
C {devices/ipin.sym} 940 -750 0 0 {name=p6 lab=vthrdn

}
C {devices/ipin.sym} 940 -730 0 0 {name=p9 lab=vtaup

}
C {devices/lab_pin.sym} 1300 -440 2 0 {name=p10 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1300 -400 2 0 {name=p11 sig_type=std_logic lab=vthrdn}
C {dpi_syn_exc_4bit_fc_v2.sym} 1150 -390 0 0 {name=x2}
C {spike_extender_with_trimming.sym} 740 -540 0 0 {name=x6}
C {devices/lab_pin.sym} 590 -560 0 0 {name=p13 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 590 -540 0 0 {name=p14 lab=spk}
C {devices/lab_pin.sym} 890 -560 2 0 {name=p16 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 890 -520 2 0 {name=p18 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 860 -640 0 0 {name=p2 lab=aVDD
}
C {devices/ipin.sym} 940 -810 0 0 {name=p48 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 600 -730 0 0 {name=p60 lab=W[0:3]

}
C {devices/lab_pin.sym} 1300 -360 2 0 {name=p8 sig_type=std_logic lab=aGND}
C {sky130_stdcells/decap_4.sym} 1210 -630 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/decap_3.sym} 1220 -750 0 0 {name=x3 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/decap_3.sym} 1210 -700 0 0 {name=x5 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/decap_6.sym} 1230 -540 0 0 {name=x7 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/decap_3.sym} 1060 -760 0 0 {name=x8 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/decap_3.sym} 1050 -710 0 0 {name=x9 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/iopin.sym} 860 -620 0 0 {name=p15 lab=aGND
}
