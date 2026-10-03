v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Analog Neuron} 420 -800 0 0 0.4 0.4 {}
N 785 -710 785 -670 {
lab=VDD}
N 785 -320 785 -280 {
lab=GND}
N 825 -420 825 -310 {
lab=GND}
N 785 -310 825 -310 {
lab=GND}
N 785 -350 825 -350 {
lab=GND}
N 785 -420 785 -380 {
lab=#net1}
N 745 -400 745 -350 {
lab=#net1}
N 745 -400 785 -400 {
lab=#net1}
N 785 -590 785 -570 {
lab=#net2}
N 785 -670 785 -650 {
lab=VDD}
N 785 -620 815 -620 {
lab=VDD}
N 815 -660 815 -620 {
lab=VDD}
N 785 -660 815 -660 {
lab=VDD}
N 815 -620 815 -570 {
lab=VDD}
N 685 -710 685 -620 {
lab=nreq}
N 685 -620 745 -620 {
lab=nreq}
N 615 -500 745 -500 {
lab=vmem
.IC=0}
N 955 -510 955 -480 {
lab=#net3}
N 915 -540 915 -450 {
lab=nreq}
N 955 -540 985 -540 {
lab=VDD}
N 985 -570 985 -540 {
lab=VDD}
N 955 -450 995 -450 {
lab=GND}
N 995 -450 995 -420 {
lab=GND}
N 785 -500 915 -500 {
lab=nreq}
N 955 -420 955 -380 {
lab=#net4}
N 995 -420 995 -290 {
lab=GND}
N 955 -320 955 -280 {
lab=GND}
N 955 -290 995 -290 {
lab=GND}
N 955 -600 955 -570 {
lab=#net5}
N 955 -630 985 -630 {
lab=VDD}
N 985 -630 985 -570 {
lab=VDD}
N 985 -680 985 -630 {
lab=VDD}
N 955 -680 985 -680 {
lab=VDD}
N 955 -700 955 -660 {
lab=VDD}
N 875 -630 915 -630 {
lab=nack}
N 875 -720 875 -630 {
lab=nack}
N 725 -180 725 -140 {
lab=GND}
N 505 -500 615 -500 {
lab=vmem
.IC=0}
N 865 -750 865 -500 {
lab=nreq}
N 865 -750 1095 -750 {
lab=nreq}
N 685 -750 865 -750 {
lab=nreq}
N 685 -750 685 -710 {
lab=nreq}
N 955 -350 995 -350 {
lab=GND}
N 675 -280 675 -240 {
lab=#net3}
N 605 -250 635 -250 {
lab=GND}
N 605 -280 635 -280 {
lab=GND}
N 605 -280 605 -250 {
lab=GND}
N 635 -360 635 -310 {
lab=vmem}
N 875 -720 1095 -720 {
lab=nack}
N 955 -500 1125 -500 {
lab=#net3}
N 1125 -500 1125 -240 {
lab=#net3}
N 1055 -240 1125 -240 {
lab=#net3}
N 635 -500 635 -360 {
lab=vmem}
N 675 -240 725 -240 {
lab=#net3}
N 725 -240 1055 -240 {
lab=#net3}
N 265 -800 265 -760 {
lab=VDD}
N 265 -730 305 -730 {
lab=VDD}
N 305 -770 305 -730 {
lab=VDD}
N 265 -770 305 -770 {
lab=VDD}
N 235 -365 265 -365 {
lab=GND}
N 265 -365 265 -315 {
lab=GND}
N 895 -350 915 -350 {
lab=vrefn}
N 885 -350 895 -350 {
lab=vrefn}
N 655 -620 685 -620 {
lab=nreq}
N 575 -620 615 -620 {
lab=VDD}
N 575 -650 575 -620 {
lab=VDD}
N 575 -650 615 -650 {
lab=VDD}
N 615 -590 615 -500 {
lab=vmem}
N 265 -315 265 -275 {
lab=GND}
N 235 -275 265 -275 {
lab=GND}
N 220 -500 410 -500 {
lab=vmem}
N 410 -500 505 -500 {
lab=vmem}
N 235 -335 235 -275 {
lab=GND}
N 95 -500 220 -500 {
lab=vmem
.IC=0}
N 265 -605 265 -500 {
lab=vmem}
N 235 -500 235 -450 {
lab=vmem}
N 745 -540 745 -500 {
lab=vmem}
N 745 -500 745 -450 {
lab=vmem}
N 785 -510 785 -480 {
lab=nreq}
N 785 -450 825 -450 {
lab=GND}
N 825 -450 825 -420 {
lab=GND}
N 815 -570 815 -540 {
lab=VDD}
N 785 -540 815 -540 {
lab=VDD}
N 235 -450 235 -395 {
lab=vmem}
N 265 -700 265 -605 {
lab=vmem}
N 725 -200 730 -200 {
lab=GND}
N 725 -200 725 -180 {
lab=GND}
N 725 -185 760 -185 {
lab=GND}
N 760 -200 760 -185 {
lab=GND}
N 790 -200 790 -185 {
lab=GND}
N 760 -185 790 -185 {
lab=GND}
N 555 -440 555 -395 {
lab=GND}
C {devices/lab_pin.sym} 785 -710 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 785 -280 0 0 {name=p7 sig_type=std_logic lab=GND}
C {sky130_fd_pr/cap_mim_m3_1.sym} 555 -470 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 955 -280 0 0 {name=p3 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 955 -700 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 725 -140 0 0 {name=p9 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 605 -280 2 1 {name=p19 sig_type=std_logic lab=GND}
C {devices/ipin.sym} 195 -365 0 0 {name=p15 lab=vleakn
}
C {devices/iopin.sym} 420 -850 0 0 {name=p13 lab=GND
}
C {devices/iopin.sym} 420 -830 0 0 {name=p16 lab=VDD}
C {devices/opin.sym} 1095 -750 0 0 {name=p17 lab=nreq}
C {devices/ipin.sym} 885 -350 1 0 {name=p5 lab=vrefn
}
C {devices/ipin.sym} 1095 -720 2 0 {name=p11 lab=nack}
C {devices/lab_pin.sym} 265 -800 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/ipin.sym} 225 -730 0 0 {name=p10 lab=ifdcp
}
C {devices/lab_pin.sym} 235 -275 3 0 {name=p22 sig_type=std_logic lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} 245 -730 0 0 {name=M1
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
C {sky130_fd_pr/pfet_01v8.sym} 765 -620 0 0 {name=M5
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
C {sky130_fd_pr/nfet_01v8.sym} 935 -450 0 0 {name=M7
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
C {devices/lab_pin.sym} 575 -650 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 95 -500 3 0 {name=p25 lab=vmem
}
C {sky130_fd_pr/pfet_01v8.sym} 935 -630 0 0 {name=M6
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
C {sky130_fd_pr/pfet_01v8.sym} 765 -540 0 0 {name=M9
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
C {sky130_fd_pr/pfet_01v8.sym} 935 -540 0 0 {name=M10
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
C {sky130_fd_pr/pfet_01v8.sym} 635 -620 0 1 {name=M4
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
C {sky130_fd_pr/nfet_01v8.sym} 765 -450 0 0 {name=M2
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
C {sky130_fd_pr/nfet_01v8.sym} 935 -350 0 0 {name=M3
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
C {sky130_fd_pr/nfet_01v8.sym} 765 -350 0 0 {name=M8
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
C {sky130_fd_pr/nfet_01v8.sym} 655 -280 0 1 {name=M11
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
C {sky130_fd_pr/nfet_01v8.sym} 215 -365 0 0 {name=M12
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
C {sky130_fd_pr/nfet_01v8.sym} 760 -220 1 0 {name=M13
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
C {devices/lab_pin.sym} 555 -395 3 0 {name=p2 sig_type=std_logic lab=GND}
