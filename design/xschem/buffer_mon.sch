v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 465 -265 465 -225 {
lab=#net1}
N 385 -225 465 -225 {
lab=#net1}
N 315 -225 385 -225 {
lab=#net1}
N 305 -355 305 -325 {
lab=#net2}
N 305 -265 305 -225 {
lab=#net1}
N 305 -225 315 -225 {
lab=#net1}
N 305 -295 465 -295 {
lab=AGND}
N 215 -295 265 -295 {
lab=mon}
N 385 -165 385 -115 {
lab=AGND}
N 345 -195 385 -195 {
lab=AGND}
N 345 -195 345 -145 {
lab=AGND}
N 345 -145 385 -145 {
lab=AGND}
N 465 -355 465 -325 {
lab=out}
N 305 -415 465 -415 {
lab=AVDD}
N 385 -445 385 -415 {
lab=AVDD}
N 505 -295 605 -295 {
lab=out}
N 265 -385 310 -385 {
lab=AVDD}
N 265 -435 265 -385 {
lab=AVDD}
N 265 -435 305 -435 {
lab=AVDD}
N 305 -435 305 -415 {
lab=AVDD}
N 460 -385 500 -385 {
lab=AVDD}
N 500 -430 500 -385 {
lab=AVDD}
N 450 -430 500 -430 {
lab=AVDD}
N 450 -430 450 -415 {
lab=AVDD}
N 345 -385 425 -385 {
lab=#net2}
N 305 -340 365 -340 {
lab=#net2}
N 365 -385 365 -340 {
lab=#net2}
N 465 -335 555 -335 {
lab=out}
N 555 -335 555 -295 {
lab=out}
C {devices/iopin.sym} 140 -115 0 0 {name=p13 lab=AGND
}
C {devices/iopin.sym} 140 -95 0 0 {name=p16 lab=AVDD}
C {devices/lab_wire.sym} 385 -295 2 0 {name=p2 sig_type=std_logic lab=AGND
}
C {devices/ipin.sym} 425 -195 2 0 {name=p10 lab=buf_n

}
C {devices/ipin.sym} 215 -295 0 0 {name=p4 lab=mon


}
C {devices/opin.sym} 605 -295 2 1 {name=p17 lab=out}
C {sky130_fd_pr/pfet_01v8.sym} 325 -385 0 1 {name=M1
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
C {sky130_fd_pr/pfet_01v8.sym} 445 -385 0 0 {name=M5
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
C {devices/lab_wire.sym} 385 -445 2 0 {name=p5 sig_type=std_logic lab=AVDD
}
C {sky130_fd_pr/nfet_01v8.sym} 405 -195 0 1 {name=M4
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
C {devices/lab_wire.sym} 385 -115 0 1 {name=p1 sig_type=std_logic lab=AGND
}
C {sky130_fd_pr/nfet_01v8.sym} 285 -295 0 0 {name=M2
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
C {sky130_fd_pr/nfet_01v8.sym} 485 -295 0 1 {name=M3
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
