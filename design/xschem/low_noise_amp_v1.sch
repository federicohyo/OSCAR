v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 500 -390 690 -390 {
lab=vdd}
N 500 -440 500 -420 {
lab=vpn}
N 500 -440 610 -440 {
lab=vpn}
N 610 -440 690 -440 {
lab=vpn}
N 690 -440 690 -420 {
lab=vpn}
N 500 -360 500 -170 {
lab=lab0}
N 690 -360 690 -170 {
lab=lab2}
N 180 -70 200 -70 {
lab=vss}
N 200 -110 200 -70 {
lab=vss}
N 200 -70 500 -70 {
lab=vss}
N 500 -110 500 -70 {
lab=vss}
N 500 -140 690 -140 {
lab=vss}
N 620 -140 620 -70 {
lab=vss}
N 500 -70 620 -70 {
lab=vss}
N 620 -70 690 -70 {
lab=vss}
N 690 -110 690 -70 {
lab=vss}
N 980 -110 980 -70 {
lab=vss}
N 690 -70 980 -70 {
lab=vss}
N 730 -140 940 -140 {
lab=lab2}
N 240 -140 460 -140 {
lab=lab0}
N 430 -200 430 -140 {
lab=lab0}
N 430 -200 500 -200 {
lab=lab0}
N 690 -200 760 -200 {
lab=lab2}
N 760 -200 760 -140 {
lab=lab2}
N 200 -540 200 -170 {
lab=lab1}
N 980 -540 980 -170 {
lab=vout}
N 240 -570 940 -570 {
lab=lab1}
N 200 -530 260 -530 {
lab=lab1}
N 260 -570 260 -530 {
lab=lab1}
N 190 -630 200 -630 {
lab=vdd}
N 200 -630 200 -600 {
lab=vdd}
N 180 -570 200 -570 {
lab=vdd}
N 180 -610 180 -570 {
lab=vdd}
N 180 -610 200 -610 {
lab=vdd}
N 980 -570 1010 -570 {
lab=vdd}
N 1010 -620 1010 -570 {
lab=vdd}
N 980 -620 1010 -620 {
lab=vdd}
N 980 -620 980 -600 {
lab=vdd}
N 980 -350 1100 -350 {
lab=vout}
N 170 -140 200 -140 {
lab=vss}
N 170 -140 170 -90 {
lab=vss}
N 170 -90 200 -90 {
lab=vss}
N 980 -140 990 -140 {
lab=vss}
N 990 -140 990 -90 {
lab=vss}
N 980 -90 990 -90 {
lab=vss}
N 610 -500 630 -500 {
lab=vdd}
N 630 -500 630 -470 {
lab=vdd}
N 610 -470 630 -470 {
lab=vdd}
C {devices/ipin.sym} 570 -470 0 0 {name=p1 lab=iref}
C {devices/ipin.sym} 460 -390 0 0 {name=p2 lab=vin_p}
C {devices/ipin.sym} 730 -390 0 1 {name=p3 lab=vin_n}
C {devices/lab_wire.sym} 600 -390 0 0 {name=p4 sig_type=std_logic lab=vdd}
C {devices/iopin.sym} 190 -630 2 0 {name=p5 lab=vdd}
C {devices/iopin.sym} 180 -70 0 1 {name=p6 lab=vss}
C {devices/opin.sym} 1100 -350 0 0 {name=p7 lab=vout}
C {sky130_fd_pr/nfet_01v8.sym} 480 -140 0 0 {name=M1
L=8
W=2
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=nfet_01v8
spiceprefix=X

}
C {sky130_fd_pr/pfet_01v8.sym} 480 -390 0 0 {name=M2
L=2
W=4
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 710 -390 0 1 {name=M3
L=2
W=4
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 590 -470 0 0 {name=M4
L=4
W=5
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 710 -140 0 1 {name=M5
L=8
W=2
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=nfet_01v8
spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 220 -140 0 1 {name=M6
L=4
W=0.8
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=nfet_01v8
spiceprefix=X}
C {sky130_fd_pr/nfet_01v8.sym} 960 -140 0 0 {name=M7
L=4
W=0.8
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=nfet_01v8
spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 220 -570 0 1 {name=M8
L=4
W=1.4
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 960 -570 0 0 {name=M9
L=4
W=1.4
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_wire.sym} 980 -620 0 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/lab_wire.sym} 610 -500 0 0 {name=p9 sig_type=std_logic lab=vdd}
C {devices/lab_wire.sym} 500 -440 0 0 {name=p10 sig_type=std_logic lab=vpn}
C {devices/lab_wire.sym} 430 -200 0 0 {name=p11 sig_type=std_logic lab=lab0}
C {devices/lab_wire.sym} 260 -530 0 0 {name=p12 sig_type=std_logic lab=lab1}
C {devices/lab_wire.sym} 760 -200 0 0 {name=p13 sig_type=std_logic lab=lab2}
