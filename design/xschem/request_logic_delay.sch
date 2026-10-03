v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 340 -220 380 -220 {
lab=req}
N 340 -260 380 -260 {
lab=A[0:15]}
C {devices/ipin.sym} 105 -130 0 0 {name=p17 lab=A[0:15]


}
C {devices/ipin.sym} 105 -105 0 0 {name=p19 lab=req


}
C {devices/opin.sym} 155 -130 0 0 {name=p21 lab=O[0:15]}
C {sky130_stdcells/and2_1.sym} 440 -240 0 0 {name=x1[0:15] VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 500 -240 2 0 {name=p49 sig_type=std_logic lab=O[0:15]}
C {devices/lab_pin.sym} 340 -220 0 0 {name=p50 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 340 -260 0 0 {name=p51 sig_type=std_logic lab=A[0:15]}
C {devices/iopin.sym} 105 -75 0 0 {name=p1 lab=dVDD


}
C {devices/iopin.sym} 105 -45 0 0 {name=p2 lab=dGND


}
