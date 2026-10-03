v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Analog Neuron -} 950 -720 0 0 0.4 0.4 {}
N 1315 -630 1315 -590 {
lab=aVDD}
N 1315 -240 1315 -200 {
lab=GND}
N 1355 -340 1355 -230 {
lab=GND}
N 1315 -230 1355 -230 {
lab=GND}
N 1315 -270 1355 -270 {
lab=GND}
N 1315 -340 1315 -300 {
lab=#net1}
N 1275 -320 1275 -270 {
lab=#net1}
N 1275 -320 1315 -320 {
lab=#net1}
N 1315 -510 1315 -490 {
lab=#net2}
N 1315 -590 1315 -570 {
lab=aVDD}
N 1315 -540 1345 -540 {
lab=aVDD}
N 1345 -580 1345 -540 {
lab=aVDD}
N 1315 -580 1345 -580 {
lab=aVDD}
N 1345 -540 1345 -490 {
lab=aVDD}
N 1215 -630 1215 -540 {
lab=nreq}
N 1215 -540 1275 -540 {
lab=nreq}
N 1145 -420 1275 -420 {
lab=vmem
.IC=0}
N 1085 -360 1085 -310 {
lab=GND}
N 1485 -430 1485 -400 {
lab=#net3}
N 1445 -460 1445 -370 {
lab=nreq}
N 1485 -460 1515 -460 {
lab=aVDD}
N 1515 -490 1515 -460 {
lab=aVDD}
N 1485 -370 1525 -370 {
lab=GND}
N 1525 -370 1525 -340 {
lab=GND}
N 1315 -420 1445 -420 {
lab=nreq}
N 1485 -340 1485 -300 {
lab=#net4}
N 1525 -340 1525 -210 {
lab=GND}
N 1485 -240 1485 -200 {
lab=GND}
N 1485 -210 1525 -210 {
lab=GND}
N 1485 -520 1485 -490 {
lab=#net5}
N 1485 -550 1515 -550 {
lab=aVDD}
N 1515 -550 1515 -490 {
lab=aVDD}
N 1515 -600 1515 -550 {
lab=aVDD}
N 1485 -600 1515 -600 {
lab=aVDD}
N 1485 -620 1485 -580 {
lab=aVDD}
N 1405 -550 1445 -550 {
lab=nack}
N 1405 -640 1405 -550 {
lab=nack}
N 1255 -100 1255 -60 {
lab=GND}
N 1035 -420 1145 -420 {
lab=vmem
.IC=0}
N 1395 -670 1395 -420 {
lab=nreq}
N 1395 -670 1625 -670 {
lab=nreq}
N 1215 -670 1395 -670 {
lab=nreq}
N 1215 -670 1215 -630 {
lab=nreq}
N 1485 -270 1525 -270 {
lab=GND}
N 1205 -200 1205 -160 {
lab=#net3}
N 1135 -170 1165 -170 {
lab=GND}
N 1135 -200 1165 -200 {
lab=GND}
N 1135 -200 1135 -170 {
lab=GND}
N 1165 -280 1165 -230 {
lab=vmem}
N 1405 -640 1625 -640 {
lab=nack}
N 1485 -420 1655 -420 {
lab=#net3}
N 1655 -420 1655 -160 {
lab=#net3}
N 1585 -160 1655 -160 {
lab=#net3}
N 1165 -420 1165 -280 {
lab=vmem}
N 1205 -160 1255 -160 {
lab=#net3}
N 1255 -160 1585 -160 {
lab=#net3}
N 795 -720 795 -680 {
lab=aVDD}
N 795 -650 835 -650 {
lab=aVDD}
N 835 -690 835 -650 {
lab=aVDD}
N 795 -690 835 -690 {
lab=aVDD}
N 765 -285 795 -285 {
lab=GND}
N 795 -285 795 -235 {
lab=GND}
N 1425 -270 1445 -270 {
lab=vrefn}
N 1415 -270 1425 -270 {
lab=vrefn}
N 1185 -540 1215 -540 {
lab=nreq}
N 1105 -540 1145 -540 {
lab=VDD}
N 1105 -570 1105 -540 {
lab=VDD}
N 1105 -570 1145 -570 {
lab=VDD}
N 1145 -510 1145 -420 {
lab=vmem}
N 795 -235 795 -195 {
lab=GND}
N 765 -195 795 -195 {
lab=GND}
N 750 -420 940 -420 {
lab=vmem}
N 940 -420 1035 -420 {
lab=vmem}
N 765 -255 765 -195 {
lab=GND}
N 625 -420 750 -420 {
lab=vmem
.IC=0}
N 795 -525 795 -420 {
lab=vmem}
N 765 -420 765 -370 {
lab=vmem}
N 1275 -460 1275 -420 {
lab=vmem}
N 1275 -420 1275 -370 {
lab=vmem}
N 1315 -430 1315 -400 {
lab=nreq}
N 1315 -370 1355 -370 {
lab=GND}
N 1355 -370 1355 -340 {
lab=GND}
N 1345 -490 1345 -460 {
lab=aVDD}
N 1315 -460 1345 -460 {
lab=aVDD}
N 765 -370 765 -315 {
lab=vmem}
N 795 -620 795 -525 {
lab=vmem}
C {devices/lab_pin.sym} 1315 -630 0 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1315 -200 0 0 {name=p7 sig_type=std_logic lab=GND}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1085 -390 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 1085 -310 0 0 {name=p2 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1485 -200 0 0 {name=p3 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1485 -620 0 0 {name=p6 sig_type=std_logic lab=aVDD}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1255 -130 2 0 {name=C2 model=cap_mim_m3_1 W=2 L=2 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 1255 -60 0 0 {name=p9 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1135 -200 2 1 {name=p19 sig_type=std_logic lab=GND}
C {devices/ipin.sym} 725 -285 0 0 {name=p15 lab=vleakn
}
C {devices/iopin.sym} 950 -770 0 0 {name=p13 lab=GND
}
C {devices/iopin.sym} 950 -750 0 0 {name=p16 lab=aVDD}
C {devices/opin.sym} 1625 -670 0 0 {name=p17 lab=nreq}
C {devices/ipin.sym} 1415 -270 1 0 {name=p5 lab=vrefn
}
C {devices/ipin.sym} 1625 -640 2 0 {name=p11 lab=nack}
C {devices/lab_pin.sym} 795 -720 0 0 {name=p8 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 755 -650 0 0 {name=p10 lab=ifdcp
}
C {devices/lab_pin.sym} 765 -195 3 0 {name=p22 sig_type=std_logic lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} 775 -650 0 0 {name=M1
L=2.0
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
C {sky130_fd_pr/pfet_01v8.sym} 1295 -540 0 0 {name=M5
L=0.25
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
C {sky130_fd_pr/nfet_01v8.sym} 1465 -370 0 0 {name=M7
L=0.15
W=0.6
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
C {devices/lab_pin.sym} 1105 -570 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 625 -420 3 0 {name=p25 lab=vmem
}
C {sky130_fd_pr/pfet_01v8.sym} 1465 -550 0 0 {name=M6
L=0.25
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
C {sky130_fd_pr/pfet_01v8.sym} 1295 -460 0 0 {name=M9
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
C {sky130_fd_pr/pfet_01v8.sym} 1465 -460 0 0 {name=M10
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
C {sky130_fd_pr/pfet_01v8.sym} 1165 -540 0 1 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} 1295 -370 0 0 {name=M2
L=0.15
W=0.6
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
C {sky130_fd_pr/nfet_01v8.sym} 1465 -270 0 0 {name=M3
L=1.0
W=0.6
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
C {sky130_fd_pr/nfet_01v8.sym} 1295 -270 0 0 {name=M8
L=0.15
W=0.6
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
C {sky130_fd_pr/nfet_01v8.sym} 1185 -200 0 1 {name=M11
L=0.2
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
C {sky130_fd_pr/nfet_01v8.sym} 745 -285 0 0 {name=M12
L=2.0
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
