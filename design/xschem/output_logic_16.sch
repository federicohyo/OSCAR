v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {neuron address encoder} 375 -300 0 0 0.4 0.4 {}
T {arbiter tree} 435 -180 0 0 0.4 0.4 {}
C {arbiter_three_16.sym} 510 -110 0 0 {name=x1}
C {encoder_16_to_4.sym} 510 -240 0 0 {name=x2}
C {devices/iopin.sym} 90 -230 0 0 {name=p109 lab=GND
}
C {devices/iopin.sym} 90 -210 0 0 {name=p110 lab=VDD}
C {devices/ipin.sym} 190 -20 0 0 {name=p1 lab=req_neu[0:15]}
C {devices/opin.sym} 50 -140 0 0 {name=p2 lab=aer_out[0:3]}
C {devices/opin.sym} 50 -170 0 0 {name=p4 lab=ack_neu[0:15]}
C {devices/opin.sym} 50 -110 0 0 {name=p152 lab=req}
C {devices/ipin.sym} 190 -80 0 0 {name=p153 lab=ack}
C {devices/ipin.sym} 190 -50 0 0 {name=p5 lab=nRes}
C {devices/lab_pin.sym} 360 -240 2 1 {name=p74 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 660 -240 2 0 {name=p76 sig_type=std_logic lab=aer_out[0:3]}
C {devices/lab_pin.sym} 360 -100 2 1 {name=p202 sig_type=std_logic lab=req_neu[0:15]}
C {devices/lab_pin.sym} 360 -140 0 0 {name=p201 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 360 -120 0 0 {name=p191 sig_type=std_logic lab=ack}
C {devices/lab_pin.sym} 660 -140 2 0 {name=p75 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 660 -80 2 0 {name=p73 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 660 -100 0 1 {name=p188 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 660 -120 2 0 {name=p3 sig_type=std_logic lab=req}
