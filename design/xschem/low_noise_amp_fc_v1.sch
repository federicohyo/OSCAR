v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 505 -162.5 505 -87.5 { lab=vss}
N 785 -162.5 785 -87.5 { lab=vss}
N 505 -87.5 572.5 -87.5 { lab=vss}
N 572.5 -87.5 785 -87.5 { lab=vss}
N 585 -262.5 585 -192.5 { lab=vbn}
N 425 -192.5 505 -192.5 { lab=vss}
N 425 -192.5 425 -87.5 { lab=vss}
N 425 -87.5 505 -87.5 { lab=vss}
N 785 -192.5 852.5 -192.5 { lab=vss}
N 852.5 -192.5 852.5 -87.5 { lab=vss}
N 785 -367.5 785 -222.5 { lab=voe1}
N 505 -487.5 505 -427.5 { lab=vp}
N 505 -487.5 785 -487.5 { lab=vp}
N 785 -487.5 785 -427.5 { lab=vp}
N 502.5 -397.5 565 -397.5 { lab=vp}
N 565 -487.5 565 -397.5 { lab=vp}
N 722.5 -487.5 722.5 -397.5 { lab=vp}
N 645 -537.5 645 -487.5 { lab=vp}
N 1105 -600 1105 -597.5 { lab=vdd}
N 1105 -627.5 1105 -600 { lab=vdd}
N 645 -627.5 1105 -627.5 { lab=vdd}
N 645 -627.5 645 -597.5 { lab=vdd}
N 1102.5 -567.5 1182.5 -567.5 { lab=vdd}
N 1182.5 -627.5 1182.5 -567.5 { lab=vdd}
N 1105 -627.5 1182.5 -627.5 { lab=vdd}
N 265 -627.5 265 -597.5 { lab=vdd}
N 265 -627.5 645 -627.5 { lab=vdd}
N 265 -487.5 367.5 -487.5 { lab=iref}
N 367.5 -567.5 367.5 -487.5 { lab=iref}
N 982.5 -567.5 1065 -567.5 { lab=iref}
N 185 -567.5 267.5 -567.5 { lab=vdd}
N 185 -627.5 185 -567.5 { lab=vdd}
N 185 -627.5 265 -627.5 { lab=vdd}
N 645 -567.5 725 -567.5 { lab=vdd}
N 725 -627.5 725 -567.5 { lab=vdd}
N 585 -265 585 -262.5 { lab=vbn}
N 722.5 -397.5 787.5 -397.5 { lab=vp}
N 505 -367.5 505 -222.5 { lab=vbn}
N 505 -265 585 -265 { lab=vbn}
N 305 -567.5 367.5 -567.5 { lab=iref}
N 490 -567.5 605 -567.5 { lab=iref}
N 367.5 -567.5 490 -567.5 { lab=iref}
N 545 -192.5 745 -192.5 { lab=vbn}
N 265 -537.5 265 -487.5 { lab=iref}
N 395 -397.5 465 -397.5 { lab=vin_n}
N 785 -317.5 905 -317.5 { lab=voe1}
N 1075 -317.5 1105 -317.5 { lab=vout}
N 165 -627.5 185 -627.5 { lab=vdd}
N 165 -87.5 425 -87.5 { lab=vss}
N 825 -397.5 885 -397.5 { lab=vin_p}
N 165 -487.5 265 -487.5 { lab=iref}
N 785 -87.5 1105 -87.5 { lab=vss}
N 1105 -87.5 1195 -87.5 { lab=vss}
N 1195 -187.5 1195 -87.5 { lab=vss}
N 1105 -187.5 1195 -187.5 { lab=vss}
N 885 -187.5 1065 -187.5 { lab=voe1}
N 1105 -317.5 1105 -217.5 { lab=vout}
N 1105 -537.5 1105 -317.5 { lab=vout}
N 1105 -367.5 1245 -367.5 { lab=vout}
N 1105 -157.5 1105 -87.5 { lab=vss}
N 965 -317.5 1015 -317.5 { lab=#net1}
N 935 -377.5 935 -357.5 { lab=vdd}
N 935 -317.5 935 -237.5 { lab=vss}
N 885 -247.5 885 -187.5 {
lab=voe1}
N 885 -317.5 885 -247.5 {
lab=voe1}
C {sky130_fd_pr/pfet_01v8.sym} 485 -397.5 0 0 {name=M1
L=4
W=16
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=500
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 805 -397.5 0 1 {name=M2
L=4
W=16
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=500
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 525 -192.5 0 1 {name=M3
L=2
W=4
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 765 -192.5 0 0 {name=M4
L=2
W=4
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 625 -567.5 0 0 {name=M5
L=4
W=8
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1085 -567.5 0 0 {name=M7
L=4
W=8
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 285 -567.5 0 1 {name=M8
L=4
W=8
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_wire.sym} 487.5 -627.5 0 0 {name=p7 sig_type=std_logic lab=vdd
}
C {devices/lab_wire.sym} 490 -567.5 0 0 {name=p9 sig_type=std_logic lab=iref

}
C {devices/lab_wire.sym} 620 -487.5 0 0 {name=p12 sig_type=std_logic lab=vp}
C {devices/lab_pin.sym} 982.5 -567.5 0 0 {name=p8 sig_type=std_logic lab=iref}
C {devices/lab_wire.sym} 657.5 -87.5 0 0 {name=p16 sig_type=std_logic lab=vss
}
C {devices/lab_wire.sym} 1192.5 -367.5 0 0 {name=p10 sig_type=std_logic lab=vout
}
C {devices/lab_wire.sym} 665 -192.5 0 0 {name=p15 sig_type=std_logic lab=vbn}
C {devices/iopin.sym} 165 -627.5 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} 165 -87.5 2 0 {name=p2 lab=vss}
C {devices/ipin.sym} 395 -397.5 0 0 {name=p3 lab=vin_n}
C {devices/ipin.sym} 885 -397.5 2 0 {name=p4 lab=vin_p}
C {devices/ipin.sym} 165 -487.5 0 0 {name=p5 lab=iref}
C {sky130_fd_pr/nfet_01v8.sym} 1085 -187.5 0 0 {name=M6
L=4
W=8
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=nfet_01v8
spiceprefix=X
}
C {devices/lab_wire.sym} 845 -317.5 0 0 {name=p13 sig_type=std_logic lab=voe1}
C {devices/opin.sym} 1245 -367.5 0 0 {name=p6 lab=vout}
C {sky130_fd_pr/nfet_01v8.sym} 935 -337.5 1 0 {name=M9
L=0.15
W=0.75
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=10
model=nfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 935 -377.5 2 0 {name=p14 sig_type=std_logic lab=vdd
}
C {devices/lab_pin.sym} 935 -237.5 2 0 {name=p11 sig_type=std_logic lab=vss
}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1045 -317.5 1 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=6 spiceprefix=X}
