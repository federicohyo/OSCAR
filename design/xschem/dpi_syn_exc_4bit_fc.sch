v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 400 -310 400 -280 {
lab=#net1}
N 400 -220 400 -170 {
lab=#net2}
N 330 -360 360 -360 {
lab=spk}
N 400 -330 400 -310 {
lab=#net1}
N 400 -360 440 -360 {
lab=GND}
N 310 -250 360 -250 {
lab=vstdn}
N 400 -530 400 -520 {
lab=vsin}
N 400 -570 400 -530 {
lab=vsin}
N 400 -690 400 -650 {
lab=VDD}
N 400 -650 400 -630 {
lab=VDD}
N 400 -600 450 -600 {
lab=VDD}
N 450 -650 450 -600 {
lab=VDD}
N 400 -650 450 -650 {
lab=VDD}
N 320 -600 360 -600 {
lab=vtau}
N 400 -550 570 -550 {
lab=vsin}
N 570 -670 570 -630 {
lab=VDD}
N 570 -630 570 -610 {
lab=VDD}
N 570 -550 680 -550 {
lab=vsin}
N 720 -640 720 -600 {
lab=VDD}
N 720 -600 720 -580 {
lab=VDD}
N 720 -550 750 -550 {
lab=VDD}
N 750 -600 750 -550 {
lab=VDD}
N 720 -600 750 -600 {
lab=VDD}
N 720 -510 720 -490 {
lab=sout}
N 720 -520 720 -510 {
lab=sout}
N 400 -520 400 -470 {
lab=vsin}
N 400 -410 400 -390 {
lab=#net3}
N 440 -440 470 -440 {
lab=vsin}
N 470 -550 470 -440 {
lab=vsin}
N 230 -400 400 -400 {
lab=#net3}
N 230 -430 230 -400 {
lab=#net3}
N 230 -520 230 -490 {
lab=VDD}
N 160 -460 190 -460 {
lab=vthn}
N 230 -460 270 -460 {
lab=GND}
N 270 -460 270 -440 {
lab=GND}
N 270 -440 320 -440 {
lab=GND}
N 320 -440 350 -440 {
lab=GND}
N 350 -440 400 -440 {
lab=GND}
N 400 -300 620 -300 {
lab=#net1}
N 620 -300 620 -270 {
lab=#net1}
N 620 -210 620 -160 {
lab=#net4}
N 620 -240 660 -240 {
lab=GND}
N 660 -240 660 -190 {
lab=GND}
N 840 -210 840 -160 {
lab=#net5}
N 840 -240 880 -240 {
lab=GND}
N 880 -240 880 -190 {
lab=GND}
N 1040 -210 1040 -160 {
lab=#net6}
N 1040 -240 1080 -240 {
lab=GND}
N 1080 -240 1080 -190 {
lab=GND}
N 1040 -300 1040 -270 {
lab=#net1}
N 620 -300 920 -300 {
lab=#net1}
N 840 -300 840 -270 {
lab=#net1}
N 400 -110 400 -80 {
lab=GND}
N 400 -140 450 -140 {
lab=GND}
N 400 -90 420 -90 {
lab=GND}
N 420 -140 420 -90 {
lab=GND}
N 620 -130 660 -130 {
lab=GND}
N 660 -190 660 -130 {
lab=GND}
N 450 -250 450 -140 {
lab=GND}
N 430 -250 450 -250 {
lab=GND}
N 400 -250 430 -250 {
lab=GND}
N 620 -100 620 -80 {
lab=GND}
N 620 -90 660 -90 {
lab=GND}
N 660 -130 660 -90 {
lab=GND}
N 840 -100 840 -80 {
lab=GND}
N 840 -130 880 -130 {
lab=GND}
N 880 -190 880 -130 {
lab=GND}
N 880 -130 880 -100 {
lab=GND}
N 840 -100 880 -100 {
lab=GND}
N 1040 -130 1080 -130 {
lab=GND}
N 1080 -190 1080 -130 {
lab=GND}
N 1040 -100 1040 -80 {
lab=GND}
N 1040 -100 1080 -100 {
lab=GND}
N 1080 -130 1080 -100 {
lab=GND}
N 340 -320 340 -250 {
lab=vstdn}
N 580 -320 580 -240 {
lab=vstdn}
N 800 -320 800 -240 {
lab=vstdn}
N 1000 -320 1000 -240 {
lab=vstdn}
N 340 -320 880 -320 {
lab=vstdn}
N 400 -80 920 -80 {
lab=GND}
N 920 -300 1040 -300 {
lab=#net1}
N 880 -320 1000 -320 {
lab=vstdn}
N 920 -80 1040 -80 {
lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 380 -360 0 0 {name=M2
L=0.25
W=0.8
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
C {sky130_fd_pr/cap_mim_m3_1.sym} 570 -580 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8.sym} 380 -600 0 0 {name=M5
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
C {devices/lab_pin.sym} 400 -690 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 570 -670 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 700 -550 0 0 {name=M6
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
C {devices/lab_pin.sym} 720 -640 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 530 -550 3 0 {name=p22 sig_type=std_logic lab=vsin}
C {sky130_fd_pr/nfet_01v8.sym} 380 -250 0 0 {name=M1
L=0.5
W=0.8
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
C {sky130_fd_pr/nfet_01v8.sym} 420 -440 0 1 {name=M4
L=0.25
W=0.8
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
C {devices/lab_pin.sym} 320 -440 1 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 70 -170 0 0 {name=p1 lab=GND
}
C {devices/iopin.sym} 70 -150 0 0 {name=p16 lab=VDD}
C {devices/iopin.sym} 320 -600 2 0 {name=p10 lab=vtau

}
C {devices/iopin.sym} 310 -250 2 0 {name=p2 lab=vstdn

}
C {devices/ipin.sym} 330 -360 0 0 {name=p6 lab=spk

}
C {devices/opin.sym} 720 -490 1 0 {name=p8 lab=sout}
C {sky130_fd_pr/nfet_01v8.sym} 210 -460 0 0 {name=M3
L=0.25
W=0.8
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
C {devices/iopin.sym} 160 -460 2 0 {name=p9 lab=vthn

}
C {devices/lab_pin.sym} 230 -520 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 440 -360 2 0 {name=p13 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 600 -240 0 0 {name=M7
L=2.0
W=0.8
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
C {sky130_fd_pr/nfet_01v8.sym} 820 -240 0 0 {name=M8
L=4.0
W=0.8
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
C {devices/lab_pin.sym} 400 -80 3 0 {name=p17 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 1020 -240 0 0 {name=M9
L=8.0
W=0.8
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
C {sky130_fd_pr/nfet_01v8.sym} 380 -140 0 0 {name=M10
L=0.25
W=0.8
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
C {sky130_fd_pr/nfet_01v8.sym} 600 -130 0 0 {name=M11
L=0.25
W=0.8
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
C {sky130_fd_pr/nfet_01v8.sym} 820 -130 0 0 {name=M12
L=0.25
W=0.8
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
C {sky130_fd_pr/nfet_01v8.sym} 1020 -130 0 0 {name=M13
L=0.25
W=0.8
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
C {devices/ipin.sym} 190 -120 0 0 {name=p12 lab=weight[0:3]

}
C {devices/lab_pin.sym} 580 -130 0 0 {name=p14 lab=weight[1]

}
C {devices/lab_pin.sym} 800 -130 0 0 {name=p15 lab=weight[2]

}
C {devices/lab_pin.sym} 1000 -130 0 0 {name=p18 lab=weight[3]

}
C {devices/lab_pin.sym} 360 -140 0 0 {name=p19 lab=weight[0]

}
