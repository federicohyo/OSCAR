v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 190 -165 190 -115 {
lab=out}
N 320 -165 320 -115 {
lab=#net1}
N 230 -85 280 -85 {
lab=#net1}
N 190 -55 190 -40 {
lab=GND}
N 190 -40 320 -40 {
lab=GND}
N 320 -55 320 -40 {
lab=GND}
N 185 -195 320 -195 {
lab=AVDD}
N 190 -270 190 -225 {
lab=#net2}
N 190 -270 245 -270 {
lab=#net2}
N 245 -270 320 -270 {
lab=#net2}
N 320 -270 320 -225 {
lab=#net2}
N 285 -300 325 -300 {
lab=buf_p}
N 215 -300 250 -300 {
lab=AVDD}
N 230 -330 245 -330 {
lab=AVDD}
N 230 -330 230 -300 {
lab=AVDD}
N 125 -195 150 -195 {
lab=out}
N 360 -195 380 -195 {
lab=mon}
N 165 -85 190 -85 {
lab=GND}
N 165 -85 165 -55 {
lab=GND}
N 165 -55 190 -55 {
lab=GND}
N 320 -55 345 -55 {
lab=GND}
N 345 -85 345 -55 {
lab=GND}
N 320 -85 345 -85 {
lab=GND}
N 135 -195 135 -145 {
lab=out}
N 135 -145 190 -145 {
lab=out}
N 265 -125 265 -85 {
lab=#net1}
N 265 -125 320 -125 {
lab=#net1}
C {sky130_fd_pr/pfet_01v8.sym} 170 -195 0 0 {name=M1
L=0.5
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
C {sky130_fd_pr/pfet_01v8.sym} 340 -195 0 1 {name=M5
L=0.5
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
C {sky130_fd_pr/pfet_01v8.sym} 265 -300 0 1 {name=M2
L=0.30
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
C {sky130_fd_pr/nfet_01v8.sym} 210 -85 0 1 {name=M3
L=0.5
W=1.0
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
C {sky130_fd_pr/nfet_01v8.sym} 300 -85 0 0 {name=M4
L=0.5
W=1.0
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
C {devices/iopin.sym} 10 -60 0 0 {name=p13 lab=GND
}
C {devices/iopin.sym} 10 -40 0 0 {name=p16 lab=AVDD}
C {devices/lab_wire.sym} 320 -40 2 0 {name=p2 sig_type=std_logic lab=GND
}
C {devices/lab_wire.sym} 245 -195 2 0 {name=p1 sig_type=std_logic lab=AVDD
}
C {devices/ipin.sym} 325 -300 2 0 {name=p10 lab=buf_p

}
C {devices/lab_wire.sym} 215 -300 0 0 {name=p3 sig_type=std_logic lab=AVDD
}
C {devices/ipin.sym} 380 -195 0 1 {name=p4 lab=mon


}
C {devices/opin.sym} 125 -195 2 0 {name=p17 lab=out}
