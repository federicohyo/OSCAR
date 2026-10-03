v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 330 -200 370 -200 {
lab=req}
N 330 -240 370 -240 {
lab=A[0:3]}
C {devices/ipin.sym} 85 -250 0 0 {name=p17 lab=A[0:3]


}
C {devices/ipin.sym} 85 -225 0 0 {name=p19 lab=req


}
C {devices/opin.sym} 135 -250 0 0 {name=p21 lab=O[0:3]}
C {sky130_stdcells/and2_1.sym} 430 -220 0 0 {name=x1[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 490 -220 2 0 {name=p49 sig_type=std_logic lab=O[0:3]}
C {devices/lab_pin.sym} 330 -200 0 0 {name=p50 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 330 -240 0 0 {name=p51 sig_type=std_logic lab=A[0:3]}
C {devices/iopin.sym} 85 -195 0 0 {name=p1 lab=VDD


}
C {devices/iopin.sym} 85 -165 0 0 {name=p2 lab=GND


}
