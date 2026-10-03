v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 250 -300 320 -300 {
lab=#net1}
N 320 -300 320 -290 {
lab=#net1}
N 320 -50 320 -20 {
lab=ST}
N 110 -20 320 -20 {
lab=ST}
N 110 -300 110 -20 {
lab=ST}
N 110 -300 170 -300 {
lab=ST}
N 40 -300 110 -300 {
lab=ST}
N 320 -60 320 -50 {
lab=ST}
N 260 -100 290 -100 {
lab=IN}
N 260 -250 260 -100 {
lab=IN}
N 260 -250 290 -250 {
lab=IN}
N 350 -250 370 -250 {
lab=OUT}
N 370 -250 370 -100 {
lab=OUT}
N 360 -100 370 -100 {
lab=OUT}
N 350 -100 360 -100 {
lab=OUT}
N 120 -180 260 -180 {
lab=IN}
N 120 -190 120 -180 {
lab=IN}
N 90 -190 120 -190 {
lab=IN}
N 90 -190 90 -180 {
lab=IN}
N 40 -180 90 -180 {
lab=IN}
N 370 -180 430 -180 {
lab=OUT}
C {sky130_stdcells/inv_1.sym} 210 -300 0 0 {name=x13 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_fd_pr/pfet_01v8.sym} 320 -270 1 0 {name=M19
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
C {sky130_fd_pr/nfet_01v8.sym} 320 -80 3 0 {name=M2
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
C {devices/lab_pin.sym} 320 -250 3 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 320 -100 1 0 {name=p1 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 10 -50 0 0 {name=p13 lab=GND
}
C {devices/iopin.sym} 10 -30 0 0 {name=p16 lab=VDD}
C {devices/ipin.sym} 40 -300 0 0 {name=p10 lab=ST
}
C {devices/ipin.sym} 40 -180 0 0 {name=p2 lab=IN
}
C {devices/opin.sym} 430 -180 0 0 {name=p17 lab=OUT}
