v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 200 -410 275 -410 {
lab=latchAddr}
N 455 -410 500 -410 {
lab=ack_neu_latched[0:3]}
N 200 -390 275 -390 {
lab=ack_neu[0:3]}
N 420 -240 420 -220 {
lab=#net1}
N 420 -240 450 -240 {
lab=#net1}
N 420 -280 450 -280 {
lab=#net2}
N 420 -300 420 -280 {
lab=#net2}
N 570 -260 595 -260 {
lab=latchAddr}
C {sky130_stdcells/dfrtp_1.sym} 365 -390 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 155 -225 0 0 {name=p45 lab=ack_neu[0:3]

}
C {devices/ipin.sym} 95 -195 0 0 {name=p31 lab=nRes}
C {devices/lab_pin.sym} 95 -195 2 0 {name=p32 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 275 -370 2 1 {name=p2 sig_type=std_logic lab=nRes}
C {devices/opin.sym} 500 -410 0 0 {name=p5 lab=ack_neu_latched[0:3]

}
C {devices/lab_pin.sym} 200 -390 2 1 {name=p1 sig_type=std_logic lab=ack_neu[0:3]}
C {sky130_stdcells/or2_1.sym} 360 -300 0 0 {name=x6 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/or2_1.sym} 360 -220 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/or2_1.sym} 510 -260 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 300 -320 2 1 {name=p3 sig_type=std_logic lab=ack_neu[0]}
C {devices/lab_pin.sym} 300 -280 2 1 {name=p4 sig_type=std_logic lab=ack_neu[1]}
C {devices/lab_pin.sym} 300 -240 2 1 {name=p6 sig_type=std_logic lab=ack_neu[2]}
C {devices/lab_pin.sym} 300 -200 2 1 {name=p7 sig_type=std_logic lab=ack_neu[3]}
C {devices/lab_pin.sym} 595 -260 2 0 {name=p8 sig_type=std_logic lab=latchAddr}
C {devices/lab_pin.sym} 200 -410 2 1 {name=p9 sig_type=std_logic lab=latchAddr}
C {devices/iopin.sym} 95 -165 0 0 {name=p10 lab=VDD}
C {devices/iopin.sym} 95 -135 0 0 {name=p11 lab=GND}
