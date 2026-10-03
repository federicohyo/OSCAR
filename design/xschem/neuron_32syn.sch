v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 740 -1230 0 0 0.4 0.4 {}
T {input spikes} 250 -1230 0 0 0.4 0.4 {}
T {synaptic weight} 460 -1235 0 0 0.4 0.4 {}
T {analog synapse} 970 -1230 0 0 0.4 0.4 {}
T {neuron biases} 1240 -1230 0 0 0.4 0.4 {}
T {reset asynch digital logic} 180 -1000 0 0 0.4 0.4 {}
T {monitor} 1520 -1230 0 0 0.4 0.4 {}
N 1220 -340 1380 -340 {
lab=#net1}
N 1380 -580 1380 -340 {
lab=#net1}
N 1220 -550 1380 -550 {
lab=#net1}
N 1250 -850 1380 -850 {
lab=#net1}
N 1380 -850 1380 -580 {
lab=#net1}
N 1250 -870 1380 -870 {
lab=nreq_neu1}
N 1520 -870 1540 -870 {
lab=req}
N 1380 -870 1420 -870 {
lab=nreq_neu1}
N 890 -870 950 -870 {
lab=#net2}
N 820 -930 950 -930 {
lab=ack_out}
N 810 -930 820 -930 {
lab=ack_out}
N 260 -660 290 -660 {
lab=setW}
N 260 -620 290 -620 {
lab=exc}
N 260 -590 290 -590 {
lab=setW}
N 260 -550 290 -550 {
lab=nExc}
N 260 -510 290 -510 {
lab=resetW}
N 260 -470 290 -470 {
lab=exc}
N 260 -430 290 -430 {
lab=resetW}
N 260 -390 290 -390 {
lab=nExc}
N 260 -350 290 -350 {
lab=syn_req}
N 260 -310 290 -310 {
lab=exc}
N 260 -280 290 -280 {
lab=syn_req}
N 260 -240 290 -240 {
lab=nExc}
N 1830 -750 1880 -750 {
lab=monout}
N 1250 -830 1370 -830 {
lab=#net3}
N 1370 -830 1370 -810 {
lab=#net3}
N 1370 -810 1390 -810 {
lab=#net3}
N 1390 -830 1390 -810 {
lab=#net3}
N 1390 -830 1420 -830 {
lab=#net3}
N 1420 -830 1420 -730 {
lab=#net3}
N 1420 -730 1530 -730 {
lab=#net3}
N 860 -870 890 -870 {
lab=#net2}
N 730 -870 780 -870 {
lab=ack_cel1}
C {synapse_array_programmable_16_to_sout.sym} 1070 -470 0 0 {name=x1}
C {synapse_array_programmable_inh_16_to_sout.sym} 1070 -260 0 0 {name=x2}
C {neuron_analog_fc.sym} 1100 -780 0 0 {name=x3}
C {c_element_rj.sym} 1100 -950 0 0 {name=x11}
C {devices/lab_pin.sym} 1250 -930 2 0 {name=p34 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1250 -970 2 0 {name=p61 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 950 -970 0 0 {name=p62 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 950 -950 0 0 {name=p39 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 1250 -950 2 0 {name=p65 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1220 -530 2 0 {name=p3 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1220 -510 2 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1220 -320 2 0 {name=p5 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1220 -300 2 0 {name=p6 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1400 -870 1 0 {name=p9 sig_type=std_logic lab=nreq_neu1}
C {devices/lab_pin.sym} 950 -730 0 0 {name=p10 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 950 -710 0 0 {name=p11 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 950 -830 0 0 {name=p12 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 950 -850 0 0 {name=p13 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 950 -790 0 0 {name=p14 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 950 -810 0 0 {name=p16 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 950 -770 0 0 {name=p17 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 950 -750 0 0 {name=p18 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 950 -690 0 0 {name=p19 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 730 -870 0 0 {name=p8 sig_type=std_logic lab=ack_cel1}
C {devices/ipin.sym} 815 -930 0 0 {name=p15 lab=ack_out


}
C {devices/iopin.sym} 330 -1060 0 0 {name=p20 lab=dGND
}
C {devices/iopin.sym} 330 -1040 0 0 {name=p21 lab=dVDD}
C {devices/ipin.sym} 840 -1090 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 380 -1170 0 0 {name=p46 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 570 -1175 0 0 {name=p22 lab=W[0:3]

}
C {devices/ipin.sym} 840 -1150 0 0 {name=p381 lab=vethrdpin

}
C {devices/ipin.sym} 840 -1120 0 0 {name=p382 lab=vetaudpip

}
C {devices/ipin.sym} 840 -1180 0 0 {name=p383 lab=vestddpin

}
C {devices/ipin.sym} 570 -1115 0 0 {name=p23 lab=setW

}
C {devices/ipin.sym} 570 -1145 0 0 {name=p24 lab=resetW

}
C {devices/ipin.sym} 380 -1140 0 0 {name=p26 lab=syn_req

}
C {devices/ipin.sym} 380 -1110 0 0 {name=p25 lab=exc

}
C {devices/ipin.sym} 1070 -1150 0 0 {name=p30 lab=vithrdpip

}
C {devices/ipin.sym} 1070 -1120 0 0 {name=p31 lab=vitaudpin

}
C {devices/ipin.sym} 1070 -1180 0 0 {name=p32 lab=vistddpip

}
C {devices/lab_pin.sym} 920 -550 0 0 {name=p27 sig_type=std_logic lab=vestddpin}
C {devices/lab_pin.sym} 920 -490 0 0 {name=p28 sig_type=std_logic lab=vethrdpin}
C {devices/lab_pin.sym} 920 -430 0 0 {name=p29 sig_type=std_logic lab=vetaudpip}
C {devices/lab_pin.sym} 920 -340 0 0 {name=p33 sig_type=std_logic lab=vistddpip}
C {devices/lab_pin.sym} 920 -280 0 0 {name=p35 sig_type=std_logic lab=vithrdpip}
C {devices/lab_pin.sym} 920 -220 0 0 {name=p36 sig_type=std_logic lab=vitaudpin}
C {sky130_stdcells/and2_1.sym} 350 -640 0 0 {name=x4 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 340 -750 0 0 {name=x5 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 350 -570 0 0 {name=x6 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 350 -490 0 0 {name=x7 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 300 -750 0 0 {name=p37 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 380 -750 2 0 {name=p38 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 410 -640 2 0 {name=p41 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 410 -570 2 0 {name=p42 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 920 -470 0 0 {name=p43 sig_type=std_logic lab=resetWe}
C {sky130_stdcells/and2_1.sym} 350 -410 0 0 {name=x8 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 410 -410 2 0 {name=p44 sig_type=std_logic lab=resetWi}
C {sky130_stdcells/and2_1.sym} 350 -330 0 0 {name=x10 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 410 -330 2 0 {name=p45 sig_type=std_logic lab=reqe}
C {sky130_stdcells/and2_1.sym} 350 -260 0 0 {name=x12 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 410 -260 2 0 {name=p47 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 920 -410 0 0 {name=p48 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 410 -490 2 0 {name=p49 sig_type=std_logic lab=resetWe}
C {devices/lab_pin.sym} 920 -260 0 0 {name=p50 sig_type=std_logic lab=resetWi}
C {devices/lab_pin.sym} 920 -450 0 0 {name=p51 sig_type=std_logic lab=reqe}
C {devices/lab_pin.sym} 920 -240 0 0 {name=p52 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 920 -200 0 0 {name=p53 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 260 -620 0 0 {name=p54 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 260 -470 0 0 {name=p56 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 260 -390 0 0 {name=p57 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 260 -240 0 0 {name=p59 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 260 -660 0 0 {name=p60 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 260 -590 0 0 {name=p63 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 260 -510 0 0 {name=p64 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 260 -430 0 0 {name=p66 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 260 -350 0 0 {name=p67 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 920 -530 0 0 {name=p69 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 920 -320 0 0 {name=p70 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 920 -510 0 0 {name=p71 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 920 -300 0 0 {name=p72 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 920 -390 0 0 {name=p73 sig_type=std_logic lab=vepulseextp}
C {devices/ipin.sym} 840 -1070 0 0 {name=p74 lab=vipulseextp

}
C {devices/lab_pin.sym} 920 -180 0 0 {name=p75 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 260 -550 0 0 {name=p55 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 260 -310 0 0 {name=p58 sig_type=std_logic lab=exc}
C {devices/opin.sym} 1540 -870 0 0 {name=p152 lab=req}
C {devices/lab_pin.sym} 260 -280 0 0 {name=p7 sig_type=std_logic lab=syn_req}
C {devices/ipin.sym} 1350 -1070 0 0 {name=p68 lab=vleakn
}
C {devices/ipin.sym} 1350 -1150 0 0 {name=p76 lab=ifdcp
}
C {devices/ipin.sym} 1350 -1110 0 0 {name=p77 lab=ifthrp
}
C {devices/ipin.sym} 1350 -1170 0 0 {name=p78 lab=ifahwp
}
C {devices/ipin.sym} 1360 -1130 0 0 {name=p79 lab=ifahthrp
}
C {devices/ipin.sym} 1350 -1030 2 1 {name=p80 lab=ifahtaun
}
C {devices/ipin.sym} 1350 -1090 2 1 {name=p81 lab=ifcascn
}
C {devices/ipin.sym} 1350 -1050 2 1 {name=p82 lab=vrefn
}
C {devices/ipin.sym} 1350 -1190 2 1 {name=p83 lab=ifnmdap
}
C {devices/ipin.sym} 370 -945 0 0 {name=p84 lab=nRes

}
C {buffer_mon.sym} 1680 -730 0 0 {name=x13}
C {devices/lab_pin.sym} 1830 -730 2 0 {name=p85 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1830 -710 2 0 {name=p86 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 440 -1060 0 0 {name=p87 lab=aGND
}
C {devices/iopin.sym} 440 -1040 0 0 {name=p88 lab=aVDD}
C {devices/lab_pin.sym} 1250 -810 2 0 {name=p1 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1250 -790 2 0 {name=p2 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 1580 -1180 0 0 {name=p89 lab=buffermonp

}
C {devices/iopin.sym} 1560 -1150 0 0 {name=p90 lab=monout}
C {devices/lab_pin.sym} 1880 -750 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1530 -750 0 0 {name=p92 sig_type=std_logic lab=buffermonp}
C {sky130_stdcells/inv_1.sym} 820 -870 0 0 {name=x14 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {schmitt_trigger.sym} 1500 -870 0 0 {name=x15}
C {devices/lab_pin.sym} 1460 -910 0 1 {name=p93 lab=dVDD}
C {devices/lab_pin.sym} 1460 -830 0 1 {name=p94 lab=dGND}
