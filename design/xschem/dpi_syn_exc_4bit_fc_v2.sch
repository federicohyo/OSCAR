v {xschem version=3.4.7RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 400 -330 400 -300 {
lab=#net1}
N 400 -240 400 -190 {
lab=#net2}
N 330 -380 360 -380 {
lab=spk}
N 400 -350 400 -330 {
lab=#net1}
N 400 -380 440 -380 {
lab=GND}
N 310 -270 360 -270 {
lab=JExcWn[0]}
N 400 -550 400 -540 {
lab=vsin}
N 400 -590 400 -550 {
lab=vsin}
N 400 -710 400 -670 {
lab=aVDD}
N 400 -670 400 -650 {
lab=aVDD}
N 400 -620 450 -620 {
lab=aVDD}
N 450 -670 450 -620 {
lab=aVDD}
N 400 -670 450 -670 {
lab=aVDD}
N 320 -620 360 -620 {
lab=vtaup}
N 400 -570 570 -570 {
lab=vsin}
N 570 -690 570 -650 {
lab=aVDD}
N 570 -650 570 -630 {
lab=aVDD}
N 570 -570 680 -570 {
lab=vsin}
N 720 -660 720 -620 {
lab=aVDD}
N 720 -620 720 -600 {
lab=aVDD}
N 720 -570 750 -570 {
lab=aVDD}
N 750 -620 750 -570 {
lab=aVDD}
N 720 -620 750 -620 {
lab=aVDD}
N 720 -530 720 -510 {
lab=sout}
N 720 -540 720 -530 {
lab=sout}
N 400 -540 400 -490 {
lab=vsin}
N 400 -430 400 -410 {
lab=#net3}
N 440 -460 470 -460 {
lab=vsin}
N 470 -570 470 -460 {
lab=vsin}
N 230 -420 400 -420 {
lab=#net3}
N 230 -450 230 -420 {
lab=#net3}
N 230 -540 230 -510 {
lab=aVDD}
N 160 -480 190 -480 {
lab=vthn}
N 230 -480 270 -480 {
lab=GND}
N 270 -480 270 -460 {
lab=GND}
N 270 -460 320 -460 {
lab=GND}
N 320 -460 350 -460 {
lab=GND}
N 350 -460 400 -460 {
lab=GND}
N 400 -320 620 -320 {
lab=#net1}
N 620 -320 620 -290 {
lab=#net1}
N 620 -230 620 -180 {
lab=#net4}
N 620 -260 660 -260 {
lab=GND}
N 660 -260 660 -210 {
lab=GND}
N 840 -230 840 -180 {
lab=#net5}
N 840 -260 880 -260 {
lab=GND}
N 880 -260 880 -210 {
lab=GND}
N 1040 -230 1040 -180 {
lab=#net6}
N 1040 -260 1080 -260 {
lab=GND}
N 1080 -260 1080 -210 {
lab=GND}
N 1040 -320 1040 -290 {
lab=#net1}
N 620 -320 920 -320 {
lab=#net1}
N 840 -320 840 -290 {
lab=#net1}
N 400 -130 400 -100 {
lab=GND}
N 400 -160 450 -160 {
lab=GND}
N 400 -110 420 -110 {
lab=GND}
N 420 -160 420 -110 {
lab=GND}
N 620 -150 660 -150 {
lab=GND}
N 660 -210 660 -150 {
lab=GND}
N 450 -270 450 -160 {
lab=GND}
N 430 -270 450 -270 {
lab=GND}
N 400 -270 430 -270 {
lab=GND}
N 620 -120 620 -100 {
lab=GND}
N 620 -110 660 -110 {
lab=GND}
N 660 -150 660 -110 {
lab=GND}
N 840 -120 840 -100 {
lab=GND}
N 840 -150 880 -150 {
lab=GND}
N 880 -210 880 -150 {
lab=GND}
N 880 -150 880 -120 {
lab=GND}
N 840 -120 880 -120 {
lab=GND}
N 1040 -150 1080 -150 {
lab=GND}
N 1080 -210 1080 -150 {
lab=GND}
N 1040 -120 1040 -100 {
lab=GND}
N 1040 -120 1080 -120 {
lab=GND}
N 1080 -150 1080 -120 {
lab=GND}
N 400 -100 920 -100 {
lab=GND}
N 920 -320 1040 -320 {
lab=#net1}
N 920 -100 1040 -100 {
lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 380 -380 0 0 {name=M2
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
C {sky130_fd_pr/cap_mim_m3_1.sym} 570 -600 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 380 -620 0 0 {name=M5
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
C {devices/lab_pin.sym} 400 -710 0 0 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 570 -690 0 0 {name=p3 sig_type=std_logic lab=aVDD}
C {sky130_fd_pr/pfet_01v8.sym} 700 -570 0 0 {name=M6
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
C {devices/lab_pin.sym} 720 -660 0 0 {name=p7 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 530 -570 3 0 {name=p22 sig_type=std_logic lab=vsin}
C {sky130_fd_pr/nfet_01v8.sym} 380 -270 0 0 {name=M1
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
C {sky130_fd_pr/nfet_01v8.sym} 420 -460 0 1 {name=M4
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
C {devices/lab_pin.sym} 320 -460 1 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 70 -190 0 0 {name=p1 lab=GND
}
C {devices/iopin.sym} 70 -170 0 0 {name=p16 lab=aVDD}
C {devices/iopin.sym} 320 -620 2 0 {name=p10 lab=vtaup

}
C {devices/ipin.sym} 330 -380 0 0 {name=p6 lab=spk

}
C {devices/opin.sym} 720 -510 1 0 {name=p8 lab=sout}
C {sky130_fd_pr/nfet_01v8.sym} 210 -480 0 0 {name=M3
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
C {devices/iopin.sym} 160 -480 2 0 {name=p9 lab=vthn

}
C {devices/lab_pin.sym} 230 -540 0 0 {name=p11 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 440 -380 2 0 {name=p13 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 600 -260 0 0 {name=M7
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
C {sky130_fd_pr/nfet_01v8.sym} 820 -260 0 0 {name=M8
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
C {devices/lab_pin.sym} 400 -100 3 0 {name=p17 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 1020 -260 0 0 {name=M9
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
C {sky130_fd_pr/nfet_01v8.sym} 380 -160 0 0 {name=M10
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
C {sky130_fd_pr/nfet_01v8.sym} 600 -150 0 0 {name=M11
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
C {sky130_fd_pr/nfet_01v8.sym} 820 -150 0 0 {name=M12
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
C {sky130_fd_pr/nfet_01v8.sym} 1020 -150 0 0 {name=M13
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
C {devices/ipin.sym} 190 -140 0 0 {name=p12 lab=weight[0:3]

}
C {devices/lab_pin.sym} 580 -150 0 0 {name=p14 lab=weight[1]

}
C {devices/lab_pin.sym} 800 -150 0 0 {name=p15 lab=weight[2]

}
C {devices/lab_pin.sym} 1000 -150 0 0 {name=p18 lab=weight[3]

}
C {devices/lab_pin.sym} 360 -160 0 0 {name=p19 lab=weight[0]

}
C {devices/iopin.sym} 200 -225 0 1 {name=p2 lab=JExcWn[0:3]


}
C {devices/lab_pin.sym} 310 -270 0 0 {name=p20 lab=JExcWn[0]

}
C {devices/lab_pin.sym} 580 -260 0 0 {name=p21 lab=JExcWn[1]

}
C {devices/lab_pin.sym} 800 -260 0 0 {name=p23 lab=JExcWn[2]

}
C {devices/lab_pin.sym} 1000 -260 0 0 {name=p24 lab=JExcWn[3]

}
