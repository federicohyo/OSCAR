v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 920 -800 0 0 0.4 0.4 {}
T {synaptic weights} 620 -800 0 0 0.4 0.4 {}
T {store synaptic weight (4 bits)} 590 -335 0 0 0.4 0.4 {}
T {analog synapse current } 1230 -800 0 0 0.4 0.4 {}
T {input spikes} 380 -800 0 0 0.4 0.4 {}
T {analog pulse extender} 630 -565 0 0 0.4 0.4 {}
N 1340 -380 1350 -380 {
lab=sout}
N 570 -360 600 -360 {
lab=#net1}
N 460 -360 490 -360 {
lab=resetW}
N 970 -400 1040 -400 {
lab=#net2}
N 600 -360 660 -360 {
lab=#net1}
N 840 -380 940 -380 {
lab=#net2}
N 940 -400 970 -400 {
lab=#net2}
N 940 -400 940 -380 {
lab=#net2}
C {devices/iopin.sym} 980 -620 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 980 -600 0 0 {name=p4 lab=VDD}
C {devices/ipin.sym} 1050 -660 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 480 -740 0 0 {name=p46 lab=spk

}
C {devices/ipin.sym} 1030 -720 0 0 {name=p47 lab=vthrdpip

}
C {devices/ipin.sym} 1030 -690 0 0 {name=p48 lab=vtaudpin

}
C {devices/ipin.sym} 1030 -750 0 0 {name=p49 lab=vstddpip

}
C {devices/ipin.sym} 720 -675 0 0 {name=p15 lab=W[0:3]

}
C {devices/ipin.sym} 720 -705 0 0 {name=p17 lab=setW

}
C {spike_extender.sym} 750 -490 0 0 {name=x1}
C {devices/lab_pin.sym} 600 -510 0 0 {name=p138 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 600 -490 0 0 {name=p76 sig_type=std_logic lab=spk}
C {devices/lab_pin.sym} 900 -510 2 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 900 -470 2 0 {name=p137 sig_type=std_logic lab=VDD}
C {devices/ipin.sym} 720 -735 0 0 {name=p5 lab=resetW

}
C {devices/lab_pin.sym} 1340 -340 2 0 {name=p44 sig_type=std_logic lab=vtaudpin
}
C {devices/lab_pin.sym} 1340 -360 2 0 {name=p45 sig_type=std_logic lab=vthrdpip}
C {devices/lab_pin.sym} 1340 -400 2 0 {name=p43 sig_type=std_logic lab=vstddpip}
C {devices/lab_pin.sym} 1340 -320 2 0 {name=p29 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1340 -300 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 660 -380 0 0 {name=p7 sig_type=std_logic lab=W[0:3]}
C {devices/iopin.sym} 1310 -750 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1350 -380 2 0 {name=p25 sig_type=std_logic lab=sout}
C {devices/lab_pin.sym} 900 -490 2 0 {name=p26 sig_type=std_logic lab=spke}
C {sky130_stdcells/inv_1.sym} 530 -360 0 0 {name=x11 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 460 -360 0 0 {name=p1 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 660 -400 0 0 {name=p12 sig_type=std_logic lab=setW}
C {dpi_syn_inh_4bit_fc.sym} 1190 -350 0 0 {name=x3}
C {devices/lab_pin.sym} 1040 -380 2 1 {name=p2 sig_type=std_logic lab=spke}
C {sky130_stdcells/dfrbp_1.sym} 750 -380 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
