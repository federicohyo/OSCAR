v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {reset asynch digital logic} 230 -830 0 0 0.4 0.4 {}
T {analog synapse} 740 -1180 0 0 0.4 0.4 {}
T {input spikes} 260 -1180 0 0 0.4 0.4 {}
T {synaptic weight} 460 -1185 0 0 0.4 0.4 {}
T {analog synapse} 970 -1180 0 0 0.4 0.4 {}
T {neuron biases} 1240 -1180 0 0 0.4 0.4 {}
T {monitor} 1520 -1180 0 0 0.4 0.4 {}
N 1230 -740 1360 -740 {
lab=vmem}
N 1210 -570 1360 -570 {
lab=vmem}
N 1330 -800 1370 -800 {
lab=nreq_neu1}
N 870 -780 930 -780 {
lab=#net1}
N 800 -860 930 -860 {
lab=ack_out}
N 790 -860 800 -860 {
lab=ack_out}
N 280 -600 310 -600 {
lab=setW}
N 280 -560 310 -560 {
lab=exc}
N 280 -530 310 -530 {
lab=setW}
N 280 -490 310 -490 {
lab=nExc}
N 280 -450 310 -450 {
lab=resetW}
N 280 -410 310 -410 {
lab=exc}
N 280 -370 310 -370 {
lab=resetW}
N 280 -330 310 -330 {
lab=nExc}
N 280 -290 310 -290 {
lab=syn_req}
N 280 -250 310 -250 {
lab=exc}
N 280 -220 310 -220 {
lab=syn_req}
N 280 -180 310 -180 {
lab=nExc}
N 1810 -740 1860 -740 {
lab=monout}
N 1400 -720 1510 -720 {
lab=vmem}
N 840 -780 870 -780 {
lab=#net1}
N 710 -780 760 -780 {
lab=ack_cel1}
N 1360 -720 1400 -720 {
lab=vmem}
N 1230 -760 1330 -760 {
lab=nreq_neu1}
N 1330 -800 1330 -760 {
lab=nreq_neu1}
N 1050 -540 1120 -540 {
lab=vmem}
N 1180 -540 1210 -540 {
lab=vmem}
N 1360 -740 1360 -720 {
lab=vmem}
N 1360 -720 1360 -570 {
lab=vmem}
N 1050 -330 1150 -330 {
lab=vmem}
N 1175 -540 1180 -540 {
lab=vmem}
N 1120 -540 1175 -540 {
lab=vmem}
N 1210 -570 1210 -540 {
lab=vmem}
N 1150 -540 1150 -330 {
lab=vmem}
N 1470 -800 1497.5 -800 {
lab=req}
C {c_element_rj.sym} 1080 -880 0 0 {name=x11}
C {devices/lab_pin.sym} 1230 -860 2 0 {name=p34 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1230 -900 2 0 {name=p61 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 930 -900 0 0 {name=p62 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 930 -880 0 0 {name=p39 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 1230 -880 2 0 {name=p65 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1050 -520 2 0 {name=p3 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1050 -480 2 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1050 -310 2 0 {name=p5 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1350 -800 1 0 {name=p9 sig_type=std_logic lab=nreq_neu1}
C {devices/lab_pin.sym} 930 -760 0 0 {name=p10 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 930 -740 0 0 {name=p11 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 930 -800 0 0 {name=p14 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 710 -780 0 0 {name=p8 sig_type=std_logic lab=ack_cel1}
C {devices/ipin.sym} 795 -860 0 0 {name=p15 lab=ack_out


}
C {devices/iopin.sym} 330 -1010 0 0 {name=p20 lab=dGND
}
C {devices/iopin.sym} 330 -990 0 0 {name=p21 lab=dVDD}
C {devices/ipin.sym} 840 -1040 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 380 -1120 0 0 {name=p46 lab=syn_addr[0:1]

}
C {devices/ipin.sym} 570 -1125 0 0 {name=p22 lab=W[0:3]

}
C {devices/ipin.sym} 570 -1065 0 0 {name=p23 lab=setW

}
C {devices/ipin.sym} 570 -1095 0 0 {name=p24 lab=resetW

}
C {devices/ipin.sym} 380 -1090 0 0 {name=p26 lab=syn_req

}
C {devices/ipin.sym} 380 -1060 0 0 {name=p25 lab=exc

}
C {sky130_stdcells/and2_1.sym} 370 -580 0 0 {name=x4 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 360 -690 0 0 {name=x5 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 370 -510 0 0 {name=x6 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 370 -430 0 0 {name=x7 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 320 -690 0 0 {name=p37 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 400 -690 2 0 {name=p38 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 430 -580 2 0 {name=p41 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 430 -510 2 0 {name=p42 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 750 -460 0 0 {name=p43 sig_type=std_logic lab=resetWe}
C {sky130_stdcells/and2_1.sym} 370 -350 0 0 {name=x8 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 430 -350 2 0 {name=p44 sig_type=std_logic lab=resetWi}
C {sky130_stdcells/and2_1.sym} 370 -270 0 0 {name=x10 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 430 -270 2 0 {name=p45 sig_type=std_logic lab=reqe}
C {sky130_stdcells/and2_1.sym} 370 -200 0 0 {name=x12 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 430 -200 2 0 {name=p47 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 750 -400 0 0 {name=p48 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 430 -430 2 0 {name=p49 sig_type=std_logic lab=resetWe}
C {devices/lab_pin.sym} 750 -250 0 0 {name=p50 sig_type=std_logic lab=resetWi}
C {devices/lab_pin.sym} 750 -420 0 0 {name=p51 sig_type=std_logic lab=reqe}
C {devices/lab_pin.sym} 750 -230 0 0 {name=p52 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 750 -190 0 0 {name=p53 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 280 -560 0 0 {name=p54 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 280 -410 0 0 {name=p56 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 280 -330 0 0 {name=p57 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 280 -180 0 0 {name=p59 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 280 -600 0 0 {name=p60 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 280 -530 0 0 {name=p63 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 280 -450 0 0 {name=p64 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 280 -370 0 0 {name=p66 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 280 -290 0 0 {name=p67 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 750 -520 0 0 {name=p69 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 750 -310 0 0 {name=p70 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 750 -500 0 0 {name=p71 sig_type=std_logic lab=syn_addr[0:1]}
C {devices/lab_pin.sym} 750 -290 0 0 {name=p72 sig_type=std_logic lab=syn_addr[0:1]}
C {devices/lab_pin.sym} 750 -380 0 0 {name=p73 sig_type=std_logic lab=vepulseextp}
C {devices/ipin.sym} 1110 -1030 0 0 {name=p74 lab=vipulseextp

}
C {devices/lab_pin.sym} 750 -210 0 0 {name=p75 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 280 -490 0 0 {name=p55 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 280 -250 0 0 {name=p58 sig_type=std_logic lab=exc}
C {devices/opin.sym} 1497.5 -800 0 0 {name=p152 lab=req}
C {devices/lab_pin.sym} 280 -220 0 0 {name=p7 sig_type=std_logic lab=syn_req}
C {devices/ipin.sym} 1345 -1100 0 0 {name=p68 lab=vleakn
}
C {devices/ipin.sym} 1345 -1130 0 0 {name=p76 lab=ifdcp
}
C {devices/ipin.sym} 1345 -1070 2 1 {name=p82 lab=vrefn
}
C {devices/ipin.sym} 370 -765 0 0 {name=p84 lab=nRes

}
C {devices/lab_pin.sym} 1810 -720 2 0 {name=p85 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1810 -700 2 0 {name=p86 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 440 -990 0 0 {name=p88 lab=aVDD}
C {devices/lab_pin.sym} 1230 -800 2 0 {name=p1 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1230 -780 2 0 {name=p2 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 1580 -1130 0 0 {name=p89 lab=buffermonp

}
C {devices/iopin.sym} 1560 -1100 0 0 {name=p90 lab=monout}
C {devices/lab_pin.sym} 1860 -740 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1510 -740 0 0 {name=p92 sig_type=std_logic lab=buffermonp}
C {sky130_stdcells/inv_1.sym} 800 -780 0 0 {name=x14 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {neuron_analog_fc_v1.sym} 1080 -770 0 0 {name=x3}
C {devices/ipin.sym} 825 -1130 0 0 {name=p12 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 1095 -1130 0 0 {name=p383 lab=JInhWp[0:3]

}
C {devices/lab_pin.sym} 750 -330 0 0 {name=p31 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 750 -540 0 0 {name=p36 sig_type=std_logic lab=JExcWn[0:3]}
C {synapse_array_programmable_4_to_sout_v1.sym} 900 -460 0 0 {name=x1}
C {synapse_array_programmable_inh_4_to_sout_v1.sym} 900 -250 0 0 {name=x2}
C {devices/lab_pin.sym} 1050 -270 2 0 {name=p27 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 750 -440 0 0 {name=p13 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 750 -480 0 0 {name=p16 sig_type=std_logic lab=vthrdn}
C {devices/ipin.sym} 840 -1060 0 0 {name=p17 lab=vtaup

}
C {devices/ipin.sym} 840 -1080 0 0 {name=p18 lab=vthrdn

}
C {devices/ipin.sym} 1090 -1060 0 0 {name=p19 lab=vtaun

}
C {devices/ipin.sym} 1090 -1080 0 0 {name=p30 lab=vthrdp

}
C {devices/lab_pin.sym} 750 -170 0 0 {name=p6 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 750 -270 0 0 {name=p28 sig_type=std_logic lab=vthrdp}
C {buffer_mon_p.sym} 1660 -720 0 0 {name=x15}
C {schmitt_trigger.sym} 1450 -800 0 0 {name=x9}
C {devices/lab_pin.sym} 1410 -760 2 0 {name=p77 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1410 -840 2 0 {name=p78 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1210 -570 0 0 {name=p29 sig_type=std_logic lab=vmem}
C {devices/lab_pin.sym} 1050 -500 2 0 {name=p32 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1050 -290 2 0 {name=p33 sig_type=std_logic lab=dVDD}
