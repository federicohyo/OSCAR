v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 420 -430 530 -430 {
lab=#net1}
N 80 -410 120 -410 {
lab=CLK}
N 80 -430 120 -430 {
lab=Da}
N 1180 -390 1210 -390 {
lab=dGND}
N 1180 -410 1210 -410 {
lab=inputAnalog[0:15]}
N 1180 -370 1210 -370 {
lab=monOUT}
N 830 -430 880 -430 {
lab=#net2}
C {decoder_4_to_16.sym} 680 -400 0 0 {name=x1}
C {devices/ipin.sym} 120 -220 0 0 {name=p5 lab=Da


}
C {devices/ipin.sym} 120 -190 0 0 {name=p8 lab=CLK


}
C {devices/ipin.sym} 120 -160 0 0 {name=p19 lab=nRes


}
C {devices/lab_pin.sym} 90 -410 0 0 {name=p2 sig_type=std_logic lab=CLK}
C {devices/lab_pin.sym} 80 -430 0 0 {name=p3 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 120 -390 0 0 {name=p18 sig_type=std_logic lab=nRes}
C {16-to-1_analog_mux.sym} 1030 -400 0 0 {name=x2}
C {devices/iopin.sym} 150 -190 0 0 {name=p10 lab=dGND}
C {devices/iopin.sym} 150 -160 0 0 {name=p12 lab=monOUT}
C {devices/lab_pin.sym} 1210 -370 0 1 {name=p1 sig_type=std_logic lab=monOUT}
C {devices/iopin.sym} 150 -130 0 0 {name=p6 lab=inputAnalog[0:15]}
C {devices/lab_pin.sym} 1210 -410 0 1 {name=p7 sig_type=std_logic lab=inputAnalog[0:15]}
C {dflip_flop_chain_4_fc_nolatch.sym} 270 -410 0 0 {name=x3}
C {devices/lab_pin.sym} 830 -390 0 1 {name=p4 sig_type=std_logic lab=dVDD}
C {devices/iopin.sym} 150 -220 0 0 {name=p20 lab=dVDD}
C {devices/lab_pin.sym} 420 -410 0 1 {name=p15 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1180 -430 0 1 {name=p13 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 420 -390 0 1 {name=p9 sig_type=std_logic lab=dGND
}
C {devices/lab_pin.sym} 1210 -390 0 1 {name=p11 sig_type=std_logic lab=dGND
}
C {devices/lab_pin.sym} 830 -370 1 1 {name=p14 sig_type=std_logic lab=dGND
}
C {devices/lab_pin.sym} 530 -410 1 1 {name=p16 sig_type=std_logic lab=dGND
}
