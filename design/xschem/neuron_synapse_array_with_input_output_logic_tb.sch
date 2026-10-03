v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Neuron biases} 710 -1105 0 0 0.4 0.4 {}
T {Excitatory syn} 390 -1095 0 0 0.4 0.4 {}
T {Power up reset} 1770 -1095 0 0 0.4 0.4 {}
T {Inhibitory syn} 240 -810 0 0 0.4 0.4 {}
N 2160 -1035 2160 -1005 {
lab=dVDD}
N 860 -1055 860 -1025 {
lab=vrefn}
N 780 -1055 780 -1025 {
lab=vleakn}
N 1060 -1045 1060 -1015 {
lab=ifahwp}
N 980 -1045 980 -1015 {
lab=ifnmdap}
N 1170 -1045 1170 -1015 {
lab=ifdcp}
N 1290 -1045 1290 -1015 {
lab=ifahthrp}
N 1410 -1045 1410 -1015 {
lab=ifthrp}
N 1530 -1045 1530 -1015 {
lab=ifcascn}
N 1660 -1045 1660 -1015 {
lab=ifahtaun}
N 425 -1025 425 -995 {
lab=vetaudpip}
N 525 -1025 525 -995 {
lab=vethrdpin}
N 630 -945 630 -925 {
lab=0}
N 630 -1035 630 -1005 {
lab=vestddpin}
N 300 -925 300 -905 {
lab=0}
N 300 -1015 300 -985 {
lab=REQIN}
N 2250 -1035 2250 -1005 {
lab=aVDD}
N 1810 -1045 1810 -1015 {
lab=nRes}
N 295 -925 635 -925 {
lab=0}
N 425 -935 425 -925 {
lab=0}
N 525 -935 525 -925 {
lab=0}
N 625 -925 1815 -925 {
lab=0}
N 1815 -955 1815 -925 {
lab=0}
N 1805 -955 1815 -955 {
lab=0}
N 1655 -955 1655 -925 {
lab=0}
N 1655 -955 1665 -955 {
lab=0}
N 1535 -955 1535 -925 {
lab=0}
N 1525 -955 1535 -955 {
lab=0}
N 1405 -955 1415 -955 {
lab=0}
N 1405 -955 1405 -925 {
lab=0}
N 785 -945 785 -925 {
lab=0}
N 785 -965 785 -945 {
lab=0}
N 775 -965 785 -965 {
lab=0}
N 855 -965 865 -965 {
lab=0}
N 855 -965 855 -925 {
lab=0}
N 975 -955 995 -955 {
lab=0}
N 995 -955 995 -925 {
lab=0}
N 1055 -955 1065 -955 {
lab=0}
N 1065 -955 1065 -925 {
lab=0}
N 1165 -955 1175 -955 {
lab=0}
N 1175 -955 1175 -925 {
lab=0}
N 1285 -955 1295 -955 {
lab=0}
N 1295 -955 1295 -925 {
lab=0}
N 2155 -945 2165 -945 {
lab=0}
N 275 -650 275 -630 {
lab=0}
N 275 -740 275 -710 {
lab=vitaudpip}
N 375 -650 375 -630 {
lab=0}
N 375 -740 375 -710 {
lab=vithrdpip}
N 480 -750 480 -720 {
lab=vistddpip}
N 765 -680 765 -660 {
lab=0}
N 765 -770 765 -740 {
lab=bufmonp}
N 100 -55 100 -35 {
lab=0}
N 100 -145 100 -115 {
lab=setW}
N 360 -135 360 -105 {
lab=resetW}
N 765 -520 765 -500 {
lab=0}
N 765 -610 765 -580 {
lab=vepulseextp}
N 775 -370 775 -350 {
lab=0}
N 775 -460 775 -430 {
lab=vipulseextp}
N 475 -660 485 -660 {
lab=0}
N 1677.5 -780 1762.5 -780 {
lab=monout[0:15]}
N 1677.5 -740 1750 -740 {
lab=aer_out[0:3]}
C {neuron_synapse_array_with_input_output_logic.sym} 1527.5 -520 0 0 {name=x1}
C {devices/vsource.sym} 2160 -975 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 1677.5 -660 2 0 {name=p35 sig_type=std_logic lab=dVDD}
C {devices/vsource.sym} 860 -995 0 0 {name=V8 value=0.4}
C {devices/lab_pin.sym} 860 -1055 0 0 {name=p45 sig_type=std_logic lab=vrefn}
C {devices/vsource.sym} 780 -995 0 0 {name=V9 value=0.0}
C {devices/lab_pin.sym} 780 -1055 0 0 {name=p46 sig_type=std_logic lab=vleakn}
C {devices/vsource.sym} 1060 -985 0 0 {name=V16 value=1.8}
C {devices/lab_pin.sym} 1060 -1045 0 0 {name=p33 sig_type=std_logic lab=ifahwp}
C {devices/vsource.sym} 980 -985 0 0 {name=V18 value=0.0}
C {devices/lab_pin.sym} 980 -1045 0 0 {name=p40 sig_type=std_logic lab=ifnmdap}
C {devices/vsource.sym} 1170 -985 0 0 {name=V19 value=1.6}
C {devices/lab_pin.sym} 1170 -1045 0 0 {name=p41 sig_type=std_logic lab=ifdcp}
C {devices/vsource.sym} 1290 -985 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 1290 -1045 0 0 {name=p42 sig_type=std_logic lab=ifahthrp}
C {devices/vsource.sym} 1410 -985 0 0 {name=V22 value=1.8}
C {devices/lab_pin.sym} 1410 -1045 0 0 {name=p43 sig_type=std_logic lab=ifthrp}
C {devices/vsource.sym} 1530 -985 0 0 {name=V23 value=0.0}
C {devices/lab_pin.sym} 1530 -1045 0 0 {name=p44 sig_type=std_logic lab=ifcascn}
C {devices/vsource.sym} 1660 -985 0 0 {name=V24 value=0.0}
C {devices/lab_pin.sym} 1660 -1045 0 0 {name=p47 sig_type=std_logic lab=ifahtaun}
C {devices/vsource.sym} 425 -965 0 0 {name=V7 value=1.5}
C {devices/lab_pin.sym} 425 -1025 0 0 {name=p16 sig_type=std_logic lab=vetaudpip}
C {devices/vsource.sym} 525 -965 0 0 {name=V13 value=0.9}
C {devices/lab_pin.sym} 525 -1025 0 0 {name=p26 sig_type=std_logic lab=vethrdpin}
C {devices/vsource.sym} 630 -975 0 0 {name=V10 value=0.47}
C {devices/lab_pin.sym} 630 -1035 0 0 {name=p39 sig_type=std_logic lab=vestddpin}
C {devices/vsource.sym} 300 -955 0 1 {name=V12 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/lab_pin.sym} 300 -1015 0 0 {name=p19 sig_type=std_logic lab=REQIN}
C {devices/vsource.sym} 2250 -975 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 2250 -1035 0 0 {name=p57 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1810 -1045 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 1810 -985 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 1ms 1)"}
C {devices/lab_pin.sym} 305 -925 0 0 {name=p94 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2160 -945 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2250 -945 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/code.sym} 15 -700 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 20 -845 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/vsource.sym} 275 -680 0 0 {name=V1 value=1.5}
C {devices/lab_pin.sym} 275 -740 0 0 {name=p8 sig_type=std_logic lab=vitaudpip}
C {devices/vsource.sym} 375 -680 0 0 {name=V3 value=0.9}
C {devices/lab_pin.sym} 375 -740 0 0 {name=p9 sig_type=std_logic lab=vithrdpip}
C {devices/vsource.sym} 480 -690 0 0 {name=V5 value=0.47}
C {devices/lab_pin.sym} 480 -750 0 0 {name=p11 sig_type=std_logic lab=vistddpip}
C {devices/vsource.sym} 765 -710 0 0 {name=V15 value=0.6}
C {devices/lab_pin.sym} 765 -770 0 0 {name=p21 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 295 -340 2 0 {name=p22 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 295 -270 2 0 {name=p23 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 295 -300 2 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 295 -230 2 0 {name=p25 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 295 -320 2 0 {name=p27 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 295 -250 2 0 {name=p28 sig_type=std_logic lab=aVDD}
C {tie_low.sym} 145 -250 0 0 {name=x6}
C {tie_low.sym} 145 -320 0 0 {name=x7}
C {devices/lab_pin.sym} 100 -145 0 0 {name=p31 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 100 -85 0 0 {name=V6 value="pulse(0 1.8 1ns 30ns 1ns 60us 120us 2)"}
C {devices/lab_pin.sym} 360 -135 0 0 {name=p32 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 360 -75 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 200us 1)"}
C {devices/vsource.sym} 765 -550 0 0 {name=V17 value=0.5}
C {devices/lab_pin.sym} 765 -610 0 0 {name=p69 sig_type=std_logic lab=vepulseextp}
C {devices/vsource.sym} 775 -400 0 0 {name=V20 value=0.5}
C {devices/lab_pin.sym} 775 -460 0 0 {name=p72 sig_type=std_logic lab=vipulseextp}
C {devices/vsource.sym} 770 -285 0 1 {name=V25 value="pulse(0 1.8 1ns 15ns 1ns 29us 200us 1)"}
C {devices/lab_pin.sym} 770 -315 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 775 -350 0 0 {name=p84 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 765 -500 0 0 {name=p87 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 275 -630 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 375 -630 0 0 {name=p90 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 765 -670 0 0 {name=p92 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 480 -660 0 0 {name=p51 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 770 -255 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 100 -35 0 0 {name=p81 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 360 -45 0 0 {name=p91 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2275 -710 2 0 {name=p86 sig_type=std_logic lab=ACK}
C {sky130_stdcells/inv_1.sym} 2155 -710 0 0 {name=x16 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 2235 -710 0 0 {name=x18 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 2115 -710 0 0 {name=p88 sig_type=std_logic lab=REQ}
C {devices/lab_pin.sym} 1677.5 -760 2 0 {name=p1 sig_type=std_logic lab=REQ}
C {devices/lab_pin.sym} 1677.5 -700 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1677.5 -720 2 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1677.5 -680 2 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2160 -1035 0 0 {name=p5 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1377.5 -780 2 1 {name=p6 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1377.5 -760 0 0 {name=p7 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1377.5 -740 0 0 {name=p10 sig_type=std_logic lab=vistddpip}
C {devices/lab_pin.sym} 1377.5 -720 0 0 {name=p12 sig_type=std_logic lab=vestddpin}
C {devices/lab_pin.sym} 1377.5 -700 0 0 {name=p13 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 1377.5 -680 0 0 {name=p14 sig_type=std_logic lab=vithrdpip}
C {devices/lab_pin.sym} 1377.5 -660 0 0 {name=p15 sig_type=std_logic lab=ACK}
C {devices/lab_pin.sym} 1377.5 -640 0 0 {name=p17 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1377.5 -620 0 0 {name=p18 sig_type=std_logic lab=vethrdpin}
C {devices/lab_pin.sym} 1377.5 -600 0 0 {name=p20 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 1377.5 -580 0 0 {name=p29 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 1377.5 -560 0 0 {name=p30 sig_type=std_logic lab=vitaudpip}
C {devices/lab_pin.sym} 1377.5 -540 0 0 {name=p34 sig_type=std_logic lab=vetaudpip}
C {devices/lab_pin.sym} 1377.5 -520 0 0 {name=p36 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 2152.5 -510 2 0 {name=p37 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 2152.5 -470 2 0 {name=p38 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2152.5 -400 2 0 {name=p48 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2152.5 -490 2 0 {name=p49 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2152.5 -420 2 0 {name=p50 sig_type=std_logic lab=aVDD}
C {tie_low.sym} 2002.5 -420 0 0 {name=x8}
C {tie_low.sym} 2002.5 -490 0 0 {name=x9}
C {tie_hi.sym} 2002.5 -350 0 0 {name=x10}
C {devices/lab_pin.sym} 2152.5 -330 2 0 {name=p53 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2152.5 -350 2 0 {name=p54 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2152.5 -440 2 0 {name=p52 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 2152.5 -370 2 0 {name=p55 sig_type=std_logic lab=syn_addr[2]}
C {tie_hi.sym} 2002.5 -280 0 0 {name=x11}
C {devices/lab_pin.sym} 2152.5 -260 2 0 {name=p58 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2152.5 -280 2 0 {name=p59 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2152.5 -300 2 0 {name=p60 sig_type=std_logic lab=syn_addr[3]}
C {devices/lab_pin.sym} 1377.5 -500 0 0 {name=p56 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1377.5 -480 0 0 {name=p61 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1377.5 -460 0 0 {name=p62 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 1377.5 -440 0 0 {name=p63 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 1377.5 -420 0 0 {name=p64 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 2605 -505 2 0 {name=p65 sig_type=std_logic lab=neu_addr[0]}
C {devices/lab_pin.sym} 2605 -465 2 0 {name=p66 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2605 -395 2 0 {name=p67 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2605 -485 2 0 {name=p68 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2605 -415 2 0 {name=p70 sig_type=std_logic lab=aVDD}
C {tie_low.sym} 2455 -415 0 0 {name=x2}
C {tie_low.sym} 2455 -485 0 0 {name=x3}
C {tie_hi.sym} 2455 -345 0 0 {name=x4}
C {devices/lab_pin.sym} 2605 -325 2 0 {name=p71 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2605 -345 2 0 {name=p73 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2605 -435 2 0 {name=p74 sig_type=std_logic lab=neu_addr[1]}
C {devices/lab_pin.sym} 2605 -365 2 0 {name=p76 sig_type=std_logic lab=neu_addr[2]}
C {tie_hi.sym} 2455 -275 0 0 {name=x5}
C {devices/lab_pin.sym} 2605 -255 2 0 {name=p77 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2605 -275 2 0 {name=p78 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 2605 -295 2 0 {name=p79 sig_type=std_logic lab=neu_addr[3]}
C {devices/lab_pin.sym} 1377.5 -400 0 0 {name=p80 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 1377.5 -380 0 0 {name=p85 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 1377.5 -360 0 0 {name=p96 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 1377.5 -340 0 0 {name=p97 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1377.5 -320 0 0 {name=p98 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 1377.5 -300 0 0 {name=p99 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1377.5 -280 0 0 {name=p100 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1377.5 -260 0 0 {name=p101 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 1762.5 -780 2 0 {name=p102 sig_type=std_logic lab=monout[0:15]}
C {devices/lab_pin.sym} 1750 -740 2 0 {name=p103 sig_type=std_logic lab=aer_out[0:3]}
C {devices/lab_pin.sym} 295 -480 2 0 {name=p104 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 295 -410 2 0 {name=p105 sig_type=std_logic lab=W[2]}
C {devices/lab_pin.sym} 295 -440 2 0 {name=p106 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 295 -370 2 0 {name=p107 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 295 -460 2 0 {name=p108 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 295 -390 2 0 {name=p109 sig_type=std_logic lab=aVDD}
C {tie_low.sym} 145 -390 0 0 {name=x12}
C {tie_low.sym} 145 -460 0 0 {name=x13}
C {devices/simulator_commands_shown.sym} 710 -140 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 1ms
.PRINT TRAN format=raw file=neuron_synapse_array_with_input_output_logic_tb.raw v(*) i(*)
.SAVE
"}
