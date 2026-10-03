v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Digital IN} 1510 -850 0 0 0.4 0.4 {}
T {Neuron with 16 synapses} 2470 -640 0 0 0.4 0.4 {}
T {Digital OUT} 1670 -850 0 0 0.4 0.4 {}
T {Neuron Biases} 1890 -850 0 0 0.4 0.4 {}
T {Synapse Biases} 2120 -840 0 0 0.4 0.4 {}
N 2750 -460 2780 -460 {
lab=nreq_neu0}
N 2390 -460 2450 -460 {
lab=nack_cel0}
N 2850 -340 2890 -340 {
lab=nreq_neu0}
N 2850 -460 2850 -360 {
lab=nreq_neu0}
N 2780 -460 2850 -460 {
lab=nreq_neu0}
N 1710 -400 1730 -400 {
lab=vtaup}
N 1710 -360 1720 -360 {
lab=vthrn}
N 1370 -400 1410 -400 {
lab=Spk_in[0]}
N 1380 -380 1410 -380 {
lab=D[0:3]}
N 1710 -380 1900 -380 {
lab=STOT}
N 1870 -400 1900 -400 {
lab=Enable}
N 3020 -360 3050 -360 {
lab=Enable}
N 2990 -340 3050 -340 {
lab=#net1}
N 1700 -130 1810 -130 {
lab=STOT}
N 2850 -360 2850 -340 {
lab=nreq_neu0}
C {devices/lab_pin.sym} 3350 -360 2 0 {name=p2 sig_type=std_logic lab=Req_out}
C {neuron_analog_fc.sym} 2600 -370 0 0 {name=x3}
C {devices/lab_pin.sym} 2850 -460 2 0 {name=p8 sig_type=std_logic lab=nreq_neu0}
C {devices/lab_pin.sym} 2450 -300 0 0 {name=p22 sig_type=std_logic lab=ifvrefn}
C {devices/lab_pin.sym} 2450 -440 0 0 {name=p23 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 2450 -420 0 0 {name=p24 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 2450 -400 0 0 {name=p25 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 2450 -380 0 0 {name=p26 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 2450 -360 0 0 {name=p27 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 2450 -340 0 0 {name=p28 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 2450 -280 0 0 {name=p29 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 2750 -400 2 0 {name=p53 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 2750 -440 2 0 {name=p54 sig_type=std_logic lab=sinp0}
C {c_element_rj.sym} 2600 -540 0 0 {name=x14}
C {devices/lab_pin.sym} 2750 -520 2 0 {name=p78 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 2750 -560 2 0 {name=p82 sig_type=std_logic lab=ack_cel0}
C {devices/lab_pin.sym} 2450 -560 0 0 {name=p84 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 2450 -540 0 0 {name=p63 sig_type=std_logic lab=Req_out}
C {devices/lab_pin.sym} 2390 -460 0 0 {name=p31 sig_type=std_logic lab=nack_cel0}
C {devices/lab_pin.sym} 2450 -520 0 0 {name=p60 sig_type=std_logic lab=Ack_in}
C {devices/lab_pin.sym} 2750 -540 2 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2750 -380 2 0 {name=p48 sig_type=std_logic lab=aVDD}
C {dpi_syn_exc_4bit_fc.sym} 1560 -350 0 0 {name=x4}
C {devices/lab_pin.sym} 1730 -400 2 0 {name=p13 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1720 -360 2 0 {name=p14 sig_type=std_logic lab=vthrn}
C {devices/lab_pin.sym} 1710 -340 2 0 {name=p15 sig_type=std_logic lab=vstdn}
C {devices/lab_pin.sym} 1370 -400 0 0 {name=p17 sig_type=std_logic lab=Spk_in[0]}
C {devices/lab_pin.sym} 1710 -320 2 0 {name=p38 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1710 -300 2 0 {name=p30 sig_type=std_logic lab=VDD}
C {dflip_flop_chain_4_fc.sym} 1560 -490 0 0 {name=x5}
C {devices/lab_pin.sym} 1410 -500 0 0 {name=p5 sig_type=std_logic lab=Clk}
C {devices/lab_pin.sym} 1410 -520 0 0 {name=p6 sig_type=std_logic lab=Win}
C {devices/lab_pin.sym} 1410 -480 0 0 {name=p18 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1410 -460 0 0 {name=p19 sig_type=std_logic lab=sDone}
C {devices/lab_pin.sym} 1710 -520 2 0 {name=p7 sig_type=std_logic lab=D[0:3]
}
C {devices/lab_pin.sym} 1390 -380 0 0 {name=p1 sig_type=std_logic lab=D[0:3]
}
C {devices/lab_pin.sym} 2950 -560 0 0 {name=p89 sig_type=std_logic lab=ack_cel0}
C {sky130_stdcells/inv_1.sym} 2990 -560 0 0 {name=x13 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 3030 -560 2 0 {name=p90 sig_type=std_logic lab=nack_cel0}
C {tranmission_gate_fc.sym} 2050 -380 0 0 {name=x1}
C {devices/lab_pin.sym} 2200 -400 2 0 {name=p16 sig_type=std_logic lab=sinp0}
C {devices/lab_pin.sym} 2200 -380 2 0 {name=p21 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 2200 -360 2 0 {name=p32 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1870 -400 1 0 {name=p33 sig_type=std_logic lab=Enable}
C {tranmission_gate_fc.sym} 3200 -340 0 0 {name=x2}
C {devices/lab_pin.sym} 3350 -340 2 0 {name=p35 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 3350 -320 2 0 {name=p36 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 3020 -360 1 0 {name=p39 sig_type=std_logic lab=Enable}
C {devices/iopin.sym} 1340 -820 0 0 {name=p34 lab=GND
}
C {devices/iopin.sym} 1340 -800 0 0 {name=p40 lab=VDD}
C {devices/iopin.sym} 1340 -780 0 0 {name=p41 lab=aVDD}
C {devices/ipin.sym} 1570 -660 0 0 {name=p42 lab=Enable
}
C {devices/ipin.sym} 1570 -760 0 0 {name=p43 lab=Clk
}
C {devices/ipin.sym} 1570 -740 0 0 {name=p44 lab=nRes
}
C {devices/ipin.sym} 1570 -710 0 0 {name=p45 lab=sDone
}
C {devices/ipin.sym} 1570 -620 0 0 {name=p46 lab=Spk_in[0:1]
}
C {devices/ipin.sym} 1570 -690 0 0 {name=p47 lab=Ack_in
}
C {devices/opin.sym} 1670 -790 0 0 {name=p49 lab=Req_out}
C {devices/ipin.sym} 1970 -810 0 0 {name=p50 lab=ifdcp
}
C {devices/ipin.sym} 1970 -770 0 0 {name=p51 lab=ifnmdap
}
C {devices/ipin.sym} 1970 -740 0 0 {name=p52 lab=ifthrp
}
C {devices/ipin.sym} 1970 -710 0 0 {name=p55 lab=ifleakn}
C {devices/ipin.sym} 1980 -680 0 0 {name=p56 lab=ifahthrp
}
C {devices/ipin.sym} 1980 -650 0 0 {name=p57 lab=ifahwp
}
C {devices/ipin.sym} 1970 -620 2 1 {name=p58 lab=ifcascn
}
C {devices/ipin.sym} 1980 -590 2 1 {name=p59 lab=ifahtaun
}
C {devices/ipin.sym} 1970 -570 0 0 {name=p61 lab=ifvrefn
}
C {devices/iopin.sym} 2200 -790 2 0 {name=p62 lab=vthrn

}
C {devices/iopin.sym} 2200 -770 2 0 {name=p64 lab=vtaup

}
C {devices/iopin.sym} 2200 -740 2 0 {name=p65 lab=vstdn

}
C {devices/ipin.sym} 1570 -790 0 0 {name=p66 lab=Win
}
C {devices/lab_pin.sym} 2450 -320 0 0 {name=p20 sig_type=std_logic lab=ifleakn}
C {dflip_flop_chain_4_fc.sym} 1550 -220 0 0 {name=x7}
C {devices/lab_pin.sym} 1400 -230 0 0 {name=p70 sig_type=std_logic lab=Clk}
C {devices/lab_pin.sym} 1400 -250 0 0 {name=p71 sig_type=std_logic lab=Dout1}
C {devices/lab_pin.sym} 1400 -210 0 0 {name=p72 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1400 -190 0 0 {name=p73 sig_type=std_logic lab=sDone}
C {devices/lab_pin.sym} 1700 -250 2 0 {name=p74 sig_type=std_logic lab=D[4:7]
}
C {dpi_syn_exc_4bit_fc.sym} 1550 -100 0 0 {name=x6}
C {devices/lab_pin.sym} 1400 -150 0 0 {name=p67 sig_type=std_logic lab=Spk_in[1]}
C {devices/lab_pin.sym} 1400 -130 0 0 {name=p68 sig_type=std_logic lab=D[4:7]}
C {devices/lab_pin.sym} 1700 -50 2 0 {name=p77 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1700 -70 2 0 {name=p83 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1700 -90 2 0 {name=p85 sig_type=std_logic lab=vstdn}
C {devices/lab_pin.sym} 1700 -110 2 0 {name=p86 sig_type=std_logic lab=vthrn}
C {devices/lab_pin.sym} 1700 -150 2 0 {name=p87 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1800 -380 3 0 {name=p88 sig_type=std_logic lab=STOT}
C {devices/lab_pin.sym} 1810 -130 2 0 {name=p91 sig_type=std_logic lab=STOT}
C {schmitt_trigger.sym} 2970 -340 0 0 {name=x9}
C {devices/lab_pin.sym} 2930 -380 0 0 {name=p3 lab=VDD}
C {devices/lab_pin.sym} 2930 -300 0 0 {name=p4 lab=GND}
C {devices/lab_pin.sym} 1710 -500 2 0 {name=p9 sig_type=std_logic lab=Dout1
}
C {devices/lab_pin.sym} 1700 -210 2 0 {name=p10 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1700 -190 2 0 {name=p11 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1710 -480 2 0 {name=p12 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1710 -460 2 0 {name=p69 sig_type=std_logic lab=VDD}
