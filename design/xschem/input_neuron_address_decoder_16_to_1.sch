v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Input neuron address (MSB XX LSB)} 410 -280 0 0 0.4 0.4 {}
N 570 -220 610 -220 {
lab=#net1}
N 570 -240 610 -240 {
lab=#net2}
N 230 -220 270 -220 {
lab=req_inp}
C {decoder_4_to_16.sym} 420 -210 0 0 {name=x2}
C {request_logic_delay.sym} 760 -220 0 0 {name=x4}
C {devices/lab_pin.sym} 910 -240 2 0 {name=p116 sig_type=std_logic lab=req_neu[0:15]}
C {devices/lab_pin.sym} 230 -220 0 0 {name=p153 sig_type=std_logic lab=req_inp}
C {devices/lab_pin.sym} 270 -240 0 0 {name=p162 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 570 -200 2 0 {name=p184 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 570 -180 2 0 {name=p185 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 910 -220 2 0 {name=p186 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 910 -200 2 0 {name=p187 sig_type=std_logic lab=dGND}
C {devices/ipin.sym} 180 -110 0 0 {name=p2 lab=neu_addr[0:3]

}
C {devices/ipin.sym} 150 -70 0 0 {name=p25 lab=req_inp

}
C {devices/iopin.sym} 230 -90 0 0 {name=p23 lab=dGND
}
C {devices/iopin.sym} 230 -70 0 0 {name=p24 lab=dVDD}
C {devices/opin.sym} 360 -100 0 0 {name=p6 lab=req_neu[0:15]}
