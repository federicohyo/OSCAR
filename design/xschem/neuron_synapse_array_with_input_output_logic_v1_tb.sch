v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 2202.5 -1632.5 3002.5 -1232.5 {flags=graph
y1=-1.6
y2=0.4
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
node="x1.req_o[15]
x1.req_o[14]
x1.req_o[13]
x1.req_o[12]
x1.req_o[11]
x1.req_o[10]
x1.req_o[9]
x1.req_o[8]
x1.req_o[7]
x1.req_o[6]
x1.req_o[5]
x1.req_o[4]
x1.req_o[3]
x1.req_o[2]
x1.req_o[1]
x1.req_o[0]"
color="15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15"
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 2197.5 -1190 2997.5 -790 {flags=graph
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
node=""
color=""
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 1357.5 -1617.5 2157.5 -1217.5 {flags=graph
y1=0
y2=1.8
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
node="monout[12]
x1.x1.x16.x1.net13
exc
x1.x1.x16.x2.net13"
color="4 6 8 15"
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 2197.5 -730 2997.5 -330 {flags=graph
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
node=""
color=""
dataset=-1
unitx=1
logx=0
logy=0
}
T {Power up reset} 580 -1635 0 0 0.4 0.4 {}
T {Neuron biases} 325 -2005 0 0 0.4 0.4 {}
T {Inhibitory syn} 697.5 -2247.5 0 0 0.4 0.4 {}
T {Excitatory syn} 1580 -2252.5 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 220 -1217.5 0 0 0.4 0.4 {}
T {Output Monitors} 1115 -1182.5 0 0 0.4 0.4 {}
N 207.5 -1567.5 207.5 -1537.5 {
lab=dVDD}
N 1060 -1520 1060 -1500 {
lab=0}
N 1060 -1610 1060 -1580 {
lab=REQIN}
N 297.5 -1567.5 297.5 -1537.5 {
lab=aVDD}
N 620 -1585 620 -1555 {
lab=nRes}
N 202.5 -1477.5 212.5 -1477.5 {
lab=0}
N 650 -1290 650 -1270 {
lab=0}
N 650 -1380 650 -1350 {
lab=setW}
N 910 -1370 910 -1340 {
lab=resetW}
N 1440 -815 1512.5 -815 {
lab=aer_out[0:3]}
N 620 -1495 625 -1495 {
lab=0}
N 130 -1860 160 -1860 {
lab=0}
N 155 -1830 155 -1825 {
lab=0}
N 155 -1825 155 -1805 {
lab=0}
N 195 -1860 225 -1860 {
lab=vleakn}
N 155 -1805 155 -1800 {
lab=0}
N 155 -1895 155 -1890 {
lab=vleakn}
N 155 -1900 155 -1895 {
lab=vleakn}
N 155 -1800 155 -1740 {
lab=0}
N 130 -1860 130 -1800 {
lab=0}
N 130 -1800 155 -1800 {
lab=0}
N 155 -1895 210 -1895 {
lab=vleakn}
N 210 -1895 210 -1860 {
lab=vleakn}
N 360 -1865 390 -1865 {
lab=VDD}
N 385 -1835 385 -1830 {
lab=ifdcp}
N 385 -1830 385 -1810 {
lab=ifdcp}
N 425 -1865 455 -1865 {
lab=ifdcp}
N 385 -1960 385 -1900 {
lab=VDD}
N 385 -1825 435 -1825 {
lab=ifdcp}
N 435 -1865 435 -1825 {
lab=ifdcp}
N 385 -1810 385 -1805 {
lab=ifdcp}
N 385 -1900 385 -1895 {
lab=VDD}
N 590 -1860 620 -1860 {
lab=0}
N 615 -1830 615 -1825 {
lab=0}
N 615 -1825 615 -1805 {
lab=0}
N 655 -1860 685 -1860 {
lab=vrefn}
N 615 -1805 615 -1800 {
lab=0}
N 615 -1895 615 -1890 {
lab=vrefn}
N 615 -1900 615 -1895 {
lab=vrefn}
N 615 -1800 615 -1740 {
lab=0}
N 590 -1860 590 -1800 {
lab=0}
N 590 -1800 615 -1800 {
lab=0}
N 615 -1895 670 -1895 {
lab=vrefn}
N 670 -1895 670 -1860 {
lab=vrefn}
N 890 -1850 920 -1850 {
lab=0}
N 915 -1820 915 -1815 {
lab=0}
N 915 -1815 915 -1795 {
lab=0}
N 955 -1850 985 -1850 {
lab=JInhWn[0]}
N 915 -1795 915 -1790 {
lab=0}
N 915 -1885 915 -1880 {
lab=JInhWn[0]}
N 915 -1890 915 -1885 {
lab=JInhWn[0]}
N 915 -1790 915 -1730 {
lab=0}
N 890 -1850 890 -1790 {
lab=0}
N 890 -1790 915 -1790 {
lab=0}
N 915 -1885 970 -1885 {
lab=JInhWn[0]}
N 970 -1885 970 -1850 {
lab=JInhWn[0]}
N 1095 -1845 1125 -1845 {
lab=0}
N 1120 -1815 1120 -1810 {
lab=0}
N 1120 -1810 1120 -1790 {
lab=0}
N 1160 -1845 1190 -1845 {
lab=JInhWn[1]}
N 1120 -1790 1120 -1785 {
lab=0}
N 1120 -1880 1120 -1875 {
lab=JInhWn[1]}
N 1120 -1885 1120 -1880 {
lab=JInhWn[1]}
N 1120 -1785 1120 -1725 {
lab=0}
N 1095 -1845 1095 -1785 {
lab=0}
N 1095 -1785 1120 -1785 {
lab=0}
N 1120 -1880 1175 -1880 {
lab=JInhWn[1]}
N 1175 -1880 1175 -1845 {
lab=JInhWn[1]}
N 1295 -1840 1325 -1840 {
lab=0}
N 1320 -1810 1320 -1805 {
lab=0}
N 1320 -1805 1320 -1785 {
lab=0}
N 1360 -1840 1390 -1840 {
lab=JInhWn[2]}
N 1320 -1785 1320 -1780 {
lab=0}
N 1320 -1875 1320 -1870 {
lab=JInhWn[2]}
N 1320 -1880 1320 -1875 {
lab=JInhWn[2]}
N 1320 -1780 1320 -1720 {
lab=0}
N 1295 -1840 1295 -1780 {
lab=0}
N 1295 -1780 1320 -1780 {
lab=0}
N 1320 -1875 1375 -1875 {
lab=JInhWn[2]}
N 1375 -1875 1375 -1840 {
lab=JInhWn[2]}
N 1495 -1835 1525 -1835 {
lab=0}
N 1520 -1805 1520 -1800 {
lab=0}
N 1520 -1800 1520 -1780 {
lab=0}
N 1560 -1835 1590 -1835 {
lab=JInhWn[3]}
N 1520 -1780 1520 -1775 {
lab=0}
N 1520 -1870 1520 -1865 {
lab=JInhWn[3]}
N 1520 -1875 1520 -1870 {
lab=JInhWn[3]}
N 1520 -1775 1520 -1715 {
lab=0}
N 1495 -1835 1495 -1775 {
lab=0}
N 1495 -1775 1520 -1775 {
lab=0}
N 1520 -1870 1575 -1870 {
lab=JInhWn[3]}
N 1575 -1870 1575 -1835 {
lab=JInhWn[3]}
N 1785 -1845 1815 -1845 {
lab=VDD}
N 1810 -1815 1810 -1810 {
lab=JExcWp[0]}
N 1810 -1810 1810 -1790 {
lab=JExcWp[0]}
N 1850 -1845 1880 -1845 {
lab=JExcWp[0]}
N 1810 -1940 1810 -1880 {
lab=VDD}
N 1810 -1805 1860 -1805 {
lab=JExcWp[0]}
N 1860 -1845 1860 -1805 {
lab=JExcWp[0]}
N 1810 -1790 1810 -1785 {
lab=JExcWp[0]}
N 1810 -1880 1810 -1875 {
lab=VDD}
N 1995 -1850 2025 -1850 {
lab=VDD}
N 2020 -1820 2020 -1815 {
lab=JExcWp[1]}
N 2020 -1815 2020 -1795 {
lab=JExcWp[1]}
N 2060 -1850 2090 -1850 {
lab=JExcWp[1]}
N 2020 -1945 2020 -1885 {
lab=VDD}
N 2020 -1810 2070 -1810 {
lab=JExcWp[1]}
N 2070 -1850 2070 -1810 {
lab=JExcWp[1]}
N 2020 -1795 2020 -1790 {
lab=JExcWp[1]}
N 2020 -1885 2020 -1880 {
lab=VDD}
N 2220 -1850 2250 -1850 {
lab=VDD}
N 2245 -1820 2245 -1815 {
lab=JExcWp[2]}
N 2245 -1815 2245 -1795 {
lab=JExcWp[2]}
N 2285 -1850 2315 -1850 {
lab=JExcWp[2]}
N 2245 -1945 2245 -1885 {
lab=VDD}
N 2245 -1810 2295 -1810 {
lab=JExcWp[2]}
N 2295 -1850 2295 -1810 {
lab=JExcWp[2]}
N 2245 -1795 2245 -1790 {
lab=JExcWp[2]}
N 2245 -1885 2245 -1880 {
lab=VDD}
N 2445 -1850 2475 -1850 {
lab=VDD}
N 2470 -1820 2470 -1815 {
lab=JExcWp[3]}
N 2470 -1815 2470 -1795 {
lab=JExcWp[3]}
N 2510 -1850 2540 -1850 {
lab=JExcWp[3]}
N 2470 -1945 2470 -1885 {
lab=VDD}
N 2470 -1810 2520 -1810 {
lab=JExcWp[3]}
N 2520 -1850 2520 -1810 {
lab=JExcWp[3]}
N 2470 -1795 2470 -1790 {
lab=JExcWp[3]}
N 2470 -1885 2470 -1880 {
lab=VDD}
N 105 -1072.5 135 -1072.5 {
lab=VDD}
N 130 -1042.5 130 -1037.5 {
lab=vepulseextp}
N 130 -1037.5 130 -1017.5 {
lab=vepulseextp}
N 170 -1072.5 200 -1072.5 {
lab=vepulseextp}
N 130 -1167.5 130 -1107.5 {
lab=VDD}
N 130 -1032.5 180 -1032.5 {
lab=vepulseextp}
N 180 -1072.5 180 -1032.5 {
lab=vepulseextp}
N 130 -1017.5 130 -1012.5 {
lab=vepulseextp}
N 130 -1107.5 130 -1102.5 {
lab=VDD}
N 395 -1082.5 425 -1082.5 {
lab=VDD}
N 420 -1052.5 420 -1047.5 {
lab=vipulseextp}
N 420 -1047.5 420 -1027.5 {
lab=vipulseextp}
N 460 -1082.5 490 -1082.5 {
lab=vipulseextp}
N 420 -1177.5 420 -1117.5 {
lab=VDD}
N 420 -1042.5 470 -1042.5 {
lab=vipulseextp}
N 470 -1082.5 470 -1042.5 {
lab=vipulseextp}
N 420 -1027.5 420 -1022.5 {
lab=vipulseextp}
N 420 -1117.5 420 -1112.5 {
lab=VDD}
N 695 -1095 725 -1095 {
lab=VDD}
N 720 -1065 720 -1060 {
lab=bufmonp}
N 720 -1060 720 -1040 {
lab=bufmonp}
N 760 -1095 790 -1095 {
lab=bufmonp}
N 720 -1190 720 -1130 {
lab=VDD}
N 720 -1055 770 -1055 {
lab=bufmonp}
N 770 -1095 770 -1055 {
lab=bufmonp}
N 720 -1040 720 -1035 {
lab=bufmonp}
N 720 -1130 720 -1125 {
lab=VDD}
N 1795 -2140 1825 -2140 {
lab=VDD}
N 1820 -2110 1820 -2105 {
lab=vtaup}
N 1820 -2105 1820 -2085 {
lab=vtaup}
N 1860 -2140 1890 -2140 {
lab=vtaup}
N 1820 -2235 1820 -2175 {
lab=VDD}
N 1820 -2100 1870 -2100 {
lab=vtaup}
N 1870 -2140 1870 -2100 {
lab=vtaup}
N 1820 -2085 1820 -2080 {
lab=vtaup}
N 1820 -2175 1820 -2170 {
lab=VDD}
N 2005 -2125 2035 -2125 {
lab=0}
N 2030 -2095 2030 -2090 {
lab=0}
N 2030 -2090 2030 -2070 {
lab=0}
N 2070 -2125 2100 -2125 {
lab=vthrdn}
N 2030 -2070 2030 -2065 {
lab=0}
N 2030 -2160 2030 -2155 {
lab=vthrdn}
N 2030 -2165 2030 -2160 {
lab=vthrdn}
N 2030 -2065 2030 -2005 {
lab=0}
N 2005 -2125 2005 -2065 {
lab=0}
N 2005 -2065 2030 -2065 {
lab=0}
N 2030 -2160 2085 -2160 {
lab=vthrdn}
N 2085 -2160 2085 -2125 {
lab=vthrdn}
N 905 -2150 935 -2150 {
lab=VDD}
N 930 -2120 930 -2115 {
lab=vthrdp}
N 930 -2115 930 -2095 {
lab=vthrdp}
N 970 -2150 1000 -2150 {
lab=vthrdp}
N 930 -2245 930 -2185 {
lab=VDD}
N 930 -2110 980 -2110 {
lab=vthrdp}
N 980 -2150 980 -2110 {
lab=vthrdp}
N 930 -2095 930 -2090 {
lab=vthrdp}
N 930 -2185 930 -2180 {
lab=VDD}
N 1115 -2135 1145 -2135 {
lab=0}
N 1140 -2105 1140 -2100 {
lab=0}
N 1140 -2100 1140 -2080 {
lab=0}
N 1180 -2135 1210 -2135 {
lab=vtaun}
N 1140 -2080 1140 -2075 {
lab=0}
N 1140 -2170 1140 -2165 {
lab=vtaun}
N 1140 -2175 1140 -2170 {
lab=vtaun}
N 1140 -2075 1140 -2015 {
lab=0}
N 1115 -2135 1115 -2075 {
lab=0}
N 1115 -2075 1140 -2075 {
lab=0}
N 1140 -2170 1195 -2170 {
lab=vtaun}
N 1195 -2170 1195 -2135 {
lab=vtaun}
N 1125 -1035 1125 -1015 {
lab=0}
N 1125 -1125 1125 -1095 {
lab=clk}
N 1360 -1030 1360 -1010 {
lab=0}
N 1360 -1120 1360 -1090 {
lab=Da}
N 1707.5 -525 1707.5 -505 {
lab=0}
N 1707.5 -615 1707.5 -585 {
lab=neu_addr[2]}
N 1707.5 -385 1707.5 -365 {
lab=0}
N 1707.5 -475 1707.5 -445 {
lab=neu_addr[3]}
N 1542.5 -525 1542.5 -505 {
lab=0}
N 1542.5 -615 1542.5 -585 {
lab=neu_addr[0]}
N 1542.5 -385 1542.5 -365 {
lab=0}
N 1542.5 -475 1542.5 -445 {
lab=neu_addr[1]}
N 675 -825 675 -805 {
lab=0}
N 675 -915 675 -885 {
lab=W[2]}
N 510 -825 510 -805 {
lab=0}
N 510 -915 510 -885 {
lab=W[3]}
N 672.5 -690 672.5 -670 {
lab=0}
N 672.5 -780 672.5 -750 {
lab=W[0]}
N 507.5 -690 507.5 -670 {
lab=0}
N 507.5 -780 507.5 -750 {
lab=W[1]}
N 662.5 -525 662.5 -505 {
lab=0}
N 662.5 -615 662.5 -585 {
lab=syn_addr[1]}
N 497.5 -525 497.5 -505 {
lab=0}
N 497.5 -615 497.5 -585 {
lab=syn_addr[0]}
N 660 -390 660 -370 {
lab=0}
N 660 -480 660 -450 {
lab=syn_addr[3]}
N 495 -390 495 -370 {
lab=0}
N 495 -480 495 -450 {
lab=syn_addr[2]}
C {devices/vsource.sym} 207.5 -1507.5 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 1440 -735 2 0 {name=p35 sig_type=std_logic lab=dVDD}
C {devices/vsource.sym} 1060 -1550 0 1 {name=V12 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/lab_pin.sym} 1060 -1610 0 0 {name=p19 sig_type=std_logic lab=REQIN}
C {devices/vsource.sym} 297.5 -1507.5 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 297.5 -1567.5 0 0 {name=p57 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 620 -1585 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 620 -1525 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 1ms 1)"}
C {devices/lab_pin.sym} 1060 -1520 0 0 {name=p94 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 207.5 -1477.5 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 297.5 -1477.5 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/code.sym} 80 -770 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 235 -755 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 507.5 -780 2 0 {name=p22 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 672.5 -780 2 0 {name=p23 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 650 -1380 0 0 {name=p31 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 650 -1320 0 0 {name=V6 value="pulse(0 1.8 1ns 30ns 1ns 60us 120us 2)"}
C {devices/lab_pin.sym} 910 -1370 0 0 {name=p32 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 910 -1310 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 200us 1)"}
C {devices/vsource.sym} 1120 -1420 0 1 {name=V25 value="pulse(0 1.8 1ns 15ns 1ns 500us 1ms 1)"}
C {devices/lab_pin.sym} 1120 -1450 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1120 -1390 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 650 -1270 0 0 {name=p81 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 910 -1280 0 0 {name=p91 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1885 -787.5 2 0 {name=p86 sig_type=std_logic lab=ACK}
C {sky130_stdcells/inv_1.sym} 1765 -787.5 0 0 {name=x16 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1845 -787.5 0 0 {name=x18 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1725 -787.5 0 0 {name=p88 sig_type=std_logic lab=REQ}
C {devices/lab_pin.sym} 1440 -855 2 0 {name=p1 sig_type=std_logic lab=REQ}
C {devices/lab_pin.sym} 1440 -795 2 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1440 -755 2 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 207.5 -1567.5 0 0 {name=p5 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1140 -855 2 1 {name=p6 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1140 -835 0 0 {name=p7 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1140 -775 0 0 {name=p15 sig_type=std_logic lab=ACK}
C {devices/lab_pin.sym} 1140 -795 0 0 {name=p17 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1140 -735 0 0 {name=p29 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 1140 -815 0 0 {name=p36 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 497.5 -615 2 0 {name=p37 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 662.5 -615 2 0 {name=p52 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 495 -480 2 0 {name=p55 sig_type=std_logic lab=syn_addr[2]}
C {devices/lab_pin.sym} 660 -480 2 0 {name=p60 sig_type=std_logic lab=syn_addr[3]}
C {devices/lab_pin.sym} 1140 -675 0 0 {name=p56 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1140 -595 0 0 {name=p61 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1140 -655 0 0 {name=p62 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 1140 -635 0 0 {name=p63 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 1707.5 -615 2 0 {name=p76 sig_type=std_logic lab=neu_addr[2]}
C {devices/lab_pin.sym} 1707.5 -475 2 0 {name=p79 sig_type=std_logic lab=neu_addr[3]}
C {devices/lab_pin.sym} 1140 -515 0 0 {name=p80 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 1140 -475 0 0 {name=p85 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 1140 -415 0 0 {name=p97 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1140 -695 0 0 {name=p99 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1140 -535 0 0 {name=p100 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1440 -835 2 0 {name=p102 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1512.5 -815 2 0 {name=p103 sig_type=std_logic lab=aer_out[0:3]}
C {neuron_synapse_array_with_input_output_logic_v1.sym} 1290 -635 0 0 {name=x1}
C {devices/lab_pin.sym} 1140 -715 0 0 {name=p11 sig_type=std_logic lab=JInhWn[0:3]}
C {devices/lab_pin.sym} 1140 -755 0 0 {name=p43 sig_type=std_logic lab=JExcWp[0:3]}
C {devices/lab_pin.sym} 970 -1862.5 0 1 {name=p13 sig_type=std_logic lab=JInhWn[0]}
C {devices/lab_pin.sym} 1860 -1817.5 0 1 {name=p14 sig_type=std_logic lab=JExcWp[0]}
C {devices/vsource.sym} 390 -1525 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 390 -1555 0 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 390 -1495 0 0 {name=p42 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 225 -1860 0 1 {name=p51 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 155 -1740 0 0 {name=p64 sig_type=std_logic lab=0}
C {devices/isource.sym} 155 -1930 0 0 {name=I8 value=0}
C {sky130_fd_pr/nfet_01v8.sym} 175 -1860 0 1 {name=M9
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
C {devices/lab_pin.sym} 155 -1960 0 0 {name=p101 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 405 -1865 0 1 {name=M10
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
C {devices/lab_pin.sym} 385 -1745 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 360 -1865 0 0 {name=p90 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 385 -1775 0 0 {name=I9 value=500p}
C {devices/lab_pin.sym} 385 -1960 0 0 {name=p104 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 455 -1865 0 1 {name=p105 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 615 -1740 0 0 {name=p106 sig_type=std_logic lab=0}
C {devices/isource.sym} 615 -1930 0 0 {name=I10 value=100p}
C {sky130_fd_pr/nfet_01v8.sym} 635 -1860 0 1 {name=M11
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
C {devices/lab_pin.sym} 615 -1960 0 0 {name=p107 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 685 -1860 0 1 {name=p110 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 915 -1730 0 0 {name=p119 sig_type=std_logic lab=0}
C {devices/isource.sym} 915 -1920 0 0 {name=I13 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 935 -1850 0 1 {name=M14
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
C {devices/lab_pin.sym} 915 -1950 0 0 {name=p121 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1175 -1857.5 0 1 {name=p41 sig_type=std_logic lab=JInhWn[1]}
C {devices/lab_pin.sym} 1120 -1725 0 0 {name=p45 sig_type=std_logic lab=0}
C {devices/isource.sym} 1120 -1915 0 0 {name=I1 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1140 -1845 0 1 {name=M1
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
C {devices/lab_pin.sym} 1120 -1945 0 0 {name=p46 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1375 -1852.5 0 1 {name=p96 sig_type=std_logic lab=JInhWn[2]}
C {devices/lab_pin.sym} 1320 -1720 0 0 {name=p98 sig_type=std_logic lab=0}
C {devices/isource.sym} 1320 -1910 0 0 {name=I2 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1340 -1840 0 1 {name=M2
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
C {devices/lab_pin.sym} 1320 -1940 0 0 {name=p108 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1575 -1847.5 0 1 {name=p109 sig_type=std_logic lab=JInhWn[3]}
C {devices/lab_pin.sym} 1520 -1715 0 0 {name=p111 sig_type=std_logic lab=0}
C {devices/isource.sym} 1520 -1905 0 0 {name=I3 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 1540 -1835 0 1 {name=M3
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
C {devices/lab_pin.sym} 1520 -1935 0 0 {name=p112 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 1830 -1845 0 1 {name=M12
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
C {devices/lab_pin.sym} 1810 -1725 0 0 {name=p16 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1785 -1845 0 0 {name=p18 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1810 -1755 0 0 {name=I11 value=4p}
C {devices/lab_pin.sym} 1810 -1940 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2070 -1822.5 0 1 {name=p26 sig_type=std_logic lab=JExcWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 2040 -1850 0 1 {name=M4
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
C {devices/lab_pin.sym} 2020 -1730 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1995 -1850 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2020 -1760 0 0 {name=I4 value=4p}
C {devices/lab_pin.sym} 2020 -1945 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2295 -1822.5 0 1 {name=p117 sig_type=std_logic lab=JExcWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 2265 -1850 0 1 {name=M5
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
C {devices/lab_pin.sym} 2245 -1730 0 0 {name=p118 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2220 -1850 0 0 {name=p120 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2245 -1760 0 0 {name=I5 value=4p}
C {devices/lab_pin.sym} 2245 -1945 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2520 -1822.5 0 1 {name=p123 sig_type=std_logic lab=JExcWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 2490 -1850 0 1 {name=M6
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
C {devices/lab_pin.sym} 2470 -1730 0 0 {name=p124 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2445 -1850 0 0 {name=p125 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2470 -1760 0 0 {name=I6 value=4p}
C {devices/lab_pin.sym} 2470 -1945 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 620 -1495 0 0 {name=p127 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 785 -1095 0 1 {name=p30 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 150 -1072.5 0 1 {name=M13
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
C {devices/lab_pin.sym} 130 -955 0 0 {name=p33 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 105 -1072.5 0 0 {name=p39 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 130 -985 0 0 {name=I12 value=1u}
C {devices/lab_pin.sym} 130 -1167.5 0 0 {name=p128 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 200 -1072.5 2 0 {name=p129 sig_type=std_logic lab=vepulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 440 -1082.5 0 1 {name=M15
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
C {devices/lab_pin.sym} 420 -965 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 395 -1082.5 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 420 -995 0 0 {name=I14 value=1u}
C {devices/lab_pin.sym} 420 -1177.5 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 490 -1082.5 2 0 {name=p133 sig_type=std_logic lab=vipulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 740 -1095 0 1 {name=M16
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
C {devices/lab_pin.sym} 720 -975 0 0 {name=p134 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 695 -1095 0 0 {name=p135 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 720 -1005 0 0 {name=I15 value=500p}
C {devices/lab_pin.sym} 720 -1190 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/title.sym} 195 -165 0 0 {name=l1 author="Federico Corradi"}
C {devices/lab_pin.sym} 510 -915 2 0 {name=p8 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 675 -915 2 0 {name=p9 sig_type=std_logic lab=W[2]}
C {devices/simulator_commands_shown.sym} 90 -320 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 250us
.PRINT TRAN format=raw file=neuron_synapse_array_with_input_output_logic_tb_v1.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
C {devices/lab_pin.sym} 1870 -2112.5 0 1 {name=p34 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 1840 -2140 0 1 {name=M7
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
C {devices/lab_pin.sym} 1820 -2020 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1795 -2140 0 0 {name=p47 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1820 -2050 0 0 {name=I7 value=1p}
C {devices/lab_pin.sym} 1820 -2235 0 0 {name=p69 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2085 -2137.5 0 1 {name=p72 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 2030 -2005 0 0 {name=p84 sig_type=std_logic lab=0}
C {devices/isource.sym} 2030 -2195 0 0 {name=I16 value=780p}
C {sky130_fd_pr/nfet_01v8.sym} 2050 -2125 0 1 {name=M8
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
C {devices/lab_pin.sym} 2030 -2225 0 0 {name=p87 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1140 -555 0 0 {name=p92 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1140 -455 0 0 {name=p137 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1140 -435 0 0 {name=p138 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1140 -495 0 0 {name=p139 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 980 -2122.5 0 1 {name=p140 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 950 -2150 0 1 {name=M17
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
C {devices/lab_pin.sym} 930 -2030 0 0 {name=p141 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 905 -2150 0 0 {name=p142 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 930 -2060 0 0 {name=I17 value=780p}
C {devices/lab_pin.sym} 930 -2245 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1195 -2147.5 0 1 {name=p144 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1140 -2015 0 0 {name=p145 sig_type=std_logic lab=0}
C {devices/isource.sym} 1140 -2205 0 0 {name=I18 value=1p}
C {sky130_fd_pr/nfet_01v8.sym} 1160 -2135 0 1 {name=M18
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
C {devices/lab_pin.sym} 1140 -2235 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 1125 -1065 0 1 {name=V18 value="pulse(0 1.8 10ns 1ns 1ns 5us 10us)"}
C {devices/lab_pin.sym} 1125 -1125 0 0 {name=p147 sig_type=std_logic lab=clk}
C {devices/vsource.sym} 1360 -1060 0 1 {name=V19 value="pulse(0 1.8 10ns 1ns 1ns 10us 20us)"}
C {devices/lab_pin.sym} 1360 -1120 0 0 {name=p148 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 1125 -1015 0 0 {name=p149 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1360 -1010 0 0 {name=p150 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1140 -575 0 0 {name=p151 sig_type=std_logic lab=clk}
C {devices/lab_pin.sym} 1140 -615 0 0 {name=p152 sig_type=std_logic lab=Da}
C {devices/vsource.sym} 1707.5 -555 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 1707.5 -505 0 0 {name=p154 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1707.5 -415 0 0 {name=V3 value=0}
C {devices/lab_pin.sym} 1707.5 -365 0 0 {name=p68 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1542.5 -615 2 0 {name=p66 sig_type=std_logic lab=neu_addr[0]}
C {devices/lab_pin.sym} 1542.5 -475 2 0 {name=p153 sig_type=std_logic lab=neu_addr[1]}
C {devices/vsource.sym} 1542.5 -555 0 0 {name=V5 value=0}
C {devices/lab_pin.sym} 1542.5 -505 0 0 {name=p155 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1542.5 -415 0 0 {name=V7 value=0}
C {devices/lab_pin.sym} 1542.5 -365 0 0 {name=p156 sig_type=std_logic lab=0}
C {devices/vsource.sym} 675 -855 0 0 {name=V8 value=1.8}
C {devices/lab_pin.sym} 675 -805 0 0 {name=p67 sig_type=std_logic lab=0}
C {devices/vsource.sym} 510 -855 0 0 {name=V9 value=0}
C {devices/lab_pin.sym} 510 -805 0 0 {name=p71 sig_type=std_logic lab=0}
C {devices/vsource.sym} 672.5 -720 0 0 {name=V10 value=1.8}
C {devices/lab_pin.sym} 672.5 -670 0 0 {name=p74 sig_type=std_logic lab=0}
C {devices/vsource.sym} 507.5 -720 0 0 {name=V13 value=0}
C {devices/lab_pin.sym} 507.5 -670 0 0 {name=p78 sig_type=std_logic lab=0}
C {devices/vsource.sym} 662.5 -555 0 0 {name=V15 value=1.8}
C {devices/lab_pin.sym} 662.5 -505 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/vsource.sym} 497.5 -555 0 0 {name=V16 value=0}
C {devices/lab_pin.sym} 497.5 -505 0 0 {name=p25 sig_type=std_logic lab=0}
C {devices/vsource.sym} 660 -420 0 0 {name=V17 value=1.8}
C {devices/lab_pin.sym} 660 -370 0 0 {name=p27 sig_type=std_logic lab=0}
C {devices/vsource.sym} 495 -420 0 0 {name=V20 value=0}
C {devices/lab_pin.sym} 495 -370 0 0 {name=p28 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1440 -775 2 0 {name=p2 sig_type=std_logic lab=0}
