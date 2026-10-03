v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 340 -310 340 -280 {
lab=#net1}
N 340 -220 340 -170 {
lab=#net2}
N 270 -360 300 -360 {
lab=spk}
N 340 -330 340 -310 {
lab=#net1}
N 340 -360 380 -360 {
lab=GND}
N 250 -250 300 -250 {
lab=JExcWn[0]}
N 340 -530 340 -520 {
lab=vsin}
N 340 -570 340 -530 {
lab=vsin}
N 340 -690 340 -650 {
lab=aVDD}
N 340 -650 340 -630 {
lab=aVDD}
N 340 -600 390 -600 {
lab=aVDD}
N 390 -650 390 -600 {
lab=aVDD}
N 340 -650 390 -650 {
lab=aVDD}
N 260 -600 300 -600 {
lab=vtaup}
N 340 -550 510 -550 {
lab=vsin}
N 510 -670 510 -630 {
lab=aVDD}
N 510 -630 510 -610 {
lab=aVDD}
N 510 -550 620 -550 {
lab=vsin}
N 660 -640 660 -600 {
lab=aVDD}
N 660 -600 660 -580 {
lab=aVDD}
N 660 -550 690 -550 {
lab=aVDD}
N 690 -600 690 -550 {
lab=aVDD}
N 660 -600 690 -600 {
lab=aVDD}
N 660 -510 660 -490 {
lab=sout}
N 660 -520 660 -510 {
lab=sout}
N 340 -520 340 -470 {
lab=vsin}
N 340 -410 340 -390 {
lab=#net3}
N 380 -440 410 -440 {
lab=vsin}
N 410 -550 410 -440 {
lab=vsin}
N 170 -400 340 -400 {
lab=#net3}
N 170 -430 170 -400 {
lab=#net3}
N 170 -520 170 -490 {
lab=aVDD}
N 100 -460 130 -460 {
lab=vthn}
N 170 -460 210 -460 {
lab=GND}
N 210 -460 210 -440 {
lab=GND}
N 210 -440 260 -440 {
lab=GND}
N 260 -440 290 -440 {
lab=GND}
N 290 -440 340 -440 {
lab=GND}
N 340 -300 560 -300 {
lab=#net1}
N 560 -300 560 -270 {
lab=#net1}
N 560 -210 560 -160 {
lab=#net4}
N 560 -240 600 -240 {
lab=GND}
N 600 -240 600 -190 {
lab=GND}
N 780 -210 780 -160 {
lab=#net5}
N 780 -240 820 -240 {
lab=GND}
N 820 -240 820 -190 {
lab=GND}
N 980 -210 980 -160 {
lab=#net6}
N 980 -240 1020 -240 {
lab=GND}
N 1020 -240 1020 -190 {
lab=GND}
N 980 -300 980 -270 {
lab=#net1}
N 560 -300 860 -300 {
lab=#net1}
N 780 -300 780 -270 {
lab=#net1}
N 340 -110 340 -80 {
lab=GND}
N 340 -140 390 -140 {
lab=GND}
N 340 -90 360 -90 {
lab=GND}
N 360 -140 360 -90 {
lab=GND}
N 560 -130 600 -130 {
lab=GND}
N 600 -190 600 -130 {
lab=GND}
N 390 -250 390 -140 {
lab=GND}
N 370 -250 390 -250 {
lab=GND}
N 340 -250 370 -250 {
lab=GND}
N 560 -100 560 -80 {
lab=GND}
N 560 -90 600 -90 {
lab=GND}
N 600 -130 600 -90 {
lab=GND}
N 780 -100 780 -80 {
lab=GND}
N 780 -130 820 -130 {
lab=GND}
N 820 -190 820 -130 {
lab=GND}
N 820 -130 820 -100 {
lab=GND}
N 780 -100 820 -100 {
lab=GND}
N 980 -130 1020 -130 {
lab=GND}
N 1020 -190 1020 -130 {
lab=GND}
N 980 -100 980 -80 {
lab=GND}
N 980 -100 1020 -100 {
lab=GND}
N 1020 -130 1020 -100 {
lab=GND}
N 340 -80 860 -80 {
lab=GND}
N 860 -300 980 -300 {
lab=#net1}
N 860 -80 980 -80 {
lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 320 -360 0 0 {name=M2
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/cap_mim_m3_1.sym} 510 -580 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 320 -600 0 0 {name=M5
L=0.2
W=1.2
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
C {devices/lab_pin.sym} 340 -690 0 0 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 510 -670 0 0 {name=p3 sig_type=std_logic lab=aVDD}
C {sky130_fd_pr/pfet_01v8.sym} 640 -550 0 0 {name=M6
L=0.2
W=1.2
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
C {devices/lab_pin.sym} 660 -640 0 0 {name=p7 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 470 -550 3 0 {name=p22 sig_type=std_logic lab=vsin}
C {sky130_fd_pr/nfet_01v8.sym} 320 -250 0 0 {name=M1
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 360 -440 0 1 {name=M4
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
model=nfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 260 -440 1 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 10 -170 0 0 {name=p1 lab=GND
}
C {devices/iopin.sym} 10 -150 0 0 {name=p16 lab=aVDD}
C {devices/iopin.sym} 260 -600 2 0 {name=p10 lab=vtaup

}
C {devices/ipin.sym} 270 -360 0 0 {name=p6 lab=spk

}
C {devices/opin.sym} 660 -490 1 0 {name=p8 lab=sout}
C {sky130_fd_pr/nfet_01v8.sym} 150 -460 0 0 {name=M3
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
model=nfet_01v8
spiceprefix=X
}
C {devices/iopin.sym} 100 -460 2 0 {name=p9 lab=vthn

}
C {devices/lab_pin.sym} 170 -520 0 0 {name=p11 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 380 -360 2 0 {name=p13 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 540 -240 0 0 {name=M7
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
C {sky130_fd_pr/nfet_01v8.sym} 760 -240 0 0 {name=M8
L=4.0
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
C {devices/lab_pin.sym} 340 -80 3 0 {name=p17 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 960 -240 0 0 {name=M9
L=8.0
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
C {sky130_fd_pr/nfet_01v8.sym} 320 -140 0 0 {name=M10
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 540 -130 0 0 {name=M11
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 760 -130 0 0 {name=M12
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
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 960 -130 0 0 {name=M13
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
model=nfet_01v8
spiceprefix=X
}
C {devices/ipin.sym} 130 -120 0 0 {name=p12 lab=weight[0:3]

}
C {devices/lab_pin.sym} 520 -130 0 0 {name=p14 lab=weight[1]

}
C {devices/lab_pin.sym} 740 -130 0 0 {name=p15 lab=weight[2]

}
C {devices/lab_pin.sym} 940 -130 0 0 {name=p18 lab=weight[3]

}
C {devices/lab_pin.sym} 300 -140 0 0 {name=p19 lab=weight[0]

}
C {devices/iopin.sym} 140 -205 0 1 {name=p2 lab=JExcWn[0:3]


}
C {devices/lab_pin.sym} 250 -250 0 0 {name=p20 lab=JExcWn[0]

}
C {devices/lab_pin.sym} 520 -240 0 0 {name=p21 lab=JExcWn[1]

}
C {devices/lab_pin.sym} 740 -240 0 0 {name=p23 lab=JExcWn[2]

}
C {devices/lab_pin.sym} 940 -240 0 0 {name=p24 lab=JExcWn[3]

}
