v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 920 -820 0 0 0.4 0.4 {}
T {synaptic weights} 620 -820 0 0 0.4 0.4 {}
T {store synaptic weight (4 bits)} 600 -460 0 0 0.4 0.4 {}
T {analog synapse current } 1230 -820 0 0 0.4 0.4 {}
T {input spikes} 380 -820 0 0 0.4 0.4 {}
N 640 -350 660 -350 {
lab=#net1}
N 560 -350 640 -350 {
lab=#net1}
N 450 -350 480 -350 {
lab=resetW}
N 920 -390 1030 -390 {
lab=#net2}
N 840 -370 920 -370 {
lab=#net2}
N 920 -390 920 -370 {
lab=#net2}
C {devices/ipin.sym} 1030 -740 0 0 {name=p40 lab=vpulseextp

}
C {devices/ipin.sym} 480 -760 0 0 {name=p46 lab=spk

}
C {devices/ipin.sym} 1030 -770 0 0 {name=p49 lab=JInhWp[0:3]

}
C {devices/ipin.sym} 720 -700 0 0 {name=p60 lab=W[0:3]

}
C {devices/ipin.sym} 720 -730 0 0 {name=p17 lab=setW

}
C {devices/ipin.sym} 720 -760 0 0 {name=p5 lab=resetW

}
C {devices/lab_pin.sym} 1330 -390 2 0 {name=p44 sig_type=std_logic lab=JInhWp[0:3]
}
C {devices/lab_pin.sym} 660 -370 0 0 {name=p7 sig_type=std_logic lab=W[0:3]}
C {devices/iopin.sym} 1310 -770 0 0 {name=p28 lab=sout
}
C {devices/lab_pin.sym} 1330 -370 2 0 {name=p25 sig_type=std_logic lab=sout}
C {sky130_stdcells/inv_1.sym} 520 -350 0 0 {name=x11 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 450 -350 0 0 {name=p1 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 660 -390 0 0 {name=p12 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1030 -370 0 0 {name=p22 sig_type=std_logic lab=spke}
C {dpi_syn_inh_4bit_fc_v2.sym} 1180 -340 0 0 {name=x2}
C {devices/ipin.sym} 1030 -710 0 0 {name=p2 lab=vthrdp

}
C {devices/ipin.sym} 1030 -690 0 0 {name=p6 lab=vtaun

}
C {devices/lab_pin.sym} 1330 -350 2 0 {name=p9 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 1330 -330 2 0 {name=p10 sig_type=std_logic lab=vtaun}
C {sky130_stdcells/dfrbp_1.sym} 750 -370 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {spike_extender_with_trimming.sym} 680 -520 0 0 {name=x4}
C {devices/lab_pin.sym} 530 -520 0 0 {name=p13 lab=spk}
C {devices/lab_pin.sym} 530 -540 0 0 {name=p14 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 830 -540 2 0 {name=p16 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 830 -500 2 0 {name=p18 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 830 -520 2 0 {name=p19 sig_type=std_logic lab=spke}
C {devices/iopin.sym} 980 -650 0 0 {name=p3 lab=GND
}
C {devices/iopin.sym} 980 -630 0 0 {name=p20 lab=VDD}
C {devices/iopin.sym} 980 -610 0 0 {name=p24 lab=aVDD}
C {devices/lab_pin.sym} 1330 -290 2 0 {name=p30 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1330 -310 2 0 {name=p31 sig_type=std_logic lab=aGND}
C {sky130_stdcells/decap_4.sym} 1090 -520 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/iopin.sym} 980 -590 0 0 {name=p4 lab=aGND}
