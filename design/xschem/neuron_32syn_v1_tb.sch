v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1780 -1195 2580 -795 {flags=graph
y1=0
y2=2
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
node="monout
exc
syn_req"
color="11 11 10"
dataset=-1
unitx=1
logx=0
logy=0
}
T {Power up reset} 915 -1180 0 0 0.4 0.4 {}
T {Neuron driven by excitatory synapse} 940 -845 0 0 0.4 0.4 {}
T {some small delay
} 1350 -545 0 0 0.4 0.4 {}
T {Stimuli pulses} 425 -1175 0 0 0.4 0.4 {}
T {# OPTION LINSOL TYPE=AztecOO PREC_TYPE=IFPACK} 135 -275 0 0 0.4 0.4 {}
T {Neuron biases} 420 -1580 0 0 0.4 0.4 {}
T {Inhibitory syn} 1277.5 -1577.5 0 0 0.4 0.4 {}
T {Excitatory syn} 2155 -1572.5 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 2395 -697.5 0 0 0.4 0.4 {}
N 320 -1105 320 -1075 {
lab=syn_req}
N 1135 -1105 1135 -1075 {
lab=nRes}
N 1270 -600 1280 -600 {
lab=aVDD}
N 1270 -620 1280 -620 {
lab=dVDD}
N 1270 -680 1340 -680 {
lab=monout}
N 1270 -580 1340 -580 {
lab=spk1}
N 910 -745 950 -745 {
lab=spk1}
N 890 -765 950 -765 {
lab=ack1}
N 960 -640 970 -640 {
lab=bufmonp}
N 960 -660 970 -660 {
lab=ifdcp}
N 960 -680 970 -680 {
lab=JInhWn[0:3]}
N 960 -580 970 -580 {
lab=syn_addr[0:3]}
N 325 -960 325 -930 {
lab=setW}
N 585 -950 585 -920 {
lab=resetW}
N 960 -500 970 -500 {
lab=resetW}
N 960 -460 970 -460 {
lab=vtaun}
N 960 -440 970 -440 {
lab=vrefn}
N 960 -340 970 -340 {
lab=vthrdn}
N 960 -320 970 -320 {
lab=ack_cel1}
N 1340 -680 1420 -680 {
lab=monout}
N 620 -1120 620 -1090 {
lab=exc}
N 225 -1435 255 -1435 {
lab=0}
N 250 -1405 250 -1400 {
lab=0}
N 250 -1400 250 -1380 {
lab=0}
N 290 -1435 320 -1435 {
lab=vleakn}
N 250 -1380 250 -1375 {
lab=0}
N 250 -1470 250 -1465 {
lab=vleakn}
N 250 -1475 250 -1470 {
lab=vleakn}
N 250 -1375 250 -1315 {
lab=0}
N 225 -1435 225 -1375 {
lab=0}
N 225 -1375 250 -1375 {
lab=0}
N 250 -1470 305 -1470 {
lab=vleakn}
N 305 -1470 305 -1435 {
lab=vleakn}
N 455 -1440 485 -1440 {
lab=VDD}
N 480 -1410 480 -1405 {
lab=ifdcp}
N 480 -1405 480 -1385 {
lab=ifdcp}
N 520 -1440 550 -1440 {
lab=ifdcp}
N 480 -1535 480 -1475 {
lab=VDD}
N 480 -1400 530 -1400 {
lab=ifdcp}
N 530 -1440 530 -1400 {
lab=ifdcp}
N 480 -1385 480 -1380 {
lab=ifdcp}
N 480 -1475 480 -1470 {
lab=VDD}
N 685 -1435 715 -1435 {
lab=0}
N 710 -1405 710 -1400 {
lab=0}
N 710 -1400 710 -1380 {
lab=0}
N 750 -1435 780 -1435 {
lab=vrefn}
N 710 -1380 710 -1375 {
lab=0}
N 710 -1470 710 -1465 {
lab=vrefn}
N 710 -1475 710 -1470 {
lab=vrefn}
N 710 -1375 710 -1315 {
lab=0}
N 685 -1435 685 -1375 {
lab=0}
N 685 -1375 710 -1375 {
lab=0}
N 710 -1470 765 -1470 {
lab=vrefn}
N 765 -1470 765 -1435 {
lab=vrefn}
N 985 -1425 1015 -1425 {
lab=0}
N 1010 -1395 1010 -1390 {
lab=0}
N 1010 -1390 1010 -1370 {
lab=0}
N 1050 -1425 1080 -1425 {
lab=JInhWn[0]}
N 1010 -1370 1010 -1365 {
lab=0}
N 1010 -1460 1010 -1455 {
lab=JInhWn[0]}
N 1010 -1465 1010 -1460 {
lab=JInhWn[0]}
N 1010 -1365 1010 -1305 {
lab=0}
N 985 -1425 985 -1365 {
lab=0}
N 985 -1365 1010 -1365 {
lab=0}
N 1010 -1460 1065 -1460 {
lab=JInhWn[0]}
N 1065 -1460 1065 -1425 {
lab=JInhWn[0]}
N 1190 -1420 1220 -1420 {
lab=0}
N 1215 -1390 1215 -1385 {
lab=0}
N 1215 -1385 1215 -1365 {
lab=0}
N 1255 -1420 1285 -1420 {
lab=JInhWn[1]}
N 1215 -1365 1215 -1360 {
lab=0}
N 1215 -1455 1215 -1450 {
lab=JInhWn[1]}
N 1215 -1460 1215 -1455 {
lab=JInhWn[1]}
N 1215 -1360 1215 -1300 {
lab=0}
N 1190 -1420 1190 -1360 {
lab=0}
N 1190 -1360 1215 -1360 {
lab=0}
N 1215 -1455 1270 -1455 {
lab=JInhWn[1]}
N 1270 -1455 1270 -1420 {
lab=JInhWn[1]}
N 1390 -1415 1420 -1415 {
lab=0}
N 1415 -1385 1415 -1380 {
lab=0}
N 1415 -1380 1415 -1360 {
lab=0}
N 1455 -1415 1485 -1415 {
lab=JInhWn[2]}
N 1415 -1360 1415 -1355 {
lab=0}
N 1415 -1450 1415 -1445 {
lab=JInhWn[2]}
N 1415 -1455 1415 -1450 {
lab=JInhWn[2]}
N 1415 -1355 1415 -1295 {
lab=0}
N 1390 -1415 1390 -1355 {
lab=0}
N 1390 -1355 1415 -1355 {
lab=0}
N 1415 -1450 1470 -1450 {
lab=JInhWn[2]}
N 1470 -1450 1470 -1415 {
lab=JInhWn[2]}
N 1590 -1410 1620 -1410 {
lab=0}
N 1615 -1380 1615 -1375 {
lab=0}
N 1615 -1375 1615 -1355 {
lab=0}
N 1655 -1410 1685 -1410 {
lab=JInhWn[3]}
N 1615 -1355 1615 -1350 {
lab=0}
N 1615 -1445 1615 -1440 {
lab=JInhWn[3]}
N 1615 -1450 1615 -1445 {
lab=JInhWn[3]}
N 1615 -1350 1615 -1290 {
lab=0}
N 1590 -1410 1590 -1350 {
lab=0}
N 1590 -1350 1615 -1350 {
lab=0}
N 1615 -1445 1670 -1445 {
lab=JInhWn[3]}
N 1670 -1445 1670 -1410 {
lab=JInhWn[3]}
N 1880 -1420 1910 -1420 {
lab=VDD}
N 1905 -1390 1905 -1385 {
lab=JExcWp[0]}
N 1905 -1385 1905 -1365 {
lab=JExcWp[0]}
N 1945 -1420 1975 -1420 {
lab=JExcWp[0]}
N 1905 -1515 1905 -1455 {
lab=VDD}
N 1905 -1380 1955 -1380 {
lab=JExcWp[0]}
N 1955 -1420 1955 -1380 {
lab=JExcWp[0]}
N 1905 -1365 1905 -1360 {
lab=JExcWp[0]}
N 1905 -1455 1905 -1450 {
lab=VDD}
N 2090 -1425 2120 -1425 {
lab=VDD}
N 2115 -1395 2115 -1390 {
lab=JExcWp[1]}
N 2115 -1390 2115 -1370 {
lab=JExcWp[1]}
N 2155 -1425 2185 -1425 {
lab=JExcWp[1]}
N 2115 -1520 2115 -1460 {
lab=VDD}
N 2115 -1385 2165 -1385 {
lab=JExcWp[1]}
N 2165 -1425 2165 -1385 {
lab=JExcWp[1]}
N 2115 -1370 2115 -1365 {
lab=JExcWp[1]}
N 2115 -1460 2115 -1455 {
lab=VDD}
N 2315 -1425 2345 -1425 {
lab=VDD}
N 2340 -1395 2340 -1390 {
lab=JExcWp[2]}
N 2340 -1390 2340 -1370 {
lab=JExcWp[2]}
N 2380 -1425 2410 -1425 {
lab=JExcWp[2]}
N 2340 -1520 2340 -1460 {
lab=VDD}
N 2340 -1385 2390 -1385 {
lab=JExcWp[2]}
N 2390 -1425 2390 -1385 {
lab=JExcWp[2]}
N 2340 -1370 2340 -1365 {
lab=JExcWp[2]}
N 2340 -1460 2340 -1455 {
lab=VDD}
N 2540 -1425 2570 -1425 {
lab=VDD}
N 2565 -1395 2565 -1390 {
lab=JExcWp[3]}
N 2565 -1390 2565 -1370 {
lab=JExcWp[3]}
N 2605 -1425 2635 -1425 {
lab=JExcWp[3]}
N 2565 -1520 2565 -1460 {
lab=VDD}
N 2565 -1385 2615 -1385 {
lab=JExcWp[3]}
N 2615 -1425 2615 -1385 {
lab=JExcWp[3]}
N 2565 -1370 2565 -1365 {
lab=JExcWp[3]}
N 2565 -1460 2565 -1455 {
lab=VDD}
N 1890 -1715 1920 -1715 {
lab=VDD}
N 1915 -1685 1915 -1680 {
lab=vtaup}
N 1915 -1680 1915 -1660 {
lab=vtaup}
N 1955 -1715 1985 -1715 {
lab=vtaup}
N 1915 -1810 1915 -1750 {
lab=VDD}
N 1915 -1675 1965 -1675 {
lab=vtaup}
N 1965 -1715 1965 -1675 {
lab=vtaup}
N 1915 -1660 1915 -1655 {
lab=vtaup}
N 1915 -1750 1915 -1745 {
lab=VDD}
N 2100 -1700 2130 -1700 {
lab=0}
N 2125 -1670 2125 -1665 {
lab=0}
N 2125 -1665 2125 -1645 {
lab=0}
N 2165 -1700 2195 -1700 {
lab=vthrdn}
N 2125 -1645 2125 -1640 {
lab=0}
N 2125 -1735 2125 -1730 {
lab=vthrdn}
N 2125 -1740 2125 -1735 {
lab=vthrdn}
N 2125 -1640 2125 -1580 {
lab=0}
N 2100 -1700 2100 -1640 {
lab=0}
N 2100 -1640 2125 -1640 {
lab=0}
N 2125 -1735 2180 -1735 {
lab=vthrdn}
N 2180 -1735 2180 -1700 {
lab=vthrdn}
N 1000 -1725 1030 -1725 {
lab=VDD}
N 1025 -1695 1025 -1690 {
lab=vthrdp}
N 1025 -1690 1025 -1670 {
lab=vthrdp}
N 1065 -1725 1095 -1725 {
lab=vthrdp}
N 1025 -1820 1025 -1760 {
lab=VDD}
N 1025 -1685 1075 -1685 {
lab=vthrdp}
N 1075 -1725 1075 -1685 {
lab=vthrdp}
N 1025 -1670 1025 -1665 {
lab=vthrdp}
N 1025 -1760 1025 -1755 {
lab=VDD}
N 1210 -1710 1240 -1710 {
lab=0}
N 1235 -1680 1235 -1675 {
lab=0}
N 1235 -1675 1235 -1655 {
lab=0}
N 1275 -1710 1305 -1710 {
lab=vtaun}
N 1235 -1655 1235 -1650 {
lab=0}
N 1235 -1745 1235 -1740 {
lab=vtaun}
N 1235 -1750 1235 -1745 {
lab=vtaun}
N 1235 -1650 1235 -1590 {
lab=0}
N 1210 -1710 1210 -1650 {
lab=0}
N 1210 -1650 1235 -1650 {
lab=0}
N 1235 -1745 1290 -1745 {
lab=vtaun}
N 1290 -1745 1290 -1710 {
lab=vtaun}
N 2280 -552.5 2310 -552.5 {
lab=VDD}
N 2305 -522.5 2305 -517.5 {
lab=vepulseextp}
N 2305 -517.5 2305 -497.5 {
lab=vepulseextp}
N 2345 -552.5 2375 -552.5 {
lab=vepulseextp}
N 2305 -647.5 2305 -587.5 {
lab=VDD}
N 2305 -512.5 2355 -512.5 {
lab=vepulseextp}
N 2355 -552.5 2355 -512.5 {
lab=vepulseextp}
N 2305 -497.5 2305 -492.5 {
lab=vepulseextp}
N 2305 -587.5 2305 -582.5 {
lab=VDD}
N 2570 -562.5 2600 -562.5 {
lab=VDD}
N 2595 -532.5 2595 -527.5 {
lab=vipulseextp}
N 2595 -527.5 2595 -507.5 {
lab=vipulseextp}
N 2635 -562.5 2665 -562.5 {
lab=vipulseextp}
N 2595 -657.5 2595 -597.5 {
lab=VDD}
N 2595 -522.5 2645 -522.5 {
lab=vipulseextp}
N 2645 -562.5 2645 -522.5 {
lab=vipulseextp}
N 2595 -507.5 2595 -502.5 {
lab=vipulseextp}
N 2595 -597.5 2595 -592.5 {
lab=VDD}
N 2870 -575 2900 -575 {
lab=VDD}
N 2895 -545 2895 -540 {
lab=bufmonp}
N 2895 -540 2895 -520 {
lab=bufmonp}
N 2935 -575 2965 -575 {
lab=bufmonp}
N 2895 -670 2895 -610 {
lab=VDD}
N 2895 -535 2945 -535 {
lab=bufmonp}
N 2945 -575 2945 -535 {
lab=bufmonp}
N 2895 -520 2895 -515 {
lab=bufmonp}
N 2895 -610 2895 -605 {
lab=VDD}
C {devices/vsource.sym} 855 -1065 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 855 -1095 0 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/vsource.sym} 320 -1045 0 1 {name=V12 value="pulse(0 1.8 35u 1ns 1ns 1ns 10us)"}
C {devices/lab_pin.sym} 320 -1105 0 0 {name=p19 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 1135 -1105 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 1135 -1045 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 1ms 1)"}
C {devices/code.sym} 110 -700 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {devices/code_shown.sym} 110 -430 0 0 {name=Xyce only_toplevel=false value="
.TRAN 0.01us 1ms 
.PRINT TRAN format=raw file=neuron_32syn_v1_tb.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO TR_singleton_filter=1 TR_amd=1
.SAVE

"}
C {sky130_fd_pr/corner.sym} 255 -695 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 1270 -660 2 0 {name=p3 sig_type=std_logic lab=0}
C {c_element_rj.sym} 1100 -765 0 0 {name=x2}
C {devices/lab_pin.sym} 1250 -785 2 0 {name=p56 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 950 -785 0 0 {name=p85 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 970 -300 0 0 {name=p10 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 960 -320 0 0 {name=p6 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 970 -540 0 0 {name=p7 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 960 -640 0 0 {name=p187 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 1935 -325 2 0 {name=p22 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 1935 -255 2 0 {name=p23 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 1935 -285 2 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1935 -215 2 0 {name=p25 sig_type=std_logic lab=0}
C {tie_low.sym} 1785 -235 0 0 {name=x6}
C {tie_low.sym} 1785 -305 0 0 {name=x7}
C {devices/lab_pin.sym} 970 -600 0 0 {name=p29 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 325 -960 0 0 {name=p31 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 325 -900 0 0 {name=V6 value="pulse(0 1.8 1ns 1ns 1ns 3us 12us 2)"}
C {devices/lab_pin.sym} 585 -950 0 0 {name=p32 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 585 -890 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 10ms 1)"}
C {devices/lab_pin.sym} 1935 -640 2 0 {name=p34 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 1935 -600 2 0 {name=p37 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1935 -530 2 0 {name=p38 sig_type=std_logic lab=0}
C {tie_low.sym} 1785 -550 0 0 {name=x8}
C {tie_low.sym} 1785 -620 0 0 {name=x9}
C {tie_hi.sym} 1785 -480 0 0 {name=x10}
C {devices/lab_pin.sym} 1935 -460 2 0 {name=p53 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1935 -570 2 0 {name=p36 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 1935 -500 2 0 {name=p55 sig_type=std_logic lab=syn_addr[2]}
C {tie_hi.sym} 1785 -410 0 0 {name=x11}
C {devices/lab_pin.sym} 1935 -390 2 0 {name=p58 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1935 -430 2 0 {name=p60 sig_type=std_logic lab=syn_addr[3]}
C {devices/lab_pin.sym} 960 -580 0 0 {name=p61 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 960 -660 0 0 {name=p62 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 960 -500 0 0 {name=p63 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 970 -400 0 0 {name=p64 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 970 -480 0 0 {name=p65 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 970 -520 0 0 {name=p70 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 970 -560 0 0 {name=p71 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 960 -440 0 0 {name=p73 sig_type=std_logic lab=vrefn}
C {devices/vsource.sym} 620 -1060 0 1 {name=V25 value="pulse(0 1.8 1ns 15ns 1ns 500us 1ms 1)"}
C {devices/lab_pin.sym} 620 -1120 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 970 -360 0 0 {name=p76 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1330 -680 1 0 {name=p77 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1500 -450 2 0 {name=p86 sig_type=std_logic lab=ack1}
C {sky130_stdcells/inv_1.sym} 1380 -450 0 0 {name=x16 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1460 -450 0 0 {name=x18 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1340 -450 0 0 {name=p88 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 890 -765 0 0 {name=p79 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1340 -580 2 0 {name=p78 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 910 -745 0 0 {name=p80 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1270 -640 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1250 -745 2 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 320 -1015 0 0 {name=p94 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1420 -650 0 1 {name=C1 model=cap_mim_m3_1 W=11 L=11 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 1420 -620 0 0 {name=p48 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 620 -1030 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 325 -870 0 0 {name=p81 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 585 -860 0 0 {name=p91 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 855 -1035 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1135 -1015 0 0 {name=p108 sig_type=std_logic lab=0}
C {devices/vsource.sym} 980 -1065 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 980 -1095 0 0 {name=p57 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 980 -1035 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1935 -235 0 1 {name=p27 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1935 -305 0 1 {name=p28 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1280 -600 0 1 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1935 -620 0 1 {name=p49 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1935 -550 0 1 {name=p50 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1935 -480 0 1 {name=p54 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1935 -410 0 1 {name=p59 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1280 -620 0 1 {name=p109 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1250 -765 0 1 {name=p4 sig_type=std_logic lab=dVDD}
C {neuron_32syn_v1.sym} 1120 -490 0 0 {name=x1}
C {devices/lab_pin.sym} 970 -620 0 0 {name=p18 sig_type=std_logic lab=JExcWp[0:3]}
C {devices/lab_pin.sym} 960 -680 2 1 {name=p30 sig_type=std_logic lab=JInhWn[0:3]}
C {devices/title.sym} 240 -160 0 0 {name=l1 author="Federico Corradi"}
C {devices/vsource.sym} 1360 -1055 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 1360 -1085 0 0 {name=p87 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1360 -1025 0 0 {name=p92 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 960 -460 0 0 {name=p8 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 970 -420 0 0 {name=p9 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 970 -380 0 0 {name=p11 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 960 -340 0 0 {name=p12 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1065 -1437.5 0 1 {name=p13 sig_type=std_logic lab=JInhWn[0]}
C {devices/lab_pin.sym} 1955 -1392.5 0 1 {name=p14 sig_type=std_logic lab=JExcWp[0]}
C {devices/lab_pin.sym} 320 -1435 0 1 {name=p51 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 250 -1315 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/isource.sym} 250 -1505 0 0 {name=I8 value=0}
C {sky130_fd_pr/nfet_01v8.sym} 270 -1435 0 1 {name=M9
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
C {devices/lab_pin.sym} 250 -1535 0 0 {name=p101 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 500 -1440 0 1 {name=M10
L=0.15
W=1.0
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
C {devices/lab_pin.sym} 480 -1320 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 455 -1440 0 0 {name=p90 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 480 -1350 0 0 {name=I9 value=500p}
C {devices/lab_pin.sym} 480 -1535 0 0 {name=p104 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 550 -1440 0 1 {name=p105 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 710 -1315 0 0 {name=p106 sig_type=std_logic lab=0}
C {devices/isource.sym} 710 -1505 0 0 {name=I10 value=100p}
C {sky130_fd_pr/nfet_01v8.sym} 730 -1435 0 1 {name=M11
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 710 -1535 0 0 {name=p107 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 780 -1435 0 1 {name=p110 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1010 -1305 0 0 {name=p119 sig_type=std_logic lab=0}
C {devices/isource.sym} 1010 -1495 0 0 {name=I13 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1030 -1425 0 1 {name=M14
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 1010 -1525 0 0 {name=p121 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1270 -1432.5 0 1 {name=p41 sig_type=std_logic lab=JInhWn[1]}
C {devices/lab_pin.sym} 1215 -1300 0 0 {name=p45 sig_type=std_logic lab=0}
C {devices/isource.sym} 1215 -1490 0 0 {name=I1 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1235 -1420 0 1 {name=M1
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 1215 -1520 0 0 {name=p46 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1470 -1427.5 0 1 {name=p96 sig_type=std_logic lab=JInhWn[2]}
C {devices/lab_pin.sym} 1415 -1295 0 0 {name=p98 sig_type=std_logic lab=0}
C {devices/isource.sym} 1415 -1485 0 0 {name=I2 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1435 -1415 0 1 {name=M2
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 1415 -1515 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1670 -1422.5 0 1 {name=p17 sig_type=std_logic lab=JInhWn[3]}
C {devices/lab_pin.sym} 1615 -1290 0 0 {name=p111 sig_type=std_logic lab=0}
C {devices/isource.sym} 1615 -1480 0 0 {name=I3 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1635 -1410 0 1 {name=M3
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 1615 -1510 0 0 {name=p112 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 1925 -1420 0 1 {name=M12
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 1905 -1300 0 0 {name=p20 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1880 -1420 0 0 {name=p21 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1905 -1330 0 0 {name=I11 value=1u}
C {devices/lab_pin.sym} 1905 -1515 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2165 -1397.5 0 1 {name=p26 sig_type=std_logic lab=JExcWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 2135 -1425 0 1 {name=M4
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 2115 -1305 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2090 -1425 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2115 -1335 0 0 {name=I4 value=1u}
C {devices/lab_pin.sym} 2115 -1520 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2390 -1397.5 0 1 {name=p117 sig_type=std_logic lab=JExcWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 2360 -1425 0 1 {name=M5
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 2340 -1305 0 0 {name=p118 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2315 -1425 0 0 {name=p120 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2340 -1335 0 0 {name=I5 value=1u}
C {devices/lab_pin.sym} 2340 -1520 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2615 -1397.5 0 1 {name=p123 sig_type=std_logic lab=JExcWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 2585 -1425 0 1 {name=M6
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 2565 -1305 0 0 {name=p124 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2540 -1425 0 0 {name=p125 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2565 -1335 0 0 {name=I6 value=10u}
C {devices/lab_pin.sym} 2565 -1520 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1965 -1687.5 0 1 {name=p33 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 1935 -1715 0 1 {name=M7
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 1915 -1595 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1890 -1715 0 0 {name=p47 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1915 -1625 0 0 {name=I7 value=1p}
C {devices/lab_pin.sym} 1915 -1810 0 0 {name=p69 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2180 -1712.5 0 1 {name=p72 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 2125 -1580 0 0 {name=p84 sig_type=std_logic lab=0}
C {devices/isource.sym} 2125 -1770 0 0 {name=I16 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 2145 -1700 0 1 {name=M8
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 2125 -1800 0 0 {name=p39 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1075 -1697.5 0 1 {name=p140 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 1045 -1725 0 1 {name=M17
L=1.0
W=1.0
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
C {devices/lab_pin.sym} 1025 -1605 0 0 {name=p141 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1000 -1725 0 0 {name=p142 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1025 -1635 0 0 {name=I17 value=780p}
C {devices/lab_pin.sym} 1025 -1820 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1290 -1722.5 0 1 {name=p144 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1235 -1590 0 0 {name=p145 sig_type=std_logic lab=0}
C {devices/isource.sym} 1235 -1780 0 0 {name=I18 value=1p}
C {sky130_fd_pr/nfet_01v8.sym} 1255 -1710 0 1 {name=M18
L=1.0
W=0.65
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
C {devices/lab_pin.sym} 1235 -1810 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2960 -575 0 1 {name=p42 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 2325 -552.5 0 1 {name=M13
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
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 2305 -435 0 0 {name=p43 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2280 -552.5 0 0 {name=p52 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2305 -465 0 0 {name=I12 value=2u}
C {devices/lab_pin.sym} 2305 -647.5 0 0 {name=p128 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2375 -552.5 2 0 {name=p129 sig_type=std_logic lab=vepulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 2615 -562.5 0 1 {name=M15
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
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 2595 -445 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2570 -562.5 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2595 -475 0 0 {name=I14 value=2u}
C {devices/lab_pin.sym} 2595 -657.5 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2665 -562.5 2 0 {name=p133 sig_type=std_logic lab=vipulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 2915 -575 0 1 {name=M16
L=1.0
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
C {devices/lab_pin.sym} 2895 -455 0 0 {name=p134 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2870 -575 0 0 {name=p135 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2895 -485 0 0 {name=I15 value=500p}
C {devices/lab_pin.sym} 2895 -670 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1930 -180 2 0 {name=p40 sig_type=std_logic lab=W[2]}
C {devices/lab_pin.sym} 1930 -110 2 0 {name=p66 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 1930 -140 2 0 {name=p67 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1930 -70 2 0 {name=p68 sig_type=std_logic lab=0}
C {tie_low.sym} 1780 -160 0 0 {name=x4}
C {devices/lab_pin.sym} 1930 -90 0 1 {name=p74 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1930 -160 0 1 {name=p97 sig_type=std_logic lab=aVDD}
C {tie_hi.sym} 1780 -90 0 0 {name=x3}
