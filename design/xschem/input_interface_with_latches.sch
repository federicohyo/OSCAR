v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Input neuron address (MSB XX LSB)} 220 -150 0 0 0.4 0.4 {}
T {Latch the inputs} 190 -370 0 0 0.4 0.4 {}
C {devices/lab_pin.sym} 150 -250 0 0 {name=p6 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 150 -310 0 0 {name=p8 sig_type=std_logic lab=req_inp}
C {devices/lab_pin.sym} 150 -290 0 0 {name=p2 sig_type=std_logic lab=syn_addr[0:3]}
C {inputs_latch_16neu.sym} 300 -260 0 0 {name=x3}
C {devices/lab_pin.sym} 150 -230 0 0 {name=p38 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 150 -270 0 0 {name=p39 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 450 -270 0 1 {name=p44 sig_type=std_logic lab=exc_latched}
C {devices/lab_pin.sym} 450 -310 0 1 {name=p59 sig_type=std_logic lab=syn_addr_latched[0:3]}
C {devices/lab_pin.sym} 450 -290 0 1 {name=p61 sig_type=std_logic lab=neu_addr_latched[0:3]}
C {devices/lab_pin.sym} 450 -250 0 1 {name=p63 sig_type=std_logic lab=req_inp_array}
C {devices/lab_pin.sym} 450 -230 2 0 {name=p24 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 450 -210 2 0 {name=p82 sig_type=std_logic lab=dGND}
C {input_neuron_address_decoder_16_to_1.sym} 420 -70 0 0 {name=x7}
C {devices/lab_pin.sym} 270 -90 0 0 {name=p48 sig_type=std_logic lab=neu_addr_latched[0:3]}
C {devices/lab_pin.sym} 270 -70 0 0 {name=p83 sig_type=std_logic lab=req_inp_array}
C {devices/lab_pin.sym} 570 -90 2 0 {name=p88 sig_type=std_logic lab=neu_req[0:15]}
C {devices/lab_pin.sym} 570 -50 2 0 {name=p89 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 570 -70 2 0 {name=p90 sig_type=std_logic lab=dGND}
C {devices/iopin.sym} 380 -490 0 0 {name=p29 lab=dGND
}
C {devices/iopin.sym} 380 -470 0 0 {name=p30 lab=dVDD}
C {devices/ipin.sym} 160 -530 0 0 {name=p49 lab=req_inp

}
C {devices/ipin.sym} 240 -420 0 0 {name=p46 lab=neu_addr[0:3]

}
C {devices/ipin.sym} 240 -440 0 0 {name=p45 lab=syn_addr[0:3]

}
C {devices/opin.sym} 370 -440 0 0 {name=p4 lab=neu_req[0:15]}
C {devices/ipin.sym} 170 -490 0 0 {name=p31 lab=nRes}
C {devices/opin.sym} 370 -410 0 0 {name=p1 lab=syn_addr_latched[0:3]}
C {devices/opin.sym} 370 -390 0 0 {name=p3 lab=exc_latched}
C {devices/ipin.sym} 170 -460 0 0 {name=p5 lab=exc}
