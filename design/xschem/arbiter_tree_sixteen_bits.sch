v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Arbiter under test} 230 -280 0 0 0.4 0.4 {}
N 440 -210 490 -210 {
lab=#net1}
N 440 -190 490 -190 {
lab=#net2}
N 790 -190 840 -190 {
lab=#net3}
N 790 -210 840 -210 {
lab=#net4}
N 1140 -210 1190 -210 {
lab=#net5}
N 1140 -190 1190 -190 {
lab=#net6}
C {arbiter_two_bits.sym} 1340 -180 0 0 {name=x3}
C {devices/lab_pin.sym} 1490 -190 0 1 {name=p21 lab=ack_cpu}
C {devices/lab_pin.sym} 1490 -210 0 1 {name=p22 lab=req_cpu}
C {arbiter_two_bits.sym} 990 -180 0 0 {name=x1[0:1]}
C {arbiter_two_bits.sym} 640 -180 0 0 {name=x2[0:3]}
C {arbiter_two_bits.sym} 290 -180 0 0 {name=x3[0:7]}
C {devices/lab_pin.sym} 140 -210 0 0 {name=p3 lab=req[0:15]}
C {devices/lab_pin.sym} 140 -190 0 0 {name=p4 lab=ack[0:15]}
C {devices/ipin.sym} 370 -370 0 0 {name=p80 lab=req[0:15]}
C {devices/opin.sym} 370 -350 0 0 {name=p60 lab=ack[0:15]}
C {devices/ipin.sym} 710 -370 0 0 {name=p5 lab=ack_cpu}
C {devices/opin.sym} 710 -350 0 0 {name=p6 lab=req_cpu}
C {devices/lab_pin.sym} 1490 -170 0 1 {name=p7 lab=VDD}
C {devices/lab_pin.sym} 1490 -150 0 1 {name=p8 lab=GND}
C {devices/lab_pin.sym} 1140 -170 0 1 {name=p9 lab=VDD}
C {devices/lab_pin.sym} 1140 -150 0 1 {name=p10 lab=GND}
C {devices/lab_pin.sym} 790 -170 0 1 {name=p11 lab=VDD}
C {devices/lab_pin.sym} 790 -150 0 1 {name=p12 lab=GND}
C {devices/lab_pin.sym} 440 -170 0 1 {name=p13 lab=VDD}
C {devices/lab_pin.sym} 440 -150 0 1 {name=p14 lab=GND}
C {devices/iopin.sym} 370 -320 0 0 {name=p15 lab=VDD}
C {devices/iopin.sym} 370 -300 0 0 {name=p16 lab=GND}
