v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {An array of 16 neurons with 32 synapses each (16E/16I)} 410 -700 0 0 0.4 0.4 {}
T {Input neuron address} 720 -930 0 0 0.4 0.4 {}
T {Ouput interface address events are encoded 
and an arbiter is taking care of req/ack cycles} 1120 -700 0 0 0.4 0.4 {}
T {neuron biases} 120 -1265 0 0 0.4 0.4 {}
T {excitatory and inhibitory syn} 330 -1255 0 0 0.4 0.4 {}
T {Output Spikes (AER)} 1350 -1250 0 0 0.4 0.4 {}
T {Digital Logic / Input Spikes (AER)} 835 -1260 0 0 0.4 0.4 {}
T {Monitors Vmem} 1630 -1260 0 0 0.4 0.4 {}
T {Synaptic Weights} 1900 -1255 0 0 0.4 0.4 {}
T {neuron address encoder} 1235 -510 0 0 0.4 0.4 {}
N 820 -870 860 -870 {
lab=#net1}
N 820 -850 860 -850 {
lab=#net2}
N 500 -850 520 -850 {
lab=req_inp}
N 490 -870 520 -870 {
lab=neu_addr[0:3]}
C {neuro_synaptic_core_16neu_32syn.sym} 680 -380 0 0 {name=x1}
C {decoder_4_to_16.sym} 670 -840 0 0 {name=x2}
C {devices/lab_pin.sym} 530 -390 0 0 {name=p1 sig_type=std_logic lab=neu_req[0:15]}
C {devices/lab_pin.sym} 490 -870 0 0 {name=p6 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 500 -850 0 0 {name=p8 sig_type=std_logic lab=req_inp}
C {devices/lab_pin.sym} 530 -510 0 0 {name=p2 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1510 -620 2 0 {name=p33 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 1510 -600 2 0 {name=p38 sig_type=std_logic lab=req_o}
C {devices/lab_pin.sym} 1210 -620 0 0 {name=p26 sig_type=std_logic lab=req_o[0:15]}
C {devices/lab_pin.sym} 830 -610 2 0 {name=p13 sig_type=std_logic lab=req_o[0:15]}
C {devices/lab_pin.sym} 830 -630 2 0 {name=p52 sig_type=std_logic lab=monout[0:15]}
C {devices/lab_pin.sym} 1210 -600 0 0 {name=p39 sig_type=std_logic lab=ack}
C {request_logic_delay.sym} 1010 -850 0 0 {name=x4}
C {devices/lab_pin.sym} 1160 -870 2 0 {name=p3 sig_type=std_logic lab=neu_req[0:15]}
C {devices/lab_pin.sym} 530 -630 0 0 {name=p386 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 530 -430 0 0 {name=p388 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 530 -150 0 0 {name=p392 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 530 -170 0 0 {name=p10 sig_type=std_logic lab=vrefn

}
C {devices/lab_pin.sym} 530 -570 0 0 {name=p51 sig_type=std_logic lab=bufmonp

}
C {devices/lab_pin.sym} 530 -130 0 0 {name=p11 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 530 -270 0 0 {name=p390 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 530 -210 0 0 {name=p9 sig_type=std_logic lab=vleakn
}
C {devices/lab_pin.sym} 530 -470 0 0 {name=p34 sig_type=std_logic lab=vithrdpip}
C {devices/lab_pin.sym} 530 -250 0 0 {name=p41 sig_type=std_logic lab=vepulseextp
}
C {devices/lab_pin.sym} 530 -230 0 0 {name=p4 sig_type=std_logic lab=ifcascn
}
C {devices/lab_pin.sym} 530 -190 0 0 {name=p5 sig_type=std_logic lab=vipulseextp
}
C {devices/lab_pin.sym} 530 -590 0 0 {name=p43 sig_type=std_logic lab=vistddpip}
C {devices/lab_pin.sym} 530 -610 0 0 {name=p7 sig_type=std_logic lab=vestddpin}
C {devices/lab_pin.sym} 530 -550 0 0 {name=p12 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 530 -530 0 0 {name=p14 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 530 -490 0 0 {name=p387 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 530 -450 0 0 {name=p15 sig_type=std_logic lab=vethrdpin}
C {devices/lab_pin.sym} 530 -410 0 0 {name=p16 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 530 -310 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 530 -290 0 0 {name=p18 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 530 -330 0 0 {name=p19 sig_type=std_logic lab=vetaudpip}
C {devices/lab_pin.sym} 530 -350 0 0 {name=p20 sig_type=std_logic lab=vitaudpin}
C {devices/lab_pin.sym} 530 -370 0 0 {name=p21 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 830 -570 2 0 {name=p22 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 830 -530 2 0 {name=p23 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 830 -550 2 0 {name=p24 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 830 -590 2 0 {name=p25 sig_type=std_logic lab=aGND}
C {devices/ipin.sym} 200 -1015 0 0 {name=p234 lab=vleakn
}
C {devices/ipin.sym} 200 -985 0 0 {name=p372 lab=vrefn

}
C {devices/ipin.sym} 200 -955 0 0 {name=p373 lab=ifahtaun
}
C {devices/ipin.sym} 200 -1045 0 0 {name=p374 lab=ifcascn
}
C {devices/ipin.sym} 200 -1075 0 0 {name=p375 lab=ifthrp
}
C {devices/ipin.sym} 200 -1105 0 0 {name=p376 lab=ifahthrp
}
C {devices/ipin.sym} 200 -1135 0 0 {name=p377 lab=ifdcp
}
C {devices/ipin.sym} 200 -1165 0 0 {name=p378 lab=ifahwp
}
C {devices/ipin.sym} 200 -1195 0 0 {name=p379 lab=ifnmdap
}
C {devices/ipin.sym} 430 -1195 0 0 {name=p380 lab=vestddpin

}
C {devices/ipin.sym} 430 -1165 0 0 {name=p381 lab=vethrdpin

}
C {devices/ipin.sym} 430 -1145 0 0 {name=p382 lab=vetaudpip

}
C {devices/ipin.sym} 590 -1195 0 0 {name=p383 lab=vistddpip

}
C {devices/ipin.sym} 590 -1165 0 0 {name=p384 lab=vithrdpip

}
C {devices/ipin.sym} 590 -1145 0 0 {name=p385 lab=vitaudpin

}
C {devices/ipin.sym} 435 -1110 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 1770 -1160 0 0 {name=p50 lab=bufmonp}
C {devices/ipin.sym} 595 -1110 0 0 {name=p27 lab=vipulseextp

}
C {devices/opin.sym} 1430 -1190 0 0 {name=p28 lab=req_o}
C {devices/opin.sym} 1430 -1160 0 0 {name=p42 lab=aer_o[0:3]}
C {devices/iopin.sym} 1170 -1025 0 0 {name=p29 lab=dGND
}
C {devices/iopin.sym} 1170 -1005 0 0 {name=p30 lab=dVDD}
C {devices/ipin.sym} 935 -1195 0 0 {name=p31 lab=nRes}
C {devices/ipin.sym} 935 -1165 0 0 {name=p37 lab=ack}
C {devices/ipin.sym} 1015 -1105 0 0 {name=p46 lab=neu_addr[0:3]

}
C {devices/ipin.sym} 955 -1075 0 0 {name=p49 lab=req_inp

}
C {devices/ipin.sym} 1015 -1135 0 0 {name=p45 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 945 -1045 0 0 {name=p47 lab=exc

}
C {devices/iopin.sym} 1270 -1025 0 0 {name=p48 lab=aGND
}
C {devices/iopin.sym} 1270 -1005 0 0 {name=p54 lab=aVDD}
C {devices/iopin.sym} 1670 -1190 0 0 {name=p55 lab=monout[0:15]}
C {devices/ipin.sym} 2080 -1200 0 0 {name=p56 lab=W[0:3]

}
C {devices/ipin.sym} 2080 -1165 0 0 {name=p57 lab=resetW

}
C {devices/ipin.sym} 2080 -1135 0 0 {name=p58 lab=setW

}
C {arbiter_tree_sixteen_bits.sym} 1360 -590 0 0 {name=x5}
C {devices/lab_pin.sym} 1520 -460 2 0 {name=p67 sig_type=std_logic lab=aer_o[0:3]}
C {encoder_16_to_4.sym} 1370 -440 0 0 {name=x6}
C {devices/lab_pin.sym} 1220 -460 2 1 {name=p32 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 1510 -580 2 0 {name=p35 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1510 -560 2 0 {name=p36 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1520 -440 2 0 {name=p44 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1520 -420 2 0 {name=p53 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 820 -830 2 0 {name=p61 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 820 -810 2 0 {name=p62 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1160 -850 2 0 {name=p59 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1160 -830 2 0 {name=p60 sig_type=std_logic lab=dGND}
