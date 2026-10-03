v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
C {arbiter_tree_sixteen_bits.sym} 260 -290 0 0 {name=x5}
C {devices/lab_pin.sym} 110 -320 0 0 {name=p65 sig_type=std_logic lab=req[0:15]}
C {devices/lab_pin.sym} 410 -300 2 0 {name=p66 sig_type=std_logic lab=req_cpu}
C {devices/lab_pin.sym} 390 -220 2 0 {name=p67 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 110 -300 0 0 {name=p68 sig_type=std_logic lab=ack_cpu}
C {encoder_16_to_4.sym} 240 -200 0 0 {name=x6}
C {devices/lab_pin.sym} 410 -320 0 1 {name=p33 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 90 -220 2 1 {name=p64 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 390 -200 2 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 390 -180 2 0 {name=p69 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 410 -280 2 0 {name=p70 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 410 -260 2 0 {name=p81 sig_type=std_logic lab=GND}
C {devices/ipin.sym} 120 -100 0 0 {name=p80 lab=req[0:15]}
C {devices/ipin.sym} 460 -100 0 0 {name=p5 lab=ack_cpu}
C {devices/opin.sym} 460 -80 0 0 {name=p6 lab=req_cpu}
C {devices/iopin.sym} 120 -50 0 0 {name=p15 lab=VDD}
C {devices/iopin.sym} 120 -30 0 0 {name=p16 lab=GND}
C {devices/opin.sym} 370 -30 0 0 {name=p1 lab=neu_addr[0:3]}
