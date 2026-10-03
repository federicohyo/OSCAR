v {xschem version=3.4.7RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Meas transistor slope factor} 170 -437.5 0 0 0.4 0.4 {}
N 235 -327.5 235 -300 {lab=#net1}
N 375 -327.5 375 -305 {lab=#net2}
N 365 -275 375 -275 {lab=#net2}
N 365 -305 365 -275 {lab=#net2}
N 365 -305 375 -305 {lab=#net2}
N 225 -270 235 -270 {lab=0}
N 225 -270 225 -240 {lab=0}
N 375 -245 375 -220 {lab=0}
N 235 -240 235 -220 {lab=0}
N 225 -240 235 -240 {lab=0}
C {sky130_fd_pr/corner.sym} 10 -140 0 0 {name=CORNER only_toplevel=false corner=tt}
C {sky130_fd_pr/nfet_01v8.sym} 255 -270 0 1 {name=M3
L=1.0
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
C {sky130_fd_pr/pfet_01v8.sym} 395 -275 0 1 {name=M9
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 235 -385 0 0 {name=p30 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 235 -220 0 1 {name=p35 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 375 -220 0 1 {name=p36 sig_type=std_logic lab=0}
C {devices/vsource.sym} 100 -255 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 100 -285 0 0 {name=p87 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 100 -225 0 0 {name=p92 sig_type=std_logic lab=0}
C {devices/vsource.sym} 240 -115 0 0 {name=V2 value=0}
C {devices/lab_pin.sym} 240 -145 0 0 {name=p1 sig_type=std_logic lab=Vgg}
C {devices/lab_pin.sym} 240 -85 0 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 275 -270 0 1 {name=p3 sig_type=std_logic lab=Vgg}
C {devices/lab_pin.sym} 415 -275 0 1 {name=p4 sig_type=std_logic lab=Vgg}
C {devices/code_shown.sym} 320 -165 0 0 {name=SPICE only_toplevel=false value="
.save all
.dc v2 0 1.8 0.001
"}
C {devices/vsource.sym} 235 -355 0 0 {name=V3 value=0}
C {devices/vsource.sym} 375 -355 0 0 {name=V4 value=0}
C {devices/lab_pin.sym} 375 -385 0 0 {name=p5 sig_type=std_logic lab=VDD}
