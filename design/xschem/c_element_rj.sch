v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {c Element as Van Berkel 1992 VLSI journal} 570 -530 0 0 0.4 0.4 {}
T {With reset modification by R. Jordans

Transistor sizing according to sky130_fd_sc_hd library} 570 -500 0 0 0.2 0.2 {}
N 120 -20 170 -20 {
lab=dGND}
N 120 -30 120 -20 {
lab=dGND}
N 120 -540 120 -470 {
lab=dVDD}
N 30 -60 80 -60 {
lab=a}
N 540 -280 570 -280 {
lab=c}
N 280 -30 280 -20 {
lab=dGND}
N 200 -80 200 -50 {
lab=c}
N 120 -180 120 -80 {
lab=#net1}
N 120 -120 170 -120 {
lab=#net1}
N 230 -120 280 -120 {
lab=#net2}
N 280 -120 280 -90 {
lab=#net2}
N 270 -180 270 -120 {
lab=#net2}
N 120 -310 120 -240 {
lab=#net3}
N 120 -410 120 -370 {
lab=#net4}
N 270 -420 270 -370 {
lab=#net5}
N 270 -310 270 -240 {
lab=#net3}
N 430 -340 460 -340 {
lab=#net6}
N 430 -340 430 -210 {
lab=#net6}
N 430 -210 460 -210 {
lab=#net6}
N 500 -310 500 -240 {
lab=c}
N 500 -520 500 -370 {
lab=dVDD}
N 120 -520 470 -520 {
lab=dVDD}
N 270 -520 270 -470 {
lab=dVDD}
N 120 -370 160 -370 {
lab=#net4}
N 220 -370 270 -370 {
lab=#net5}
N 190 -430 190 -400 {
lab=c}
N 500 -180 500 -170 {
lab=dGND}
N 500 -170 500 -20 {
lab=dGND}
N 50 -440 80 -440 {
lab=a}
N 60 -340 80 -340 {
lab=b}
N 40 -210 80 -210 {
lab=b}
N 310 -440 330 -440 {
lab=b}
N 310 -340 340 -340 {
lab=a}
N 310 -210 340 -210 {
lab=a}
N 320 -60 350 -60 {
lab=b}
N 500 -280 540 -280 {
lab=c}
N 120 -280 270 -280 {
lab=#net3}
N 430 -380 430 -340 {
lab=#net6}
N 430 -520 430 -440 {
lab=dVDD}
N 370 -410 390 -410 {
lab=nrst}
N 270 -280 330 -280 {
lab=#net3}
N 420 -280 430 -280 {
lab=#net6}
N 170 -20 280 -20 {
lab=dGND}
N 390 -20 500 -20 {
lab=dGND}
N 320 -20 360 -20 {
lab=dGND}
N 280 -20 320 -20 {
lab=dGND}
N 330 -280 360 -280 {
lab=#net3}
N 360 -20 390 -20 {
lab=dGND}
N 470 -520 500 -520 {
lab=dVDD}
N 390 -410 390 -320 {
lab=nrst}
N 500 -340 520 -340 {
lab=dVDD}
N 430 -410 450 -410 {
lab=dVDD}
N 250 -440 270 -440 {
lab=dVDD}
N 120 -440 140 -440 {
lab=dVDD}
N 120 -340 140 -340 {
lab=dVDD}
N 250 -340 270 -340 {
lab=dVDD}
N 190 -370 190 -350 {
lab=dVDD}
N 500 -210 510 -210 {
lab=dGND}
N 390 -280 390 -270 {
lab=dGND}
N 120 -210 130 -210 {
lab=dGND}
N 260 -210 270 -210 {
lab=dGND}
N 200 -130 200 -120 {
lab=dGND}
N 120 -60 130 -60 {
lab=dGND}
N 270 -60 280 -60 {
lab=dGND}
C {devices/iopin.sym} 770 -170 0 0 {name=p13 lab=dGND
}
C {devices/iopin.sym} 770 -190 0 0 {name=p16 lab=dVDD}
C {devices/opin.sym} 570 -280 0 0 {name=p17 lab=c}
C {devices/ipin.sym} 790 -330 0 0 {name=p1 lab=b


}
C {devices/lab_wire.sym} 120 -540 0 0 {name=p4 sig_type=std_logic lab=dVDD
}
C {devices/lab_wire.sym} 200 -50 0 1 {name=p5 sig_type=std_logic lab=c
}
C {devices/lab_wire.sym} 190 -430 0 1 {name=p8 sig_type=std_logic lab=c
}
C {devices/ipin.sym} 790 -350 0 0 {name=p9 lab=a


}
C {devices/lab_wire.sym} 30 -60 0 0 {name=p6 sig_type=std_logic lab=a}
C {devices/lab_wire.sym} 50 -440 0 0 {name=p10 sig_type=std_logic lab=a}
C {devices/lab_wire.sym} 340 -340 2 0 {name=p11 sig_type=std_logic lab=a}
C {devices/lab_wire.sym} 340 -210 2 0 {name=p12 sig_type=std_logic lab=a}
C {devices/lab_wire.sym} 330 -440 0 1 {name=p14 sig_type=std_logic lab=b}
C {devices/lab_wire.sym} 60 -340 0 1 {name=p15 sig_type=std_logic lab=b}
C {devices/lab_wire.sym} 40 -210 0 1 {name=p18 sig_type=std_logic lab=b}
C {devices/lab_wire.sym} 350 -60 0 1 {name=p19 sig_type=std_logic lab=b}
C {devices/ipin.sym} 790 -380 0 0 {name=p2 lab=nrst


}
C {devices/lab_pin.sym} 370 -410 0 0 {name=l1 sig_type=std_logic lab=nrst}
C {devices/lab_wire.sym} 500 -20 0 1 {name=p3 sig_type=std_logic lab=dGND
}
C {sky130_fd_pr/pfet_01v8.sym} 480 -340 0 0 {name=M14
L=0.15
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
C {devices/lab_pin.sym} 520 -340 2 0 {name=p26 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/pfet_01v8.sym} 410 -410 0 0 {name=M5
L=0.15
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
C {devices/lab_pin.sym} 450 -410 2 0 {name=p7 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/pfet_01v8.sym} 290 -440 0 1 {name=M6
L=0.15
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
C {devices/lab_pin.sym} 250 -440 2 1 {name=p20 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/pfet_01v8.sym} 100 -440 0 0 {name=M4
L=0.15
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
C {devices/lab_pin.sym} 140 -440 2 0 {name=p21 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/pfet_01v8.sym} 100 -340 0 0 {name=M7
L=0.15
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
C {devices/lab_pin.sym} 140 -340 2 0 {name=p22 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/pfet_01v8.sym} 290 -340 0 1 {name=M8
L=0.15
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
C {devices/lab_pin.sym} 250 -340 2 1 {name=p23 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/pfet_01v8.sym} 190 -390 3 1 {name=M10
L=0.15
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
C {devices/lab_pin.sym} 190 -350 1 1 {name=p24 sig_type=std_logic lab=dVDD}
C {sky130_fd_pr/nfet_01v8.sym} 480 -210 0 0 {name=M12
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
C {devices/lab_pin.sym} 510 -210 2 0 {name=p25 sig_type=std_logic lab=dGND}
C {sky130_fd_pr/nfet_01v8.sym} 390 -300 3 1 {name=M1
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
C {devices/lab_pin.sym} 390 -270 3 0 {name=p27 sig_type=std_logic lab=dGND}
C {sky130_fd_pr/nfet_01v8.sym} 100 -210 0 0 {name=M2
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
C {devices/lab_pin.sym} 130 -210 2 0 {name=p28 sig_type=std_logic lab=dGND}
C {sky130_fd_pr/nfet_01v8.sym} 290 -210 0 1 {name=M3
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
C {devices/lab_pin.sym} 260 -210 2 1 {name=p29 sig_type=std_logic lab=dGND}
C {sky130_fd_pr/nfet_01v8.sym} 200 -100 1 1 {name=M9
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
C {devices/lab_pin.sym} 200 -130 3 1 {name=p30 sig_type=std_logic lab=dGND}
C {sky130_fd_pr/nfet_01v8.sym} 100 -60 0 0 {name=M11
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
C {devices/lab_pin.sym} 130 -60 0 1 {name=p31 sig_type=std_logic lab=dGND}
C {sky130_fd_pr/nfet_01v8.sym} 300 -60 0 1 {name=M13
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
C {devices/lab_pin.sym} 270 -60 2 1 {name=p32 sig_type=std_logic lab=dGND}
