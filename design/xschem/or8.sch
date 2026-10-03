v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 240 -250 240 -200 {
lab=#net1}
N 240 -200 250 -200 {
lab=#net1}
N 240 -160 250 -160 {
lab=#net2}
N 240 -160 240 -100 {
lab=#net2}
N 370 -180 390 -180 {
lab=out}
C {sky130_stdcells/or4_1.sym} 180 -250 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/or4_1.sym} 180 -100 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/or2_1.sym} 310 -180 0 0 {name=x3 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 120 -40 0 0 {name=p10 lab=a


}
C {devices/ipin.sym} 120 -80 0 0 {name=p1 lab=b


}
C {devices/ipin.sym} 120 -120 0 0 {name=p5 lab=c


}
C {devices/ipin.sym} 120 -160 0 0 {name=p6 lab=d


}
C {devices/ipin.sym} 120 -190 0 0 {name=p19 lab=e


}
C {devices/ipin.sym} 120 -230 0 0 {name=p26 lab=f


}
C {devices/ipin.sym} 120 -270 0 0 {name=p27 lab=g


}
C {devices/ipin.sym} 120 -310 0 0 {name=p29 lab=h


}
C {devices/opin.sym} 390 -180 0 0 {name=p17 lab=out}
C {devices/iopin.sym} 120 0 0 0 {name=p2 lab=VDD


}
C {devices/iopin.sym} 120 30 0 0 {name=p3 lab=GND


}
