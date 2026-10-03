v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 550 -220 690 -220 {
lab=D[0:3]}
C {devices/ipin.sym} 320 -410 0 0 {name=p5 lab=Da


}
C {devices/opin.sym} 360 -410 0 0 {name=p17 lab=D[0:3]}
C {devices/ipin.sym} 320 -380 0 0 {name=p8 lab=CLK


}
C {devices/ipin.sym} 320 -350 0 0 {name=p19 lab=nRes


}
C {sky130_stdcells/dfrtp_1.sym} 460 -200 0 0 {name=x1[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 370 -220 0 0 {name=p18 sig_type=std_logic lab=CLK}
C {devices/lab_pin.sym} 370 -180 0 0 {name=p25 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 370 -200 0 0 {name=p26 sig_type=std_logic lab=Da,D[0:2]}
C {devices/lab_pin.sym} 690 -220 2 0 {name=p29 sig_type=std_logic lab=D[0:3]}
C {devices/iopin.sym} 320 -320 0 0 {name=p1 lab=VDD


}
C {devices/iopin.sym} 320 -290 0 0 {name=p2 lab=GND


}
