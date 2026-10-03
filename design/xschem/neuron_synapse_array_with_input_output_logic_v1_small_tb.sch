v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 2412.5 -1402.5 3212.5 -1002.5 {flags=graph
y1=0
y2=1.8
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.00025
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color=13
node=x1.x1.x4[0].x1.x1[3].x2.vsin
hilight_wave=0}
B 2 2412.5 -975 3212.5 -575 {flags=graph
y1=0

ypos1=0.3
ypos2=2.3
divy=5
subdivy=1
unity=1
x1=0
x2=0.00025
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0


digital=1
color="7 8 12 17 7 7 7"
node="W[3]
x1.x1.x4[0].x1.x1[12].net2[1]
x1.x1.x4[0].x1.net2[12]
x1.neu_req[0]
x1.x1.x4[0].reqe
x1.x1.x4[0].x1.D[3]
x1.x1.x4[0].x1.x1[3].spke"
y2=2}
B 2 2407.5 -1817.5 3207.5 -1417.5 {flags=graph
y1=0
y2=1.9
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.00025
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="nres
exc
reqin"
color="4 11 12"
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 2407.5 -560 3207.5 -160 {flags=graph
y1=0
y2=0.2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.00025
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0

color="21 14 18 13"
node="x1.x1.x4[3].net1
x1.x1.x4[2].net1
x1.x1.x4[1].net1
x1.x1.x4[0].net1"}
T {Power up reset} 450 -1135 0 0 0.4 0.4 {}
T {Neuron biases} 325 -1475 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 220 -687.5 0 0 0.4 0.4 {}
T {Excitatory syn} 1130 -1450 0 0 0.4 0.4 {}
T {Inhibitory syn} 1135 -1797.5 0 0 0.4 0.4 {}
T {Output Monitors} 280 -347.5 0 0 0.4 0.4 {}
N 207.5 -1037.5 207.5 -1007.5 {
lab=dVDD}
N 810 -1030 810 -1000 {
lab=REQIN}
N 297.5 -1037.5 297.5 -1007.5 {
lab=aVDD}
N 202.5 -947.5 212.5 -947.5 {
lab=0}
N 1790 -965 1862.5 -965 {
lab=aer_out[0:1]}
N 130 -1330 160 -1330 {
lab=0}
N 155 -1300 155 -1295 {
lab=0}
N 155 -1295 155 -1275 {
lab=0}
N 195 -1330 225 -1330 {
lab=vleakn}
N 155 -1275 155 -1270 {
lab=0}
N 155 -1365 155 -1360 {
lab=vleakn}
N 155 -1370 155 -1365 {
lab=vleakn}
N 155 -1270 155 -1210 {
lab=0}
N 130 -1330 130 -1270 {
lab=0}
N 130 -1270 155 -1270 {
lab=0}
N 155 -1365 210 -1365 {
lab=vleakn}
N 210 -1365 210 -1330 {
lab=vleakn}
N 360 -1335 390 -1335 {
lab=VDD}
N 385 -1305 385 -1300 {
lab=ifdcp}
N 385 -1300 385 -1280 {
lab=ifdcp}
N 425 -1335 455 -1335 {
lab=ifdcp}
N 385 -1430 385 -1370 {
lab=VDD}
N 385 -1295 435 -1295 {
lab=ifdcp}
N 435 -1335 435 -1295 {
lab=ifdcp}
N 385 -1280 385 -1275 {
lab=ifdcp}
N 385 -1370 385 -1365 {
lab=VDD}
N 590 -1330 620 -1330 {
lab=0}
N 615 -1300 615 -1295 {
lab=0}
N 615 -1295 615 -1275 {
lab=0}
N 655 -1330 685 -1330 {
lab=vrefn}
N 615 -1275 615 -1270 {
lab=0}
N 615 -1365 615 -1360 {
lab=vrefn}
N 615 -1370 615 -1365 {
lab=vrefn}
N 615 -1270 615 -1210 {
lab=0}
N 590 -1330 590 -1270 {
lab=0}
N 590 -1270 615 -1270 {
lab=0}
N 615 -1365 670 -1365 {
lab=vrefn}
N 670 -1365 670 -1330 {
lab=vrefn}
N 105 -542.5 135 -542.5 {
lab=VDD}
N 130 -512.5 130 -507.5 {
lab=vepulseextp}
N 130 -507.5 130 -487.5 {
lab=vepulseextp}
N 170 -542.5 200 -542.5 {
lab=vepulseextp}
N 130 -637.5 130 -577.5 {
lab=VDD}
N 130 -502.5 180 -502.5 {
lab=vepulseextp}
N 180 -542.5 180 -502.5 {
lab=vepulseextp}
N 130 -487.5 130 -482.5 {
lab=vepulseextp}
N 130 -577.5 130 -572.5 {
lab=VDD}
N 395 -552.5 425 -552.5 {
lab=VDD}
N 420 -522.5 420 -517.5 {
lab=vipulseextp}
N 420 -517.5 420 -497.5 {
lab=vipulseextp}
N 460 -552.5 490 -552.5 {
lab=vipulseextp}
N 420 -647.5 420 -587.5 {
lab=VDD}
N 420 -512.5 470 -512.5 {
lab=vipulseextp}
N 470 -552.5 470 -512.5 {
lab=vipulseextp}
N 420 -497.5 420 -492.5 {
lab=vipulseextp}
N 420 -587.5 420 -582.5 {
lab=VDD}
N 695 -565 725 -565 {
lab=VDD}
N 720 -535 720 -530 {
lab=bufmonp}
N 720 -530 720 -510 {
lab=bufmonp}
N 760 -565 790 -565 {
lab=bufmonp}
N 720 -660 720 -600 {
lab=VDD}
N 720 -525 770 -525 {
lab=bufmonp}
N 770 -565 770 -525 {
lab=bufmonp}
N 720 -510 720 -505 {
lab=bufmonp}
N 720 -600 720 -595 {
lab=VDD}
N 1442.5 -1297.5 1472.5 -1297.5 {
lab=VDD}
N 1467.5 -1267.5 1467.5 -1262.5 {
lab=JExcWn[0]}
N 1467.5 -1262.5 1467.5 -1242.5 {
lab=JExcWn[0]}
N 1507.5 -1297.5 1537.5 -1297.5 {
lab=JExcWn[0]}
N 1467.5 -1392.5 1467.5 -1332.5 {
lab=VDD}
N 1467.5 -1257.5 1517.5 -1257.5 {
lab=JExcWn[0]}
N 1517.5 -1297.5 1517.5 -1257.5 {
lab=JExcWn[0]}
N 1467.5 -1242.5 1467.5 -1237.5 {
lab=JExcWn[0]}
N 1467.5 -1332.5 1467.5 -1327.5 {
lab=VDD}
N 1652.5 -1302.5 1682.5 -1302.5 {
lab=VDD}
N 1677.5 -1272.5 1677.5 -1267.5 {
lab=JExcWn[1]}
N 1677.5 -1267.5 1677.5 -1247.5 {
lab=JExcWn[1]}
N 1717.5 -1302.5 1747.5 -1302.5 {
lab=JExcWn[1]}
N 1677.5 -1397.5 1677.5 -1337.5 {
lab=VDD}
N 1677.5 -1262.5 1727.5 -1262.5 {
lab=JExcWn[1]}
N 1727.5 -1302.5 1727.5 -1262.5 {
lab=JExcWn[1]}
N 1677.5 -1247.5 1677.5 -1242.5 {
lab=JExcWn[1]}
N 1677.5 -1337.5 1677.5 -1332.5 {
lab=VDD}
N 1877.5 -1302.5 1907.5 -1302.5 {
lab=VDD}
N 1902.5 -1272.5 1902.5 -1267.5 {
lab=JExcWn[2]}
N 1902.5 -1267.5 1902.5 -1247.5 {
lab=JExcWn[2]}
N 1942.5 -1302.5 1972.5 -1302.5 {
lab=JExcWn[2]}
N 1902.5 -1397.5 1902.5 -1337.5 {
lab=VDD}
N 1902.5 -1262.5 1952.5 -1262.5 {
lab=JExcWn[2]}
N 1952.5 -1302.5 1952.5 -1262.5 {
lab=JExcWn[2]}
N 1902.5 -1247.5 1902.5 -1242.5 {
lab=JExcWn[2]}
N 1902.5 -1337.5 1902.5 -1332.5 {
lab=VDD}
N 2102.5 -1302.5 2132.5 -1302.5 {
lab=VDD}
N 2127.5 -1272.5 2127.5 -1267.5 {
lab=JExcWn[3]}
N 2127.5 -1267.5 2127.5 -1247.5 {
lab=JExcWn[3]}
N 2167.5 -1302.5 2197.5 -1302.5 {
lab=JExcWn[3]}
N 2127.5 -1397.5 2127.5 -1337.5 {
lab=VDD}
N 2127.5 -1262.5 2177.5 -1262.5 {
lab=JExcWn[3]}
N 2177.5 -1302.5 2177.5 -1262.5 {
lab=JExcWn[3]}
N 2127.5 -1247.5 2127.5 -1242.5 {
lab=JExcWn[3]}
N 2127.5 -1337.5 2127.5 -1332.5 {
lab=VDD}
N 997.5 -1297.5 1027.5 -1297.5 {
lab=VDD}
N 1022.5 -1267.5 1022.5 -1262.5 {
lab=vtaup}
N 1022.5 -1262.5 1022.5 -1242.5 {
lab=vtaup}
N 1062.5 -1297.5 1092.5 -1297.5 {
lab=vtaup}
N 1022.5 -1392.5 1022.5 -1332.5 {
lab=VDD}
N 1022.5 -1257.5 1072.5 -1257.5 {
lab=vtaup}
N 1072.5 -1297.5 1072.5 -1257.5 {
lab=vtaup}
N 1022.5 -1242.5 1022.5 -1237.5 {
lab=vtaup}
N 1022.5 -1332.5 1022.5 -1327.5 {
lab=VDD}
N 1207.5 -1282.5 1237.5 -1282.5 {
lab=0}
N 1232.5 -1252.5 1232.5 -1247.5 {
lab=0}
N 1232.5 -1247.5 1232.5 -1227.5 {
lab=0}
N 1272.5 -1282.5 1302.5 -1282.5 {
lab=vthrdn}
N 1232.5 -1227.5 1232.5 -1222.5 {
lab=0}
N 1232.5 -1317.5 1232.5 -1312.5 {
lab=vthrdn}
N 1232.5 -1322.5 1232.5 -1317.5 {
lab=vthrdn}
N 1232.5 -1222.5 1232.5 -1162.5 {
lab=0}
N 1207.5 -1282.5 1207.5 -1222.5 {
lab=0}
N 1207.5 -1222.5 1232.5 -1222.5 {
lab=0}
N 1232.5 -1317.5 1287.5 -1317.5 {
lab=vthrdn}
N 1287.5 -1317.5 1287.5 -1282.5 {
lab=vthrdn}
N 997.5 -1640 1027.5 -1640 {
lab=VDD}
N 1022.5 -1610 1022.5 -1605 {
lab=JInhWp[0]}
N 1022.5 -1605 1022.5 -1585 {
lab=JInhWp[0]}
N 1062.5 -1640 1092.5 -1640 {
lab=JInhWp[0]}
N 1022.5 -1735 1022.5 -1675 {
lab=VDD}
N 1022.5 -1600 1072.5 -1600 {
lab=JInhWp[0]}
N 1072.5 -1640 1072.5 -1600 {
lab=JInhWp[0]}
N 1022.5 -1585 1022.5 -1580 {
lab=JInhWp[0]}
N 1022.5 -1675 1022.5 -1670 {
lab=VDD}
N 1207.5 -1645 1237.5 -1645 {
lab=VDD}
N 1232.5 -1615 1232.5 -1610 {
lab=JInhWp[1]}
N 1232.5 -1610 1232.5 -1590 {
lab=JInhWp[1]}
N 1272.5 -1645 1302.5 -1645 {
lab=JInhWp[1]}
N 1232.5 -1740 1232.5 -1680 {
lab=VDD}
N 1232.5 -1605 1282.5 -1605 {
lab=JInhWp[1]}
N 1282.5 -1645 1282.5 -1605 {
lab=JInhWp[1]}
N 1232.5 -1590 1232.5 -1585 {
lab=JInhWp[1]}
N 1232.5 -1680 1232.5 -1675 {
lab=VDD}
N 1432.5 -1645 1462.5 -1645 {
lab=VDD}
N 1457.5 -1615 1457.5 -1610 {
lab=JInhWp[2]}
N 1457.5 -1610 1457.5 -1590 {
lab=JInhWp[2]}
N 1497.5 -1645 1527.5 -1645 {
lab=JInhWp[2]}
N 1457.5 -1740 1457.5 -1680 {
lab=VDD}
N 1457.5 -1605 1507.5 -1605 {
lab=JInhWp[2]}
N 1507.5 -1645 1507.5 -1605 {
lab=JInhWp[2]}
N 1457.5 -1590 1457.5 -1585 {
lab=JInhWp[2]}
N 1457.5 -1680 1457.5 -1675 {
lab=VDD}
N 1657.5 -1645 1687.5 -1645 {
lab=VDD}
N 1682.5 -1615 1682.5 -1610 {
lab=JInhWp[3]}
N 1682.5 -1610 1682.5 -1590 {
lab=JInhWp[3]}
N 1722.5 -1645 1752.5 -1645 {
lab=JInhWp[3]}
N 1682.5 -1740 1682.5 -1680 {
lab=VDD}
N 1682.5 -1605 1732.5 -1605 {
lab=JInhWp[3]}
N 1732.5 -1645 1732.5 -1605 {
lab=JInhWp[3]}
N 1682.5 -1590 1682.5 -1585 {
lab=JInhWp[3]}
N 1682.5 -1680 1682.5 -1675 {
lab=VDD}
N 1927.5 -1645 1957.5 -1645 {
lab=VDD}
N 1952.5 -1615 1952.5 -1610 {
lab=vthrdp}
N 1952.5 -1610 1952.5 -1590 {
lab=vthrdp}
N 1992.5 -1645 2022.5 -1645 {
lab=vthrdp}
N 1952.5 -1740 1952.5 -1680 {
lab=VDD}
N 1952.5 -1605 2002.5 -1605 {
lab=vthrdp}
N 2002.5 -1645 2002.5 -1605 {
lab=vthrdp}
N 1952.5 -1590 1952.5 -1585 {
lab=vthrdp}
N 1952.5 -1680 1952.5 -1675 {
lab=VDD}
N 2137.5 -1630 2167.5 -1630 {
lab=0}
N 2162.5 -1600 2162.5 -1595 {
lab=0}
N 2162.5 -1595 2162.5 -1575 {
lab=0}
N 2202.5 -1630 2232.5 -1630 {
lab=vtaun}
N 2162.5 -1575 2162.5 -1570 {
lab=0}
N 2162.5 -1665 2162.5 -1660 {
lab=vtaun}
N 2162.5 -1670 2162.5 -1665 {
lab=vtaun}
N 2162.5 -1570 2162.5 -1510 {
lab=0}
N 2137.5 -1630 2137.5 -1570 {
lab=0}
N 2137.5 -1570 2162.5 -1570 {
lab=0}
N 2162.5 -1665 2217.5 -1665 {
lab=vtaun}
N 2217.5 -1665 2217.5 -1630 {
lab=vtaun}
N 247.5 -882.5 247.5 -852.5 {
lab=exc}
N 940 -782.5 940 -762.5 {
lab=0}
N 940 -872.5 940 -842.5 {
lab=nRes}
N 377.5 -795 377.5 -775 {
lab=0}
N 377.5 -885 377.5 -855 {
lab=setW}
N 637.5 -865 637.5 -835 {
lab=resetW}
N 290 -200 290 -180 {
lab=0}
N 290 -290 290 -260 {
lab=clk}
N 525 -195 525 -175 {
lab=0}
N 525 -285 525 -255 {
lab=Da}
C {devices/vsource.sym} 207.5 -977.5 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 1790 -905 2 0 {name=p35 sig_type=std_logic lab=dVDD}
C {devices/vsource.sym} 810 -970 0 1 {name=V12 value="pulse(0 1.8 1ns 1ns 1ns 1ns 3us 100)"}
C {devices/lab_pin.sym} 810 -1030 0 0 {name=p19 sig_type=std_logic lab=REQIN}
C {devices/vsource.sym} 297.5 -977.5 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 297.5 -1037.5 0 0 {name=p57 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 810 -940 0 0 {name=p94 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 207.5 -947.5 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 297.5 -947.5 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/code.sym} 170 -1680 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 325 -1665 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 1095 -510 2 0 {name=p22 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 1025 -510 2 0 {name=p23 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 2235 -937.5 2 0 {name=p86 sig_type=std_logic lab=ACK}
C {sky130_stdcells/inv_1.sym} 2115 -937.5 0 0 {name=x16 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 2195 -937.5 0 0 {name=x18 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 2075 -937.5 0 0 {name=p88 sig_type=std_logic lab=REQ}
C {devices/lab_pin.sym} 1790 -985 2 0 {name=p1 sig_type=std_logic lab=REQ}
C {devices/lab_pin.sym} 1790 -945 2 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1790 -925 2 0 {name=p4 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 207.5 -1037.5 0 0 {name=p5 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1490 -1005 2 1 {name=p6 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1490 -985 0 0 {name=p7 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1490 -945 0 0 {name=p15 sig_type=std_logic lab=ACK}
C {devices/lab_pin.sym} 1490 -925 0 0 {name=p17 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1490 -885 0 0 {name=p29 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 1490 -965 0 0 {name=p36 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1575 -360 2 0 {name=p37 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 1490 -360 2 1 {name=p52 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 1565 -490 2 0 {name=p55 sig_type=std_logic lab=syn_addr[2]}
C {devices/lab_pin.sym} 1490 -490 2 1 {name=p60 sig_type=std_logic lab=syn_addr[3]}
C {devices/lab_pin.sym} 1490 -825 0 0 {name=p56 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 1490 -805 0 0 {name=p61 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1490 -785 0 0 {name=p62 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 1490 -765 0 0 {name=p63 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 2127.5 -690 2 1 {name=p65 sig_type=std_logic lab=neu_addr[0]}
C {devices/lab_pin.sym} 2212.5 -687.5 2 0 {name=p74 sig_type=std_logic lab=neu_addr[1]}
C {devices/lab_pin.sym} 1490 -705 0 0 {name=p80 sig_type=std_logic lab=neu_addr[0:1]}
C {devices/lab_pin.sym} 1490 -625 0 0 {name=p85 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 1490 -565 0 0 {name=p97 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1490 -845 0 0 {name=p99 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1490 -725 0 0 {name=p100 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1790 -1005 2 0 {name=p102 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1862.5 -965 2 0 {name=p103 sig_type=std_logic lab=aer_out[0:1]}
C {devices/lab_pin.sym} 1490 -865 0 0 {name=p11 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 1490 -905 0 0 {name=p43 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/vsource.sym} 390 -995 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 390 -1025 0 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 390 -965 0 0 {name=p42 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 225 -1330 0 1 {name=p51 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 155 -1210 0 0 {name=p64 sig_type=std_logic lab=0}
C {devices/isource.sym} 155 -1400 0 0 {name=I8 value=0}
C {sky130_fd_pr/nfet_01v8.sym} 175 -1330 0 1 {name=M9
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
C {devices/lab_pin.sym} 155 -1430 0 0 {name=p101 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 405 -1335 0 1 {name=M10
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
C {devices/lab_pin.sym} 385 -1215 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 360 -1335 0 0 {name=p90 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 385 -1245 0 0 {name=I9 value=500p}
C {devices/lab_pin.sym} 385 -1430 0 0 {name=p104 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 455 -1335 0 1 {name=p105 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 615 -1210 0 0 {name=p106 sig_type=std_logic lab=0}
C {devices/isource.sym} 615 -1400 0 0 {name=I10 value=100p}
C {sky130_fd_pr/nfet_01v8.sym} 635 -1330 0 1 {name=M11
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
C {devices/lab_pin.sym} 615 -1430 0 0 {name=p107 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 685 -1330 0 1 {name=p110 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 785 -565 0 1 {name=p30 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 150 -542.5 0 1 {name=M13
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
C {devices/lab_pin.sym} 130 -425 0 0 {name=p33 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 105 -542.5 0 0 {name=p39 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 130 -455 0 0 {name=I12 value=0.5u}
C {devices/lab_pin.sym} 130 -637.5 0 0 {name=p128 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 200 -542.5 2 0 {name=p129 sig_type=std_logic lab=vepulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 440 -552.5 0 1 {name=M15
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
C {devices/lab_pin.sym} 420 -435 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 395 -552.5 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 420 -465 0 0 {name=I14 value=0.5u}
C {devices/lab_pin.sym} 420 -647.5 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 490 -552.5 2 0 {name=p133 sig_type=std_logic lab=vipulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 740 -565 0 1 {name=M16
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
C {devices/lab_pin.sym} 720 -445 0 0 {name=p134 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 695 -565 0 0 {name=p135 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 720 -475 0 0 {name=I15 value=500p}
C {devices/lab_pin.sym} 720 -660 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1240 -505 2 0 {name=p8 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 1165 -505 2 0 {name=p9 sig_type=std_logic lab=W[2]}
C {devices/simulator_commands_shown.sym} 1320 -120 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 250us
.PRINT TRAN format=raw file=neuron_synapse_array_with_input_output_logic_tb_v1_small.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
C {devices/lab_pin.sym} 1490 -685 0 0 {name=p92 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1490 -605 0 0 {name=p137 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1490 -585 0 0 {name=p138 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1490 -665 0 0 {name=p139 sig_type=std_logic lab=vthrdp}
C {neuron_synapse_array_with_input_output_logic_v1_small.sym} 1640 -785 0 0 {name=x1}
C {devices/title.sym} 215 -45 0 0 {name=l1 author="Federico Corradi"}
C {devices/lab_pin.sym} 1517.5 -1270 0 1 {name=p13 sig_type=std_logic lab=JExcWn[0]}
C {sky130_fd_pr/pfet_01v8.sym} 1487.5 -1297.5 0 1 {name=M12
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
C {devices/lab_pin.sym} 1467.5 -1177.5 0 0 {name=p14 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1442.5 -1297.5 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1467.5 -1207.5 0 0 {name=I11 value=1u}
C {devices/lab_pin.sym} 1467.5 -1392.5 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1727.5 -1275 0 1 {name=p18 sig_type=std_logic lab=JExcWn[1]}
C {sky130_fd_pr/pfet_01v8.sym} 1697.5 -1302.5 0 1 {name=M1
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
C {devices/lab_pin.sym} 1677.5 -1182.5 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1652.5 -1302.5 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1677.5 -1212.5 0 0 {name=I1 value=1.2u}
C {devices/lab_pin.sym} 1677.5 -1397.5 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1952.5 -1275 0 1 {name=p118 sig_type=std_logic lab=JExcWn[2]}
C {sky130_fd_pr/pfet_01v8.sym} 1922.5 -1302.5 0 1 {name=M2
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
C {devices/lab_pin.sym} 1902.5 -1182.5 0 0 {name=p120 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1877.5 -1302.5 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1902.5 -1212.5 0 0 {name=I2 value=1u}
C {devices/lab_pin.sym} 1902.5 -1397.5 0 0 {name=p123 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2177.5 -1275 0 1 {name=p124 sig_type=std_logic lab=JExcWn[3]}
C {sky130_fd_pr/pfet_01v8.sym} 2147.5 -1302.5 0 1 {name=M3
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
C {devices/lab_pin.sym} 2127.5 -1182.5 0 0 {name=p125 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2102.5 -1302.5 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2127.5 -1212.5 0 0 {name=I3 value=1u}
C {devices/lab_pin.sym} 2127.5 -1397.5 0 0 {name=p34 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1072.5 -1270 0 1 {name=p41 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 1042.5 -1297.5 0 1 {name=M4
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
C {devices/lab_pin.sym} 1022.5 -1177.5 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 997.5 -1297.5 0 0 {name=p45 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1022.5 -1207.5 0 0 {name=I4 value=25p}
C {devices/lab_pin.sym} 1022.5 -1392.5 0 0 {name=p46 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1287.5 -1295 0 1 {name=p47 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1232.5 -1162.5 0 0 {name=p69 sig_type=std_logic lab=0}
C {devices/isource.sym} 1232.5 -1352.5 0 0 {name=I16 value=1u}
C {sky130_fd_pr/nfet_01v8.sym} 1252.5 -1282.5 0 1 {name=M5
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
C {devices/lab_pin.sym} 1232.5 -1382.5 0 0 {name=p71 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1072.5 -1612.5 0 1 {name=p72 sig_type=std_logic lab=JInhWp[0]}
C {sky130_fd_pr/pfet_01v8.sym} 1042.5 -1640 0 1 {name=M6
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
C {devices/lab_pin.sym} 1022.5 -1520 0 0 {name=p73 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 997.5 -1640 0 0 {name=p76 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1022.5 -1550 0 0 {name=I5 value=500p}
C {devices/lab_pin.sym} 1022.5 -1735 0 0 {name=p77 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1282.5 -1617.5 0 1 {name=p78 sig_type=std_logic lab=JInhWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 1252.5 -1645 0 1 {name=M7
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
C {devices/lab_pin.sym} 1232.5 -1525 0 0 {name=p79 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1207.5 -1645 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1232.5 -1555 0 0 {name=I6 value=500p}
C {devices/lab_pin.sym} 1232.5 -1740 0 0 {name=p84 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1507.5 -1617.5 0 1 {name=p87 sig_type=std_logic lab=JInhWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 1477.5 -1645 0 1 {name=M8
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
C {devices/lab_pin.sym} 1457.5 -1525 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1432.5 -1645 0 0 {name=p98 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1457.5 -1555 0 0 {name=I7 value=500p}
C {devices/lab_pin.sym} 1457.5 -1740 0 0 {name=p108 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1732.5 -1617.5 0 1 {name=p109 sig_type=std_logic lab=JInhWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 1702.5 -1645 0 1 {name=M14
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
C {devices/lab_pin.sym} 1682.5 -1525 0 0 {name=p111 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1657.5 -1645 0 0 {name=p112 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1682.5 -1555 0 0 {name=I13 value=500p}
C {devices/lab_pin.sym} 1682.5 -1740 0 0 {name=p117 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2002.5 -1617.5 0 1 {name=p119 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 1972.5 -1645 0 1 {name=M17
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
C {devices/lab_pin.sym} 1952.5 -1525 0 0 {name=p121 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1927.5 -1645 0 0 {name=p140 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1952.5 -1555 0 0 {name=I17 value=1u}
C {devices/lab_pin.sym} 1952.5 -1740 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2217.5 -1642.5 0 1 {name=p141 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 2162.5 -1510 0 0 {name=p142 sig_type=std_logic lab=0}
C {devices/isource.sym} 2162.5 -1700 0 0 {name=I18 value=300p}
C {sky130_fd_pr/nfet_01v8.sym} 2182.5 -1630 0 1 {name=M18
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
C {devices/lab_pin.sym} 2162.5 -1730 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 247.5 -822.5 0 1 {name=V25 value="pulse(0 1.8 25ns 1ns 1ns 1.8ms 3.6ms 1)"}
C {devices/lab_pin.sym} 247.5 -882.5 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 247.5 -792.5 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 940 -872.5 0 0 {name=p31 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 940 -812.5 0 0 {name=V3 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 940 -762.5 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 377.5 -885 0 0 {name=p81 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 377.5 -825 0 0 {name=V6 value="pulse(0 1.8 35u 1ns 1ns 1ns 10us)"}
C {devices/lab_pin.sym} 637.5 -865 0 0 {name=p91 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 637.5 -805 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 10ms 1)"}
C {devices/lab_pin.sym} 377.5 -775 0 0 {name=p83 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 637.5 -775 0 0 {name=p127 sig_type=std_logic lab=0}
C {devices/vsource.sym} 290 -230 0 1 {name=V18 value="pulse(0 1.8 10ns 1ns 1ns 5us 10us 30)"}
C {devices/lab_pin.sym} 290 -290 0 0 {name=p144 sig_type=std_logic lab=clk}
C {devices/vsource.sym} 525 -225 0 1 {name=V19 value="pulse(0 1.8 10ns 1ns 1ns 10us 20us)"}
C {devices/lab_pin.sym} 525 -285 0 0 {name=p145 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 1490 -645 0 0 {name=p147 sig_type=std_logic lab=clk}
C {devices/lab_pin.sym} 1490 -745 0 0 {name=p148 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 290 -180 0 0 {name=p149 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 525 -175 0 0 {name=p150 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1240 -475 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 1240 -445 0 0 {name=p12 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1165 -475 0 0 {name=V5 value=1.8}
C {devices/lab_pin.sym} 1165 -445 0 0 {name=p20 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1095 -480 0 0 {name=V7 value=1.8}
C {devices/lab_pin.sym} 1095 -450 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1025 -480 0 0 {name=V8 value=0}
C {devices/lab_pin.sym} 1025 -450 0 0 {name=p27 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1490 -460 0 0 {name=V9 value=1.8}
C {devices/lab_pin.sym} 1490 -430 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1565 -460 0 0 {name=V10 value=0}
C {devices/lab_pin.sym} 1565 -430 0 0 {name=p21 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1490 -330 0 0 {name=V11 value=1.8}
C {devices/lab_pin.sym} 1490 -300 0 0 {name=p25 sig_type=std_logic lab=0}
C {devices/vsource.sym} 1575 -330 0 0 {name=V13 value=0}
C {devices/lab_pin.sym} 1575 -300 0 0 {name=p28 sig_type=std_logic lab=0}
C {devices/vsource.sym} 2212.5 -657.5 0 0 {name=V15 value=0}
C {devices/lab_pin.sym} 2212.5 -627.5 0 0 {name=p38 sig_type=std_logic lab=0}
C {devices/vsource.sym} 2127.5 -660 0 0 {name=V16 value=1.8}
C {devices/lab_pin.sym} 2127.5 -630 0 0 {name=p48 sig_type=std_logic lab=0}
