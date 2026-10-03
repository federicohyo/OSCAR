v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Arbiter under test} 220 -170 0 0 0.4 0.4 {}
N 430 -110 530 -110 {
lab=#net1}
N 430 -90 530 -90 {
lab=#net2}
C {arbiter_two_bits.sym} 680 -80 0 0 {name=x3}
C {devices/lab_pin.sym} 830 -90 0 1 {name=p21 lab=ack_cpu}
C {devices/lab_pin.sym} 830 -110 0 1 {name=p22 lab=req_cpu}
C {arbiter_two_bits.sym} 280 -80 0 0 {name=x1[0:1]}
C {devices/lab_pin.sym} 130 -110 0 0 {name=p3 lab=req[0:3]}
C {devices/lab_pin.sym} 130 -90 0 0 {name=p4 lab=ack[0:3]}
C {devices/ipin.sym} 360 -260 0 0 {name=p1 lab=req[0:3]}
C {devices/opin.sym} 360 -240 0 0 {name=p2 lab=ack[0:3]}
C {devices/ipin.sym} 700 -260 0 0 {name=p5 lab=ack_cpu}
C {devices/opin.sym} 700 -240 0 0 {name=p6 lab=req_cpu}
C {devices/lab_pin.sym} 830 -70 0 1 {name=p7 lab=VDD}
C {devices/lab_pin.sym} 830 -50 0 1 {name=p8 lab=GND}
C {devices/lab_pin.sym} 430 -70 0 1 {name=p9 lab=VDD}
C {devices/lab_pin.sym} 430 -50 0 1 {name=p10 lab=GND}
C {devices/iopin.sym} 360 -210 0 0 {name=p11 lab=VDD}
C {devices/iopin.sym} 360 -190 0 0 {name=p12 lab=GND}
