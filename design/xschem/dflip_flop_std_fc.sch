v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 520 -60 560 -60 {
lab=nQ}
N 70 -60 120 -60 {
lab=D}
N 100 -80 120 -80 {
lab=CLK}
N 330 -60 340 -60 {
lab=sOut}
N 520 -80 560 -80 {
lab=Q}
N 100 -40 120 -40 {
lab=nRes}
N 330 -40 340 -40 {
lab=nRes}
N 300 -80 320 -80 {
lab=sOut}
N 320 -80 320 -60 {
lab=sOut}
N 320 -60 330 -60 {
lab=sOut}
N 330 -80 340 -80 {
lab=sDone}
N 330 -120 330 -80 {
lab=sDone}
N 320 -120 320 -80 {
lab=sOut}
C {devices/ipin.sym} 110 -260 0 0 {name=p3 lab=D


}
C {devices/opin.sym} 160 -250 0 0 {name=p17 lab=Q}
C {devices/ipin.sym} 110 -230 0 0 {name=p4 lab=CLK


}
C {devices/opin.sym} 160 -220 0 0 {name=p5 lab=nQ}
C {devices/lab_wire.sym} 100 -80 0 0 {name=p38 sig_type=std_logic lab=CLK
}
C {devices/lab_wire.sym} 70 -60 0 0 {name=p37 sig_type=std_logic lab=D
}
C {devices/lab_wire.sym} 560 -80 2 0 {name=p9 sig_type=std_logic lab=Q
}
C {devices/lab_wire.sym} 560 -60 2 0 {name=p8 sig_type=std_logic lab=nQ
}
C {sky130_stdcells/dfrtp_1.sym} 210 -60 0 0 {name=x5 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_wire.sym} 330 -120 1 0 {name=p1 sig_type=std_logic lab=sDone
}
C {devices/ipin.sym} 110 -200 0 0 {name=p2 lab=nRes


}
C {devices/lab_wire.sym} 100 -40 0 0 {name=p6 sig_type=std_logic lab=nRes}
C {devices/lab_wire.sym} 330 -40 0 0 {name=p7 sig_type=std_logic lab=nRes}
C {sky130_stdcells/dfrbp_2.sym} 430 -60 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/opin.sym} 160 -170 0 0 {name=p11 lab=sOut}
C {devices/lab_wire.sym} 320 -120 0 0 {name=p12 sig_type=std_logic lab=sOut

}
C {devices/ipin.sym} 110 -170 0 0 {name=p10 lab=sDone

}
C {devices/iopin.sym} 110 -140 0 0 {name=p13 lab=VDD

}
C {devices/iopin.sym} 110 -110 0 0 {name=p14 lab=GND

}
