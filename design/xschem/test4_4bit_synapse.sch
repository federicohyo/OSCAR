v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 570 -345 570 -325 {
lab=0}
N 570 -435 570 -405 {
lab=VDD}
N 1350 -520 1350 -500 {
lab=0}
N 1350 -610 1350 -580 {
lab=JExcWn[0]}
N 1455 -520 1455 -500 {
lab=0}
N 1455 -610 1455 -580 {
lab=JExcWn[1]}
N 1560 -520 1560 -500 {
lab=0}
N 1560 -610 1560 -580 {
lab=JExcWn[2]}
N 1660 -520 1660 -500 {
lab=0}
N 1660 -610 1660 -580 {
lab=JExcWn[3]}
N 1630 -345 1630 -325 {
lab=0}
N 1630 -435 1630 -405 {
lab=vthn}
N 1200 -45 1200 -25 {
lab=0}
N 1360 -680 1360 -660 {
lab=0}
N 1465 -680 1465 -660 {
lab=0}
N 1570 -680 1570 -660 {
lab=0}
N 1670 -680 1670 -660 {
lab=0}
N 815 15 845 15 {
lab=#net1}
N 925 15 1035 15 {
lab=nreq}
N 615 15 735 15 {
lab=#net2}
N 615 15 615 90 {
lab=#net2}
N 615 90 680 90 {
lab=#net2}
N 1560 -345 1560 -325 {
lab=0}
N 1560 -435 1560 -405 {
lab=vrefn}
N 1180 110 1180 130 {
lab=0}
N 930 -730 930 -710 {
lab=0}
N 1455 15 1455 45 {
lab=vtaup}
N 1455 105 1455 125 {
lab=0}
N 1750 110 1750 130 {
lab=0}
N 1750 20 1750 50 {
lab=spk}
N 1250 230 1250 250 {
lab=0}
N 1180 20 1180 55 {
lab=vleakn}
N 1470 270 1470 290 {
lab=0}
N 1035 15 1035 70 {
lab=nreq}
N 980 70 1035 70 {
lab=nreq}
N 590 -680 590 -660 {
lab=0}
N 590 -770 590 -740 {
lab=weight0}
N 700 -580 700 -560 {
lab=0}
N 700 -670 700 -640 {
lab=weight1}
N 810 -470 810 -450 {
lab=0}
N 810 -560 810 -530 {
lab=weight2}
N 940 -370 940 -350 {
lab=0}
N 940 -460 940 -430 {
lab=weight3}
N 780 215 780 255 {
lab=VDD}
N 780 285 820 285 {
lab=VDD}
N 820 245 820 285 {
lab=VDD}
N 780 245 820 245 {
lab=VDD}
N 780 650 810 650 {
lab=0}
N 810 650 810 700 {
lab=0}
N 810 700 810 740 {
lab=0}
N 780 740 810 740 {
lab=0}
N 735 515 925 515 {
lab=vmem1}
N 780 680 780 740 {
lab=0}
N 780 565 780 620 {
lab=vmem1}
N 780 315 780 410 {
lab=#net3}
N 990 705 990 750 {
lab=0}
N 780 515 780 565 {
lab=vmem1}
N 990 515 990 535 {
lab=vmem1}
N 690 515 735 515 {
lab=vmem1}
N 990 535 990 550 {
lab=vmem1}
N 990 610 990 645 {
lab=#net4}
N 720 285 740 285 {
lab=input_syn}
N 925 515 990 515 {
lab=vmem1}
N 780 470 780 515 {
lab=vmem1}
N 640 285 720 285 {
lab=input_syn}
C {devices/lab_pin.sym} 980 -200 2 0 {name=p25 sig_type=std_logic lab=vsin}
C {devices/lab_pin.sym} 980 -180 2 0 {name=p1 sig_type=std_logic lab=vthn}
C {devices/lab_pin.sym} 980 -140 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 980 -220 2 0 {name=p3 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 980 -120 2 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 980 -100 2 0 {name=p5 sig_type=std_logic lab=JExcWn[0]}
C {devices/lab_pin.sym} 980 -80 2 0 {name=p6 sig_type=std_logic lab=JExcWn[1]}
C {devices/lab_pin.sym} 980 -60 2 0 {name=p7 sig_type=std_logic lab=JExcWn[2]}
C {devices/lab_pin.sym} 980 -40 2 0 {name=p8 sig_type=std_logic lab=JExcWn[3]}
C {devices/lab_pin.sym} 680 -220 2 1 {name=p9 sig_type=std_logic lab=spk}
C {devices/lab_pin.sym} 680 -200 2 1 {name=p10 sig_type=std_logic lab=weight0}
C {devices/lab_pin.sym} 680 -180 2 1 {name=p11 sig_type=std_logic lab=weight1}
C {devices/lab_pin.sym} 680 -160 2 1 {name=p12 sig_type=std_logic lab=weight2}
C {devices/lab_pin.sym} 680 -140 2 1 {name=p13 sig_type=std_logic lab=weight3}
C {devices/vsource.sym} 570 -375 0 0 {name=V2 value=1.8
}
C {devices/lab_pin.sym} 570 -435 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 570 -325 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/code.sym} 1650 -255 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 1530 -255 0 0 {name=CORNER1 only_toplevel=true corner=tt}
C {devices/vsource.sym} 1350 -550 0 0 {name=V1 value=\{W0\}
}
C {devices/vsource.sym} 1455 -550 0 0 {name=V3 value=\{W1\}
}
C {devices/vsource.sym} 1560 -550 0 0 {name=V4 value=\{W2\}
}
C {devices/vsource.sym} 1660 -550 0 0 {name=V5 value=\{W3\}
}
C {devices/lab_pin.sym} 1350 -500 0 0 {name=p22 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1455 -500 0 0 {name=p23 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1560 -500 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1660 -500 0 0 {name=p26 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1350 -610 2 0 {name=p27 sig_type=std_logic lab=JExcWn[0]}
C {devices/lab_pin.sym} 1455 -610 2 0 {name=p28 sig_type=std_logic lab=JExcWn[1]}
C {devices/lab_pin.sym} 1560 -610 2 0 {name=p29 sig_type=std_logic lab=JExcWn[2]}
C {devices/lab_pin.sym} 1660 -610 2 0 {name=p30 sig_type=std_logic lab=JExcWn[3]}
C {devices/vsource.sym} 1630 -375 0 0 {name=V10 value=1.6
}
C {devices/lab_pin.sym} 1630 -325 0 0 {name=p31 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1630 -435 2 0 {name=p34 sig_type=std_logic lab=vthn}
C {devices/vsource.sym} 1200 -75 0 0 {name=V13 value="pwl(0 1.8 5u 0.95 6u 1.8 15u 1.8 16u 0.95 25u 1.8 30u 1.8)"}
C {devices/lab_pin.sym} 1200 -25 0 0 {name=p38 sig_type=std_logic lab=0}
C {dpi_syn_exc_4bit_fc_v2_revis.sym} 830 -130 0 0 {name=x1}
C {devices/lab_pin.sym} 980 -160 2 0 {name=p39 sig_type=std_logic lab=vmid}
C {devices/lab_pin.sym} 1360 -660 0 0 {name=p41 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1465 -660 0 0 {name=p42 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1570 -660 0 0 {name=p43 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1670 -660 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/code_shown.sym} 7.3828125 -279.6484375 0 0 {name=Xyce10 only_toplevel=false value="
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=ifpack
.savecurrents

.save all
.param pw = 10u
.param period = 70u
.param W0 = 0.5
.param W1 = 0.5
.param W2 = 0.5
.param W3 = 0.5

.control
let stop_vsin = 1.8

tran 0.01u 500u
write 'comparison_vsin_.raw' input_syn vsin
plot input_syn vsin
.endc
"}
C {neuron_analog_fc_v2_norail_revis.sym} 830 100 0 0 {name=x2}
C {devices/lab_pin.sym} 980 90 2 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 980 110 2 0 {name=p45 sig_type=std_logic lab=VDD}
C {sky130_stdcells/inv_1.sym} 885 15 0 1 {name=x4 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 775 15 0 1 {name=x5 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 680 70 2 1 {name=p46 sig_type=std_logic lab=vsin}
C {devices/lab_pin.sym} 680 110 2 1 {name=p47 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 680 130 2 1 {name=p48 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 980 130 2 0 {name=p49 sig_type=std_logic lab=vmem}
C {devices/vsource.sym} 1560 -375 0 0 {name=V14 value=0.4}
C {devices/lab_pin.sym} 1560 -435 0 0 {name=p50 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1560 -325 0 0 {name=p101 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1180 20 0 0 {name=p51 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1180 130 0 0 {name=p100 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 930 -710 0 0 {name=p53 sig_type=std_logic lab=0}
C {devices/vsource.sym} 930 -760 0 0 {name=V19 value="pulse(0 1.8 10u 1ns 1ns 1600us 3200us 1)"}
C {devices/lab_pin.sym} 1455 15 2 0 {name=p60 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1455 125 0 0 {name=p61 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1455 75 0 0 {name=V20 value="pulse(1.1 1.8 11u 1ns 1ns \{pw\} \{period\} 100)"}
C {devices/lab_pin.sym} 1750 130 0 0 {name=p62 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1750 20 2 1 {name=p63 sig_type=std_logic lab=spk}
C {devices/vsource.sym} 1750 80 0 0 {name=V21 value="pulse(0 1.8 11u 1ns 1ns \{pw\} \{period\} 100)"}
C {devices/lab_pin.sym} 1250 250 0 0 {name=p14 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1250 200 0 0 {name=V6 value="pwl(0 1.8 10u 1.8 10.01u 0)"}
C {devices/lab_pin.sym} 1470 290 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1470 245 0 0 {name=V8 value="pulse(1.8 0 11u 1ns 1ns 5us 20us 16)"}
C {devices/vsource.sym} 1180 80 0 0 {name=V7 value="pulse(0.55 0 11u 1ns 1ns \{pw\} \{period\} 100)"}
C {devices/lab_pin.sym} 590 -770 0 0 {name=p16 sig_type=std_logic lab=weight0}
C {devices/lab_pin.sym} 590 -660 0 0 {name=p17 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 700 -670 0 0 {name=p18 sig_type=std_logic lab=weight1}
C {devices/lab_pin.sym} 700 -560 0 0 {name=p19 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 810 -560 0 0 {name=p20 sig_type=std_logic lab=weight2}
C {devices/lab_pin.sym} 810 -450 0 0 {name=p21 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 940 -460 0 0 {name=p33 sig_type=std_logic lab=weight3}
C {devices/lab_pin.sym} 940 -350 0 0 {name=p36 sig_type=std_logic lab=0}
C {devices/vsource.sym} 940 -400 0 0 {name=V9 value=1.8
}
C {devices/vsource.sym} 810 -500 0 0 {name=V11 value=1.8
}
C {devices/vsource.sym} 700 -610 0 0 {name=V12 value=1.8
}
C {devices/vsource.sym} 590 -710 0 0 {name=V15 value=1.8
}
C {devices/lab_pin.sym} 1035 70 2 0 {name=p37 sig_type=std_logic lab=nreq}
C {sky130_fd_pr/cap_mim_m3_1.sym} 990 675 2 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/ipin.sym} 740 650 0 0 {name=p40 lab=vleakn
}
C {devices/lab_pin.sym} 780 215 0 0 {name=p55 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 780 740 3 0 {name=p57 sig_type=std_logic lab=0}
C {sky130_fd_pr/pfet_01v8.sym} 760 285 0 0 {name=M1
L=0.2
W=1.2
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {devices/iopin.sym} 690 515 3 0 {name=p58 lab=vmem1
}
C {sky130_fd_pr/nfet_01v8.sym} 760 650 0 0 {name=M12
L=2.0
W=1.0
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 990 750 3 0 {name=p59 sig_type=std_logic lab=0}
C {devices/ammeter.sym} 990 580 0 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {devices/vsource.sym} 780 440 0 0 {name=V16 value=0
}
C {devices/lab_pin.sym} 640 345 3 0 {name=p54 sig_type=std_logic lab=0}
C {devices/vsource.sym} 640 315 0 0 {name=V17 value="pwl(0 1.735 11u 1.735 26u 1.7274157673218087 26.01u 1.735)"}
C {devices/lab_pin.sym} 640 285 0 0 {name=p52 sig_type=std_logic lab=input_syn}
