v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 350 -275 350 -235 {
lab=#net1}
N 350 -175 350 -150 {
lab=#net2}
N 350 -95 350 -50 {
lab=GND}
N 350 -75 385 -75 {
lab=GND}
N 385 -305 385 -75 {
lab=GND}
N 350 -305 385 -305 {
lab=GND}
N 350 -205 385 -205 {
lab=GND}
N 345 -125 385 -125 {
lab=GND}
N 350 -385 350 -335 {
lab=#net3}
N 565 -275 565 -235 {
lab=#net4}
N 565 -175 565 -150 {
lab=#net5}
N 565 -95 565 -50 {
lab=GND}
N 565 -75 600 -75 {
lab=GND}
N 600 -305 600 -75 {
lab=GND}
N 565 -305 600 -305 {
lab=GND}
N 565 -205 600 -205 {
lab=GND}
N 560 -125 600 -125 {
lab=GND}
N 770 -275 770 -235 {
lab=#net6}
N 770 -175 770 -150 {
lab=#net7}
N 770 -95 770 -50 {
lab=GND}
N 770 -75 805 -75 {
lab=GND}
N 805 -305 805 -75 {
lab=GND}
N 770 -305 805 -305 {
lab=GND}
N 770 -205 805 -205 {
lab=GND}
N 765 -125 805 -125 {
lab=GND}
N 970 -275 970 -235 {
lab=#net8}
N 970 -175 970 -150 {
lab=#net9}
N 970 -95 970 -50 {
lab=GND}
N 970 -75 1005 -75 {
lab=GND}
N 1005 -305 1005 -75 {
lab=GND}
N 970 -305 1005 -305 {
lab=GND}
N 970 -205 1005 -205 {
lab=GND}
N 965 -125 1005 -125 {
lab=GND}
N 565 -350 565 -335 {
lab=#net3}
N 565 -350 575 -350 {
lab=#net3}
N 575 -360 575 -350 {
lab=#net3}
N 350 -360 575 -360 {
lab=#net3}
N 575 -360 770 -360 {
lab=#net3}
N 770 -360 780 -360 {
lab=#net3}
N 780 -360 780 -350 {
lab=#net3}
N 770 -350 780 -350 {
lab=#net3}
N 770 -350 770 -335 {
lab=#net3}
N 780 -360 970 -360 {
lab=#net3}
N 970 -360 970 -335 {
lab=#net3}
N 515 -205 525 -205 {
lab=JInhWn[1]}
N 720 -205 730 -205 {
lab=JInhWn[2]}
N 910 -210 910 -205 {
lab=JInhWn[3]}
N 910 -205 930 -205 {
lab=JInhWn[3]}
N 290 -125 310 -125 {
lab=SpkI}
N 310 -125 310 -65 {
lab=SpkI}
N 310 -65 340 -65 {
lab=SpkI}
N 340 -65 340 -60 {
lab=SpkI}
N 340 -60 360 -60 {
lab=SpkI}
N 360 -65 360 -60 {
lab=SpkI}
N 360 -65 525 -65 {
lab=SpkI}
N 525 -125 525 -65 {
lab=SpkI}
N 525 -65 555 -65 {
lab=SpkI}
N 555 -65 555 -60 {
lab=SpkI}
N 555 -60 580 -60 {
lab=SpkI}
N 580 -65 580 -60 {
lab=SpkI}
N 580 -65 730 -65 {
lab=SpkI}
N 730 -125 730 -65 {
lab=SpkI}
N 730 -65 760 -65 {
lab=SpkI}
N 760 -65 760 -60 {
lab=SpkI}
N 760 -60 775 -60 {
lab=SpkI}
N 775 -65 775 -60 {
lab=SpkI}
N 775 -65 930 -65 {
lab=SpkI}
N 930 -125 930 -65 {
lab=SpkI}
N 185 -482.5 185 -452.5 {
lab=nSpkI}
N 145 -512.5 145 -422.5 {
lab=SpkI}
N 185 -512.5 215 -512.5 {
lab=VDD}
N 215 -542.5 215 -512.5 {
lab=VDD}
N 185 -422.5 225 -422.5 {
lab=GND}
N 225 -422.5 225 -392.5 {
lab=GND}
N 185 -567.5 185 -542.5 {
lab=VDD}
N 185 -542.5 215 -542.5 {
lab=VDD}
N 185 -392.5 225 -392.5 {
lab=GND}
N 185 -392.5 185 -377.5 {
lab=GND}
N 185 -467.5 210 -467.5 {
lab=nSpkI}
N 350 -385 415 -385 {
lab=#net3}
N 632.5 -470 712.5 -470 {
lab=#net3}
N 415 -385 712.5 -385 {
lab=#net3}
N 712.5 -470 712.5 -385 {
lab=#net3}
C {devices/iopin.sym} 55 -125 0 0 {name=p13 lab=GND
}
C {sky130_fd_pr/nfet_01v8.sym} 330 -305 0 0 {name=M2
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
C {sky130_fd_pr/nfet_01v8.sym} 330 -205 0 0 {name=M3
L=1.0
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
C {sky130_fd_pr/nfet_01v8.sym} 330 -125 0 0 {name=M1
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
C {devices/lab_pin.sym} 350 -50 0 0 {name=p26 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 310 -305 0 0 {name=p1 lab=weight[0]

}
C {devices/lab_pin.sym} 310 -205 2 1 {name=p12 lab=JInhWn[0]


}
C {devices/opin.sym} 632.5 -490 0 0 {name=p8 lab=sout}
C {devices/ipin.sym} 290 -125 2 1 {name=p18 lab=SpkI


}
C {sky130_fd_pr/nfet_01v8.sym} 545 -305 0 0 {name=M4
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
C {devices/lab_pin.sym} 565 -50 0 0 {name=p2 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 525 -305 0 0 {name=p3 lab=weight[1]

}
C {devices/lab_pin.sym} 515 -205 2 1 {name=p4 lab=JInhWn[1]


}
C {devices/lab_pin.sym} 770 -50 0 0 {name=p5 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 730 -305 0 0 {name=p6 lab=weight[2]

}
C {devices/lab_pin.sym} 720 -205 2 1 {name=p7 lab=JInhWn[2]


}
C {devices/lab_pin.sym} 970 -50 0 0 {name=p9 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 930 -305 0 0 {name=p10 lab=weight[3]

}
C {devices/lab_pin.sym} 910 -210 2 1 {name=p11 lab=JInhWn[3]


}
C {sky130_fd_pr/nfet_01v8.sym} 545 -205 0 0 {name=M5
L=1.0
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
C {sky130_fd_pr/nfet_01v8.sym} 545 -125 0 0 {name=M6
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
C {sky130_fd_pr/nfet_01v8.sym} 750 -305 0 0 {name=M7
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
C {sky130_fd_pr/nfet_01v8.sym} 750 -205 0 0 {name=M8
L=1.0
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
C {sky130_fd_pr/nfet_01v8.sym} 750 -125 0 0 {name=M9
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
C {sky130_fd_pr/nfet_01v8.sym} 950 -305 0 0 {name=M10
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
C {sky130_fd_pr/nfet_01v8.sym} 950 -205 0 0 {name=M11
L=1.0
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
C {sky130_fd_pr/nfet_01v8.sym} 950 -125 0 0 {name=M12
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
C {devices/iopin.sym} 57.5 -97.5 0 0 {name=p14 lab=VDD
}
C {devices/lab_pin.sym} 145 -467.5 0 0 {name=p15 sig_type=std_logic lab=SpkI}
C {sky130_fd_pr/pfet_01v8.sym} 165 -512.5 0 0 {name=M16
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
C {devices/lab_pin.sym} 185 -567.5 1 0 {name=p27 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} 165 -422.5 0 0 {name=M17
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
C {devices/lab_pin.sym} 185 -377.5 0 0 {name=p16 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 210 -467.5 0 1 {name=p17 sig_type=std_logic lab=nSpkI}
C {devices/lab_pin.sym} 632.5 -430 2 0 {name=p20 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 632.5 -450 2 0 {name=p21 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 332.5 -470 0 0 {name=p22 sig_type=std_logic lab=SpkI}
C {devices/lab_pin.sym} 332.5 -490 2 1 {name=p19 sig_type=std_logic lab=nSpkI}
C {tg.sym} 482.5 -460 0 0 {name=x1}
C {devices/iopin.sym} 70 -155 2 0 {name=p23 lab=JInhWn[0:3]


}
C {devices/ipin.sym} 70 -185 0 0 {name=p24 lab=weight[0:3]

}
