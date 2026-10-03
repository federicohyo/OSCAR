v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 940 -1160 0 0 0.4 0.4 {}
T {input spikes} 460 -1160 0 0 0.4 0.4 {}
T {synaptic weight} 660 -1170 0 0 0.4 0.4 {}
T {analog synapse} 1170 -1160 0 0 0.4 0.4 {}
T {neuron biases} 1440 -1160 0 0 0.4 0.4 {}
T {reset asynch digital logic} 390 -840 0 0 0.4 0.4 {}
T {monitor} 1720 -1160 0 0 0.4 0.4 {}
N 1420 -290 1580 -290 {
lab=#net1}
N 1420 -500 1580 -500 {
lab=#net1}
N 1450 -680 1580 -680 {
lab=#net1}
N 1670 -740 1690 -740 {
lab=req}
N 1090 -720 1150 -720 {
lab=#net2}
N 1020 -800 1150 -800 {
lab=ack_out}
N 1010 -800 1020 -800 {
lab=ack_out}
N 460 -590 490 -590 {
lab=setW}
N 460 -550 490 -550 {
lab=exc}
N 460 -520 490 -520 {
lab=setW}
N 460 -480 490 -480 {
lab=nExc}
N 460 -440 490 -440 {
lab=resetW}
N 460 -400 490 -400 {
lab=exc}
N 460 -360 490 -360 {
lab=resetW}
N 460 -320 490 -320 {
lab=nExc}
N 460 -280 490 -280 {
lab=syn_req}
N 460 -240 490 -240 {
lab=exc}
N 460 -210 490 -210 {
lab=syn_req}
N 460 -170 490 -170 {
lab=nExc}
N 2030 -680 2080 -680 {
lab=monout}
N 1620 -660 1730 -660 {
lab=#net1}
N 1060 -720 1090 -720 {
lab=#net2}
N 930 -720 980 -720 {
lab=ack_cel1}
N 1580 -680 1580 -510 {
lab=#net1}
N 1580 -660 1620 -660 {
lab=#net1}
N 1450 -700 1550 -700 {
lab=nreq_neu1}
N 1550 -740 1550 -700 {
lab=nreq_neu1}
N 1580 -510 1580 -290 {
lab=#net1}
N 1550 -740 1580 -740 {
lab=nreq_neu1}
C {c_element_rj.sym} 1300 -820 0 0 {name=x11}
C {devices/lab_pin.sym} 1450 -800 2 0 {name=p34 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1450 -840 2 0 {name=p61 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1150 -840 0 0 {name=p62 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1150 -820 0 0 {name=p39 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 1450 -820 2 0 {name=p65 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1420 -440 2 0 {name=p4 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1420 -270 2 0 {name=p5 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1570 -740 1 0 {name=p9 sig_type=std_logic lab=nreq_neu1}
C {devices/lab_pin.sym} 1150 -700 0 0 {name=p10 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1150 -680 0 0 {name=p11 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1150 -740 0 0 {name=p14 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 930 -720 0 0 {name=p8 sig_type=std_logic lab=ack_cel1}
C {devices/ipin.sym} 1020 -800 0 0 {name=p15 lab=ack_out


}
C {devices/iopin.sym} 530 -990 0 0 {name=p20 lab=dGND
}
C {devices/iopin.sym} 530 -970 0 0 {name=p21 lab=dVDD}
C {devices/ipin.sym} 1030 -1080 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 580 -1100 0 0 {name=p46 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 770 -1110 0 0 {name=p22 lab=W[0:3]

}
C {devices/ipin.sym} 770 -1050 0 0 {name=p23 lab=setW

}
C {devices/ipin.sym} 770 -1080 0 0 {name=p24 lab=resetW

}
C {devices/ipin.sym} 580 -1070 0 0 {name=p26 lab=syn_req

}
C {devices/ipin.sym} 580 -1040 0 0 {name=p25 lab=exc

}
C {sky130_stdcells/and2_1.sym} 550 -570 0 0 {name=x4 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 540 -680 0 0 {name=x5 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 550 -500 0 0 {name=x6 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 550 -420 0 0 {name=x7 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 500 -680 0 0 {name=p37 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 580 -680 2 0 {name=p38 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 610 -570 2 0 {name=p41 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 610 -500 2 0 {name=p42 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 1120 -420 0 0 {name=p43 sig_type=std_logic lab=resetWe}
C {sky130_stdcells/and2_1.sym} 550 -340 0 0 {name=x8 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 610 -340 2 0 {name=p44 sig_type=std_logic lab=resetWi}
C {sky130_stdcells/and2_1.sym} 550 -260 0 0 {name=x10 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 610 -260 2 0 {name=p45 sig_type=std_logic lab=reqe}
C {sky130_stdcells/and2_1.sym} 550 -190 0 0 {name=x12 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 610 -190 2 0 {name=p47 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 1120 -380 0 0 {name=p48 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 610 -420 2 0 {name=p49 sig_type=std_logic lab=resetWe}
C {devices/lab_pin.sym} 1120 -210 0 0 {name=p50 sig_type=std_logic lab=resetWi}
C {devices/lab_pin.sym} 1120 -400 0 0 {name=p51 sig_type=std_logic lab=reqe}
C {devices/lab_pin.sym} 1120 -190 0 0 {name=p52 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 1120 -150 0 0 {name=p53 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 460 -550 0 0 {name=p54 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 460 -400 0 0 {name=p56 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 460 -320 0 0 {name=p57 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 460 -170 0 0 {name=p59 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 460 -590 0 0 {name=p60 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 460 -520 0 0 {name=p63 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 460 -440 0 0 {name=p64 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 460 -360 0 0 {name=p66 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 460 -280 0 0 {name=p67 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 1120 -500 0 0 {name=p69 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1120 -290 0 0 {name=p70 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1120 -460 0 0 {name=p71 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1120 -250 0 0 {name=p72 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1120 -440 0 0 {name=p73 sig_type=std_logic lab=vepulseextp}
C {devices/ipin.sym} 1300 -1080 0 0 {name=p74 lab=vipulseextp

}
C {devices/lab_pin.sym} 1120 -230 0 0 {name=p75 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 460 -480 0 0 {name=p55 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 460 -240 0 0 {name=p58 sig_type=std_logic lab=exc}
C {devices/opin.sym} 1690 -740 0 0 {name=p152 lab=req}
C {devices/lab_pin.sym} 460 -210 0 0 {name=p7 sig_type=std_logic lab=syn_req}
C {devices/ipin.sym} 1550 -1080 0 0 {name=p68 lab=vleakn
}
C {devices/ipin.sym} 1550 -1110 0 0 {name=p76 lab=ifdcp
}
C {devices/ipin.sym} 1550 -1050 2 1 {name=p82 lab=vrefn
}
C {devices/ipin.sym} 580 -790 0 0 {name=p84 lab=nRes

}
C {devices/lab_pin.sym} 2030 -660 2 0 {name=p85 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 2030 -640 2 0 {name=p86 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 640 -970 0 0 {name=p88 lab=aVDD}
C {devices/lab_pin.sym} 1450 -740 2 0 {name=p1 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1450 -720 2 0 {name=p2 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 1780 -1110 0 0 {name=p89 lab=buffermonp

}
C {devices/iopin.sym} 1760 -1080 0 0 {name=p90 lab=monout}
C {devices/lab_pin.sym} 2080 -680 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1730 -680 0 0 {name=p92 sig_type=std_logic lab=buffermonp}
C {sky130_stdcells/inv_1.sym} 1020 -720 0 0 {name=x14 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__}
C {devices/ipin.sym} 1030 -1110 0 0 {name=p12 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 1300 -1110 0 0 {name=p383 lab=JInhWp[0:3]

}
C {synapse_array_programmable_16_to_sout_v1.sym} 1270 -420 0 0 {name=x1}
C {synapse_array_programmable_inh_16_to_sout_v1.sym} 1270 -210 0 0 {name=x2}
C {devices/lab_pin.sym} 1120 -270 0 0 {name=p31 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 1420 -250 2 0 {name=p27 sig_type=std_logic lab=dVDD}
C {schmitt_trigger.sym} 1660 -740 0 0 {name=x9}
C {devices/lab_pin.sym} 1620 -700 2 0 {name=p77 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1620 -780 2 0 {name=p78 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1120 -480 0 0 {name=p6 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/ipin.sym} 1030 -1060 0 0 {name=p13 lab=vtaun

}
C {devices/ipin.sym} 1030 -1040 0 0 {name=p16 lab=vthrdp

}
C {devices/lab_pin.sym} 1120 -130 0 0 {name=p17 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1120 -170 0 0 {name=p18 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 1120 -360 0 0 {name=p19 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1120 -340 0 0 {name=p28 sig_type=std_logic lab=vtaup}
C {devices/ipin.sym} 1300 -1050 0 0 {name=p29 lab=vtaup

}
C {devices/ipin.sym} 1300 -1030 0 0 {name=p30 lab=vthrdn

}
C {devices/lab_pin.sym} 1420 -460 2 0 {name=p32 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1420 -480 2 0 {name=p33 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1420 -230 2 0 {name=p36 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 640 -940 0 0 {name=p3 lab=aGND
}
C {devices/lab_pin.sym} 1420 -420 2 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1420 -210 2 0 {name=p79 sig_type=std_logic lab=aGND}
C {neuron_analog_fc_v2_norail.sym} 1300 -710 0 0 {name=x3}
C {buffer_mon_p_norail.sym} 1880 -660 0 0 {name=x13}
