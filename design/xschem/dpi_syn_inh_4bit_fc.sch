v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 540 -470 540 -430 {
lab=#net1}
N 540 -430 540 -410 {
lab=#net1}
N 540 -380 590 -380 {
lab=VDD}
N 540 -350 540 -330 {
lab=#net2}
N 620 -270 620 -260 {
lab=#net2}
N 540 -270 620 -270 {
lab=#net2}
N 470 -270 540 -270 {
lab=#net2}
N 470 -270 470 -260 {
lab=#net2}
N 470 -230 620 -230 {
lab=VDD}
N 360 -230 430 -230 {
lab=vthrdp}
N 470 -200 470 -160 {
lab=GND}
N 620 -80 620 -40 {
lab=GND}
N 580 -110 620 -110 {
lab=GND}
N 580 -110 580 -60 {
lab=GND}
N 580 -60 620 -60 {
lab=GND}
N 660 -110 710 -110 {
lab=vtaun}
N 660 -230 730 -230 {
lab=vsin}
N 620 -200 620 -140 {
lab=vsin}
N 730 -230 860 -230 {
lab=vsin}
N 900 -230 950 -230 {
lab=GND}
N 950 -230 950 -130 {
lab=GND}
N 900 -130 950 -130 {
lab=GND}
N 900 -280 900 -260 {
lab=sout}
N 140 -390 140 -370 {
lab=#net3}
N 140 -340 160 -340 {
lab=GND}
N 160 -340 160 -310 {
lab=GND}
N 140 -310 160 -310 {
lab=GND}
N 140 -310 140 -280 {
lab=GND}
N 100 -420 100 -340 {
lab=spk}
N 60 -380 100 -380 {
lab=spk}
N 140 -500 140 -450 {
lab=VDD}
N 360 -380 500 -380 {
lab=#net3}
N 620 -170 680 -170 {
lab=vsin}
N 680 -230 680 -170 {
lab=vsin}
N 140 -420 170 -420 {
lab=VDD}
N 170 -460 170 -420 {
lab=VDD}
N 140 -460 170 -460 {
lab=VDD}
N 320 -790 320 -760 {
lab=VDD}
N 320 -700 320 -650 {
lab=#net4}
N 320 -810 320 -790 {
lab=VDD}
N 230 -730 280 -730 {
lab=vstdp}
N 320 -780 540 -780 {
lab=VDD}
N 540 -780 540 -750 {
lab=VDD}
N 540 -690 540 -640 {
lab=#net5}
N 540 -720 580 -720 {
lab=VDD}
N 580 -720 580 -670 {
lab=VDD}
N 790 -690 790 -640 {
lab=#net6}
N 790 -720 830 -720 {
lab=VDD}
N 830 -720 830 -670 {
lab=VDD}
N 1020 -690 1020 -640 {
lab=#net7}
N 1020 -720 1060 -720 {
lab=VDD}
N 1060 -720 1060 -670 {
lab=VDD}
N 1020 -780 1020 -750 {
lab=VDD}
N 540 -780 840 -780 {
lab=VDD}
N 790 -780 790 -750 {
lab=VDD}
N 320 -590 320 -560 {
lab=#net1}
N 320 -620 370 -620 {
lab=VDD}
N 540 -610 580 -610 {
lab=VDD}
N 580 -670 580 -610 {
lab=VDD}
N 370 -730 370 -620 {
lab=VDD}
N 350 -730 370 -730 {
lab=VDD}
N 320 -730 350 -730 {
lab=VDD}
N 540 -580 540 -560 {
lab=#net1}
N 790 -580 790 -560 {
lab=#net1}
N 790 -610 830 -610 {
lab=VDD}
N 830 -670 830 -610 {
lab=VDD}
N 1020 -610 1060 -610 {
lab=VDD}
N 1060 -670 1060 -610 {
lab=VDD}
N 1020 -580 1020 -560 {
lab=#net1}
N 260 -800 260 -730 {
lab=vstdp}
N 500 -800 500 -720 {
lab=vstdp}
N 750 -800 750 -720 {
lab=vstdp}
N 980 -800 980 -720 {
lab=vstdp}
N 260 -800 800 -800 {
lab=vstdp}
N 320 -560 840 -560 {
lab=#net1}
N 140 -380 360 -380 {
lab=#net3}
N 540 -330 540 -270 {
lab=#net2}
N 540 -560 540 -470 {
lab=#net1}
N 1060 -780 1060 -720 {
lab=VDD}
N 1010 -780 1060 -780 {
lab=VDD}
N 830 -780 830 -720 {
lab=VDD}
N 580 -780 580 -720 {
lab=VDD}
N 370 -780 370 -730 {
lab=VDD}
N 900 -140 900 -130 {
lab=GND}
N 840 -560 1020 -560 {
lab=#net1}
N 840 -780 1010 -780 {
lab=VDD}
N 800 -800 980 -800 {
lab=vstdp}
C {sky130_fd_pr/pfet_01v8.sym} 520 -380 0 0 {name=M5
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
C {devices/lab_pin.sym} 320 -810 1 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/ipin.sym} 60 -380 0 0 {name=p1 lab=spk

}
C {devices/iopin.sym} 230 -730 2 0 {name=p2 lab=vstdp

}
C {sky130_fd_pr/pfet_01v8.sym} 450 -230 0 0 {name=M2
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
C {sky130_fd_pr/pfet_01v8.sym} 640 -230 0 1 {name=M3
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
C {devices/iopin.sym} 360 -230 2 0 {name=p3 lab=vthrdp

}
C {devices/lab_pin.sym} 470 -160 0 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 620 -40 0 0 {name=p6 sig_type=std_logic lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 640 -110 0 1 {name=M4
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
C {devices/iopin.sym} 710 -110 0 0 {name=p7 lab=vtaun

}
C {sky130_fd_pr/nfet_01v8.sym} 880 -230 0 0 {name=M6
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
C {devices/lab_pin.sym} 900 -130 0 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 900 -280 3 0 {name=p9 lab=sout}
C {sky130_fd_pr/nfet_01v8.sym} 120 -340 0 0 {name=M7
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
C {sky130_fd_pr/pfet_01v8.sym} 120 -420 0 0 {name=M8
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
C {devices/lab_pin.sym} 140 -280 0 0 {name=p10 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 140 -500 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} 800 -50 0 0 {name=p12 lab=GND
}
C {devices/iopin.sym} 800 -30 0 0 {name=p16 lab=VDD}
C {devices/lab_pin.sym} 540 -230 3 0 {name=p13 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/cap_mim_m3_1.sym} 770 -200 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 770 -170 0 0 {name=p14 sig_type=std_logic lab=GND}
C {devices/ipin.sym} 215 -650 0 0 {name=p18 lab=weight_b[0:3]

}
C {sky130_fd_pr/pfet_01v8.sym} 300 -730 0 0 {name=M9
L=0.4
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
C {sky130_fd_pr/pfet_01v8.sym} 300 -620 0 0 {name=M10
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
C {sky130_fd_pr/pfet_01v8.sym} 520 -610 0 0 {name=M11
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
C {sky130_fd_pr/pfet_01v8.sym} 520 -720 0 0 {name=M1
L=1.5
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
C {sky130_fd_pr/pfet_01v8.sym} 770 -720 0 0 {name=M12
L=3.0
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
C {sky130_fd_pr/pfet_01v8.sym} 1000 -720 0 0 {name=M13
L=6.0
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
C {sky130_fd_pr/pfet_01v8.sym} 770 -610 0 0 {name=M14
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
C {sky130_fd_pr/pfet_01v8.sym} 1000 -610 0 0 {name=M15
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
C {devices/lab_pin.sym} 730 -230 1 0 {name=p15 sig_type=std_logic lab=vsin}
C {devices/lab_pin.sym} 590 -380 0 1 {name=p17 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 280 -620 0 0 {name=p25 sig_type=std_logic lab=weight_b[0]}
C {devices/ammeter.sym} 900 -170 0 0 {name=Vmeas savecurrent=true}
C {devices/lab_pin.sym} 500 -610 0 0 {name=p29 sig_type=std_logic lab=weight_b[1]}
C {devices/lab_pin.sym} 750 -610 0 0 {name=p38 sig_type=std_logic lab=weight_b[2]}
C {devices/lab_pin.sym} 980 -610 0 0 {name=p37 sig_type=std_logic lab=weight_b[3]}
