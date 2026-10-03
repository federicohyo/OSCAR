v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 160 -70 160 -40 {
lab=GND}
N 160 -40 190 -40 {
lab=GND}
N 190 -100 190 -40 {
lab=GND}
N 160 -100 190 -100 {
lab=GND}
N 60 -100 120 -100 {
lab=#net1}
N 60 -190 60 -100 {
lab=#net1}
N 60 -190 120 -190 {
lab=#net1}
N 60 -130 160 -130 {
lab=#net1
.IC=0}
N 160 -160 250 -160 {
lab=out}
N 160 -190 190 -190 {
lab=VDD}
N 190 -220 190 -190 {
lab=VDD}
N 160 -220 190 -220 {
lab=VDD}
N 160 -230 160 -220 {
lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 140 -190 0 0 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} 140 -100 0 0 {name=M2
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
C {devices/iopin.sym} 20 -70 0 0 {name=p34 lab=VDD}
C {devices/iopin.sym} 20 -40 0 0 {name=p35 lab=GND}
C {devices/lab_pin.sym} 160 -230 2 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 190 -50 2 0 {name=p2 sig_type=std_logic lab=GND}
C {devices/opin.sym} 250 -160 0 0 {name=p1 lab=out}
