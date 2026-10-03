v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 160 -50 160 -20 {
lab=GND}
N 160 -20 190 -20 {
lab=GND}
N 190 -80 190 -20 {
lab=GND}
N 160 -80 190 -80 {
lab=GND}
N 60 -80 120 -80 {
lab=#net1}
N 60 -170 60 -80 {
lab=#net1}
N 60 -170 120 -170 {
lab=#net1}
N 160 -170 190 -170 {
lab=VDD}
N 190 -200 190 -170 {
lab=VDD}
N 160 -200 190 -200 {
lab=VDD}
N 160 -210 160 -200 {
lab=VDD}
N 160 -110 260 -110 {
lab=out}
N 60 -140 160 -140 {
lab=#net1
.IC=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 140 -170 0 0 {name=M4
L=0.15
W=1
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
C {sky130_fd_pr/nfet_01v8.sym} 140 -80 0 0 {name=M2
L=0.15
W=0.65
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
C {devices/iopin.sym} 20 -50 0 0 {name=p34 lab=VDD}
C {devices/iopin.sym} 20 -20 0 0 {name=p35 lab=GND}
C {devices/lab_pin.sym} 160 -210 2 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 190 -30 2 0 {name=p2 sig_type=std_logic lab=GND}
C {devices/opin.sym} 260 -110 0 0 {name=p1 lab=out}
