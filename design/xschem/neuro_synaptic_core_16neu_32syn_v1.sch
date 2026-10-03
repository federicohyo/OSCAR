v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {input spikes} 415 -340 0 0 0.4 0.4 {}
T {synaptic weight} 625 -345 0 0 0.4 0.4 {}
T {neuron biases} 1405 -340 0 0 0.4 0.4 {}
T {reset asynch digital logic} 345 -110 0 0 0.4 0.4 {}
T {monitor} 1685 -340 0 0 0.4 0.4 {}
T {AER} 235 -340 0 0 0.4 0.4 {}
T {analog synapse} 915 -340 0 0 0.4 0.4 {}
T {analog synapse} 1145 -340 0 0 0.4 0.4 {}
C {devices/iopin.sym} 495 -170 0 0 {name=p519 lab=dGND
}
C {devices/iopin.sym} 495 -150 0 0 {name=p520 lab=dVDD}
C {devices/ipin.sym} 545 -280 0 0 {name=p522 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 735 -285 0 0 {name=p523 lab=W[0:3]

}
C {devices/ipin.sym} 735 -225 0 0 {name=p527 lab=setW

}
C {devices/ipin.sym} 735 -255 0 0 {name=p528 lab=resetW

}
C {devices/ipin.sym} 545 -250 0 0 {name=p529 lab=neu_req[0:15]

}
C {devices/ipin.sym} 545 -220 0 0 {name=p530 lab=exc

}
C {devices/ipin.sym} 1515 -267.5 0 0 {name=p535 lab=vleakn
}
C {devices/ipin.sym} 1515 -290 0 0 {name=p536 lab=ifdcp
}
C {devices/ipin.sym} 1515 -247.5 2 1 {name=p542 lab=vrefn
}
C {devices/ipin.sym} 535 -55 0 0 {name=p544 lab=nRes

}
C {devices/iopin.sym} 605 -150 0 0 {name=p546 lab=aVDD}
C {devices/ipin.sym} 1745 -290 0 0 {name=p547 lab=bufmonp

}
C {devices/iopin.sym} 1725 -260 0 0 {name=p548 lab=monout[0:15]}
C {devices/ipin.sym} 325 -280 0 0 {name=p513 lab=ack_neu[0:15]

}
C {devices/opin.sym} 195 -240 0 0 {name=p514 lab=req_neu_out[0:15]

}
C {devices/ipin.sym} 1040 -260 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 1280 -260 0 0 {name=p74 lab=vipulseextp

}
C {devices/ipin.sym} 1040 -290 0 0 {name=p12 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 1280 -290 0 0 {name=p383 lab=JInhWp[0:3]

}
C {neuron_32syn_v1.sym} 1050 -650 0 0 {name=x4[0:15]}
C {devices/lab_pin.sym} 1200 -740 2 0 {name=p92 sig_type=std_logic lab=req_neu_out[0:15]}
C {devices/lab_pin.sym} 1200 -820 2 0 {name=p94 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1200 -800 2 0 {name=p96 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1200 -780 2 0 {name=p97 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1200 -840 2 0 {name=p98 sig_type=std_logic lab=monout[0:15]}
C {devices/lab_pin.sym} 900 -460 0 0 {name=p99 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 900 -720 0 0 {name=p100 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 900 -760 0 0 {name=p101 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 900 -800 0 0 {name=p102 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 900 -740 0 0 {name=p103 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 900 -820 0 0 {name=p104 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 900 -660 0 0 {name=p105 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 900 -580 0 0 {name=p106 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 900 -680 0 0 {name=p107 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 900 -700 0 0 {name=p108 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 900 -600 0 0 {name=p109 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 900 -520 0 0 {name=p110 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 900 -840 0 0 {name=p111 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 900 -780 0 0 {name=p112 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 900 -480 0 0 {name=p119 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 900 -640 0 0 {name=p120 sig_type=std_logic lab=neu_req[0:15]}
C {devices/ipin.sym} 1040 -230 0 0 {name=p1 lab=vthrdp

}
C {devices/ipin.sym} 1040 -200 0 0 {name=p2 lab=vtaun

}
C {devices/ipin.sym} 1290 -230 0 0 {name=p3 lab=vthrdn

}
C {devices/ipin.sym} 1290 -200 0 0 {name=p4 lab=vtaup

}
C {devices/lab_pin.sym} 900 -500 0 0 {name=p5 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 900 -540 0 0 {name=p6 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 900 -560 0 0 {name=p7 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 900 -620 0 0 {name=p8 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1200 -760 2 0 {name=p9 sig_type=std_logic lab=aGND}
C {devices/iopin.sym} 605 -170 0 0 {name=p10 lab=aGND}
