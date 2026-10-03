v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 350 -330 360 -330 {
lab=A}
N 360 -330 360 -210 {
lab=A}
N 360 -210 370 -210 {
lab=A}
N 360 -280 370 -280 {
lab=A}
N 360 -470 360 -330 {
lab=A}
N 360 -470 370 -470 {
lab=A}
N 360 -390 370 -390 {
lab=A}
N 410 -440 410 -420 {
lab=#net1}
N 410 -430 510 -430 {
lab=#net1}
N 410 -360 410 -310 {
lab=Y}
N 410 -330 590 -330 {
lab=Y}
N 540 -330 540 -290 {
lab=Y}
N 540 -390 540 -330 {
lab=Y}
N 410 -250 510 -250 {
lab=#net2}
N 410 -250 410 -240 {
lab=#net2}
N 410 -180 410 -140 {
lab=GND}
N 570 -250 600 -250 {
lab=VDD}
N 590 -330 600 -330 {
lab=Y}
N 570 -430 600 -430 {
lab=GND}
N 410 -520 410 -500 {
lab=VDD}
N 410 -150 540 -150 {
lab=GND}
N 540 -250 540 -150 {
lab=GND}
N 410 -210 460 -210 {
lab=GND}
N 460 -210 460 -150 {
lab=GND}
N 460 -280 460 -210 {
lab=GND}
N 410 -280 460 -280 {
lab=GND}
N 410 -390 460 -390 {
lab=VDD}
N 460 -510 460 -390 {
lab=VDD}
N 410 -510 460 -510 {
lab=VDD}
N 410 -470 460 -470 {
lab=VDD}
N 460 -510 540 -510 {
lab=VDD}
N 540 -510 540 -430 {
lab=VDD}
C {devices/ipin.sym} 60 -440 0 0 {name=p1 lab=A}
C {devices/opin.sym} 60 -420 0 0 {name=p2 lab=Y}
C {devices/iopin.sym} 60 -400 0 0 {name=p3 lab=VDD}
C {devices/iopin.sym} 60 -380 0 0 {name=p4 lab=GND}
C {devices/lab_wire.sym} 350 -330 0 0 {name=p5 sig_type=std_logic lab=A}
C {devices/lab_wire.sym} 600 -330 0 1 {name=p6 sig_type=std_logic lab=Y}
C {devices/lab_wire.sym} 410 -140 2 0 {name=p7 sig_type=std_logic lab=GND}
C {devices/lab_wire.sym} 600 -430 2 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/lab_wire.sym} 600 -250 2 0 {name=p9 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 410 -520 0 1 {name=p10 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} 390 -210 0 0 {name=M3
W=0.65
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 390 -280 0 0 {name=M1
W=0.65
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 540 -270 1 0 {name=M7
W=0.42
L=0.15
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 390 -470 0 0 {name=M4
W=1
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 390 -390 0 0 {name=M2
W=1
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 540 -410 3 0 {name=M5
W=0.82
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
