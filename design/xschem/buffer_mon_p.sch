v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 190 -145 190 -95 {
lab=out}
N 320 -145 320 -95 {
lab=#net1}
N 230 -65 280 -65 {
lab=#net1}
N 190 -35 190 -20 {
lab=GND}
N 190 -20 320 -20 {
lab=GND}
N 320 -35 320 -20 {
lab=GND}
N 185 -175 320 -175 {
lab=AVDD}
N 190 -250 190 -205 {
lab=#net2}
N 190 -250 245 -250 {
lab=#net2}
N 245 -250 320 -250 {
lab=#net2}
N 320 -250 320 -205 {
lab=#net2}
N 285 -280 325 -280 {
lab=buf_p}
N 215 -280 250 -280 {
lab=AVDD}
N 230 -310 245 -310 {
lab=AVDD}
N 230 -310 230 -280 {
lab=AVDD}
N 125 -175 150 -175 {
lab=out}
N 360 -175 380 -175 {
lab=mon}
N 165 -65 190 -65 {
lab=GND}
N 165 -65 165 -35 {
lab=GND}
N 165 -35 190 -35 {
lab=GND}
N 320 -35 345 -35 {
lab=GND}
N 345 -65 345 -35 {
lab=GND}
N 320 -65 345 -65 {
lab=GND}
N 135 -175 135 -125 {
lab=out}
N 135 -125 190 -125 {
lab=out}
N 265 -105 265 -65 {
lab=#net1}
N 265 -105 320 -105 {
lab=#net1}
C {sky130_fd_pr/pfet_01v8.sym} 170 -175 0 0 {name=M1
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
C {sky130_fd_pr/pfet_01v8.sym} 340 -175 0 1 {name=M5
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
C {sky130_fd_pr/pfet_01v8.sym} 265 -280 0 1 {name=M2
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
C {sky130_fd_pr/nfet_01v8.sym} 210 -65 0 1 {name=M3
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
C {sky130_fd_pr/nfet_01v8.sym} 300 -65 0 0 {name=M4
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
C {devices/iopin.sym} 10 -40 0 0 {name=p13 lab=GND
}
C {devices/iopin.sym} 10 -20 0 0 {name=p16 lab=AVDD}
C {devices/lab_wire.sym} 320 -20 2 0 {name=p2 sig_type=std_logic lab=GND
}
C {devices/lab_wire.sym} 245 -175 2 0 {name=p1 sig_type=std_logic lab=AVDD
}
C {devices/ipin.sym} 325 -280 2 0 {name=p10 lab=buf_p

}
C {devices/lab_wire.sym} 215 -280 0 0 {name=p3 sig_type=std_logic lab=AVDD
}
C {devices/ipin.sym} 380 -175 0 1 {name=p4 lab=mon


}
C {devices/opin.sym} 125 -175 2 0 {name=p17 lab=out}
