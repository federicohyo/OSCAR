v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {An array of 16 neurons with 32 synapses each (16E_16I)} 340 -660 0 0 0.4 0.4 {}
T {Input neuron address (MSB XX LSB)} 1100 -900 0 0 0.4 0.4 {}
T {Ouput interface address events are encoded 
and an arbiter is taking care of req_ack cycles} 1080 -680 0 0 0.4 0.4 {}
T {neuron biases} 80 -1240 0 0 0.4 0.4 {}
T {excitatory and inhibitory syn} 300 -1220 0 0 0.4 0.4 {}
T {Output Spikes (AER)} 1220 -1220 0 0 0.4 0.4 {}
T {Digital Logic / Input Spikes (AER)} 800 -1240 0 0 0.4 0.4 {}
T {Monitors Vmem} 1500 -1240 0 0 0.4 0.4 {}
T {Synaptic Weights} 1720 -1220 0 0 0.4 0.4 {}
T {analog synapse} 320 -1180 0 0 0.4 0.4 {}
T {analog synapse} 540 -1180 0 0 0.4 0.4 {}
T {neuron address encoder (LSB XX MSB)} 1580 -500 0 0 0.4 0.4 {}
T {Latch the inputs} 200 -920 0 0 0.4 0.4 {}
T {monitor analog neurons, one at the time (analog output)} 1040 -440 0 0 0.4 0.4 {}
N 900 -1160 940 -1160 {
lab=nRes}
N 900 -1140 940 -1140 {
lab=ack}
C {devices/lab_pin.sym} 490 -390 0 0 {name=p1 sig_type=std_logic lab=neu_req[0:15]}
C {devices/lab_pin.sym} 160 -800 0 0 {name=p6 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 160 -860 0 0 {name=p8 sig_type=std_logic lab=req_inp}
C {devices/lab_pin.sym} 160 -840 0 0 {name=p2 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 790 -590 2 0 {name=p13 sig_type=std_logic lab=req_o[0:15]}
C {devices/lab_pin.sym} 1460 -330 2 0 {name=p52 sig_type=std_logic lab=monout[0:15]}
C {devices/lab_pin.sym} 490 -570 0 0 {name=p388 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 490 -370 0 0 {name=p10 sig_type=std_logic lab=vrefn

}
C {devices/lab_pin.sym} 490 -590 0 0 {name=p51 sig_type=std_logic lab=bufmonp

}
C {devices/lab_pin.sym} 490 -230 0 0 {name=p11 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 490 -470 0 0 {name=p9 sig_type=std_logic lab=vleakn
}
C {devices/lab_pin.sym} 490 -430 0 0 {name=p41 sig_type=std_logic lab=vepulseextp
}
C {devices/lab_pin.sym} 490 -450 0 0 {name=p5 sig_type=std_logic lab=vipulseextp
}
C {devices/lab_pin.sym} 490 -530 0 0 {name=p12 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 490 -410 0 0 {name=p16 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 490 -310 0 0 {name=p17 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 490 -290 0 0 {name=p18 sig_type=std_logic lab=exc_latched}
C {devices/lab_pin.sym} 790 -570 2 0 {name=p22 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 790 -510 2 0 {name=p23 sig_type=std_logic lab=dVDD}
C {devices/ipin.sym} 160 -1120 0 0 {name=p234 lab=vleakn
}
C {devices/ipin.sym} 160 -1080 0 0 {name=p372 lab=vrefn

}
C {devices/ipin.sym} 160 -1140 0 0 {name=p377 lab=ifdcp
}
C {devices/ipin.sym} 1640 -1140 0 0 {name=p50 lab=bufmonp}
C {devices/opin.sym} 1300 -1160 0 0 {name=p28 lab=req_o}
C {devices/opin.sym} 1300 -1140 0 0 {name=p42 lab=aer_o[0:3]}
C {devices/iopin.sym} 1140 -1000 0 0 {name=p29 lab=dGND
}
C {devices/iopin.sym} 1140 -980 0 0 {name=p30 lab=dVDD}
C {devices/ipin.sym} 900 -1160 0 0 {name=p31 lab=nRes}
C {devices/lab_pin.sym} 940 -1160 2 0 {name=p32 sig_type=std_logic lab=nRes}
C {devices/ipin.sym} 900 -1140 0 0 {name=p37 lab=ack}
C {devices/ipin.sym} 980 -1080 0 0 {name=p46 lab=neu_addr[0:3]

}
C {devices/ipin.sym} 920 -1040 0 0 {name=p49 lab=req_inp

}
C {devices/ipin.sym} 980 -1100 0 0 {name=p45 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 900 -1020 0 0 {name=p47 lab=exc

}
C {devices/iopin.sym} 1240 -980 0 0 {name=p54 lab=aVDD}
C {devices/iopin.sym} 1540 -1160 0 0 {name=p55 lab=monout}
C {devices/ipin.sym} 1900 -1180 0 0 {name=p56 lab=W[0:3]

}
C {devices/ipin.sym} 1900 -1140 0 0 {name=p57 lab=resetW

}
C {devices/ipin.sym} 1900 -1100 0 0 {name=p58 lab=setW

}
C {devices/ipin.sym} 460 -1100 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 680 -1100 0 0 {name=p74 lab=vipulseextp

}
C {devices/ipin.sym} 460 -1140 0 0 {name=p27 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 680 -1140 0 0 {name=p383 lab=JInhWp[0:3]

}
C {neuro_synaptic_core_16neu_32syn_v1.sym} 640 -420 0 0 {name=x1}
C {devices/lab_pin.sym} 490 -610 0 0 {name=p19 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 490 -550 0 0 {name=p43 sig_type=std_logic lab=JExcWn[0:3]}
C {arbiter_tree_sixteen_bits.sym} 1330 -570 0 0 {name=x5}
C {devices/lab_pin.sym} 1180 -600 0 0 {name=p65 sig_type=std_logic lab=req_o[0:15]}
C {devices/lab_pin.sym} 1480 -580 2 0 {name=p66 sig_type=std_logic lab=req_o}
C {devices/lab_pin.sym} 1460 -500 2 0 {name=p67 sig_type=std_logic lab=aer_o[0:3]}
C {devices/lab_pin.sym} 1180 -580 0 0 {name=p68 sig_type=std_logic lab=ack}
C {encoder_16_to_4.sym} 1310 -480 0 0 {name=x6}
C {devices/lab_pin.sym} 1480 -600 0 1 {name=p33 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 490 -490 2 1 {name=p14 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/ipin.sym} 700 -1060 0 0 {name=p4 lab=vthrdp

}
C {devices/ipin.sym} 700 -1040 0 0 {name=p7 lab=vtaun

}
C {devices/ipin.sym} 420 -1080 0 0 {name=p15 lab=vthrdn

}
C {devices/ipin.sym} 420 -1040 0 0 {name=p20 lab=vtaup

}
C {devices/lab_pin.sym} 490 -350 0 0 {name=p21 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 490 -330 0 0 {name=p34 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 490 -250 0 0 {name=p35 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 490 -270 0 0 {name=p36 sig_type=std_logic lab=vtaup}
C {inputs_latch_16neu.sym} 310 -810 0 0 {name=x3}
C {devices/lab_pin.sym} 160 -780 0 0 {name=p38 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 160 -820 0 0 {name=p39 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 460 -820 0 1 {name=p44 sig_type=std_logic lab=exc_latched}
C {devices/lab_pin.sym} 460 -800 0 1 {name=p63 sig_type=std_logic lab=req_inp_array}
C {monitor_select.sym} 1310 -360 0 0 {name=x8}
C {devices/lab_pin.sym} 790 -610 2 0 {name=p71 sig_type=std_logic lab=monout[0:15]}
C {devices/ipin.sym} 1620 -1100 0 0 {name=p72 lab=Da


}
C {devices/ipin.sym} 1620 -1080 0 0 {name=p73 lab=CLK


}
C {devices/lab_pin.sym} 1160 -350 0 0 {name=p75 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1160 -390 2 1 {name=p76 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 1160 -370 2 1 {name=p77 sig_type=std_logic lab=CLK}
C {devices/lab_pin.sym} 1460 -350 2 0 {name=p78 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1160 -500 2 1 {name=p64 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 1460 -480 2 0 {name=p26 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1460 -460 2 0 {name=p69 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1480 -560 2 0 {name=p70 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1480 -540 2 0 {name=p81 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 460 -780 2 0 {name=p24 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 460 -760 2 0 {name=p82 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1460 -370 2 0 {name=p79 sig_type=std_logic lab=dGND}
C {input_neuron_address_decoder_16_to_1.sym} 1300 -820 0 0 {name=x7}
C {devices/lab_pin.sym} 1150 -820 0 0 {name=p83 sig_type=std_logic lab=req_inp_array}
C {devices/lab_pin.sym} 1450 -840 2 0 {name=p88 sig_type=std_logic lab=neu_req[0:15]}
C {devices/lab_pin.sym} 1450 -800 2 0 {name=p89 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1450 -820 2 0 {name=p90 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1460 -390 2 0 {name=p3 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 790 -550 2 0 {name=p25 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 790 -530 2 0 {name=p62 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 1240 -1000 0 0 {name=p53 lab=aGND}
C {devices/lab_pin.sym} 460 -840 0 1 {name=p48 sig_type=std_logic lab=neu_addr_latched[0:3]}
C {devices/lab_pin.sym} 1150 -840 0 0 {name=p59 sig_type=std_logic lab=neu_addr_latched[0:3]}
C {devices/lab_pin.sym} 460 -860 0 1 {name=p60 sig_type=std_logic lab=syn_addr_latched[0:3]}
C {devices/lab_pin.sym} 490 -510 0 0 {name=p61 sig_type=std_logic lab=syn_addr_latched[0:3]}
