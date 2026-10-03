v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {input spikes} 245 -340 0 0 0.4 0.4 {}
T {synaptic weight} 455 -345 0 0 0.4 0.4 {}
T {neuron biases} 1235 -340 0 0 0.4 0.4 {}
T {reset asynch digital logic} 175 -110 0 0 0.4 0.4 {}
T {monitor} 1515 -340 0 0 0.4 0.4 {}
T {AER} 65 -340 0 0 0.4 0.4 {}
T {analog synapse} 745 -340 0 0 0.4 0.4 {}
T {analog synapse} 975 -340 0 0 0.4 0.4 {}
C {devices/iopin.sym} 325 -170 0 0 {name=p519 lab=dGND
}
C {devices/iopin.sym} 325 -150 0 0 {name=p520 lab=dVDD}
C {devices/ipin.sym} 375 -280 0 0 {name=p522 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 565 -285 0 0 {name=p523 lab=W[0:3]

}
C {devices/ipin.sym} 565 -225 0 0 {name=p527 lab=setW

}
C {devices/ipin.sym} 565 -255 0 0 {name=p528 lab=resetW

}
C {devices/ipin.sym} 375 -250 0 0 {name=p529 lab=neu_req[0:3]

}
C {devices/ipin.sym} 375 -220 0 0 {name=p530 lab=exc

}
C {devices/ipin.sym} 1345 -267.5 0 0 {name=p535 lab=vleakn
}
C {devices/ipin.sym} 1345 -290 0 0 {name=p536 lab=ifdcp
}
C {devices/ipin.sym} 1345 -247.5 2 1 {name=p542 lab=vrefn
}
C {devices/ipin.sym} 365 -55 0 0 {name=p544 lab=nRes

}
C {devices/iopin.sym} 435 -150 0 0 {name=p546 lab=aVDD}
C {devices/ipin.sym} 1575 -290 0 0 {name=p547 lab=bufmonp

}
C {devices/iopin.sym} 1555 -260 0 0 {name=p548 lab=monout[0:3]}
C {devices/ipin.sym} 155 -280 0 0 {name=p513 lab=ack_neu[0:3]

}
C {devices/opin.sym} 25 -240 0 0 {name=p514 lab=req_neu_out[0:3]

}
C {devices/ipin.sym} 870 -260 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 1110 -260 0 0 {name=p74 lab=vipulseextp

}
C {devices/ipin.sym} 870 -290 0 0 {name=p12 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 1110 -290 0 0 {name=p383 lab=JInhWp[0:3]

}
C {neuron_32syn_v1.sym} 880 -650 0 0 {name=x4[0:3]}
C {devices/lab_pin.sym} 1030 -760 2 0 {name=p92 sig_type=std_logic lab=req_neu_out[0:3]}
C {devices/lab_pin.sym} 1030 -820 2 0 {name=p94 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1030 -800 2 0 {name=p96 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1030 -780 2 0 {name=p97 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1030 -840 2 0 {name=p98 sig_type=std_logic lab=monout[0:3]}
C {devices/lab_pin.sym} 730 -460 0 0 {name=p99 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 730 -720 0 0 {name=p100 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 730 -840 0 0 {name=p101 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 730 -800 0 0 {name=p102 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 730 -740 0 0 {name=p103 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 730 -820 0 0 {name=p104 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 730 -660 0 0 {name=p105 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 730 -580 0 0 {name=p106 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 730 -680 0 0 {name=p107 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 730 -700 0 0 {name=p108 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 730 -600 0 0 {name=p109 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 730 -520 0 0 {name=p110 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 730 -760 0 0 {name=p111 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 730 -780 0 0 {name=p112 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 730 -480 0 0 {name=p119 sig_type=std_logic lab=ack_neu[0:3]}
C {devices/lab_pin.sym} 730 -640 0 0 {name=p120 sig_type=std_logic lab=neu_req[0:3]}
C {devices/ipin.sym} 870 -230 0 0 {name=p1 lab=vthrdp

}
C {devices/ipin.sym} 870 -200 0 0 {name=p2 lab=vtaun

}
C {devices/ipin.sym} 1120 -230 0 0 {name=p3 lab=vthrdn

}
C {devices/ipin.sym} 1120 -200 0 0 {name=p4 lab=vtaup

}
C {devices/lab_pin.sym} 730 -500 0 0 {name=p5 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 730 -540 0 0 {name=p6 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 730 -560 0 0 {name=p7 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 730 -620 0 0 {name=p8 sig_type=std_logic lab=vtaun}
