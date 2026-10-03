v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {neuron address encoder} 415 -360 0 0 0.4 0.4 {}
T {arbiter tree} 495 -190 0 0 0.4 0.4 {}
C {encoder_16_to_4.sym} 550 -290 0 0 {name=x1}
C {devices/iopin.sym} 100 -240 0 0 {name=p109 lab=GND
}
C {devices/iopin.sym} 100 -220 0 0 {name=p110 lab=VDD}
C {devices/ipin.sym} 190 -70 0 0 {name=p1 lab=req_neu[0:15]}
C {devices/opin.sym} 60 -160 0 0 {name=p2 lab=aer_out[0:3]}
C {devices/opin.sym} 60 -190 0 0 {name=p4 lab=ack_neu[0:15]}
C {devices/opin.sym} 60 -130 0 0 {name=p152 lab=req}
C {devices/ipin.sym} 190 -100 0 0 {name=p153 lab=ack}
C {devices/ipin.sym} 190 -40 0 0 {name=p5 lab=nRes}
C {devices/lab_pin.sym} 400 -310 2 1 {name=p74 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 700 -310 2 0 {name=p76 sig_type=std_logic lab=aer_out[0:3]}
C {arbiter_three_16.sym} 550 -120 0 0 {name=x2}
C {devices/lab_pin.sym} 400 -150 0 0 {name=p201 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 400 -110 2 1 {name=p202 sig_type=std_logic lab=req_neu[0:15]}
C {devices/lab_pin.sym} 400 -130 0 0 {name=p191 sig_type=std_logic lab=ack}
C {devices/lab_pin.sym} 700 -90 2 0 {name=p189 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 700 -150 2 0 {name=p190 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 700 -110 0 1 {name=p188 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 700 -130 2 0 {name=p3 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 700 -290 2 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 700 -270 2 0 {name=p7 sig_type=std_logic lab=GND}
