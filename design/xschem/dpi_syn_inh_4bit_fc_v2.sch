v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 580 -490 580 -450 {
lab=#net1}
N 580 -450 580 -430 {
lab=#net1}
N 580 -400 630 -400 {
lab=aVDD}
N 580 -370 580 -350 {
lab=#net2}
N 660 -290 660 -280 {
lab=#net2}
N 580 -290 660 -290 {
lab=#net2}
N 510 -290 580 -290 {
lab=#net2}
N 510 -290 510 -280 {
lab=#net2}
N 510 -250 660 -250 {
lab=aVDD}
N 400 -250 470 -250 {
lab=vthrdp}
N 510 -220 510 -180 {
lab=GND}
N 660 -100 660 -60 {
lab=GND}
N 620 -130 660 -130 {
lab=GND}
N 620 -130 620 -80 {
lab=GND}
N 620 -80 660 -80 {
lab=GND}
N 700 -130 750 -130 {
lab=vtaun}
N 700 -250 770 -250 {
lab=vsin}
N 660 -220 660 -160 {
lab=vsin}
N 770 -250 900 -250 {
lab=vsin}
N 940 -250 990 -250 {
lab=GND}
N 990 -250 990 -150 {
lab=GND}
N 940 -150 990 -150 {
lab=GND}
N 940 -300 940 -280 {
lab=sout}
N 180 -410 180 -390 {
lab=#net3}
N 180 -360 200 -360 {
lab=GND}
N 200 -360 200 -330 {
lab=GND}
N 180 -330 200 -330 {
lab=GND}
N 180 -330 180 -300 {
lab=GND}
N 140 -440 140 -360 {
lab=spk}
N 100 -400 140 -400 {
lab=spk}
N 180 -520 180 -470 {
lab=aVDD}
N 400 -400 540 -400 {
lab=#net3}
N 660 -190 720 -190 {
lab=vsin}
N 720 -250 720 -190 {
lab=vsin}
N 180 -440 210 -440 {
lab=aVDD}
N 210 -480 210 -440 {
lab=aVDD}
N 180 -480 210 -480 {
lab=aVDD}
N 360 -810 360 -780 {
lab=aVDD}
N 360 -720 360 -670 {
lab=#net4}
N 360 -830 360 -810 {
lab=aVDD}
N 270 -750 320 -750 {
lab=JInhWp[0]}
N 360 -800 580 -800 {
lab=aVDD}
N 580 -800 580 -770 {
lab=aVDD}
N 580 -710 580 -660 {
lab=#net5}
N 580 -740 620 -740 {
lab=aVDD}
N 620 -740 620 -690 {
lab=aVDD}
N 830 -710 830 -660 {
lab=#net6}
N 830 -740 870 -740 {
lab=aVDD}
N 870 -740 870 -690 {
lab=aVDD}
N 1060 -710 1060 -660 {
lab=#net7}
N 1060 -740 1100 -740 {
lab=aVDD}
N 1100 -740 1100 -690 {
lab=aVDD}
N 1060 -800 1060 -770 {
lab=aVDD}
N 580 -800 880 -800 {
lab=aVDD}
N 830 -800 830 -770 {
lab=aVDD}
N 360 -610 360 -580 {
lab=#net1}
N 360 -640 410 -640 {
lab=aVDD}
N 580 -630 620 -630 {
lab=aVDD}
N 620 -690 620 -630 {
lab=aVDD}
N 410 -750 410 -640 {
lab=aVDD}
N 390 -750 410 -750 {
lab=aVDD}
N 360 -750 390 -750 {
lab=aVDD}
N 580 -600 580 -580 {
lab=#net1}
N 830 -600 830 -580 {
lab=#net1}
N 830 -630 870 -630 {
lab=aVDD}
N 870 -690 870 -630 {
lab=aVDD}
N 1060 -630 1100 -630 {
lab=aVDD}
N 1100 -690 1100 -630 {
lab=aVDD}
N 1060 -600 1060 -580 {
lab=#net1}
N 540 -820 540 -740 {
lab=JInhWp[1]}
N 790 -820 790 -740 {
lab=JInhWp[2]}
N 1020 -820 1020 -740 {
lab=JInhWp[3]}
N 360 -580 880 -580 {
lab=#net1}
N 180 -400 400 -400 {
lab=#net3}
N 580 -350 580 -290 {
lab=#net2}
N 580 -580 580 -490 {
lab=#net1}
N 1100 -800 1100 -740 {
lab=aVDD}
N 1050 -800 1100 -800 {
lab=aVDD}
N 870 -800 870 -740 {
lab=aVDD}
N 620 -800 620 -740 {
lab=aVDD}
N 410 -800 410 -750 {
lab=aVDD}
N 940 -160 940 -150 {
lab=GND}
N 880 -580 1060 -580 {
lab=#net1}
N 880 -800 1050 -800 {
lab=aVDD}
N 940 -220 940 -160 {
lab=GND}
N 800 -260 800 -250 {
lab=vsin}
C {sky130_fd_pr/pfet_01v8.sym} 560 -400 0 0 {name=M5
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
C {devices/lab_pin.sym} 360 -830 1 0 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 100 -400 0 0 {name=p1 lab=spk

}
C {sky130_fd_pr/pfet_01v8.sym} 490 -250 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} 680 -250 0 1 {name=M3
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
C {devices/iopin.sym} 400 -250 2 0 {name=p3 lab=vthrdp

}
C {devices/lab_pin.sym} 510 -180 0 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 660 -60 0 0 {name=p6 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 680 -130 0 1 {name=M4
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
C {devices/iopin.sym} 750 -130 0 0 {name=p7 lab=vtaun

}
C {sky130_fd_pr/nfet_01v8.sym} 920 -250 0 0 {name=M6
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
C {devices/lab_pin.sym} 940 -150 0 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 940 -300 3 0 {name=p9 lab=sout}
C {sky130_fd_pr/nfet_01v8.sym} 160 -360 0 0 {name=M7
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
C {sky130_fd_pr/pfet_01v8.sym} 160 -440 0 0 {name=M8
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
C {devices/lab_pin.sym} 180 -300 0 0 {name=p10 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 180 -520 0 0 {name=p11 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 840 -70 0 0 {name=p12 lab=GND
}
C {devices/iopin.sym} 840 -50 0 0 {name=p16 lab=aVDD}
C {devices/lab_pin.sym} 580 -250 3 0 {name=p13 sig_type=std_logic lab=aVDD}
C {sky130_fd_pr/cap_mim_m3_1.sym} 800 -290 2 1 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/ipin.sym} 250 -670 0 0 {name=p40 lab=weight_b[0:3]

}
C {sky130_fd_pr/pfet_01v8.sym} 340 -750 0 0 {name=M9
L=1.2
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
C {sky130_fd_pr/pfet_01v8.sym} 340 -640 0 0 {name=M10
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
C {sky130_fd_pr/pfet_01v8.sym} 560 -630 0 0 {name=M11
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
C {sky130_fd_pr/pfet_01v8.sym} 560 -740 0 0 {name=M1
L=2.0
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
C {sky130_fd_pr/pfet_01v8.sym} 810 -740 0 0 {name=M12
L=4.0
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
C {sky130_fd_pr/pfet_01v8.sym} 1040 -740 0 0 {name=M13
L=8.0
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
C {sky130_fd_pr/pfet_01v8.sym} 810 -630 0 0 {name=M14
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
C {sky130_fd_pr/pfet_01v8.sym} 1040 -630 0 0 {name=M15
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
C {devices/lab_pin.sym} 720 -190 0 1 {name=p15 sig_type=std_logic lab=vsin}
C {devices/lab_pin.sym} 630 -400 0 1 {name=p17 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 320 -640 0 0 {name=p25 sig_type=std_logic lab=weight_b[0]}
C {devices/lab_pin.sym} 540 -630 0 0 {name=p29 sig_type=std_logic lab=weight_b[1]}
C {devices/lab_pin.sym} 790 -630 0 0 {name=p38 sig_type=std_logic lab=weight_b[2]}
C {devices/lab_pin.sym} 1020 -630 0 0 {name=p37 sig_type=std_logic lab=weight_b[3]}
C {devices/iopin.sym} 60 -810 0 0 {name=p30 lab=JInhWp[0:3]


}
C {devices/lab_pin.sym} 270 -750 1 0 {name=p20 sig_type=std_logic lab=JInhWp[0]}
C {devices/lab_pin.sym} 540 -820 1 0 {name=p2 sig_type=std_logic lab=JInhWp[1]}
C {devices/lab_pin.sym} 790 -820 1 0 {name=p21 sig_type=std_logic lab=JInhWp[2]}
C {devices/lab_pin.sym} 1020 -820 1 0 {name=p22 sig_type=std_logic lab=JInhWp[3]}
C {devices/lab_pin.sym} 800 -320 0 0 {name=p14 sig_type=std_logic lab=GND}
