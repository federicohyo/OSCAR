v {xschem version=3.4.7RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 720 -1180 0 0 0.4 0.4 {}
T {input spikes} 240 -1180 0 0 0.4 0.4 {}
T {synaptic weight} 440 -1190 0 0 0.4 0.4 {}
T {analog synapse} 950 -1180 0 0 0.4 0.4 {}
T {neuron biases} 1220 -1180 0 0 0.4 0.4 {}
T {reset asynch digital logic} 170 -860 0 0 0.4 0.4 {}
T {monitor} 1500 -1180 0 0 0.4 0.4 {}
N 1200 -310 1360 -310 {
lab=#net1}
N 1200 -520 1360 -520 {
lab=#net1}
N 1230 -700 1360 -700 {
lab=#net1}
N 1450 -760 1470 -760 {
lab=req}
N 870 -740 930 -740 {
lab=#net2}
N 800 -820 930 -820 {
lab=ack_out}
N 790 -820 800 -820 {
lab=ack_out}
N 240 -610 270 -610 {
lab=setW}
N 240 -570 270 -570 {
lab=exc}
N 240 -540 270 -540 {
lab=setW}
N 240 -500 270 -500 {
lab=nExc}
N 240 -460 270 -460 {
lab=resetW}
N 240 -420 270 -420 {
lab=exc}
N 240 -380 270 -380 {
lab=resetW}
N 240 -340 270 -340 {
lab=nExc}
N 240 -300 270 -300 {
lab=syn_req}
N 240 -260 270 -260 {
lab=exc}
N 240 -230 270 -230 {
lab=syn_req}
N 240 -190 270 -190 {
lab=nExc}
N 1810 -700 1860 -700 {
lab=monout}
N 1400 -680 1510 -680 {
lab=#net1}
N 840 -740 870 -740 {
lab=#net2}
N 710 -740 760 -740 {
lab=ack_cel1}
N 1360 -700 1360 -530 {
lab=#net1}
N 1360 -680 1400 -680 {
lab=#net1}
N 1230 -720 1330 -720 {
lab=nreq_neu1}
N 1330 -760 1330 -720 {
lab=nreq_neu1}
N 1360 -530 1360 -310 {
lab=#net1}
N 1330 -760 1360 -760 {
lab=nreq_neu1}
C {c_element_rj.sym} 1080 -840 0 0 {name=x11}
C {devices/lab_pin.sym} 1230 -820 2 0 {name=p34 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1230 -860 2 0 {name=p61 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 930 -860 0 0 {name=p62 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 930 -840 0 0 {name=p39 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 1230 -840 2 0 {name=p65 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1200 -460 2 0 {name=p4 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1200 -290 2 0 {name=p5 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1350 -760 1 0 {name=p9 sig_type=std_logic lab=nreq_neu1}
C {devices/lab_pin.sym} 930 -720 0 0 {name=p10 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 930 -700 0 0 {name=p11 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 930 -760 0 0 {name=p14 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 710 -740 0 0 {name=p8 sig_type=std_logic lab=ack_cel1}
C {devices/ipin.sym} 800 -820 0 0 {name=p15 lab=ack_out


}
C {devices/iopin.sym} 310 -1010 0 0 {name=p20 lab=dGND
}
C {devices/iopin.sym} 310 -990 0 0 {name=p21 lab=dVDD}
C {devices/ipin.sym} 810 -1100 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 360 -1120 0 0 {name=p46 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 550 -1130 0 0 {name=p22 lab=W[0:3]

}
C {devices/ipin.sym} 550 -1070 0 0 {name=p23 lab=setW

}
C {devices/ipin.sym} 550 -1100 0 0 {name=p24 lab=resetW

}
C {devices/ipin.sym} 360 -1090 0 0 {name=p26 lab=syn_req

}
C {devices/ipin.sym} 360 -1060 0 0 {name=p25 lab=exc

}
C {sky130_stdcells/and2_1.sym} 330 -590 0 0 {name=x4 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 320 -700 0 0 {name=x5 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 330 -520 0 0 {name=x6 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 330 -440 0 0 {name=x7 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 280 -700 0 0 {name=p37 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 360 -700 2 0 {name=p38 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 390 -590 2 0 {name=p41 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 390 -520 2 0 {name=p42 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 900 -440 0 0 {name=p43 sig_type=std_logic lab=resetWe}
C {sky130_stdcells/and2_1.sym} 330 -360 0 0 {name=x8 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 390 -360 2 0 {name=p44 sig_type=std_logic lab=resetWi}
C {sky130_stdcells/and2_1.sym} 330 -280 0 0 {name=x10 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 390 -280 2 0 {name=p45 sig_type=std_logic lab=reqe}
C {sky130_stdcells/and2_1.sym} 330 -210 0 0 {name=x12 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 390 -210 2 0 {name=p47 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 900 -400 0 0 {name=p48 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 390 -440 2 0 {name=p49 sig_type=std_logic lab=resetWe}
C {devices/lab_pin.sym} 900 -230 0 0 {name=p50 sig_type=std_logic lab=resetWi}
C {devices/lab_pin.sym} 900 -420 0 0 {name=p51 sig_type=std_logic lab=reqe}
C {devices/lab_pin.sym} 900 -210 0 0 {name=p52 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 900 -170 0 0 {name=p53 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 240 -570 0 0 {name=p54 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 240 -420 0 0 {name=p56 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 240 -340 0 0 {name=p57 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 240 -190 0 0 {name=p59 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 240 -610 0 0 {name=p60 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 240 -540 0 0 {name=p63 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 240 -460 0 0 {name=p64 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 240 -380 0 0 {name=p66 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 240 -300 0 0 {name=p67 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 900 -520 0 0 {name=p69 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 900 -310 0 0 {name=p70 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 900 -480 0 0 {name=p71 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 900 -270 0 0 {name=p72 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 900 -460 0 0 {name=p73 sig_type=std_logic lab=vepulseextp}
C {devices/ipin.sym} 1080 -1100 0 0 {name=p74 lab=vipulseextp

}
C {devices/lab_pin.sym} 900 -250 0 0 {name=p75 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 240 -500 0 0 {name=p55 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 240 -260 0 0 {name=p58 sig_type=std_logic lab=exc}
C {devices/opin.sym} 1470 -760 0 0 {name=p152 lab=req}
C {devices/lab_pin.sym} 240 -230 0 0 {name=p7 sig_type=std_logic lab=syn_req}
C {devices/ipin.sym} 1330 -1100 0 0 {name=p68 lab=vleakn
}
C {devices/ipin.sym} 1330 -1130 0 0 {name=p76 lab=ifdcp
}
C {devices/ipin.sym} 1330 -1070 2 1 {name=p82 lab=vrefn
}
C {devices/ipin.sym} 360 -810 0 0 {name=p84 lab=nRes

}
C {devices/lab_pin.sym} 1810 -680 2 0 {name=p85 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1810 -660 2 0 {name=p86 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 420 -990 0 0 {name=p88 lab=aVDD}
C {devices/lab_pin.sym} 1230 -760 2 0 {name=p1 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1230 -740 2 0 {name=p2 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 1560 -1130 0 0 {name=p89 lab=buffermonp

}
C {devices/iopin.sym} 1540 -1100 0 0 {name=p90 lab=monout}
C {devices/lab_pin.sym} 1860 -700 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1510 -700 0 0 {name=p92 sig_type=std_logic lab=buffermonp}
C {sky130_stdcells/inv_1.sym} 800 -740 0 0 {name=x14 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__}
C {devices/ipin.sym} 810 -1130 0 0 {name=p12 lab=JExcWn[0:3]

}
C {devices/ipin.sym} 1080 -1130 0 0 {name=p383 lab=JInhWp[0:3]

}
C {synapse_array_programmable_16_to_sout_v1.sym} 1050 -440 0 0 {name=x1}
C {synapse_array_programmable_inh_16_to_sout_v1.sym} 1050 -230 0 0 {name=x2}
C {devices/lab_pin.sym} 900 -290 0 0 {name=p31 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 1200 -270 2 0 {name=p27 sig_type=std_logic lab=dVDD}
C {schmitt_trigger.sym} 1440 -760 0 0 {name=x9}
C {devices/lab_pin.sym} 1400 -720 2 0 {name=p77 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1400 -800 2 0 {name=p78 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 900 -500 0 0 {name=p6 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/ipin.sym} 810 -1080 0 0 {name=p13 lab=vtaun

}
C {devices/ipin.sym} 810 -1060 0 0 {name=p16 lab=vthrdp

}
C {devices/lab_pin.sym} 900 -150 0 0 {name=p17 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 900 -190 0 0 {name=p18 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 900 -380 0 0 {name=p19 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 900 -360 0 0 {name=p28 sig_type=std_logic lab=vtaup}
C {devices/ipin.sym} 1080 -1070 0 0 {name=p29 lab=vtaup

}
C {devices/ipin.sym} 1080 -1050 0 0 {name=p30 lab=vthrdn

}
C {devices/lab_pin.sym} 1200 -480 2 0 {name=p32 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1200 -500 2 0 {name=p33 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1200 -250 2 0 {name=p36 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 420 -960 0 0 {name=p3 lab=aGND
}
C {devices/lab_pin.sym} 1200 -440 2 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1200 -230 2 0 {name=p79 sig_type=std_logic lab=aGND}
C {neuron_analog_fc_v2_norail.sym} 1080 -730 0 0 {name=x3}
C {buffer_mon_p_norail.sym} 1660 -680 0 0 {name=x13}
