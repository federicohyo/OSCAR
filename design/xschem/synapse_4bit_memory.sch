v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 840 -850 0 0 0.4 0.4 {}
T {synaptic weights} 540 -850 0 0 0.4 0.4 {}
T {store synaptic weight (4 bits)} 530 -375 0 0 0.4 0.4 {}
T {analog synapse current } 1150 -850 0 0 0.4 0.4 {}
T {input spikes} 300 -850 0 0 0.4 0.4 {}
T {analog pulse extender} 550 -615 0 0 0.4 0.4 {}
N 820 -540 940 -540 {
lab=spke}
N 940 -540 950 -540 {
lab=spke}
N 890 -520 890 -460 {
lab=#net1}
N 890 -520 950 -520 {
lab=#net1}
N 820 -450 890 -450 {
lab=#net1}
N 890 -460 890 -450 {
lab=#net1}
N 1250 -520 1260 -520 {
lab=sout}
N 760 -450 820 -450 {
lab=#net1}
N 390 -410 420 -410 {
lab=resetW}
N 500 -410 580 -410 {
lab=#net2}
C {devices/iopin.sym} 900 -670 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 900 -650 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 970 -710 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 400 -790 0 0 {name=p46 lab=spk

}
C {devices/ipin.sym} 950 -770 0 0 {name=p47 lab=vthrdpin

}
C {devices/ipin.sym} 950 -740 0 0 {name=p48 lab=vtaudpip

}
C {devices/ipin.sym} 950 -800 0 0 {name=p49 lab=vstddpin

}
C {devices/ipin.sym} 640 -725 0 0 {name=p15 lab=W[0:3]

}
C {devices/ipin.sym} 640 -755 0 0 {name=p17 lab=setW

}
C {spike_extender.sym} 670 -540 0 0 {name=x1}
C {dpi_syn_exc_4bit_fc.sym} 1100 -490 0 0 {name=x3}
C {devices/lab_pin.sym} 520 -560 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 520 -540 0 0 {name=p76 sig_type=std_logic lab=spk}
C {devices/lab_pin.sym} 820 -560 2 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 820 -520 2 0 {name=p137 sig_type=std_logic lab=VDD}
C {devices/ipin.sym} 640 -785 0 0 {name=p5 lab=resetW

}
C {devices/lab_pin.sym} 1250 -540 2 0 {name=p44 sig_type=std_logic lab=vtaudpip
}
C {devices/lab_pin.sym} 1250 -500 2 0 {name=p45 sig_type=std_logic lab=vthrdpin}
C {devices/lab_pin.sym} 1250 -480 2 0 {name=p43 sig_type=std_logic lab=vstddpin}
C {devices/lab_pin.sym} 1250 -460 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1250 -440 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {sky130_stdcells/dfrtp_1.sym} 670 -430 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 580 -430 0 0 {name=p7 sig_type=std_logic lab=W[0:3]}
C {devices/iopin.sym} 1230 -800 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1260 -520 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 900 -540 1 0 {name=p26 sig_type=std_logic lab=spke}
C {sky130_stdcells/inv_1.sym} 460 -410 0 0 {name=x11 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 390 -410 0 0 {name=p1 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 580 -450 0 0 {name=p12 sig_type=std_logic lab=setW}
