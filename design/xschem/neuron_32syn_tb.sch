v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 2200 -680 3000 -280 {flags=graph
y1=0
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.001
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=monout
color=4
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 2260 -1150 3060 -750 {flags=graph
y1=0
y2=1.8
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1

x2=0.001
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="x1.net1
exc
resetw
setw"
color="4 7 6 8"
dataset=-1
unitx=1
logx=0
logy=0
x1=0}
T {Neuron biases} 655 -1150 0 0 0.4 0.4 {}
T {Excitatory syn} 335 -1140 0 0 0.4 0.4 {}
T {Power up reset} 1715 -1140 0 0 0.4 0.4 {}
T {Neuron driven by excitatory synapse} 1770 -890 0 0 0.4 0.4 {}
T {some small delay
} 1760 -670 0 0 0.4 0.4 {}
T {Inhibitory syn} 285 -880 0 0 0.4 0.4 {}
N 805 -1100 805 -1070 {
lab=vrefn}
N 725 -1100 725 -1070 {
lab=vleakn}
N 1005 -1090 1005 -1060 {
lab=ifahwp}
N 925 -1090 925 -1060 {
lab=ifnmdap}
N 1115 -1090 1115 -1060 {
lab=ifdcp}
N 1235 -1090 1235 -1060 {
lab=ifahthrp}
N 1355 -1090 1355 -1060 {
lab=ifthrp}
N 1475 -1090 1475 -1060 {
lab=ifcascn}
N 1605 -1090 1605 -1060 {
lab=ifahtaun}
N 370 -1070 370 -1040 {
lab=vetaudpip}
N 470 -1070 470 -1040 {
lab=vethrdpin}
N 575 -1080 575 -1050 {
lab=vestddpin}
N 245 -1060 245 -1030 {
lab=syn_req}
N 1755 -1090 1755 -1060 {
lab=nRes}
N 1400 -770 1410 -770 {
lab=dVDD}
N 1400 -790 1410 -790 {
lab=aVDD}
N 1400 -850 1470 -850 {
lab=monout}
N 1400 -750 1470 -750 {
lab=spk1}
N 1740 -790 1780 -790 {
lab=spk1}
N 1720 -810 1780 -810 {
lab=ack1}
N 320 -810 320 -780 {
lab=vitaudpip}
N 420 -810 420 -780 {
lab=vithrdpip}
N 525 -820 525 -790 {
lab=vistddpin}
N 1090 -810 1100 -810 {
lab=vistddpin}
N 1090 -830 1100 -830 {
lab=vestddpin}
N 1090 -850 1100 -850 {
lab=ifnmdap}
N 810 -840 810 -810 {
lab=bufmonp}
N 1090 -750 1100 -750 {
lab=ifahwp}
N 145 -215 145 -185 {
lab=setW}
N 405 -205 405 -175 {
lab=resetW}
N 1090 -670 1100 -670 {
lab=ifdcp}
N 1090 -630 1100 -630 {
lab=syn_req}
N 1090 -610 1100 -610 {
lab=ifahthrp}
N 1090 -510 1100 -510 {
lab=ifthrp}
N 1090 -490 1100 -490 {
lab=ifcascn}
N 810 -680 810 -650 {
lab=vepulseextp}
N 820 -440 820 -420 {
lab=0}
N 1090 -410 1100 -410 {
lab=vrefn}
N 1090 -390 1100 -390 {
lab=ifahtaun}
N 1470 -850 1550 -850 {
lab=monout}
C {devices/vsource.sym} 390 -620 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 390 -650 0 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/vsource.sym} 805 -1040 0 0 {name=V8 value=0.4}
C {devices/lab_pin.sym} 805 -1100 0 0 {name=p45 sig_type=std_logic lab=vrefn}
C {devices/vsource.sym} 725 -1040 0 0 {name=V9 value=0}
C {devices/lab_pin.sym} 725 -1100 0 0 {name=p46 sig_type=std_logic lab=vleakn}
C {devices/vsource.sym} 1005 -1030 0 0 {name=V16 value=1.8}
C {devices/lab_pin.sym} 1005 -1090 0 0 {name=p33 sig_type=std_logic lab=ifahwp}
C {devices/vsource.sym} 925 -1030 0 0 {name=V18 value=0.45}
C {devices/lab_pin.sym} 925 -1090 0 0 {name=p40 sig_type=std_logic lab=ifnmdap}
C {devices/vsource.sym} 1115 -1030 0 0 {name=V19 value=1.7}
C {devices/lab_pin.sym} 1115 -1090 0 0 {name=p41 sig_type=std_logic lab=ifdcp}
C {devices/vsource.sym} 1235 -1030 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 1235 -1090 0 0 {name=p42 sig_type=std_logic lab=ifahthrp}
C {devices/vsource.sym} 1355 -1030 0 0 {name=V22 value=1.8}
C {devices/lab_pin.sym} 1355 -1090 0 0 {name=p43 sig_type=std_logic lab=ifthrp}
C {devices/vsource.sym} 1475 -1030 0 0 {name=V23 value=0.0}
C {devices/lab_pin.sym} 1475 -1090 0 0 {name=p44 sig_type=std_logic lab=ifcascn}
C {devices/vsource.sym} 1605 -1030 0 0 {name=V24 value=0.0}
C {devices/lab_pin.sym} 1605 -1090 0 0 {name=p47 sig_type=std_logic lab=ifahtaun}
C {devices/vsource.sym} 370 -1010 0 0 {name=V7 value=1.5}
C {devices/lab_pin.sym} 370 -1070 0 0 {name=p16 sig_type=std_logic lab=vetaudpip}
C {devices/vsource.sym} 470 -1010 0 0 {name=V13 value=0.9}
C {devices/lab_pin.sym} 470 -1070 0 0 {name=p26 sig_type=std_logic lab=vethrdpin}
C {devices/vsource.sym} 575 -1020 0 0 {name=V10 value=0.47}
C {devices/lab_pin.sym} 575 -1080 0 0 {name=p39 sig_type=std_logic lab=vestddpin}
C {devices/vsource.sym} 245 -1000 0 1 {name=V12 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/lab_pin.sym} 245 -1060 0 0 {name=p19 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 1755 -1090 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 1755 -1030 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 1ms 1)"}
C {devices/code.sym} 80 -660 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {devices/code_shown.sym} 1095 -275 0 0 {name=Xyce only_toplevel=false value="
.TRAN 0.01us 1ms 
.PRINT TRAN format=raw file=neuron_32syn_tb_xyce.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO
.SAVE

"}
C {sky130_fd_pr/corner.sym} 65 -835 0 0 {name=CORNER only_toplevel=true corner=tt}
C {neuron_32syn.sym} 1250 -600 0 0 {name=x1}
C {devices/lab_pin.sym} 1400 -830 2 0 {name=p3 sig_type=std_logic lab=0}
C {c_element_rj.sym} 1930 -810 0 0 {name=x2}
C {devices/lab_pin.sym} 2080 -830 2 0 {name=p56 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1780 -830 0 0 {name=p85 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1100 -370 0 0 {name=p10 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1100 -350 0 0 {name=p6 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1100 -450 0 0 {name=p7 sig_type=std_logic lab=vleakn}
C {devices/vsource.sym} 320 -750 0 0 {name=V1 value=1.5}
C {devices/lab_pin.sym} 320 -810 0 0 {name=p8 sig_type=std_logic lab=vitaudpip}
C {devices/vsource.sym} 420 -750 0 0 {name=V3 value=0.9}
C {devices/lab_pin.sym} 420 -810 0 0 {name=p9 sig_type=std_logic lab=vithrdpip}
C {devices/vsource.sym} 525 -760 0 0 {name=V5 value=0.47}
C {devices/lab_pin.sym} 525 -820 0 0 {name=p11 sig_type=std_logic lab=vistddpin}
C {devices/lab_pin.sym} 1100 -590 0 0 {name=p12 sig_type=std_logic lab=vitaudpip}
C {devices/lab_pin.sym} 1100 -690 0 0 {name=p13 sig_type=std_logic lab=vithrdpip}
C {devices/lab_pin.sym} 1095 -810 0 0 {name=p14 sig_type=std_logic lab=vistddpin}
C {devices/lab_pin.sym} 1100 -570 0 0 {name=p15 sig_type=std_logic lab=vetaudpip}
C {devices/lab_pin.sym} 1100 -710 0 0 {name=p17 sig_type=std_logic lab=vethrdpin}
C {devices/lab_pin.sym} 1095 -830 0 0 {name=p18 sig_type=std_logic lab=vestddpin}
C {devices/lab_pin.sym} 1095 -850 0 0 {name=p20 sig_type=std_logic lab=ifnmdap}
C {devices/vsource.sym} 810 -780 0 0 {name=V15 value=0.6}
C {devices/lab_pin.sym} 1100 -790 0 0 {name=p187 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 810 -840 0 0 {name=p21 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 340 -410 2 0 {name=p22 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 340 -340 2 0 {name=p23 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 340 -370 2 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 340 -300 2 0 {name=p25 sig_type=std_logic lab=0}
C {tie_low.sym} 190 -320 0 0 {name=x6}
C {tie_low.sym} 190 -390 0 0 {name=x7}
C {devices/lab_pin.sym} 1100 -770 0 0 {name=p29 sig_type=std_logic lab=W[0:1]}
C {devices/lab_pin.sym} 1095 -750 0 0 {name=p30 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 145 -215 0 0 {name=p31 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 145 -155 0 0 {name=V6 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/lab_pin.sym} 405 -205 0 0 {name=p32 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 405 -145 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 200ms 1)"}
C {devices/lab_pin.sym} 1930 -570 2 0 {name=p34 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 1930 -530 2 0 {name=p37 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1930 -460 2 0 {name=p38 sig_type=std_logic lab=0}
C {tie_low.sym} 1780 -480 0 0 {name=x8}
C {tie_low.sym} 1780 -550 0 0 {name=x9}
C {tie_hi.sym} 1780 -410 0 0 {name=x10}
C {devices/lab_pin.sym} 1930 -390 2 0 {name=p53 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1930 -500 2 0 {name=p36 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 1930 -430 2 0 {name=p55 sig_type=std_logic lab=syn_addr[2]}
C {tie_hi.sym} 1780 -340 0 0 {name=x11}
C {devices/lab_pin.sym} 1930 -320 2 0 {name=p58 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1930 -360 2 0 {name=p60 sig_type=std_logic lab=syn_addr[3]}
C {devices/lab_pin.sym} 1100 -730 0 0 {name=p61 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1095 -670 0 0 {name=p62 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1100 -650 0 0 {name=p63 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1100 -550 0 0 {name=p64 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1095 -630 0 0 {name=p65 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 1095 -610 0 0 {name=p66 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 1095 -510 0 0 {name=p67 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 1095 -490 0 0 {name=p68 sig_type=std_logic lab=ifcascn}
C {devices/vsource.sym} 810 -620 0 0 {name=V17 value=0.65}
C {devices/lab_pin.sym} 810 -680 0 0 {name=p69 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 1100 -470 0 0 {name=p70 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 1100 -430 0 0 {name=p71 sig_type=std_logic lab=vipulseextp}
C {devices/vsource.sym} 820 -470 0 0 {name=V20 value=0.65}
C {devices/lab_pin.sym} 820 -500 0 0 {name=p72 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 1095 -410 0 0 {name=p73 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1095 -390 0 0 {name=p74 sig_type=std_logic lab=ifahtaun}
C {devices/vsource.sym} 815 -355 0 1 {name=V25 value="pulse(1.8 0 1ns 15ns 1ns 500us 1ms 1)"}
C {devices/lab_pin.sym} 815 -385 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1100 -530 0 0 {name=p76 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1440 -850 1 0 {name=p77 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1930 -710 2 0 {name=p86 sig_type=std_logic lab=ack1}
C {sky130_stdcells/inv_1.sym} 1810 -710 0 0 {name=x16 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1890 -710 0 0 {name=x18 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1770 -710 0 0 {name=p88 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1720 -810 0 0 {name=p79 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1470 -750 2 0 {name=p78 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1740 -790 0 0 {name=p80 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1400 -810 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2080 -790 2 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 820 -420 0 0 {name=p84 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 810 -590 0 0 {name=p87 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 320 -720 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 420 -720 0 0 {name=p90 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 810 -750 0 0 {name=p92 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 245 -970 0 0 {name=p94 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1550 -820 0 1 {name=C1 model=cap_mim_m3_1 W=11 L=11 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 1550 -790 0 0 {name=p48 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 525 -730 0 0 {name=p51 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 815 -325 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 145 -125 0 0 {name=p81 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 405 -115 0 0 {name=p91 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 390 -590 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 370 -980 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 470 -980 0 0 {name=p97 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 575 -990 0 0 {name=p98 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 725 -1010 0 0 {name=p99 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 805 -1010 0 0 {name=p100 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 925 -1000 0 0 {name=p101 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1005 -1000 0 0 {name=p102 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1115 -1000 0 0 {name=p103 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1235 -1000 0 0 {name=p104 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1355 -1000 0 0 {name=p105 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1475 -1000 0 0 {name=p106 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1605 -1000 0 0 {name=p107 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1755 -1000 0 0 {name=p108 sig_type=std_logic lab=0}
C {devices/vsource.sym} 505 -630 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 505 -660 0 0 {name=p57 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 505 -600 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 340 -320 0 1 {name=p27 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 340 -390 0 1 {name=p28 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1410 -790 0 1 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1930 -550 0 1 {name=p49 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1930 -480 0 1 {name=p50 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1930 -410 0 1 {name=p54 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1930 -340 0 1 {name=p59 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1410 -770 0 1 {name=p109 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 2080 -810 0 1 {name=p4 sig_type=std_logic lab=dVDD}
