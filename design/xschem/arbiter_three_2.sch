v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 70 -120 100 -120 {
lab=ack_out}
C {arbiter_cell_two_bits_fc.sym} 250 -80 0 0 {name=x1}
C {devices/lab_pin.sym} 400 -80 2 0 {name=p49 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 400 -120 2 0 {name=p59 sig_type=std_logic lab=ack_neu[1]}
C {devices/lab_pin.sym} 70 -120 1 0 {name=p1 sig_type=std_logic lab=ack_out}
C {devices/lab_pin.sym} 400 -100 2 0 {name=p5 sig_type=std_logic lab=ack_neu[0]}
C {devices/lab_pin.sym} 100 -100 0 0 {name=p2 sig_type=std_logic lab=req_neu[0]}
C {devices/lab_pin.sym} 100 -80 0 0 {name=p3 sig_type=std_logic lab=req_neu[1]}
C {devices/ipin.sym} 240 -260 0 0 {name=p67 lab=ack_out}
C {devices/opin.sym} 160 -230 0 0 {name=p68 lab=req_out}
C {devices/ipin.sym} 270 -300 0 0 {name=p69 lab=req_neu[0:1]}
C {devices/opin.sym} 130 -330 0 0 {name=p4 lab=ack_neu[0:1]}
C {devices/lab_pin.sym} 400 -60 2 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 400 -40 2 0 {name=p7 sig_type=std_logic lab=GND}
C {devices/iopin.sym} 160 -200 0 0 {name=p8 lab=VDD}
C {devices/iopin.sym} 160 -170 0 0 {name=p9 lab=GND}
