v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Analog Neuron} 440 -690 0 0 0.4 0.4 {}
N 805 -600 805 -560 {
lab=VDD}
N 805 -210 805 -170 {
lab=GND}
N 845 -310 845 -200 {
lab=GND}
N 805 -200 845 -200 {
lab=GND}
N 805 -240 845 -240 {
lab=GND}
N 805 -310 805 -270 {
lab=#net1}
N 765 -290 765 -240 {
lab=#net1}
N 765 -290 805 -290 {
lab=#net1}
N 805 -480 805 -460 {
lab=#net2}
N 805 -560 805 -540 {
lab=VDD}
N 805 -510 835 -510 {
lab=VDD}
N 835 -550 835 -510 {
lab=VDD}
N 805 -550 835 -550 {
lab=VDD}
N 835 -510 835 -460 {
lab=VDD}
N 705 -600 705 -510 {
lab=nreq}
N 705 -510 765 -510 {
lab=nreq}
N 635 -390 765 -390 {
lab=vmem
.IC=0}
N 975 -400 975 -370 {
lab=#net3}
N 935 -430 935 -340 {
lab=nreq}
N 975 -430 1005 -430 {
lab=VDD}
N 1005 -460 1005 -430 {
lab=VDD}
N 975 -340 1015 -340 {
lab=GND}
N 1015 -340 1015 -310 {
lab=GND}
N 805 -390 935 -390 {
lab=nreq}
N 975 -310 975 -270 {
lab=#net4}
N 1015 -310 1015 -180 {
lab=GND}
N 975 -210 975 -170 {
lab=GND}
N 975 -180 1015 -180 {
lab=GND}
N 975 -490 975 -460 {
lab=#net5}
N 975 -520 1005 -520 {
lab=VDD}
N 1005 -520 1005 -460 {
lab=VDD}
N 1005 -570 1005 -520 {
lab=VDD}
N 975 -570 1005 -570 {
lab=VDD}
N 975 -590 975 -550 {
lab=VDD}
N 895 -520 935 -520 {
lab=nack}
N 895 -610 895 -520 {
lab=nack}
N 745 -70 745 -30 {
lab=GND}
N 525 -390 635 -390 {
lab=vmem
.IC=0}
N 885 -640 885 -390 {
lab=nreq}
N 885 -640 1115 -640 {
lab=nreq}
N 705 -640 885 -640 {
lab=nreq}
N 705 -640 705 -600 {
lab=nreq}
N 975 -240 1015 -240 {
lab=GND}
N 695 -170 695 -130 {
lab=#net3}
N 625 -140 655 -140 {
lab=GND}
N 625 -170 655 -170 {
lab=GND}
N 625 -170 625 -140 {
lab=GND}
N 655 -250 655 -200 {
lab=vmem}
N 895 -610 1115 -610 {
lab=nack}
N 975 -390 1145 -390 {
lab=#net3}
N 1145 -390 1145 -130 {
lab=#net3}
N 1075 -130 1145 -130 {
lab=#net3}
N 655 -390 655 -250 {
lab=vmem}
N 695 -130 745 -130 {
lab=#net3}
N 745 -130 1075 -130 {
lab=#net3}
N 285 -690 285 -650 {
lab=VDD}
N 285 -620 325 -620 {
lab=VDD}
N 325 -660 325 -620 {
lab=VDD}
N 285 -660 325 -660 {
lab=VDD}
N 255 -255 285 -255 {
lab=GND}
N 285 -255 285 -205 {
lab=GND}
N 915 -240 935 -240 {
lab=vrefn}
N 905 -240 915 -240 {
lab=vrefn}
N 675 -510 705 -510 {
lab=nreq}
N 595 -510 635 -510 {
lab=VDD}
N 595 -540 595 -510 {
lab=VDD}
N 595 -540 635 -540 {
lab=VDD}
N 635 -480 635 -390 {
lab=vmem}
N 285 -205 285 -165 {
lab=GND}
N 255 -165 285 -165 {
lab=GND}
N 240 -390 430 -390 {
lab=vmem}
N 430 -390 525 -390 {
lab=vmem}
N 255 -225 255 -165 {
lab=GND}
N 115 -390 240 -390 {
lab=vmem
.IC=0}
N 285 -495 285 -390 {
lab=vmem}
N 255 -390 255 -340 {
lab=vmem}
N 765 -430 765 -390 {
lab=vmem}
N 765 -390 765 -340 {
lab=vmem}
N 805 -400 805 -370 {
lab=nreq}
N 805 -340 845 -340 {
lab=GND}
N 845 -340 845 -310 {
lab=GND}
N 835 -460 835 -430 {
lab=VDD}
N 805 -430 835 -430 {
lab=VDD}
N 255 -340 255 -285 {
lab=vmem}
N 285 -590 285 -495 {
lab=vmem}
N 745 -90 750 -90 {
lab=GND}
N 745 -90 745 -70 {
lab=GND}
N 745 -75 780 -75 {
lab=GND}
N 780 -90 780 -75 {
lab=GND}
N 810 -90 810 -75 {
lab=GND}
N 780 -75 810 -75 {
lab=GND}
N 575 -330 575 -285 {
lab=GND}
C {devices/lab_pin.sym} 805 -600 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 805 -170 0 0 {name=p7 sig_type=std_logic lab=GND}
C {sky130_fd_pr/cap_mim_m3_1.sym} 575 -360 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 975 -170 0 0 {name=p3 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 975 -590 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 745 -30 0 0 {name=p9 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 625 -170 2 1 {name=p19 sig_type=std_logic lab=GND}
C {devices/ipin.sym} 215 -255 0 0 {name=p15 lab=vleakn
}
C {devices/iopin.sym} 440 -740 0 0 {name=p13 lab=GND
}
C {devices/iopin.sym} 440 -720 0 0 {name=p16 lab=VDD}
C {devices/opin.sym} 1115 -640 0 0 {name=p17 lab=nreq}
C {devices/ipin.sym} 905 -240 1 0 {name=p5 lab=vrefn
}
C {devices/ipin.sym} 1115 -610 2 0 {name=p11 lab=nack}
C {devices/lab_pin.sym} 285 -690 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/ipin.sym} 245 -620 0 0 {name=p10 lab=ifdcp
}
C {devices/lab_pin.sym} 255 -165 3 0 {name=p22 sig_type=std_logic lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} 265 -620 0 0 {name=M1
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
C {sky130_fd_pr/pfet_01v8.sym} 785 -510 0 0 {name=M5
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
C {sky130_fd_pr/nfet_01v8.sym} 955 -340 0 0 {name=M7
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
C {devices/lab_pin.sym} 595 -540 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 115 -390 3 0 {name=p25 lab=vmem
}
C {sky130_fd_pr/pfet_01v8.sym} 955 -520 0 0 {name=M6
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
C {sky130_fd_pr/pfet_01v8.sym} 785 -430 0 0 {name=M9
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
C {sky130_fd_pr/pfet_01v8.sym} 955 -430 0 0 {name=M10
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
C {sky130_fd_pr/pfet_01v8.sym} 655 -510 0 1 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} 785 -340 0 0 {name=M2
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
C {sky130_fd_pr/nfet_01v8.sym} 955 -240 0 0 {name=M3
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
C {sky130_fd_pr/nfet_01v8.sym} 785 -240 0 0 {name=M8
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
C {sky130_fd_pr/nfet_01v8.sym} 675 -170 0 1 {name=M11
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
C {sky130_fd_pr/nfet_01v8.sym} 235 -255 0 0 {name=M12
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
C {sky130_fd_pr/nfet_01v8.sym} 780 -110 1 0 {name=M13
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
C {devices/lab_pin.sym} 575 -285 3 0 {name=p2 sig_type=std_logic lab=GND}
