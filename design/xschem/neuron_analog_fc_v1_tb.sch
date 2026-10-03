v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 2520 -1770 3320 -1370 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0001
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
B 2 2522.5 -1337.5 3322.5 -937.5 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0001
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
B 2 2522.5 -912.5 3322.5 -512.5 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.0001
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
T {some small delay
} 1940 -980 0 0 0.4 0.4 {}
T {Simple Neuron (v1) driven by excitatory synapse} 1165 -1027.5 0 0 0.4 0.4 {}
T {Neuron biases} 1070 -1415 0 0 0.4 0.4 {}
T {Power up reset} 1705 -1770 0 0 0.4 0.4 {}
T {Excitatory syn} 337.5 -1815 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 1702.5 -2132.5 0 0 0.4 0.4 {}
T {excitatory} 1335 -320 0 0 0.4 0.4 {}
T {inhibitory} 2007.5 -297.5 0 0 0.4 0.4 {}
T {Inhibitory syn} 342.5 -2162.5 0 0 0.4 0.4 {}
T {excitatory} 1335 -110 0 0 0.4 0.4 {}
T {inhibitory} 2007.5 -87.5 0 0 0.4 0.4 {}
T {some small delay
} 1975 -1152.5 0 0 0.4 0.4 {}
T {Simple Neuron (v2) driven by excitatory synapse} 1790 -1382.5 0 0 0.4 0.4 {}
N 1695 -1710 1695 -1680 {
lab=vspke}
N 1695 -1620 1695 -1610 {
lab=0}
N 1700 -1445 1700 -1425 {
lab=0}
N 1700 -1535 1700 -1505 {
lab=VDD}
N 1850 -1460 1850 -1440 {
lab=0}
N 1850 -1550 1850 -1520 {
lab=nRes}
N 875 -1270 905 -1270 {
lab=0}
N 900 -1240 900 -1235 {
lab=0}
N 900 -1235 900 -1215 {
lab=0}
N 940 -1270 970 -1270 {
lab=vleakn}
N 900 -1215 900 -1210 {
lab=0}
N 900 -1305 900 -1300 {
lab=vleakn}
N 900 -1310 900 -1305 {
lab=vleakn}
N 900 -1210 900 -1150 {
lab=0}
N 875 -1270 875 -1210 {
lab=0}
N 875 -1210 900 -1210 {
lab=0}
N 900 -1305 955 -1305 {
lab=vleakn}
N 955 -1305 955 -1270 {
lab=vleakn}
N 1105 -1275 1135 -1275 {
lab=VDD}
N 1130 -1245 1130 -1240 {
lab=ifdcp}
N 1130 -1240 1130 -1220 {
lab=ifdcp}
N 1170 -1275 1200 -1275 {
lab=ifdcp}
N 1130 -1370 1130 -1310 {
lab=VDD}
N 1130 -1235 1180 -1235 {
lab=ifdcp}
N 1180 -1275 1180 -1235 {
lab=ifdcp}
N 1130 -1220 1130 -1215 {
lab=ifdcp}
N 1130 -1310 1130 -1305 {
lab=VDD}
N 1335 -1270 1365 -1270 {
lab=0}
N 1360 -1240 1360 -1235 {
lab=0}
N 1360 -1235 1360 -1215 {
lab=0}
N 1400 -1270 1430 -1270 {
lab=vrefn}
N 1360 -1215 1360 -1210 {
lab=0}
N 1360 -1305 1360 -1300 {
lab=vrefn}
N 1360 -1310 1360 -1305 {
lab=vrefn}
N 1360 -1210 1360 -1150 {
lab=0}
N 1335 -1270 1335 -1210 {
lab=0}
N 1335 -1210 1360 -1210 {
lab=0}
N 1360 -1305 1415 -1305 {
lab=vrefn}
N 1415 -1305 1415 -1270 {
lab=vrefn}
N 2125 -765 2175 -765 {
lab=monout}
N 1547.5 -480 1677.5 -480 {
lab=vmem2}
N 1117.5 -460 1247.5 -460 {
lab=vspke}
N 650 -1662.5 680 -1662.5 {
lab=VDD}
N 675 -1632.5 675 -1627.5 {
lab=JExcWn[0]}
N 675 -1627.5 675 -1607.5 {
lab=JExcWn[0]}
N 715 -1662.5 745 -1662.5 {
lab=JExcWn[0]}
N 675 -1757.5 675 -1697.5 {
lab=VDD}
N 675 -1622.5 725 -1622.5 {
lab=JExcWn[0]}
N 725 -1662.5 725 -1622.5 {
lab=JExcWn[0]}
N 675 -1607.5 675 -1602.5 {
lab=JExcWn[0]}
N 675 -1697.5 675 -1692.5 {
lab=VDD}
N 860 -1667.5 890 -1667.5 {
lab=VDD}
N 885 -1637.5 885 -1632.5 {
lab=JExcWn[1]}
N 885 -1632.5 885 -1612.5 {
lab=JExcWn[1]}
N 925 -1667.5 955 -1667.5 {
lab=JExcWn[1]}
N 885 -1762.5 885 -1702.5 {
lab=VDD}
N 885 -1627.5 935 -1627.5 {
lab=JExcWn[1]}
N 935 -1667.5 935 -1627.5 {
lab=JExcWn[1]}
N 885 -1612.5 885 -1607.5 {
lab=JExcWn[1]}
N 885 -1702.5 885 -1697.5 {
lab=VDD}
N 1085 -1667.5 1115 -1667.5 {
lab=VDD}
N 1110 -1637.5 1110 -1632.5 {
lab=JExcWn[2]}
N 1110 -1632.5 1110 -1612.5 {
lab=JExcWn[2]}
N 1150 -1667.5 1180 -1667.5 {
lab=JExcWn[2]}
N 1110 -1762.5 1110 -1702.5 {
lab=VDD}
N 1110 -1627.5 1160 -1627.5 {
lab=JExcWn[2]}
N 1160 -1667.5 1160 -1627.5 {
lab=JExcWn[2]}
N 1110 -1612.5 1110 -1607.5 {
lab=JExcWn[2]}
N 1110 -1702.5 1110 -1697.5 {
lab=VDD}
N 1310 -1667.5 1340 -1667.5 {
lab=VDD}
N 1335 -1637.5 1335 -1632.5 {
lab=JExcWn[3]}
N 1335 -1632.5 1335 -1612.5 {
lab=JExcWn[3]}
N 1375 -1667.5 1405 -1667.5 {
lab=JExcWn[3]}
N 1335 -1762.5 1335 -1702.5 {
lab=VDD}
N 1335 -1627.5 1385 -1627.5 {
lab=JExcWn[3]}
N 1385 -1667.5 1385 -1627.5 {
lab=JExcWn[3]}
N 1335 -1612.5 1335 -1607.5 {
lab=JExcWn[3]}
N 1335 -1702.5 1335 -1697.5 {
lab=VDD}
N 205 -1662.5 235 -1662.5 {
lab=VDD}
N 230 -1632.5 230 -1627.5 {
lab=vtaup}
N 230 -1627.5 230 -1607.5 {
lab=vtaup}
N 270 -1662.5 300 -1662.5 {
lab=vtaup}
N 230 -1757.5 230 -1697.5 {
lab=VDD}
N 230 -1622.5 280 -1622.5 {
lab=vtaup}
N 280 -1662.5 280 -1622.5 {
lab=vtaup}
N 230 -1607.5 230 -1602.5 {
lab=vtaup}
N 230 -1697.5 230 -1692.5 {
lab=VDD}
N 415 -1647.5 445 -1647.5 {
lab=0}
N 440 -1617.5 440 -1612.5 {
lab=0}
N 440 -1612.5 440 -1592.5 {
lab=0}
N 480 -1647.5 510 -1647.5 {
lab=vthrdn}
N 440 -1592.5 440 -1587.5 {
lab=0}
N 440 -1682.5 440 -1677.5 {
lab=vthrdn}
N 440 -1687.5 440 -1682.5 {
lab=vthrdn}
N 440 -1587.5 440 -1527.5 {
lab=0}
N 415 -1647.5 415 -1587.5 {
lab=0}
N 415 -1587.5 440 -1587.5 {
lab=0}
N 440 -1682.5 495 -1682.5 {
lab=vthrdn}
N 495 -1682.5 495 -1647.5 {
lab=vthrdn}
N 1665 -1970 1695 -1970 {
lab=VDD}
N 1690 -1940 1690 -1935 {
lab=vpulseextp}
N 1690 -1935 1690 -1915 {
lab=vpulseextp}
N 1730 -1970 1760 -1970 {
lab=vpulseextp}
N 1690 -2065 1690 -2005 {
lab=VDD}
N 1690 -1930 1740 -1930 {
lab=vpulseextp}
N 1740 -1970 1740 -1930 {
lab=vpulseextp}
N 1690 -1915 1690 -1910 {
lab=vpulseextp}
N 1690 -2005 1690 -2000 {
lab=VDD}
N 1930 -1987.5 1960 -1987.5 {
lab=VDD}
N 1955 -1957.5 1955 -1952.5 {
lab=bufmonp}
N 1955 -1952.5 1955 -1932.5 {
lab=bufmonp}
N 1995 -1987.5 2025 -1987.5 {
lab=bufmonp}
N 1955 -2082.5 1955 -2022.5 {
lab=VDD}
N 1955 -1947.5 2005 -1947.5 {
lab=bufmonp}
N 2005 -1987.5 2005 -1947.5 {
lab=bufmonp}
N 1955 -1932.5 1955 -1927.5 {
lab=bufmonp}
N 1955 -2022.5 1955 -2017.5 {
lab=VDD}
N 1845 -1615 1845 -1595 {
lab=0}
N 1845 -1705 1845 -1675 {
lab=setW}
N 2105 -1695 2105 -1665 {
lab=resetW}
N 1932.5 -880 2025 -880 {
lab=spk2}
N 2220 -470 2350 -470 {
lab=vmem2}
N 205 -2005 235 -2005 {
lab=VDD}
N 230 -1975 230 -1970 {
lab=JInhWp[0]}
N 230 -1970 230 -1950 {
lab=JInhWp[0]}
N 270 -2005 300 -2005 {
lab=JInhWp[0]}
N 230 -2100 230 -2040 {
lab=VDD}
N 230 -1965 280 -1965 {
lab=JInhWp[0]}
N 280 -2005 280 -1965 {
lab=JInhWp[0]}
N 230 -1950 230 -1945 {
lab=JInhWp[0]}
N 230 -2040 230 -2035 {
lab=VDD}
N 415 -2010 445 -2010 {
lab=VDD}
N 440 -1980 440 -1975 {
lab=JInhWp[1]}
N 440 -1975 440 -1955 {
lab=JInhWp[1]}
N 480 -2010 510 -2010 {
lab=JInhWp[1]}
N 440 -2105 440 -2045 {
lab=VDD}
N 440 -1970 490 -1970 {
lab=JInhWp[1]}
N 490 -2010 490 -1970 {
lab=JInhWp[1]}
N 440 -1955 440 -1950 {
lab=JInhWp[1]}
N 440 -2045 440 -2040 {
lab=VDD}
N 640 -2010 670 -2010 {
lab=VDD}
N 665 -1980 665 -1975 {
lab=JInhWp[2]}
N 665 -1975 665 -1955 {
lab=JInhWp[2]}
N 705 -2010 735 -2010 {
lab=JInhWp[2]}
N 665 -2105 665 -2045 {
lab=VDD}
N 665 -1970 715 -1970 {
lab=JInhWp[2]}
N 715 -2010 715 -1970 {
lab=JInhWp[2]}
N 665 -1955 665 -1950 {
lab=JInhWp[2]}
N 665 -2045 665 -2040 {
lab=VDD}
N 865 -2010 895 -2010 {
lab=VDD}
N 890 -1980 890 -1975 {
lab=JInhWp[3]}
N 890 -1975 890 -1955 {
lab=JInhWp[3]}
N 930 -2010 960 -2010 {
lab=JInhWp[3]}
N 890 -2105 890 -2045 {
lab=VDD}
N 890 -1970 940 -1970 {
lab=JInhWp[3]}
N 940 -2010 940 -1970 {
lab=JInhWp[3]}
N 890 -1955 890 -1950 {
lab=JInhWp[3]}
N 890 -2045 890 -2040 {
lab=VDD}
N 1135 -2010 1165 -2010 {
lab=VDD}
N 1160 -1980 1160 -1975 {
lab=vthrdp}
N 1160 -1975 1160 -1955 {
lab=vthrdp}
N 1200 -2010 1230 -2010 {
lab=vthrdp}
N 1160 -2105 1160 -2045 {
lab=VDD}
N 1160 -1970 1210 -1970 {
lab=vthrdp}
N 1210 -2010 1210 -1970 {
lab=vthrdp}
N 1160 -1955 1160 -1950 {
lab=vthrdp}
N 1160 -2045 1160 -2040 {
lab=VDD}
N 1345 -1995 1375 -1995 {
lab=0}
N 1370 -1965 1370 -1960 {
lab=0}
N 1370 -1960 1370 -1940 {
lab=0}
N 1410 -1995 1440 -1995 {
lab=vtaun}
N 1370 -1940 1370 -1935 {
lab=0}
N 1370 -2030 1370 -2025 {
lab=vtaun}
N 1370 -2035 1370 -2030 {
lab=vtaun}
N 1370 -1935 1370 -1875 {
lab=0}
N 1345 -1995 1345 -1935 {
lab=0}
N 1345 -1935 1370 -1935 {
lab=0}
N 1370 -2030 1425 -2030 {
lab=vtaun}
N 1425 -2030 1425 -1995 {
lab=vtaun}
N 2312.5 -1547.5 2312.5 -1517.5 {
lab=vspki}
N 2312.5 -1457.5 2312.5 -1447.5 {
lab=0}
N 1547.5 -270 1677.5 -270 {
lab=vmem1}
N 1117.5 -250 1247.5 -250 {
lab=vspke}
N 2220 -260 2350 -260 {
lab=vmem1}
N 1967.5 -1052.5 2060 -1052.5 {
lab=spk1}
N 240 -915 240 -895 {
lab=0}
N 240 -1005 240 -975 {
lab=W[1]}
N 340 -915 340 -895 {
lab=0}
N 340 -1005 340 -975 {
lab=W[0]}
N 530 -905 530 -885 {
lab=0}
N 530 -995 530 -965 {
lab=W[2]}
N 640 -905 640 -885 {
lab=0}
N 640 -995 640 -965 {
lab=W[3]}
C {c_element_rj.sym} 1410 -917.5 0 0 {name=x22}
C {devices/lab_pin.sym} 1260 -917.5 0 0 {name=p140 sig_type=std_logic lab=ack2}
C {devices/lab_pin.sym} 1260 -897.5 0 0 {name=p141 sig_type=std_logic lab=spk2}
C {devices/lab_pin.sym} 1560 -937.5 2 0 {name=p142 sig_type=std_logic lab=ack_cel2}
C {devices/lab_pin.sym} 1260 -937.5 0 0 {name=p144 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1560 -917.5 2 0 {name=p145 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1560 -897.5 0 1 {name=p147 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2185 -880 2 0 {name=p148 sig_type=std_logic lab=ack2}
C {devices/lab_pin.sym} 1832.5 -880 0 0 {name=p149 sig_type=std_logic lab=nspk_tmp2}
C {sky130_stdcells/inv_1.sym} 2065 -880 0 0 {name=x24 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 2145 -880 0 0 {name=x25 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1985 -880 3 0 {name=p150 sig_type=std_logic lab=spk2}
C {devices/lab_pin.sym} 1365 -837.5 0 0 {name=p151 sig_type=std_logic lab=ack_cel2}
C {sky130_stdcells/inv_1.sym} 1405 -837.5 0 0 {name=x26 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1445 -837.5 2 0 {name=p153 sig_type=std_logic lab=nack_cel2}
C {devices/vsource.sym} 1695 -1650 0 1 {name=V12 value="pulse(0 1.8 1ns 1ns 1ns 1ns 3us 100)"}
C {devices/lab_pin.sym} 1695 -1710 0 0 {name=p19 sig_type=std_logic lab=vspke}
C {devices/lab_pin.sym} 1695 -1620 0 0 {name=p99 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1700 -1475 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 1700 -1535 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 970 -1270 0 1 {name=p46 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1850 -1550 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 1850 -1490 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 1700 -1425 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1850 -1440 0 0 {name=p98 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1555 -722.5 0 1 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1555 -702.5 2 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1555 -682.5 2 0 {name=p5 sig_type=std_logic lab=nspk_tmp2}
C {devices/lab_pin.sym} 1255 -682.5 0 0 {name=p11 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1555 -662.5 0 1 {name=p23 sig_type=std_logic lab=vmem2}
C {devices/lab_pin.sym} 1255 -702.5 0 0 {name=p24 sig_type=std_logic lab=nack_cel2}
C {devices/lab_pin.sym} 1255 -662.5 0 0 {name=p8 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1255 -722.5 0 0 {name=p10 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 900 -1150 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/isource.sym} 900 -1340 0 0 {name=I3 value=100f}
C {sky130_fd_pr/nfet_01v8.sym} 920 -1270 0 1 {name=M4
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
C {devices/lab_pin.sym} 900 -1370 0 0 {name=p64 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 1150 -1275 0 1 {name=M6
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
C {devices/lab_pin.sym} 1130 -1155 0 0 {name=p63 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1105 -1275 0 0 {name=p67 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1130 -1185 0 0 {name=I5 value=0}
C {devices/lab_pin.sym} 1130 -1370 0 0 {name=p70 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1200 -1275 0 1 {name=p68 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1360 -1150 0 0 {name=p65 sig_type=std_logic lab=0}
C {devices/isource.sym} 1360 -1340 0 0 {name=I4 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 1380 -1270 0 1 {name=M5
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
C {devices/lab_pin.sym} 1360 -1370 0 0 {name=p66 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1430 -1270 0 1 {name=p41 sig_type=std_logic lab=vrefn}
C {devices/title.sym} 300 -77.5 0 0 {name=l1 author="Federico Corradi"}
C {devices/lab_pin.sym} 2175 -765 2 0 {name=p91 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1825 -745 0 0 {name=p45 sig_type=std_logic lab=vmem2}
C {devices/lab_pin.sym} 2125 -745 0 1 {name=p69 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2125 -725 2 0 {name=p71 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1825 -765 0 0 {name=p74 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 240 -1003.75 2 0 {name=p90 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 340 -1005 2 0 {name=p92 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 1125 -460 0 0 {name=p112 sig_type=std_logic lab=vspke}
C {devices/lab_pin.sym} 1677.5 -480 2 0 {name=p79 sig_type=std_logic lab=vmem2}
C {devices/lab_pin.sym} 1547.5 -460 2 0 {name=p80 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1547.5 -440 2 0 {name=p81 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1247.5 -360 0 0 {name=p85 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1247.5 -400 0 0 {name=p86 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1247.5 -440 0 0 {name=p87 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1247.5 -420 0 0 {name=p88 sig_type=std_logic lab=vpulseextp
}
C {synapse_4bit_memory_v1.sym} 1397.5 -410 0 0 {name=x7}
C {devices/lab_pin.sym} 1247.5 -480 0 0 {name=p89 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 1247.5 -380 0 0 {name=p101 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1247.5 -340 0 0 {name=p102 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 725 -1635 0 1 {name=p54 sig_type=std_logic lab=JExcWn[0]}
C {sky130_fd_pr/pfet_01v8.sym} 695 -1662.5 0 1 {name=M12
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
C {devices/lab_pin.sym} 675 -1542.5 0 0 {name=p105 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 650 -1662.5 0 0 {name=p106 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 675 -1572.5 0 0 {name=I11 value=1u}
C {devices/lab_pin.sym} 675 -1757.5 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 935 -1640 0 1 {name=p107 sig_type=std_logic lab=JExcWn[1]}
C {sky130_fd_pr/pfet_01v8.sym} 905 -1667.5 0 1 {name=M9
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
C {devices/lab_pin.sym} 885 -1547.5 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 860 -1667.5 0 0 {name=p110 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 885 -1577.5 0 0 {name=I9 value=1u}
C {devices/lab_pin.sym} 885 -1762.5 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1160 -1640 0 1 {name=p118 sig_type=std_logic lab=JExcWn[2]}
C {sky130_fd_pr/pfet_01v8.sym} 1130 -1667.5 0 1 {name=M10
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
C {devices/lab_pin.sym} 1110 -1547.5 0 0 {name=p120 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1085 -1667.5 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1110 -1577.5 0 0 {name=I10 value=1u}
C {devices/lab_pin.sym} 1110 -1762.5 0 0 {name=p123 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1385 -1640 0 1 {name=p124 sig_type=std_logic lab=JExcWn[3]}
C {sky130_fd_pr/pfet_01v8.sym} 1355 -1667.5 0 1 {name=M11
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
C {devices/lab_pin.sym} 1335 -1547.5 0 0 {name=p125 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1310 -1667.5 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1335 -1577.5 0 0 {name=I12 value=1u}
C {devices/lab_pin.sym} 1335 -1762.5 0 0 {name=p127 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 280 -1635 0 1 {name=p129 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 250 -1662.5 0 1 {name=M13
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
C {devices/lab_pin.sym} 230 -1542.5 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 205 -1662.5 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 230 -1572.5 0 0 {name=I14 value=25p}
C {devices/lab_pin.sym} 230 -1757.5 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 495 -1660 0 1 {name=p134 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 440 -1527.5 0 0 {name=p135 sig_type=std_logic lab=0}
C {devices/isource.sym} 440 -1717.5 0 0 {name=I16 value=1u}
C {sky130_fd_pr/nfet_01v8.sym} 460 -1647.5 0 1 {name=M15
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
C {devices/lab_pin.sym} 440 -1747.5 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2020 -1987.5 0 1 {name=p117 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 1710 -1970 0 1 {name=M16
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
C {devices/lab_pin.sym} 1690 -1852.5 0 0 {name=p128 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1665 -1970 0 0 {name=p155 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1690 -1882.5 0 0 {name=I15 value=0.5u}
C {devices/lab_pin.sym} 1690 -2065 0 0 {name=p156 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1760 -1970 2 0 {name=p157 sig_type=std_logic lab=vpulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 1975 -1987.5 0 1 {name=M20
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
C {devices/lab_pin.sym} 1955 -1867.5 0 0 {name=p162 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1930 -1987.5 0 0 {name=p163 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1955 -1897.5 0 0 {name=I20 value=500p}
C {devices/lab_pin.sym} 1955 -2082.5 0 0 {name=p164 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 530 -995 2 0 {name=p14 sig_type=std_logic lab=W[2]}
C {devices/lab_pin.sym} 640 -995 2 0 {name=p16 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 1845 -1705 0 0 {name=p7 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 1845 -1645 0 0 {name=V6 value="pulse(0 1.8 35u 1ns 1ns 1ns 10us)"}
C {devices/lab_pin.sym} 2105 -1695 0 0 {name=p22 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 2105 -1635 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 10ms 1)"}
C {devices/lab_pin.sym} 1845 -1595 0 0 {name=p26 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2105 -1605 0 0 {name=p59 sig_type=std_logic lab=0}
C {schmitt_trigger.sym} 1912.5 -880 0 0 {name=x3}
C {devices/lab_pin.sym} 1872.5 -840 2 0 {name=p60 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1872.5 -920 2 0 {name=p78 sig_type=std_logic lab=VDD}
C {buffer_mon_p.sym} 1975 -745 0 0 {name=x13}
C {synapse_4bit_memory_inh_v1.sym} 2070 -400 0 0 {name=x1}
C {devices/lab_pin.sym} 2350 -470 2 0 {name=p1 sig_type=std_logic lab=vmem2}
C {devices/lab_pin.sym} 2220 -450 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2220 -430 2 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1920 -350 0 0 {name=p9 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1920 -390 0 0 {name=p12 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1920 -430 0 0 {name=p13 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 280 -1977.5 0 1 {name=p17 sig_type=std_logic lab=JInhWp[0]}
C {sky130_fd_pr/pfet_01v8.sym} 250 -2005 0 1 {name=M1
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
C {devices/lab_pin.sym} 230 -1885 0 0 {name=p18 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 205 -2005 0 0 {name=p21 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 230 -1915 0 0 {name=I1 value=500p}
C {devices/lab_pin.sym} 230 -2100 0 0 {name=p20 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 490 -1982.5 0 1 {name=p25 sig_type=std_logic lab=JInhWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 460 -2010 0 1 {name=M2
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
C {devices/lab_pin.sym} 440 -1890 0 0 {name=p27 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 415 -2010 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 440 -1920 0 0 {name=I2 value=500p}
C {devices/lab_pin.sym} 440 -2105 0 0 {name=p28 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 715 -1982.5 0 1 {name=p29 sig_type=std_logic lab=JInhWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 685 -2010 0 1 {name=M3
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
C {devices/lab_pin.sym} 665 -1890 0 0 {name=p30 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 640 -2010 0 0 {name=p31 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 665 -1920 0 0 {name=I6 value=500p}
C {devices/lab_pin.sym} 665 -2105 0 0 {name=p32 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 940 -1982.5 0 1 {name=p33 sig_type=std_logic lab=JInhWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 910 -2010 0 1 {name=M7
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
C {devices/lab_pin.sym} 890 -1890 0 0 {name=p34 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 865 -2010 0 0 {name=p36 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 890 -1920 0 0 {name=I7 value=500p}
C {devices/lab_pin.sym} 890 -2105 0 0 {name=p37 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1210 -1982.5 0 1 {name=p38 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 1180 -2010 0 1 {name=M17
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
C {devices/lab_pin.sym} 1160 -1890 0 0 {name=p39 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1135 -2010 0 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1160 -1920 0 0 {name=I17 value=1u}
C {devices/lab_pin.sym} 1160 -2105 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1425 -2007.5 0 1 {name=p42 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1370 -1875 0 0 {name=p43 sig_type=std_logic lab=0}
C {devices/isource.sym} 1370 -2065 0 0 {name=I18 value=300p}
C {sky130_fd_pr/nfet_01v8.sym} 1390 -1995 0 1 {name=M18
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
C {devices/lab_pin.sym} 1370 -2095 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1920 -470 0 0 {name=p44 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/vsource.sym} 2312.5 -1487.5 0 1 {name=V1 value="pulse(0 1.8 3ns 1ns 1ns 1ns 100us 100)"}
C {devices/lab_pin.sym} 2312.5 -1547.5 0 0 {name=p47 sig_type=std_logic lab=vspki}
C {devices/lab_pin.sym} 2312.5 -1457.5 0 0 {name=p48 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1920 -450 0 0 {name=p49 sig_type=std_logic lab=vspki}
C {devices/lab_pin.sym} 1920 -410 0 0 {name=p50 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 1920 -370 0 0 {name=p51 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 1920 -330 0 0 {name=p52 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1125 -250 0 0 {name=p53 sig_type=std_logic lab=vspke}
C {devices/lab_pin.sym} 1677.5 -270 2 0 {name=p61 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 1547.5 -250 2 0 {name=p62 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1547.5 -230 2 0 {name=p72 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1247.5 -150 0 0 {name=p73 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1247.5 -190 0 0 {name=p75 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1247.5 -230 0 0 {name=p76 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1247.5 -210 0 0 {name=p77 sig_type=std_logic lab=vpulseextp
}
C {synapse_4bit_memory_v1.sym} 1397.5 -200 0 0 {name=x2}
C {devices/lab_pin.sym} 1247.5 -270 0 0 {name=p82 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 1247.5 -170 0 0 {name=p84 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1247.5 -130 0 0 {name=p97 sig_type=std_logic lab=vtaup}
C {synapse_4bit_memory_inh_v1.sym} 2070 -190 0 0 {name=x4}
C {devices/lab_pin.sym} 2350 -260 2 0 {name=p103 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 2220 -240 2 0 {name=p104 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2220 -220 2 0 {name=p108 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1920 -140 0 0 {name=p109 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1920 -180 0 0 {name=p111 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1920 -220 0 0 {name=p119 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1920 -260 0 0 {name=p121 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 1920 -240 0 0 {name=p133 sig_type=std_logic lab=vspki}
C {devices/lab_pin.sym} 1920 -200 0 0 {name=p137 sig_type=std_logic lab=vpulseextp
}
C {devices/lab_pin.sym} 1920 -160 0 0 {name=p138 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 1920 -120 0 0 {name=p139 sig_type=std_logic lab=vtaun}
C {neuron_analog_fc_v2.sym} 1400 -590 0 0 {name=x5}
C {devices/lab_pin.sym} 1250 -580 0 0 {name=p152 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1250 -600 0 0 {name=p154 sig_type=std_logic lab=nack_cel1}
C {devices/lab_pin.sym} 1250 -560 0 0 {name=p158 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1250 -620 0 0 {name=p159 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1550 -620 0 1 {name=p160 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1550 -600 2 0 {name=p161 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1550 -580 2 0 {name=p165 sig_type=std_logic lab=nspk_tmp1}
C {devices/lab_pin.sym} 1550 -560 0 1 {name=p166 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 2220 -1052.5 2 0 {name=p167 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1867.5 -1052.5 0 0 {name=p168 sig_type=std_logic lab=nspk_tmp1}
C {sky130_stdcells/inv_1.sym} 2100 -1052.5 0 0 {name=x6 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 2180 -1052.5 0 0 {name=x10 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 2020 -1052.5 3 0 {name=p169 sig_type=std_logic lab=spk1}
C {schmitt_trigger.sym} 1947.5 -1052.5 0 0 {name=x14}
C {devices/lab_pin.sym} 1907.5 -1012.5 2 0 {name=p170 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1907.5 -1092.5 2 0 {name=p171 sig_type=std_logic lab=VDD}
C {c_element_rj.sym} 2035 -1272.5 0 0 {name=x15}
C {devices/lab_pin.sym} 1885 -1272.5 0 0 {name=p172 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1885 -1252.5 0 0 {name=p173 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 2185 -1292.5 2 0 {name=p174 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1885 -1292.5 0 0 {name=p175 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 2185 -1272.5 2 0 {name=p176 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2185 -1252.5 0 1 {name=p177 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1990 -1192.5 0 0 {name=p178 sig_type=std_logic lab=ack_cel1}
C {sky130_stdcells/inv_1.sym} 2030 -1192.5 0 0 {name=x16 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 2070 -1192.5 2 0 {name=p179 sig_type=std_logic lab=nack_cel1}
C {devices/simulator_commands_shown.sym} 210 -415 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value="
.save all
.control
tran 0.1ns 10us
write neuron_analog_fb_tb_v1.raw
set appendwrite
.endc
"}
C {devices/vsource.sym} 240 -945 0 0 {name=V4 value=0}
C {devices/lab_pin.sym} 240 -895 0 0 {name=p182 sig_type=std_logic lab=0}
C {devices/vsource.sym} 340 -945 0 0 {name=V5 value=0}
C {devices/lab_pin.sym} 340 -895 0 0 {name=p184 sig_type=std_logic lab=0}
C {devices/vsource.sym} 530 -935 0 0 {name=V7 value=1.8}
C {devices/lab_pin.sym} 530 -885 0 0 {name=p187 sig_type=std_logic lab=0}
C {devices/vsource.sym} 640 -935 0 0 {name=V8 value=1.8}
C {devices/lab_pin.sym} 640 -885 0 0 {name=p189 sig_type=std_logic lab=0}
C {devices/simulator_commands_shown.sym} 200 -675 0 0 {name=COMMANDS2
simulator=Xyce
only_toplevel=false 
value="
.TRAN 0.01us 500us
.PRINT TRAN format=raw file=neuron_analog_fb_tb_v1.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO TR_singleton_filter=1 TR_amd=1
.SAVE
"}
C {sky130_fd_pr/corner.sym} 430 -1340 0 0 {name=CORNER only_toplevel=false corner=tt}
C {devices/code.sym} 210 -1370 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice)"}
C {neuron_analog_fc_v2.sym} 1405 -692.5 0 0 {name=x8}
