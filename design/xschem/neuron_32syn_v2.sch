v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {analog synapse} 620 -1170 0 0 0.4 0.4 {}
T {input spikes} 140 -1170 0 0 0.4 0.4 {}
T {synaptic weight} 340 -1175 0 0 0.4 0.4 {}
T {analog synapse} 850 -1170 0 0 0.4 0.4 {}
T {neuron biases} 1120 -1170 0 0 0.4 0.4 {}
T {reset asynch digital logic} 70 -850 0 0 0.4 0.4 {}
T {monitor} 1400 -1170 0 0 0.4 0.4 {}
N 1100 -280 1260 -280 {
lab=#net1}
N 1260 -520 1260 -280 {
lab=#net1}
N 1100 -510 1260 -510 {
lab=#net1}
N 1130 -690 1260 -690 {
lab=#net1}
N 1350 -750 1370 -750 {
lab=req}
N 1230 -750 1270 -750 {
lab=nreq_neu1}
N 770 -730 830 -730 {
lab=#net2}
N 700 -810 830 -810 {
lab=ack_out}
N 690 -810 700 -810 {
lab=ack_out}
N 140 -600 170 -600 {
lab=setW}
N 140 -560 170 -560 {
lab=exc}
N 140 -530 170 -530 {
lab=setW}
N 140 -490 170 -490 {
lab=nExc}
N 140 -450 170 -450 {
lab=resetW}
N 140 -410 170 -410 {
lab=exc}
N 140 -370 170 -370 {
lab=resetW}
N 140 -330 170 -330 {
lab=nExc}
N 140 -290 170 -290 {
lab=syn_req}
N 140 -250 170 -250 {
lab=exc}
N 140 -220 170 -220 {
lab=syn_req}
N 140 -180 170 -180 {
lab=nExc}
N 1710 -690 1760 -690 {
lab=monout}
N 1300 -670 1410 -670 {
lab=#net1}
N 740 -730 770 -730 {
lab=#net2}
N 610 -730 660 -730 {
lab=ack_cel1}
N 1260 -690 1260 -520 {
lab=#net1}
N 1260 -670 1300 -670 {
lab=#net1}
N 1130 -710 1230 -710 {
lab=nreq_neu1}
N 1230 -750 1230 -710 {
lab=nreq_neu1}
C {c_element_rj.sym} 980 -830 0 0 {name=x11}
C {devices/lab_pin.sym} 1130 -810 2 0 {name=p34 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1130 -850 2 0 {name=p61 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 830 -850 0 0 {name=p62 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 830 -830 0 0 {name=p39 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 1130 -830 2 0 {name=p65 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1100 -490 2 0 {name=p3 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1100 -470 2 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1100 -260 2 0 {name=p5 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1250 -750 1 0 {name=p9 sig_type=std_logic lab=nreq_neu1}
C {devices/lab_pin.sym} 830 -710 0 0 {name=p10 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 830 -690 0 0 {name=p11 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 830 -750 0 0 {name=p14 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 610 -730 0 0 {name=p8 sig_type=std_logic lab=ack_cel1}
C {devices/ipin.sym} 695 -810 0 0 {name=p15 lab=ack_out


}
C {devices/iopin.sym} 210 -1000 0 0 {name=p20 lab=dGND
}
C {devices/iopin.sym} 210 -980 0 0 {name=p21 lab=dVDD}
C {devices/ipin.sym} 710 -1090 0 0 {name=p40 lab=vepulseextp

}
C {devices/ipin.sym} 260 -1110 0 0 {name=p46 lab=syn_addr[0:3]

}
C {devices/ipin.sym} 450 -1115 0 0 {name=p22 lab=W[0:3]

}
C {devices/ipin.sym} 450 -1055 0 0 {name=p23 lab=setW

}
C {devices/ipin.sym} 450 -1085 0 0 {name=p24 lab=resetW

}
C {devices/ipin.sym} 260 -1080 0 0 {name=p26 lab=syn_req

}
C {devices/ipin.sym} 260 -1050 0 0 {name=p25 lab=exc

}
C {sky130_stdcells/and2_1.sym} 230 -580 0 0 {name=x4 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 220 -690 0 0 {name=x5 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 230 -510 0 0 {name=x6 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/and2_1.sym} 230 -430 0 0 {name=x7 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 180 -690 0 0 {name=p37 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 260 -690 2 0 {name=p38 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 290 -580 2 0 {name=p41 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 290 -510 2 0 {name=p42 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 800 -430 0 0 {name=p43 sig_type=std_logic lab=resetWe}
C {sky130_stdcells/and2_1.sym} 230 -350 0 0 {name=x8 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 290 -350 2 0 {name=p44 sig_type=std_logic lab=resetWi}
C {sky130_stdcells/and2_1.sym} 230 -270 0 0 {name=x10 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 290 -270 2 0 {name=p45 sig_type=std_logic lab=reqe}
C {sky130_stdcells/and2_1.sym} 230 -200 0 0 {name=x12 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 290 -200 2 0 {name=p47 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 800 -390 0 0 {name=p48 sig_type=std_logic lab=setWe}
C {devices/lab_pin.sym} 290 -430 2 0 {name=p49 sig_type=std_logic lab=resetWe}
C {devices/lab_pin.sym} 800 -200 0 0 {name=p50 sig_type=std_logic lab=resetWi}
C {devices/lab_pin.sym} 800 -410 0 0 {name=p51 sig_type=std_logic lab=reqe}
C {devices/lab_pin.sym} 800 -180 0 0 {name=p52 sig_type=std_logic lab=reqi}
C {devices/lab_pin.sym} 800 -140 0 0 {name=p53 sig_type=std_logic lab=setWi}
C {devices/lab_pin.sym} 140 -560 0 0 {name=p54 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 140 -410 0 0 {name=p56 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 140 -330 0 0 {name=p57 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 140 -180 0 0 {name=p59 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 140 -600 0 0 {name=p60 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 140 -530 0 0 {name=p63 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 140 -450 0 0 {name=p64 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 140 -370 0 0 {name=p66 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 140 -290 0 0 {name=p67 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 800 -490 0 0 {name=p69 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 800 -260 0 0 {name=p70 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 800 -470 0 0 {name=p71 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 800 -240 0 0 {name=p72 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 800 -450 0 0 {name=p73 sig_type=std_logic lab=vepulseextp}
C {devices/ipin.sym} 980 -1090 0 0 {name=p74 lab=vipulseextp

}
C {devices/lab_pin.sym} 800 -220 0 0 {name=p75 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 140 -490 0 0 {name=p55 sig_type=std_logic lab=nExc}
C {devices/lab_pin.sym} 140 -250 0 0 {name=p58 sig_type=std_logic lab=exc}
C {devices/opin.sym} 1370 -750 0 0 {name=p152 lab=req}
C {devices/lab_pin.sym} 140 -220 0 0 {name=p7 sig_type=std_logic lab=syn_req}
C {devices/ipin.sym} 1225 -1090 0 0 {name=p68 lab=vleakn
}
C {devices/ipin.sym} 1225 -1120 0 0 {name=p76 lab=ifdcp
}
C {devices/ipin.sym} 1225 -1060 2 1 {name=p82 lab=vrefn
}
C {devices/ipin.sym} 260 -795 0 0 {name=p84 lab=nRes

}
C {devices/lab_pin.sym} 1710 -670 2 0 {name=p85 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1710 -650 2 0 {name=p86 sig_type=std_logic lab=aVDD}
C {devices/iopin.sym} 320 -1000 0 0 {name=p87 lab=aGND
}
C {devices/iopin.sym} 320 -980 0 0 {name=p88 lab=aVDD}
C {devices/lab_pin.sym} 1130 -750 2 0 {name=p1 sig_type=std_logic lab=aGND}
C {devices/lab_pin.sym} 1130 -730 2 0 {name=p2 sig_type=std_logic lab=aVDD}
C {devices/ipin.sym} 1460 -1120 0 0 {name=p89 lab=buffermonp

}
C {devices/iopin.sym} 1440 -1090 0 0 {name=p90 lab=monout}
C {devices/lab_pin.sym} 1760 -690 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1410 -690 0 0 {name=p92 sig_type=std_logic lab=buffermonp}
C {sky130_stdcells/inv_1.sym} 700 -730 0 0 {name=x14 VGND=dGND VNB=dGND VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {neuron_analog_fc_v1.sym} 980 -720 0 0 {name=x3}
C {devices/ipin.sym} 710 -1120 0 0 {name=p12 lab=JExcWp[0:3]

}
C {devices/ipin.sym} 980 -1120 0 0 {name=p383 lab=JInhWn[0:3]

}
C {synapse_array_programmable_16_to_sout_v1.sym} 950 -430 0 0 {name=x1}
C {devices/lab_pin.sym} 800 -280 0 0 {name=p31 sig_type=std_logic lab=JInhWn[0:3]}
C {devices/lab_pin.sym} 800 -510 0 0 {name=p36 sig_type=std_logic lab=JExcWp[0:3]}
C {devices/lab_pin.sym} 1100 -240 2 0 {name=p27 sig_type=std_logic lab=aVDD}
C {buffer_mon_p.sym} 1560 -670 0 0 {name=x13}
C {schmitt_trigger.sym} 1340 -750 0 0 {name=x9}
C {devices/lab_pin.sym} 1300 -710 2 0 {name=p77 sig_type=std_logic lab=dGND}
C {devices/lab_pin.sym} 1300 -790 2 0 {name=p78 sig_type=std_logic lab=dVDD}
C {devices/ipin.sym} 990 -1055 0 0 {name=p6 lab=vthrdp

}
C {devices/ipin.sym} 990 -1025 0 0 {name=p13 lab=vtaun

}
C {devices/lab_pin.sym} 800 -160 0 0 {name=p16 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 800 -120 0 0 {name=p17 sig_type=std_logic lab=vtaun}
C {devices/ipin.sym} 705 -1060 0 0 {name=p18 lab=vthrdn

}
C {devices/ipin.sym} 705 -1030 0 0 {name=p19 lab=vtaup

}
C {synapse_array_programmable_inh_16_to_sout_v1.sym} 950 -200 0 0 {name=x2}
C {devices/lab_pin.sym} 800 -370 0 0 {name=p28 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 800 -350 0 0 {name=p29 sig_type=std_logic lab=vtaup}
