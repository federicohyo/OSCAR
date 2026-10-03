v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 120 -160 120 -130 {
lab=GND}
N 120 -190 150 -190 {
lab=GND}
N 150 -190 150 -150 {
lab=GND}
N 120 -150 150 -150 {
lab=GND}
N 120 -240 120 -220 {
lab=#net1}
N 60 -190 80 -190 {
lab=spk}
N 120 -350 160 -350 {
lab=VDD}
N 160 -400 160 -350 {
lab=VDD}
N 120 -400 160 -400 {
lab=VDD}
N 120 -430 120 -380 {
lab=VDD}
N 120 -320 120 -240 {
lab=#net1
.IC=1.8V}
N 40 -350 80 -350 {
lab=vpulseextp}
N 450 -270 450 -210 {
lab=#net2}
N 490 -310 490 -300 {
lab=VDD}
N 490 -340 490 -310 {
lab=VDD}
N 490 -180 490 -140 {
lab=GND}
N 490 -210 520 -210 {
lab=GND}
N 520 -210 520 -170 {
lab=GND}
N 490 -170 520 -170 {
lab=GND}
N 490 -270 510 -270 {
lab=VDD}
N 510 -310 510 -270 {
lab=VDD}
N 490 -310 510 -310 {
lab=VDD}
N 550 -270 550 -210 {
lab=#net3}
N 590 -310 590 -300 {
lab=VDD}
N 590 -340 590 -310 {
lab=VDD}
N 590 -180 590 -140 {
lab=GND}
N 590 -210 620 -210 {
lab=GND}
N 620 -210 620 -170 {
lab=GND}
N 590 -170 620 -170 {
lab=GND}
N 590 -270 610 -270 {
lab=VDD}
N 610 -310 610 -270 {
lab=VDD}
N 590 -310 610 -310 {
lab=VDD}
N 590 -240 670 -240 {
lab=spkext}
N 490 -240 550 -240 {
lab=#net3}
N 420 -240 450 -240 {
lab=#net2}
N 352.5 -270 352.5 -210 {
lab=#net1}
N 392.5 -310 392.5 -300 {
lab=VDD}
N 392.5 -340 392.5 -310 {
lab=VDD}
N 392.5 -180 392.5 -140 {
lab=GND}
N 392.5 -210 422.5 -210 {
lab=GND}
N 422.5 -210 422.5 -170 {
lab=GND}
N 392.5 -170 422.5 -170 {
lab=GND}
N 392.5 -270 412.5 -270 {
lab=VDD}
N 412.5 -310 412.5 -270 {
lab=VDD}
N 392.5 -310 412.5 -310 {
lab=VDD}
N 392.5 -240 420 -240 {
lab=#net2}
N 120 -240 190 -240 {
lab=#net1}
N 190 -240 352.5 -240 {
lab=#net1}
N 240 -200 240 -140 {
lab=GND}
N 240 -200 300 -200 {
lab=GND}
C {devices/iopin.sym} 40 -40 0 0 {name=p16 lab=GND
}
C {devices/iopin.sym} 40 -20 0 0 {name=p19 lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} 100 -190 0 0 {name=M1
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
C {devices/lab_wire.sym} 120 -130 0 0 {name=p3 sig_type=std_logic lab=GND
}
C {devices/ipin.sym} 35 -75 2 0 {name=p4 lab=spk


}
C {devices/lab_wire.sym} 60 -190 0 0 {name=p12 sig_type=std_logic lab=spk

}
C {devices/opin.sym} 185 -25 2 0 {name=p7 lab=spkext


}
C {devices/lab_wire.sym} 670 -240 2 0 {name=p8 sig_type=std_logic lab=spkext

}
C {sky130_fd_pr/pfet_01v8.sym} 100 -350 0 0 {name=M6
L=2
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
C {devices/lab_wire.sym} 120 -430 0 0 {name=p9 sig_type=std_logic lab=VDD
}
C {devices/ipin.sym} 125 -75 2 0 {name=p10 lab=vpulseextp


}
C {devices/lab_wire.sym} 40 -350 0 0 {name=p11 sig_type=std_logic lab=vpulseextp


}
C {devices/lab_wire.sym} 240 -140 0 0 {name=p13 sig_type=std_logic lab=GND
}
C {sky130_fd_pr/nfet_01v8.sym} 470 -210 0 0 {name=M5
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
C {devices/lab_wire.sym} 490 -340 0 0 {name=p5 sig_type=std_logic lab=VDD
}
C {devices/lab_wire.sym} 490 -140 0 0 {name=p6 sig_type=std_logic lab=GND
}
C {sky130_fd_pr/nfet_01v8.sym} 570 -210 0 0 {name=M8
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
C {devices/lab_wire.sym} 590 -340 0 0 {name=p14 sig_type=std_logic lab=VDD
}
C {devices/lab_wire.sym} 590 -140 0 0 {name=p15 sig_type=std_logic lab=GND
}
C {sky130_fd_pr/pfet_01v8.sym} 470 -270 0 0 {name=M4
L=0.15
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
C {sky130_fd_pr/pfet_01v8.sym} 570 -270 0 0 {name=M7
L=0.15
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
C {sky130_fd_pr/nfet_01v8.sym} 372.5 -210 0 0 {name=M2
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
C {devices/lab_wire.sym} 392.5 -340 0 0 {name=p1 sig_type=std_logic lab=VDD
}
C {devices/lab_wire.sym} 392.5 -140 0 0 {name=p2 sig_type=std_logic lab=GND
}
C {sky130_fd_pr/pfet_01v8.sym} 372.5 -270 0 0 {name=M3
L=0.15
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
C {sky130_fd_pr/nfet_01v8.sym} 270 -220 1 0 {name=M9
L=1
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
