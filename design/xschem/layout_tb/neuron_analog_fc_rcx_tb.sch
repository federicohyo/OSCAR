v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 2450 -2160 3250 -1760 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0005
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="monout
x7.x2.vsin
x7.net2[0]
x7.net2[1]
x7.net2[2]
x7.net2[3]
ack2
x1.x2.vsin"
color="4 6 9 8 10 12 18 10"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=2}
B 2 2452.5 -1727.5 3252.5 -1327.5 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0005
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="vspke
x7.x6.vpulseshort"
color="4 4"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=0
digital=1}
B 2 2452.5 -1302.5 3252.5 -902.5 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0005
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="resetW
x7.x2.vsin
x1.x2.vsin
x7.net2[0]
x7.net2[1]
x7.net2[2]
x7.net2[3]
spk2
ack2
vspki
vspke
setw"
color="5 16 12 4 4 4 4 8 13 7 10 7"
dataset=-1
unitx=1
logx=0
logy=0
digital=1
}
B 2 2460 -870 3260 -470 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0005
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="vspke
x7.x6.vpulseshort"
color="4 7"
dataset=-1
unitx=1
logx=0
logy=0
}
T {Neuron biases} 980 -1465 0 0 0.4 0.4 {}
T {Power up reset} 1615 -1820 0 0 0.4 0.4 {}
T {Excitatory syn} 247.5 -1865 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 1612.5 -2182.5 0 0 0.4 0.4 {}
T {excitatory} 1245 -370 0 0 0.4 0.4 {}
T {inhibitory} 1917.5 -347.5 0 0 0.4 0.4 {}
T {Inhibitory syn} 252.5 -2212.5 0 0 0.4 0.4 {}
T {some small delay
} 1885 -1042.5 0 0 0.4 0.4 {}
T {Simple Neuron (v2) driven by excitatory synapse} 1070 -992.5 0 0 0.4 0.4 {}
N 1605 -1760 1605 -1730 {
lab=vspke}
N 1605 -1670 1605 -1660 {
lab=0}
N 1610 -1495 1610 -1475 {
lab=0}
N 1610 -1585 1610 -1555 {
lab=VDD}
N 1760 -1510 1760 -1490 {
lab=0}
N 1760 -1600 1760 -1570 {
lab=nRes}
N 785 -1320 815 -1320 {
lab=0}
N 810 -1290 810 -1285 {
lab=0}
N 810 -1285 810 -1265 {
lab=0}
N 850 -1320 880 -1320 {
lab=vleakn}
N 810 -1265 810 -1260 {
lab=0}
N 810 -1355 810 -1350 {
lab=vleakn}
N 810 -1360 810 -1355 {
lab=vleakn}
N 810 -1260 810 -1200 {
lab=0}
N 785 -1320 785 -1260 {
lab=0}
N 785 -1260 810 -1260 {
lab=0}
N 810 -1355 865 -1355 {
lab=vleakn}
N 865 -1355 865 -1320 {
lab=vleakn}
N 1015 -1325 1045 -1325 {
lab=VDD}
N 1040 -1295 1040 -1290 {
lab=ifdcp}
N 1040 -1290 1040 -1270 {
lab=ifdcp}
N 1080 -1325 1110 -1325 {
lab=ifdcp}
N 1040 -1420 1040 -1360 {
lab=VDD}
N 1040 -1285 1090 -1285 {
lab=ifdcp}
N 1090 -1325 1090 -1285 {
lab=ifdcp}
N 1040 -1270 1040 -1265 {
lab=ifdcp}
N 1040 -1360 1040 -1355 {
lab=VDD}
N 1245 -1320 1275 -1320 {
lab=0}
N 1270 -1290 1270 -1285 {
lab=0}
N 1270 -1285 1270 -1265 {
lab=0}
N 1310 -1320 1340 -1320 {
lab=vrefn}
N 1270 -1265 1270 -1260 {
lab=0}
N 1270 -1355 1270 -1350 {
lab=vrefn}
N 1270 -1360 1270 -1355 {
lab=vrefn}
N 1270 -1260 1270 -1200 {
lab=0}
N 1245 -1320 1245 -1260 {
lab=0}
N 1245 -1260 1270 -1260 {
lab=0}
N 1270 -1355 1325 -1355 {
lab=vrefn}
N 1325 -1355 1325 -1320 {
lab=vrefn}
N 2035 -815 2085 -815 {
lab=monout}
N 1457.5 -530 1587.5 -530 {
lab=vmem1}
N 1027.5 -510 1157.5 -510 {
lab=vspke}
N 560 -1712.5 590 -1712.5 {
lab=VDD}
N 585 -1682.5 585 -1677.5 {
lab=JExcWn[0]}
N 585 -1677.5 585 -1657.5 {
lab=JExcWn[0]}
N 625 -1712.5 655 -1712.5 {
lab=JExcWn[0]}
N 585 -1807.5 585 -1747.5 {
lab=VDD}
N 585 -1672.5 635 -1672.5 {
lab=JExcWn[0]}
N 635 -1712.5 635 -1672.5 {
lab=JExcWn[0]}
N 585 -1657.5 585 -1652.5 {
lab=JExcWn[0]}
N 585 -1747.5 585 -1742.5 {
lab=VDD}
N 770 -1717.5 800 -1717.5 {
lab=VDD}
N 795 -1687.5 795 -1682.5 {
lab=JExcWn[1]}
N 795 -1682.5 795 -1662.5 {
lab=JExcWn[1]}
N 835 -1717.5 865 -1717.5 {
lab=JExcWn[1]}
N 795 -1812.5 795 -1752.5 {
lab=VDD}
N 795 -1677.5 845 -1677.5 {
lab=JExcWn[1]}
N 845 -1717.5 845 -1677.5 {
lab=JExcWn[1]}
N 795 -1662.5 795 -1657.5 {
lab=JExcWn[1]}
N 795 -1752.5 795 -1747.5 {
lab=VDD}
N 995 -1717.5 1025 -1717.5 {
lab=VDD}
N 1020 -1687.5 1020 -1682.5 {
lab=JExcWn[2]}
N 1020 -1682.5 1020 -1662.5 {
lab=JExcWn[2]}
N 1060 -1717.5 1090 -1717.5 {
lab=JExcWn[2]}
N 1020 -1812.5 1020 -1752.5 {
lab=VDD}
N 1020 -1677.5 1070 -1677.5 {
lab=JExcWn[2]}
N 1070 -1717.5 1070 -1677.5 {
lab=JExcWn[2]}
N 1020 -1662.5 1020 -1657.5 {
lab=JExcWn[2]}
N 1020 -1752.5 1020 -1747.5 {
lab=VDD}
N 1220 -1717.5 1250 -1717.5 {
lab=VDD}
N 1245 -1687.5 1245 -1682.5 {
lab=JExcWn[3]}
N 1245 -1682.5 1245 -1662.5 {
lab=JExcWn[3]}
N 1285 -1717.5 1315 -1717.5 {
lab=JExcWn[3]}
N 1245 -1812.5 1245 -1752.5 {
lab=VDD}
N 1245 -1677.5 1295 -1677.5 {
lab=JExcWn[3]}
N 1295 -1717.5 1295 -1677.5 {
lab=JExcWn[3]}
N 1245 -1662.5 1245 -1657.5 {
lab=JExcWn[3]}
N 1245 -1752.5 1245 -1747.5 {
lab=VDD}
N 115 -1712.5 145 -1712.5 {
lab=VDD}
N 140 -1682.5 140 -1677.5 {
lab=vtaup}
N 140 -1677.5 140 -1657.5 {
lab=vtaup}
N 180 -1712.5 210 -1712.5 {
lab=vtaup}
N 140 -1807.5 140 -1747.5 {
lab=VDD}
N 140 -1672.5 190 -1672.5 {
lab=vtaup}
N 190 -1712.5 190 -1672.5 {
lab=vtaup}
N 140 -1657.5 140 -1652.5 {
lab=vtaup}
N 140 -1747.5 140 -1742.5 {
lab=VDD}
N 325 -1697.5 355 -1697.5 {
lab=0}
N 350 -1667.5 350 -1662.5 {
lab=0}
N 350 -1662.5 350 -1642.5 {
lab=0}
N 390 -1697.5 420 -1697.5 {
lab=vthrdn}
N 350 -1642.5 350 -1637.5 {
lab=0}
N 350 -1732.5 350 -1727.5 {
lab=vthrdn}
N 350 -1737.5 350 -1732.5 {
lab=vthrdn}
N 350 -1637.5 350 -1577.5 {
lab=0}
N 325 -1697.5 325 -1637.5 {
lab=0}
N 325 -1637.5 350 -1637.5 {
lab=0}
N 350 -1732.5 405 -1732.5 {
lab=vthrdn}
N 405 -1732.5 405 -1697.5 {
lab=vthrdn}
N 1575 -2020 1605 -2020 {
lab=VDD}
N 1600 -1990 1600 -1985 {
lab=vpulseextp}
N 1600 -1985 1600 -1965 {
lab=vpulseextp}
N 1640 -2020 1670 -2020 {
lab=vpulseextp}
N 1600 -2115 1600 -2055 {
lab=VDD}
N 1600 -1980 1650 -1980 {
lab=vpulseextp}
N 1650 -2020 1650 -1980 {
lab=vpulseextp}
N 1600 -1965 1600 -1960 {
lab=vpulseextp}
N 1600 -2055 1600 -2050 {
lab=VDD}
N 1840 -2037.5 1870 -2037.5 {
lab=VDD}
N 1865 -2007.5 1865 -2002.5 {
lab=bufmonp}
N 1865 -2002.5 1865 -1982.5 {
lab=bufmonp}
N 1905 -2037.5 1935 -2037.5 {
lab=bufmonp}
N 1865 -2132.5 1865 -2072.5 {
lab=VDD}
N 1865 -1997.5 1915 -1997.5 {
lab=bufmonp}
N 1915 -2037.5 1915 -1997.5 {
lab=bufmonp}
N 1865 -1982.5 1865 -1977.5 {
lab=bufmonp}
N 1865 -2072.5 1865 -2067.5 {
lab=VDD}
N 1755 -1665 1755 -1645 {
lab=0}
N 1755 -1755 1755 -1725 {
lab=setW}
N 2015 -1745 2015 -1715 {
lab=resetW}
N 2130 -520 2260 -520 {
lab=vmem1}
N 115 -2055 145 -2055 {
lab=VDD}
N 140 -2025 140 -2020 {
lab=JInhWp[0]}
N 140 -2020 140 -2000 {
lab=JInhWp[0]}
N 180 -2055 210 -2055 {
lab=JInhWp[0]}
N 140 -2150 140 -2090 {
lab=VDD}
N 140 -2015 190 -2015 {
lab=JInhWp[0]}
N 190 -2055 190 -2015 {
lab=JInhWp[0]}
N 140 -2000 140 -1995 {
lab=JInhWp[0]}
N 140 -2090 140 -2085 {
lab=VDD}
N 325 -2060 355 -2060 {
lab=VDD}
N 350 -2030 350 -2025 {
lab=JInhWp[1]}
N 350 -2025 350 -2005 {
lab=JInhWp[1]}
N 390 -2060 420 -2060 {
lab=JInhWp[1]}
N 350 -2155 350 -2095 {
lab=VDD}
N 350 -2020 400 -2020 {
lab=JInhWp[1]}
N 400 -2060 400 -2020 {
lab=JInhWp[1]}
N 350 -2005 350 -2000 {
lab=JInhWp[1]}
N 350 -2095 350 -2090 {
lab=VDD}
N 550 -2060 580 -2060 {
lab=VDD}
N 575 -2030 575 -2025 {
lab=JInhWp[2]}
N 575 -2025 575 -2005 {
lab=JInhWp[2]}
N 615 -2060 645 -2060 {
lab=JInhWp[2]}
N 575 -2155 575 -2095 {
lab=VDD}
N 575 -2020 625 -2020 {
lab=JInhWp[2]}
N 625 -2060 625 -2020 {
lab=JInhWp[2]}
N 575 -2005 575 -2000 {
lab=JInhWp[2]}
N 575 -2095 575 -2090 {
lab=VDD}
N 775 -2060 805 -2060 {
lab=VDD}
N 800 -2030 800 -2025 {
lab=JInhWp[3]}
N 800 -2025 800 -2005 {
lab=JInhWp[3]}
N 840 -2060 870 -2060 {
lab=JInhWp[3]}
N 800 -2155 800 -2095 {
lab=VDD}
N 800 -2020 850 -2020 {
lab=JInhWp[3]}
N 850 -2060 850 -2020 {
lab=JInhWp[3]}
N 800 -2005 800 -2000 {
lab=JInhWp[3]}
N 800 -2095 800 -2090 {
lab=VDD}
N 1045 -2060 1075 -2060 {
lab=VDD}
N 1070 -2030 1070 -2025 {
lab=vthrdp}
N 1070 -2025 1070 -2005 {
lab=vthrdp}
N 1110 -2060 1140 -2060 {
lab=vthrdp}
N 1070 -2155 1070 -2095 {
lab=VDD}
N 1070 -2020 1120 -2020 {
lab=vthrdp}
N 1120 -2060 1120 -2020 {
lab=vthrdp}
N 1070 -2005 1070 -2000 {
lab=vthrdp}
N 1070 -2095 1070 -2090 {
lab=VDD}
N 1255 -2045 1285 -2045 {
lab=0}
N 1280 -2015 1280 -2010 {
lab=0}
N 1280 -2010 1280 -1990 {
lab=0}
N 1320 -2045 1350 -2045 {
lab=vtaun}
N 1280 -1990 1280 -1985 {
lab=0}
N 1280 -2080 1280 -2075 {
lab=vtaun}
N 1280 -2085 1280 -2080 {
lab=vtaun}
N 1280 -1985 1280 -1925 {
lab=0}
N 1255 -2045 1255 -1985 {
lab=0}
N 1255 -1985 1280 -1985 {
lab=0}
N 1280 -2080 1335 -2080 {
lab=vtaun}
N 1335 -2080 1335 -2045 {
lab=vtaun}
N 2222.5 -1597.5 2222.5 -1567.5 {
lab=vspki}
N 2222.5 -1507.5 2222.5 -1497.5 {
lab=0}
N 1877.5 -942.5 1970 -942.5 {
lab=spk1}
N 150 -965 150 -945 {
lab=0}
N 150 -1055 150 -1025 {
lab=W[1]}
N 250 -965 250 -945 {
lab=0}
N 250 -1055 250 -1025 {
lab=W[0]}
N 440 -955 440 -935 {
lab=0}
N 440 -1045 440 -1015 {
lab=W[2]}
N 550 -955 550 -935 {
lab=0}
N 550 -1045 550 -1015 {
lab=W[3]}
C {devices/vsource.sym} 1605 -1700 0 1 {name=V12 value="pulse(0 1.8 1ns 1ns 1ns 1ns 3us 100)"}
C {devices/lab_pin.sym} 1605 -1760 0 0 {name=p19 sig_type=std_logic lab=vspke}
C {devices/lab_pin.sym} 1605 -1670 0 0 {name=p99 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1610 -1525 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 1610 -1585 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 880 -1320 0 1 {name=p46 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1760 -1600 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 1760 -1540 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 1610 -1475 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1760 -1490 0 0 {name=p98 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 810 -1200 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/isource.sym} 810 -1390 0 0 {name=I3 value=100f}
C {sky130_fd_pr/nfet_01v8.sym} 830 -1320 0 1 {name=M4
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
C {devices/lab_pin.sym} 810 -1420 0 0 {name=p64 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 1060 -1325 0 1 {name=M6
L=1.0
W=2.0
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
C {devices/lab_pin.sym} 1040 -1205 0 0 {name=p63 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1015 -1325 0 0 {name=p67 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1040 -1235 0 0 {name=I5 value=0}
C {devices/lab_pin.sym} 1040 -1420 0 0 {name=p70 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1110 -1325 0 1 {name=p68 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1270 -1200 0 0 {name=p65 sig_type=std_logic lab=0}
C {devices/isource.sym} 1270 -1390 0 0 {name=I4 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 1290 -1320 0 1 {name=M5
L=1
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
C {devices/lab_pin.sym} 1270 -1420 0 0 {name=p66 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1340 -1320 0 1 {name=p41 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 2085 -815 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1735 -795 0 0 {name=p45 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 2035 -795 0 1 {name=p69 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2035 -775 2 0 {name=p71 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1735 -815 0 0 {name=p74 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 150 -1053.75 2 0 {name=p90 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 250 -1055 2 0 {name=p92 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 1035 -510 0 0 {name=p112 sig_type=std_logic lab=vspke}
C {devices/lab_pin.sym} 1587.5 -530 2 0 {name=p79 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 1457.5 -510 2 0 {name=p80 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1457.5 -490 2 0 {name=p81 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1157.5 -410 0 0 {name=p85 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1157.5 -450 0 0 {name=p86 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1157.5 -490 0 0 {name=p87 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1157.5 -470 0 0 {name=p88 sig_type=std_logic lab=vpulseextp
}
C {synapse_4bit_memory_v1.sym} 1307.5 -460 0 0 {name=x7}
C {devices/lab_pin.sym} 1157.5 -530 0 0 {name=p89 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 1157.5 -430 0 0 {name=p101 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1157.5 -390 0 0 {name=p102 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 635 -1685 0 1 {name=p54 sig_type=std_logic lab=JExcWn[0]}
C {sky130_fd_pr/pfet_01v8.sym} 605 -1712.5 0 1 {name=M12
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
C {devices/lab_pin.sym} 585 -1592.5 0 0 {name=p105 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 560 -1712.5 0 0 {name=p106 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 585 -1622.5 0 0 {name=I11 value=1u}
C {devices/lab_pin.sym} 585 -1807.5 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 845 -1690 0 1 {name=p107 sig_type=std_logic lab=JExcWn[1]}
C {sky130_fd_pr/pfet_01v8.sym} 815 -1717.5 0 1 {name=M9
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
C {devices/lab_pin.sym} 795 -1597.5 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 770 -1717.5 0 0 {name=p110 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 795 -1627.5 0 0 {name=I9 value=1u}
C {devices/lab_pin.sym} 795 -1812.5 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1070 -1690 0 1 {name=p118 sig_type=std_logic lab=JExcWn[2]}
C {sky130_fd_pr/pfet_01v8.sym} 1040 -1717.5 0 1 {name=M10
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
C {devices/lab_pin.sym} 1020 -1597.5 0 0 {name=p120 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 995 -1717.5 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1020 -1627.5 0 0 {name=I10 value=1u}
C {devices/lab_pin.sym} 1020 -1812.5 0 0 {name=p123 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1295 -1690 0 1 {name=p124 sig_type=std_logic lab=JExcWn[3]}
C {sky130_fd_pr/pfet_01v8.sym} 1265 -1717.5 0 1 {name=M11
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
C {devices/lab_pin.sym} 1245 -1597.5 0 0 {name=p125 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1220 -1717.5 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1245 -1627.5 0 0 {name=I12 value=1u}
C {devices/lab_pin.sym} 1245 -1812.5 0 0 {name=p127 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 190 -1685 0 1 {name=p129 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 160 -1712.5 0 1 {name=M13
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
C {devices/lab_pin.sym} 140 -1592.5 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 115 -1712.5 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 140 -1622.5 0 0 {name=I14 value=25p}
C {devices/lab_pin.sym} 140 -1807.5 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 405 -1710 0 1 {name=p134 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 350 -1577.5 0 0 {name=p135 sig_type=std_logic lab=0}
C {devices/isource.sym} 350 -1767.5 0 0 {name=I16 value=1u}
C {sky130_fd_pr/nfet_01v8.sym} 370 -1697.5 0 1 {name=M15
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
C {devices/lab_pin.sym} 350 -1797.5 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1930 -2037.5 0 1 {name=p117 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 1620 -2020 0 1 {name=M16
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
C {devices/lab_pin.sym} 1600 -1902.5 0 0 {name=p128 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1575 -2020 0 0 {name=p155 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1600 -1932.5 0 0 {name=I15 value=0.5u}
C {devices/lab_pin.sym} 1600 -2115 0 0 {name=p156 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1670 -2020 2 0 {name=p157 sig_type=std_logic lab=vpulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 1885 -2037.5 0 1 {name=M20
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
C {devices/lab_pin.sym} 1865 -1917.5 0 0 {name=p162 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1840 -2037.5 0 0 {name=p163 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1865 -1947.5 0 0 {name=I20 value=500p}
C {devices/lab_pin.sym} 1865 -2132.5 0 0 {name=p164 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 440 -1045 2 0 {name=p14 sig_type=std_logic lab=W[2]}
C {devices/lab_pin.sym} 550 -1045 2 0 {name=p16 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 1755 -1755 0 0 {name=p7 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 1755 -1695 0 0 {name=V6 value="pulse(0 1.8 35u 1ns 1ns 1ns 10us)"}
C {devices/lab_pin.sym} 2015 -1745 0 0 {name=p22 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 2015 -1685 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 10ms 1)"}
C {devices/lab_pin.sym} 1755 -1645 0 0 {name=p26 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2015 -1655 0 0 {name=p59 sig_type=std_logic lab=0}
C {buffer_mon_p.sym} 1885 -795 0 0 {name=x13}
C {synapse_4bit_memory_inh_v1.sym} 1980 -450 0 0 {name=x1}
C {devices/lab_pin.sym} 2260 -520 2 0 {name=p1 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 2130 -500 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2130 -480 2 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1830 -400 0 0 {name=p9 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1830 -440 0 0 {name=p12 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1830 -480 0 0 {name=p13 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 190 -2027.5 0 1 {name=p17 sig_type=std_logic lab=JInhWp[0]}
C {sky130_fd_pr/pfet_01v8.sym} 160 -2055 0 1 {name=M1
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
C {devices/lab_pin.sym} 140 -1935 0 0 {name=p18 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 115 -2055 0 0 {name=p21 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 140 -1965 0 0 {name=I1 value=500p}
C {devices/lab_pin.sym} 140 -2150 0 0 {name=p20 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 400 -2032.5 0 1 {name=p25 sig_type=std_logic lab=JInhWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 370 -2060 0 1 {name=M2
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
C {devices/lab_pin.sym} 350 -1940 0 0 {name=p27 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 325 -2060 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 350 -1970 0 0 {name=I2 value=500p}
C {devices/lab_pin.sym} 350 -2155 0 0 {name=p28 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 625 -2032.5 0 1 {name=p29 sig_type=std_logic lab=JInhWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 595 -2060 0 1 {name=M3
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
C {devices/lab_pin.sym} 575 -1940 0 0 {name=p30 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 550 -2060 0 0 {name=p31 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 575 -1970 0 0 {name=I6 value=500p}
C {devices/lab_pin.sym} 575 -2155 0 0 {name=p32 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 850 -2032.5 0 1 {name=p33 sig_type=std_logic lab=JInhWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 820 -2060 0 1 {name=M7
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
C {devices/lab_pin.sym} 800 -1940 0 0 {name=p34 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 775 -2060 0 0 {name=p36 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 800 -1970 0 0 {name=I7 value=500p}
C {devices/lab_pin.sym} 800 -2155 0 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1120 -2032.5 0 1 {name=p38 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 1090 -2060 0 1 {name=M17
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
C {devices/lab_pin.sym} 1070 -1940 0 0 {name=p39 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1045 -2060 0 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1070 -1970 0 0 {name=I17 value=1u}
C {devices/lab_pin.sym} 1070 -2155 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1335 -2057.5 0 1 {name=p42 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1280 -1925 0 0 {name=p43 sig_type=std_logic lab=0}
C {devices/isource.sym} 1280 -2115 0 0 {name=I18 value=300p}
C {sky130_fd_pr/nfet_01v8.sym} 1300 -2045 0 1 {name=M18
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
C {devices/lab_pin.sym} 1280 -2145 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1830 -520 0 0 {name=p44 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/vsource.sym} 2222.5 -1537.5 0 1 {name=V1 value="pulse(0 1.8 3ns 1ns 1ns 1ns 100us 100)"}
C {devices/lab_pin.sym} 2222.5 -1597.5 0 0 {name=p47 sig_type=std_logic lab=vspki}
C {devices/lab_pin.sym} 2222.5 -1507.5 0 0 {name=p48 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1830 -500 0 0 {name=p49 sig_type=std_logic lab=vspki}
C {devices/lab_pin.sym} 1830 -460 0 0 {name=p50 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 1830 -420 0 0 {name=p51 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 1830 -380 0 0 {name=p52 sig_type=std_logic lab=vtaun}
C {neuron_analog_fc_v2.sym} 1310 -640 0 0 {name=x5
schematic=neuron_analog_fc_v2_rcx
spice_sym_def="tcleval(.include [abs_sym_path neuron_analog_fc_v2_rcx.spice])"
tclcommand="textwindow [abs_sym_path neuron_analog_fc_v2_rcx.spice]"}
C {devices/lab_pin.sym} 1160 -630 0 0 {name=p152 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1160 -650 0 0 {name=p154 sig_type=std_logic lab=nack_cel1}
C {devices/lab_pin.sym} 1160 -610 0 0 {name=p158 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1160 -670 0 0 {name=p159 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1460 -670 0 1 {name=p160 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1460 -650 2 0 {name=p161 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1460 -630 2 0 {name=p165 sig_type=std_logic lab=nspk_tmp1}
C {devices/lab_pin.sym} 1460 -610 0 1 {name=p166 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 2130 -942.5 2 0 {name=p167 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1777.5 -942.5 0 0 {name=p168 sig_type=std_logic lab=nspk_tmp1}
C {sky130_stdcells/inv_1.sym} 2010 -942.5 0 0 {name=x6 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 2090 -942.5 0 0 {name=x10 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1930 -942.5 3 0 {name=p169 sig_type=std_logic lab=spk1}
C {schmitt_trigger.sym} 1857.5 -942.5 0 0 {name=x14}
C {devices/lab_pin.sym} 1817.5 -902.5 2 0 {name=p170 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1817.5 -982.5 2 0 {name=p171 sig_type=std_logic lab=VDD}
C {c_element_rj.sym} 1315 -882.5 0 0 {name=x15
schematic=c_element_rj_rcx
spice_sym_def="tcleval(.include [abs_sym_path c_element_rj_rcx.spice])"
tclcommand="textwindow [abs_sym_path c_element_rj_rcx.spice]"}
C {devices/lab_pin.sym} 1165 -882.5 0 0 {name=p172 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1165 -862.5 0 0 {name=p173 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1465 -902.5 2 0 {name=p174 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1165 -902.5 0 0 {name=p175 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1465 -882.5 2 0 {name=p176 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1465 -862.5 0 1 {name=p177 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1270 -802.5 0 0 {name=p178 sig_type=std_logic lab=ack_cel1}
C {sky130_stdcells/inv_1.sym} 1310 -802.5 0 0 {name=x16 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1350 -802.5 2 0 {name=p179 sig_type=std_logic lab=nack_cel1}
C {devices/simulator_commands_shown.sym} 120 -465 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value="
.save all
.control
tran 0.1ns 10us
write neuron_analog_fb_tb_rcx.raw
set appendwrite
.endc
"}
C {devices/vsource.sym} 150 -995 0 0 {name=V4 value=0}
C {devices/lab_pin.sym} 150 -945 0 0 {name=p182 sig_type=std_logic lab=0}
C {devices/vsource.sym} 250 -995 0 0 {name=V5 value=0}
C {devices/lab_pin.sym} 250 -945 0 0 {name=p184 sig_type=std_logic lab=0}
C {devices/vsource.sym} 440 -985 0 0 {name=V7 value=1.8}
C {devices/lab_pin.sym} 440 -935 0 0 {name=p187 sig_type=std_logic lab=0}
C {devices/vsource.sym} 550 -985 0 0 {name=V8 value=1.8}
C {devices/lab_pin.sym} 550 -935 0 0 {name=p189 sig_type=std_logic lab=0}
C {devices/simulator_commands_shown.sym} 110 -725 0 0 {name=COMMANDS2
simulator=Xyce
only_toplevel=false 
value="
.TRAN 0.01us 500us
.PRINT TRAN format=raw file=neuron_analog_fb_tb_rcx.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO TR_singleton_filter=1 TR_amd=1
.SAVE
"}
C {sky130_fd_pr/corner.sym} 340 -1390 0 0 {name=CORNER only_toplevel=false corner=tt}
C {devices/code.sym} 120 -1420 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice)"}
C {devices/title.sym} 240 -237.5 0 0 {name=l1 author="Federico Corradi"}
