v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 1705 -1130 0 0 0.4 0.4 {}
T {input spikes} 1215 -1130 0 0 0.4 0.4 {}
T {synaptic weight} 1425 -1135 0 0 0.4 0.4 {}
T {analog synapse} 1935 -1130 0 0 0.4 0.4 {}
T {neuron biases} 2205 -1130 0 0 0.4 0.4 {}
T {reset asynch digital logic} 1145 -900 0 0 0.4 0.4 {}
T {monitor} 2485 -1130 0 0 0.4 0.4 {}
T {AER} 1035 -1130 0 0 0.4 0.4 {}
N 1870 -730 1880 -730 {
lab=dGND}
N 1870 -750 1880 -750 {
lab=aGND}
N 1870 -690 1880 -690 {
lab=dVDD}
N 1870 -710 1880 -710 {
lab=aVDD}
N 1870 -770 1940 -770 {
lab=monout[0:15]}
N 1870 -670 1940 -670 {
lab=req_neu_out[0:15]}
N 1560 -370 1570 -370 {
lab=vleakn}
N 1560 -730 1570 -730 {
lab=vistddpip}
N 1560 -750 1570 -750 {
lab=vestddpin}
N 1560 -770 1570 -770 {
lab=ifnmdap}
N 1560 -670 1570 -670 {
lab=ifahwp}
N 1560 -590 1570 -590 {
lab=ifdcp}
N 1560 -550 1570 -550 {
lab=neu_req[0:15]}
N 1560 -530 1570 -530 {
lab=ifahthrp}
N 1560 -430 1570 -430 {
lab=ifthrp}
N 1560 -410 1570 -410 {
lab=ifcascn}
N 1560 -330 1570 -330 {
lab=vrefn}
N 1560 -310 1570 -310 {
lab=ifahtaun}
C {neuron_32syn.sym} 1720 -520 0 0 {name=x1[0:15]}
C {devices/lab_pin.sym} 1875 -730 2 0 {name=p2 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1875 -750 2 0 {name=p3 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1875 -690 2 0 {name=p4 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1875 -710 2 0 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1570 -290 0 0 {name=p10 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1570 -270 0 0 {name=p6 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 1565 -370 0 0 {name=p7 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1570 -510 0 0 {name=p12 sig_type=std_logic lab=vitaudpin}
C {devices/lab_pin.sym} 1570 -610 0 0 {name=p13 sig_type=std_logic lab=vithrdpip}
C {devices/lab_pin.sym} 1565 -730 0 0 {name=p14 sig_type=std_logic lab=vistddpip}
C {devices/lab_pin.sym} 1570 -490 0 0 {name=p15 sig_type=std_logic lab=vetaudpip}
C {devices/lab_pin.sym} 1570 -630 0 0 {name=p17 sig_type=std_logic lab=vethrdpin}
C {devices/lab_pin.sym} 1565 -750 0 0 {name=p18 sig_type=std_logic lab=vestddpin}
C {devices/lab_pin.sym} 1565 -770 0 0 {name=p20 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 1570 -710 0 0 {name=p187 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 1570 -690 0 0 {name=p29 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1565 -670 0 0 {name=p30 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 1570 -650 0 0 {name=p61 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1565 -590 0 0 {name=p62 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1570 -570 0 0 {name=p63 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1570 -470 0 0 {name=p64 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1565 -530 0 0 {name=p66 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 1565 -430 0 0 {name=p67 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 1565 -410 0 0 {name=p68 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 1570 -390 0 0 {name=p70 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 1570 -350 0 0 {name=p71 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 1565 -330 0 0 {name=p73 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1565 -310 0 0 {name=p74 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 1570 -450 0 0 {name=p76 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1940 -770 2 0 {name=p77 sig_type=std_logic lab=monout[0:15]}
C {devices/lab_pin.sym} 1940 -670 2 0 {name=p38 sig_type=std_logic lab=req_neu_out[0:15]}
C {devices/lab_pin.sym} 1560 -550 0 0 {name=p93 sig_type=std_logic lab=neu_req[0:15]}
C {devices/iopin.sym} 1295 -960 0 0 {name=p519 lab=dGND
}
C {devices/iopin.sym} 1295 -940 0 0 {name=p520 lab=dVDD}
C {devices/ipin.sym} 1805 -990 0 0 {name=p521 lab=vepulseextp

}
C {devices/ipin.sym} 1345 -1070 0 0 {name=p522 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 1535 -1075 0 0 {name=p523 lab=W[0:3]

}
C {devices/ipin.sym} 1805 -1050 0 0 {name=p524 lab=vethrdpin

}
C {devices/ipin.sym} 1805 -1020 0 0 {name=p525 lab=vetaudpip

}
C {devices/ipin.sym} 1805 -1080 0 0 {name=p526 lab=vestddpin

}
C {devices/ipin.sym} 1535 -1015 0 0 {name=p527 lab=setW

}
C {devices/ipin.sym} 1535 -1045 0 0 {name=p528 lab=resetW

}
C {devices/ipin.sym} 1345 -1040 0 0 {name=p529 lab=neu_req[0:15]

}
C {devices/ipin.sym} 1345 -1010 0 0 {name=p530 lab=exc

}
C {devices/ipin.sym} 2035 -1050 0 0 {name=p531 lab=vithrdpip

}
C {devices/ipin.sym} 2035 -1020 0 0 {name=p532 lab=vitaudpin

}
C {devices/ipin.sym} 2035 -1080 0 0 {name=p533 lab=vistddpip

}
C {devices/ipin.sym} 1805 -970 0 0 {name=p534 lab=vipulseextp

}
C {devices/ipin.sym} 2315 -970 0 0 {name=p535 lab=vleakn
}
C {devices/ipin.sym} 2315 -1050 0 0 {name=p536 lab=ifdcp
}
C {devices/ipin.sym} 2315 -1010 0 0 {name=p537 lab=ifthrp
}
C {devices/ipin.sym} 2315 -1070 0 0 {name=p538 lab=ifahwp
}
C {devices/ipin.sym} 2325 -1030 0 0 {name=p539 lab=ifahthrp
}
C {devices/ipin.sym} 2315 -930 2 1 {name=p540 lab=ifahtaun
}
C {devices/ipin.sym} 2315 -990 2 1 {name=p541 lab=ifcascn
}
C {devices/ipin.sym} 2315 -950 2 1 {name=p542 lab=vrefn
}
C {devices/ipin.sym} 2315 -1090 2 1 {name=p543 lab=ifnmdap
}
C {devices/ipin.sym} 1335 -845 0 0 {name=p544 lab=nRes

}
C {devices/iopin.sym} 1405 -960 0 0 {name=p545 lab=aGND
}
C {devices/iopin.sym} 1405 -940 0 0 {name=p546 lab=aVDD}
C {devices/ipin.sym} 2545 -1080 0 0 {name=p547 lab=bufmonp

}
C {devices/iopin.sym} 2525 -1050 0 0 {name=p548 lab=monout[0:15]}
C {devices/ipin.sym} 1125 -1070 0 0 {name=p513 lab=ack_neu[0:15]

}
C {devices/opin.sym} 995 -1030 0 0 {name=p514 lab=req_neu_out[0:15]

}
