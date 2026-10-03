v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {General Purpose Open Source Operational Amplifier (OpAmp)

https://github.com/diegohernando/caravel_fulgor_opamp/tree/master?tab=readme-ov-file} 200 -760 0 0 0.4 0.4 {}
N 580 -170 580 -90 { lab=vss}
N 860 -170 860 -90 { lab=vss}
N 580 -90 650 -90 { lab=vss}
N 650 -90 860 -90 { lab=vss}
N 660 -270 660 -200 { lab=#net1}
N 500 -200 580 -200 { lab=vss}
N 500 -200 500 -90 { lab=vss}
N 500 -90 580 -90 { lab=vss}
N 860 -200 930 -200 { lab=#net2}
N 930 -200 930 -90 { lab=#net2}
N 860 -370 860 -230 { lab=voe1}
N 580 -490 580 -430 { lab=vp}
N 580 -490 860 -490 { lab=vp}
N 860 -490 860 -430 { lab=vp}
N 580 -400 640 -400 { lab=vp}
N 640 -490 640 -400 { lab=vp}
N 800 -490 800 -400 { lab=vp}
N 720 -540 720 -490 { lab=vp}
N 1180 -610 1180 -600 { lab=vdd}
N 1180 -630 1180 -610 { lab=vdd}
N 720 -630 1180 -630 { lab=vdd}
N 720 -630 720 -600 { lab=vdd}
N 1180 -570 1260 -570 { lab=vdd}
N 1260 -630 1260 -570 { lab=vdd}
N 1180 -630 1260 -630 { lab=vdd}
N 340 -630 340 -600 { lab=vdd}
N 340 -630 720 -630 { lab=vdd}
N 340 -490 440 -490 { lab=iref}
N 440 -570 440 -490 { lab=iref}
N 1060 -570 1140 -570 { lab=iref}
N 260 -570 340 -570 { lab=vdd}
N 260 -630 260 -570 { lab=vdd}
N 260 -630 340 -630 { lab=vdd}
N 720 -570 800 -570 { lab=vdd}
N 800 -630 800 -570 { lab=vdd}
N 800 -400 860 -400 { lab=#net3}
N 580 -370 580 -230 { lab=#net4}
N 580 -270 660 -270 { lab=#net1}
N 380 -570 440 -570 { lab=#net5}
N 560 -570 680 -570 { lab=iref}
N 440 -570 560 -570 { lab=iref}
N 620 -200 820 -200 { lab=#net6}
N 340 -540 340 -490 { lab=#net7}
N 470 -400 540 -400 { lab=#net8}
N 1040 -320 1090 -320 { lab=#net9}
N 1010 -380 1010 -360 { lab=vdd}
N 1010 -320 1010 -240 { lab=vss}
N 860 -320 980 -320 { lab=voe1}
N 1150 -320 1180 -320 { lab=#net10}
N 240 -630 260 -630 { lab=#net11}
N 240 -90 500 -90 { lab=#net12}
N 900 -400 960 -400 { lab=#net13}
N 240 -490 340 -490 { lab=#net14}
N 860 -90 1180 -90 { lab=#net15}
N 1180 -90 1270 -90 { lab=#net15}
N 1270 -190 1270 -90 { lab=#net15}
N 1180 -190 1270 -190 { lab=#net15}
N 960 -190 1140 -190 { lab=voe1}
N 960 -320 960 -190 { lab=voe1}
N 1180 -320 1180 -220 { lab=#net10}
N 1180 -540 1180 -320 { lab=#net10}
N 1180 -370 1320 -370 { lab=#net10}
N 1180 -160 1180 -90 { lab=#net15}
C {sky130_fd_pr/pfet_01v8.sym} 560 -400 0 0 {name=M1
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=200
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 880 -400 0 1 {name=M2
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=200
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 600 -200 0 1 {name=M3
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 840 -200 0 0 {name=M4
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 700 -570 0 0 {name=M5
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1160 -570 0 0 {name=M7
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=150
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 360 -570 0 1 {name=M8
L=0.3
W=3
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=15
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_wire.sym} 560 -630 0 0 {name=p7 sig_type=std_logic lab=vdd
}
C {devices/lab_wire.sym} 560 -570 0 0 {name=p9 sig_type=std_logic lab=iref

}
C {devices/lab_wire.sym} 690 -490 0 0 {name=p12 sig_type=std_logic lab=vp}
C {devices/lab_pin.sym} 1060 -570 0 0 {name=p8 sig_type=std_logic lab=iref}
C {devices/lab_wire.sym} 730 -90 0 0 {name=p16 sig_type=std_logic lab=vss
}
C {devices/lab_wire.sym} 1270 -370 0 0 {name=p10 sig_type=std_logic lab=vout
}
C {devices/lab_wire.sym} 740 -200 0 0 {name=p15 sig_type=std_logic lab=vbn}
C {sky130_fd_pr/nfet_01v8.sym} 1010 -340 1 0 {name=M9
L=0.15
W=0.75
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=6
model=nfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 1010 -380 2 0 {name=p14 sig_type=std_logic lab=vdd
}
C {devices/lab_pin.sym} 1010 -240 2 0 {name=p11 sig_type=std_logic lab=vss
}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1120 -320 1 0 {name=C1 model=cap_mim_m3_1 W=17.55 L=15 MF=6 spiceprefix=X}
C {devices/iopin.sym} 240 -630 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} 240 -90 2 0 {name=p2 lab=vss}
C {devices/ipin.sym} 470 -400 0 0 {name=p3 lab=vin_n}
C {devices/ipin.sym} 960 -400 2 0 {name=p4 lab=vin_p}
C {devices/ipin.sym} 240 -490 0 0 {name=p5 lab=iref}
C {sky130_fd_pr/nfet_01v8.sym} 1160 -190 0 0 {name=M6
L=0.45
W=4.5
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=150
model=nfet_01v8
spiceprefix=X
}
C {devices/lab_wire.sym} 920 -320 0 0 {name=p13 sig_type=std_logic lab=voe1}
C {devices/opin.sym} 1320 -370 0 0 {name=p6 lab=vout}
