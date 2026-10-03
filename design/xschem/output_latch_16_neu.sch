v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 210 -450 290 -450 {
lab=latchAddr}
N 470 -450 510 -450 {
lab=ack_neu_latched[0:15]}
N 210 -430 290 -430 {
lab=ack_neu[0:15]}
N 620 -250 650 -250 {
lab=#net1}
N 620 -250 620 -190 {
lab=#net1}
N 610 -190 620 -190 {
lab=#net1}
N 770 -270 800 -270 {
lab=latchAddr}
N 610 -360 650 -360 {
lab=#net2}
N 650 -360 650 -290 {
lab=#net2}
C {sky130_stdcells/dfrtp_1.sym} 380 -430 0 0 {name=x2[0:15] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 170 -270 0 0 {name=p45 lab=ack_neu[0:15]

}
C {devices/ipin.sym} 110 -240 0 0 {name=p31 lab=nRes}
C {devices/lab_pin.sym} 110 -240 2 0 {name=p32 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 290 -410 2 1 {name=p2 sig_type=std_logic lab=nRes}
C {devices/opin.sym} 510 -450 0 0 {name=p5 lab=ack_neu_latched[0:15]

}
C {devices/lab_pin.sym} 210 -430 2 1 {name=p1 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 310 -360 2 1 {name=p3 sig_type=std_logic lab=ack_neu[0]}
C {devices/lab_pin.sym} 310 -340 2 1 {name=p4 sig_type=std_logic lab=ack_neu[1]}
C {devices/lab_pin.sym} 310 -320 2 1 {name=p6 sig_type=std_logic lab=ack_neu[2]}
C {devices/lab_pin.sym} 310 -300 2 1 {name=p7 sig_type=std_logic lab=ack_neu[3]}
C {devices/lab_pin.sym} 800 -270 2 0 {name=p8 sig_type=std_logic lab=latchAddr}
C {devices/lab_pin.sym} 210 -450 2 1 {name=p9 sig_type=std_logic lab=latchAddr}
C {or8.sym} 460 -290 0 0 {name=x3}
C {devices/lab_pin.sym} 310 -280 2 1 {name=p10 sig_type=std_logic lab=ack_neu[4]}
C {devices/lab_pin.sym} 310 -260 2 1 {name=p11 sig_type=std_logic lab=ack_neu[5]}
C {devices/lab_pin.sym} 310 -240 2 1 {name=p12 sig_type=std_logic lab=ack_neu[6]}
C {devices/lab_pin.sym} 310 -220 2 1 {name=p13 sig_type=std_logic lab=ack_neu[7]}
C {devices/lab_pin.sym} 310 -190 2 1 {name=p14 sig_type=std_logic lab=ack_neu[8]}
C {devices/lab_pin.sym} 310 -170 2 1 {name=p15 sig_type=std_logic lab=ack_neu[9]}
C {devices/lab_pin.sym} 310 -150 2 1 {name=p16 sig_type=std_logic lab=ack_neu[10]}
C {devices/lab_pin.sym} 310 -130 2 1 {name=p17 sig_type=std_logic lab=ack_neu[11]}
C {or8.sym} 460 -120 0 0 {name=x1}
C {devices/lab_pin.sym} 310 -110 2 1 {name=p18 sig_type=std_logic lab=ack_neu[12]}
C {devices/lab_pin.sym} 310 -90 2 1 {name=p19 sig_type=std_logic lab=ack_neu[13]}
C {devices/lab_pin.sym} 310 -70 2 1 {name=p20 sig_type=std_logic lab=ack_neu[14]}
C {devices/lab_pin.sym} 310 -50 2 1 {name=p21 sig_type=std_logic lab=ack_neu[15]}
C {sky130_stdcells/or2_1.sym} 710 -270 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/iopin.sym} 110 -210 0 0 {name=p22 lab=VDD}
C {devices/iopin.sym} 110 -180 0 0 {name=p23 lab=GND}
C {devices/lab_pin.sym} 610 -170 2 0 {name=p24 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 610 -150 2 0 {name=p25 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 610 -340 2 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 610 -320 2 0 {name=p27 sig_type=std_logic lab=GND}
