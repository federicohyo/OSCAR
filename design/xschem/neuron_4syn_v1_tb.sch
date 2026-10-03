v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 2850 -1425 4260 -495 {flags=graph
y1=-2.1e-08
y2=1.8
ypos1=-0.075190172
ypos2=2.7172005
divy=5
subdivy=1
unity=1
x1=0
x2=0.002
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="monout
exc
x1.vmem
syn_req
ack1
spk1
\\"exc[0].vsin; x1.x1.x1[0].x2.vsin\\"
\\"exc[1].vsin; x1.x1.x1[1].x2.vsin\\"
\\"exc[2].vsin; x1.x1.x1[2].x2.vsin\\"
\\"exc[3].vsin; x1.x1.x1[3].x2.vsin\\"

\\"inh[0].vsin; x1.x2.x1[0].x2.vsin\\"
\\"inh[1].vsin; x1.x2.x1[1].x2.vsin\\"
\\"inh[2].vsin; x1.x2.x1[2].x2.vsin\\"
\\"inh[3].vsin; x1.x2.x1[3].x2.vsin\\""
color="5 4 8 6 6 6 4 4 4 4 7 7 7 7"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
B 2 2850 -2160 4250 -1470 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.002
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
T {Power up reset} 357.5 -915 0 0 0.4 0.4 {}
T {Neuron driven by excitatory synapse} 1560 -695 0 0 0.4 0.4 {}
T {some small delay
} 2180 -645 0 0 0.4 0.4 {}
T {Stimuli pulses} 852.5 -1097.5 0 0 0.4 0.4 {}
T {# OPTION LINSOL TYPE=AztecOO PREC_TYPE=IFPACK} 75 -195 0 0 0.4 0.4 {}
T {Neuron biases} 405 -1485 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 2282.5 -475 0 0 0.4 0.4 {}
T {Excitatory syn} 1560 -1120 0 0 0.4 0.4 {}
T {Inhibitory syn} 1565 -1467.5 0 0 0.4 0.4 {}
N 787.5 -1027.5 787.5 -997.5 {
lab=syn_req}
N 1890 -470 1900 -470 {
lab=aVDD}
N 1890 -490 1900 -490 {
lab=dVDD}
N 1890 -530 1960 -530 {
lab=monout}
N 1890 -450 1960 -450 {
lab=spk1}
N 1530 -595 1570 -595 {
lab=spk1}
N 1510 -615 1570 -615 {
lab=ack1}
N 1580 -490 1590 -490 {
lab=JExcWn[0:3]}
N 1580 -510 1590 -510 {
lab=ifdcp}
N 1580 -530 1590 -530 {
lab=JInhWp[0:3]}
N 1580 -430 1590 -430 {
lab=syn_addr[0:1]}
N 1580 -350 1590 -350 {
lab=vthrdp}
N 1580 -310 1590 -310 {
lab=vrefn}
N 1580 -290 1590 -290 {
lab=setW}
N 1580 -190 1590 -190 {
lab=vipulseextp}
N 1580 -170 1590 -170 {
lab=ack_cel1}
N 1960 -530 2040 -530 {
lab=monout}
N 1087.5 -1042.5 1087.5 -1012.5 {
lab=exc}
N 210 -1340 240 -1340 {
lab=0}
N 235 -1310 235 -1305 {
lab=0}
N 235 -1305 235 -1285 {
lab=0}
N 275 -1340 305 -1340 {
lab=vleakn}
N 235 -1285 235 -1280 {
lab=0}
N 235 -1375 235 -1370 {
lab=vleakn}
N 235 -1380 235 -1375 {
lab=vleakn}
N 235 -1280 235 -1220 {
lab=0}
N 210 -1340 210 -1280 {
lab=0}
N 210 -1280 235 -1280 {
lab=0}
N 235 -1375 290 -1375 {
lab=vleakn}
N 290 -1375 290 -1340 {
lab=vleakn}
N 440 -1345 470 -1345 {
lab=VDD}
N 465 -1315 465 -1310 {
lab=ifdcp}
N 465 -1310 465 -1290 {
lab=ifdcp}
N 505 -1345 535 -1345 {
lab=ifdcp}
N 465 -1440 465 -1380 {
lab=VDD}
N 465 -1305 515 -1305 {
lab=ifdcp}
N 515 -1345 515 -1305 {
lab=ifdcp}
N 465 -1290 465 -1285 {
lab=ifdcp}
N 465 -1380 465 -1375 {
lab=VDD}
N 670 -1340 700 -1340 {
lab=0}
N 695 -1310 695 -1305 {
lab=0}
N 695 -1305 695 -1285 {
lab=0}
N 735 -1340 765 -1340 {
lab=vrefn}
N 695 -1285 695 -1280 {
lab=0}
N 695 -1375 695 -1370 {
lab=vrefn}
N 695 -1380 695 -1375 {
lab=vrefn}
N 695 -1280 695 -1220 {
lab=0}
N 670 -1340 670 -1280 {
lab=0}
N 670 -1280 695 -1280 {
lab=0}
N 695 -1375 750 -1375 {
lab=vrefn}
N 750 -1375 750 -1340 {
lab=vrefn}
N 2167.5 -330 2197.5 -330 {
lab=VDD}
N 2192.5 -300 2192.5 -295 {
lab=vepulseextp}
N 2192.5 -295 2192.5 -275 {
lab=vepulseextp}
N 2232.5 -330 2262.5 -330 {
lab=vepulseextp}
N 2192.5 -425 2192.5 -365 {
lab=VDD}
N 2192.5 -290 2242.5 -290 {
lab=vepulseextp}
N 2242.5 -330 2242.5 -290 {
lab=vepulseextp}
N 2192.5 -275 2192.5 -270 {
lab=vepulseextp}
N 2192.5 -365 2192.5 -360 {
lab=VDD}
N 2457.5 -340 2487.5 -340 {
lab=VDD}
N 2482.5 -310 2482.5 -305 {
lab=vipulseextp}
N 2482.5 -305 2482.5 -285 {
lab=vipulseextp}
N 2522.5 -340 2552.5 -340 {
lab=vipulseextp}
N 2482.5 -435 2482.5 -375 {
lab=VDD}
N 2482.5 -300 2532.5 -300 {
lab=vipulseextp}
N 2532.5 -340 2532.5 -300 {
lab=vipulseextp}
N 2482.5 -285 2482.5 -280 {
lab=vipulseextp}
N 2482.5 -375 2482.5 -370 {
lab=VDD}
N 2757.5 -352.5 2787.5 -352.5 {
lab=VDD}
N 2782.5 -322.5 2782.5 -317.5 {
lab=bufmonp}
N 2782.5 -317.5 2782.5 -297.5 {
lab=bufmonp}
N 2822.5 -352.5 2852.5 -352.5 {
lab=bufmonp}
N 2782.5 -447.5 2782.5 -387.5 {
lab=VDD}
N 2782.5 -312.5 2832.5 -312.5 {
lab=bufmonp}
N 2832.5 -352.5 2832.5 -312.5 {
lab=bufmonp}
N 2782.5 -297.5 2782.5 -292.5 {
lab=bufmonp}
N 2782.5 -387.5 2782.5 -382.5 {
lab=VDD}
N 1872.5 -967.5 1902.5 -967.5 {
lab=VDD}
N 1897.5 -937.5 1897.5 -932.5 {
lab=JExcWn[0]}
N 1897.5 -932.5 1897.5 -912.5 {
lab=JExcWn[0]}
N 1937.5 -967.5 1967.5 -967.5 {
lab=JExcWn[0]}
N 1897.5 -1062.5 1897.5 -1002.5 {
lab=VDD}
N 1897.5 -927.5 1947.5 -927.5 {
lab=JExcWn[0]}
N 1947.5 -967.5 1947.5 -927.5 {
lab=JExcWn[0]}
N 1897.5 -912.5 1897.5 -907.5 {
lab=JExcWn[0]}
N 1897.5 -1002.5 1897.5 -997.5 {
lab=VDD}
N 2082.5 -972.5 2112.5 -972.5 {
lab=VDD}
N 2107.5 -942.5 2107.5 -937.5 {
lab=JExcWn[1]}
N 2107.5 -937.5 2107.5 -917.5 {
lab=JExcWn[1]}
N 2147.5 -972.5 2177.5 -972.5 {
lab=JExcWn[1]}
N 2107.5 -1067.5 2107.5 -1007.5 {
lab=VDD}
N 2107.5 -932.5 2157.5 -932.5 {
lab=JExcWn[1]}
N 2157.5 -972.5 2157.5 -932.5 {
lab=JExcWn[1]}
N 2107.5 -917.5 2107.5 -912.5 {
lab=JExcWn[1]}
N 2107.5 -1007.5 2107.5 -1002.5 {
lab=VDD}
N 2307.5 -972.5 2337.5 -972.5 {
lab=VDD}
N 2332.5 -942.5 2332.5 -937.5 {
lab=JExcWn[2]}
N 2332.5 -937.5 2332.5 -917.5 {
lab=JExcWn[2]}
N 2372.5 -972.5 2402.5 -972.5 {
lab=JExcWn[2]}
N 2332.5 -1067.5 2332.5 -1007.5 {
lab=VDD}
N 2332.5 -932.5 2382.5 -932.5 {
lab=JExcWn[2]}
N 2382.5 -972.5 2382.5 -932.5 {
lab=JExcWn[2]}
N 2332.5 -917.5 2332.5 -912.5 {
lab=JExcWn[2]}
N 2332.5 -1007.5 2332.5 -1002.5 {
lab=VDD}
N 2532.5 -972.5 2562.5 -972.5 {
lab=VDD}
N 2557.5 -942.5 2557.5 -937.5 {
lab=JExcWn[3]}
N 2557.5 -937.5 2557.5 -917.5 {
lab=JExcWn[3]}
N 2597.5 -972.5 2627.5 -972.5 {
lab=JExcWn[3]}
N 2557.5 -1067.5 2557.5 -1007.5 {
lab=VDD}
N 2557.5 -932.5 2607.5 -932.5 {
lab=JExcWn[3]}
N 2607.5 -972.5 2607.5 -932.5 {
lab=JExcWn[3]}
N 2557.5 -917.5 2557.5 -912.5 {
lab=JExcWn[3]}
N 2557.5 -1007.5 2557.5 -1002.5 {
lab=VDD}
N 1427.5 -967.5 1457.5 -967.5 {
lab=VDD}
N 1452.5 -937.5 1452.5 -932.5 {
lab=vtaup}
N 1452.5 -932.5 1452.5 -912.5 {
lab=vtaup}
N 1492.5 -967.5 1522.5 -967.5 {
lab=vtaup}
N 1452.5 -1062.5 1452.5 -1002.5 {
lab=VDD}
N 1452.5 -927.5 1502.5 -927.5 {
lab=vtaup}
N 1502.5 -967.5 1502.5 -927.5 {
lab=vtaup}
N 1452.5 -912.5 1452.5 -907.5 {
lab=vtaup}
N 1452.5 -1002.5 1452.5 -997.5 {
lab=VDD}
N 1637.5 -952.5 1667.5 -952.5 {
lab=0}
N 1662.5 -922.5 1662.5 -917.5 {
lab=0}
N 1662.5 -917.5 1662.5 -897.5 {
lab=0}
N 1702.5 -952.5 1732.5 -952.5 {
lab=vthrdn}
N 1662.5 -897.5 1662.5 -892.5 {
lab=0}
N 1662.5 -987.5 1662.5 -982.5 {
lab=vthrdn}
N 1662.5 -992.5 1662.5 -987.5 {
lab=vthrdn}
N 1662.5 -892.5 1662.5 -832.5 {
lab=0}
N 1637.5 -952.5 1637.5 -892.5 {
lab=0}
N 1637.5 -892.5 1662.5 -892.5 {
lab=0}
N 1662.5 -987.5 1717.5 -987.5 {
lab=vthrdn}
N 1717.5 -987.5 1717.5 -952.5 {
lab=vthrdn}
N 1427.5 -1310 1457.5 -1310 {
lab=VDD}
N 1452.5 -1280 1452.5 -1275 {
lab=JInhWp[0]}
N 1452.5 -1275 1452.5 -1255 {
lab=JInhWp[0]}
N 1492.5 -1310 1522.5 -1310 {
lab=JInhWp[0]}
N 1452.5 -1405 1452.5 -1345 {
lab=VDD}
N 1452.5 -1270 1502.5 -1270 {
lab=JInhWp[0]}
N 1502.5 -1310 1502.5 -1270 {
lab=JInhWp[0]}
N 1452.5 -1255 1452.5 -1250 {
lab=JInhWp[0]}
N 1452.5 -1345 1452.5 -1340 {
lab=VDD}
N 1637.5 -1315 1667.5 -1315 {
lab=VDD}
N 1662.5 -1285 1662.5 -1280 {
lab=JInhWp[1]}
N 1662.5 -1280 1662.5 -1260 {
lab=JInhWp[1]}
N 1702.5 -1315 1732.5 -1315 {
lab=JInhWp[1]}
N 1662.5 -1410 1662.5 -1350 {
lab=VDD}
N 1662.5 -1275 1712.5 -1275 {
lab=JInhWp[1]}
N 1712.5 -1315 1712.5 -1275 {
lab=JInhWp[1]}
N 1662.5 -1260 1662.5 -1255 {
lab=JInhWp[1]}
N 1662.5 -1350 1662.5 -1345 {
lab=VDD}
N 1862.5 -1315 1892.5 -1315 {
lab=VDD}
N 1887.5 -1285 1887.5 -1280 {
lab=JInhWp[2]}
N 1887.5 -1280 1887.5 -1260 {
lab=JInhWp[2]}
N 1927.5 -1315 1957.5 -1315 {
lab=JInhWp[2]}
N 1887.5 -1410 1887.5 -1350 {
lab=VDD}
N 1887.5 -1275 1937.5 -1275 {
lab=JInhWp[2]}
N 1937.5 -1315 1937.5 -1275 {
lab=JInhWp[2]}
N 1887.5 -1260 1887.5 -1255 {
lab=JInhWp[2]}
N 1887.5 -1350 1887.5 -1345 {
lab=VDD}
N 2087.5 -1315 2117.5 -1315 {
lab=VDD}
N 2112.5 -1285 2112.5 -1280 {
lab=JInhWp[3]}
N 2112.5 -1280 2112.5 -1260 {
lab=JInhWp[3]}
N 2152.5 -1315 2182.5 -1315 {
lab=JInhWp[3]}
N 2112.5 -1410 2112.5 -1350 {
lab=VDD}
N 2112.5 -1275 2162.5 -1275 {
lab=JInhWp[3]}
N 2162.5 -1315 2162.5 -1275 {
lab=JInhWp[3]}
N 2112.5 -1260 2112.5 -1255 {
lab=JInhWp[3]}
N 2112.5 -1350 2112.5 -1345 {
lab=VDD}
N 2357.5 -1315 2387.5 -1315 {
lab=VDD}
N 2382.5 -1285 2382.5 -1280 {
lab=vthrdp}
N 2382.5 -1280 2382.5 -1260 {
lab=vthrdp}
N 2422.5 -1315 2452.5 -1315 {
lab=vthrdp}
N 2382.5 -1410 2382.5 -1350 {
lab=VDD}
N 2382.5 -1275 2432.5 -1275 {
lab=vthrdp}
N 2432.5 -1315 2432.5 -1275 {
lab=vthrdp}
N 2382.5 -1260 2382.5 -1255 {
lab=vthrdp}
N 2382.5 -1350 2382.5 -1345 {
lab=VDD}
N 2567.5 -1300 2597.5 -1300 {
lab=0}
N 2592.5 -1270 2592.5 -1265 {
lab=0}
N 2592.5 -1265 2592.5 -1245 {
lab=0}
N 2632.5 -1300 2662.5 -1300 {
lab=vtaun}
N 2592.5 -1245 2592.5 -1240 {
lab=0}
N 2592.5 -1335 2592.5 -1330 {
lab=vtaun}
N 2592.5 -1340 2592.5 -1335 {
lab=vtaun}
N 2592.5 -1240 2592.5 -1180 {
lab=0}
N 2567.5 -1300 2567.5 -1240 {
lab=0}
N 2567.5 -1240 2592.5 -1240 {
lab=0}
N 2592.5 -1335 2647.5 -1335 {
lab=vtaun}
N 2647.5 -1335 2647.5 -1300 {
lab=vtaun}
N 190 -822.5 190 -802.5 {
lab=0}
N 190 -912.5 190 -882.5 {
lab=nRes}
N 157.5 -1045 157.5 -1025 {
lab=0}
N 157.5 -1135 157.5 -1105 {
lab=setW}
N 417.5 -1125 417.5 -1095 {
lab=resetW}
C {devices/vsource.sym} 545 -827.5 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 545 -857.5 0 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/vsource.sym} 787.5 -967.5 0 1 {name=V12 value="pulse(0 1.8 1ns 1ns 1ns 1ns 3us)"}
C {devices/lab_pin.sym} 787.5 -1027.5 0 0 {name=p19 sig_type=std_logic lab=syn_req}
C {devices/code.sym} 970 -1390 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 1115 -1385 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 1890 -510 2 0 {name=p3 sig_type=std_logic lab=0}
C {c_element_rj.sym} 1720 -615 0 0 {name=x2}
C {devices/lab_pin.sym} 1870 -635 2 0 {name=p56 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1570 -635 0 0 {name=p85 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1590 -150 0 0 {name=p10 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1580 -170 0 0 {name=p6 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 1590 -410 0 0 {name=p7 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 1590 -470 0 0 {name=p187 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 1195 -365 2 0 {name=p22 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 1195 -435 2 0 {name=p23 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 1195 -395 2 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1195 -325 2 0 {name=p25 sig_type=std_logic lab=0}
C {tie_low.sym} 1045 -345 0 0 {name=x6}
C {tie_hi.sym} 1045 -415 0 0 {name=x7}
C {devices/lab_pin.sym} 1590 -450 0 0 {name=p29 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 1195 -620 2 0 {name=p34 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 1195 -580 2 0 {name=p37 sig_type=std_logic lab=0}
C {tie_low.sym} 1045 -600 0 0 {name=x9}
C {tie_hi.sym} 1045 -520 0 0 {name=x11}
C {devices/lab_pin.sym} 1195 -500 2 0 {name=p58 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1195 -540 2 0 {name=p60 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 1580 -430 0 0 {name=p61 sig_type=std_logic lab=syn_addr[0:1]}
C {devices/lab_pin.sym} 1590 -390 0 0 {name=p63 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 1580 -290 0 0 {name=p64 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1590 -370 0 0 {name=p65 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 1590 -210 0 0 {name=p70 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 1580 -190 0 0 {name=p71 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 1580 -310 0 0 {name=p73 sig_type=std_logic lab=vrefn}
C {devices/vsource.sym} 1087.5 -982.5 0 1 {name=V25 value="pulse(0 1.8 25ns 1ns 1ns 1.8ms 3.6ms 1)"}
C {devices/lab_pin.sym} 1087.5 -1042.5 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1590 -230 0 0 {name=p76 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1950 -530 1 0 {name=p77 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 2360 -560 2 0 {name=p86 sig_type=std_logic lab=ack1}
C {sky130_stdcells/inv_1.sym} 2240 -560 0 0 {name=x16 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 2320 -560 0 0 {name=x18 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 2200 -560 0 0 {name=p88 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1510 -615 0 0 {name=p79 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1960 -450 2 0 {name=p78 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1530 -595 0 0 {name=p80 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1870 -595 2 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 787.5 -937.5 0 0 {name=p94 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1087.5 -952.5 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 545 -797.5 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/vsource.sym} 670 -827.5 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 670 -857.5 0 0 {name=p57 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 670 -797.5 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1195 -345 0 1 {name=p27 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1195 -415 0 1 {name=p28 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1900 -470 0 1 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1195 -600 0 1 {name=p49 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1195 -520 0 1 {name=p59 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1900 -490 0 1 {name=p109 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1870 -615 0 1 {name=p4 sig_type=std_logic lab=dVDD}
C {devices/title.sym} 180 -80 0 0 {name=l1 author="Federico Corradi"}
C {neuron_4syn_v1.sym} 1740 -340 0 0 {name=x1}
C {devices/vsource.sym} 780 -827.5 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 780 -857.5 0 0 {name=p36 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 780 -797.5 0 0 {name=p38 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1590 -250 0 0 {name=p13 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 1590 -270 0 0 {name=p17 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1590 -330 0 0 {name=p18 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1580 -350 0 0 {name=p20 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 1580 -510 0 0 {name=p30 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 305 -1340 0 1 {name=p51 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 235 -1220 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/isource.sym} 235 -1410 0 0 {name=I8 value=0}
C {sky130_fd_pr/nfet_01v8.sym} 255 -1340 0 1 {name=M9
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
C {devices/lab_pin.sym} 235 -1440 0 0 {name=p101 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 485 -1345 0 1 {name=M10
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
C {devices/lab_pin.sym} 465 -1225 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 440 -1345 0 0 {name=p90 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 465 -1255 0 0 {name=I9 value=500p}
C {devices/lab_pin.sym} 465 -1440 0 0 {name=p104 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 535 -1345 0 1 {name=p105 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 695 -1220 0 0 {name=p106 sig_type=std_logic lab=0}
C {devices/isource.sym} 695 -1410 0 0 {name=I10 value=100p}
C {sky130_fd_pr/nfet_01v8.sym} 715 -1340 0 1 {name=M11
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
C {devices/lab_pin.sym} 695 -1440 0 0 {name=p107 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 765 -1340 0 1 {name=p110 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1580 -490 0 0 {name=p12 sig_type=std_logic lab=JExcWn[0:3]}
C {devices/lab_pin.sym} 1582.5 -530 0 0 {name=p40 sig_type=std_logic lab=JInhWp[0:3]}
C {devices/lab_pin.sym} 2847.5 -352.5 0 1 {name=p42 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 2212.5 -330 0 1 {name=M13
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
C {devices/lab_pin.sym} 2192.5 -212.5 0 0 {name=p43 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2167.5 -330 0 0 {name=p52 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2192.5 -242.5 0 0 {name=I12 value=0.5u}
C {devices/lab_pin.sym} 2192.5 -425 0 0 {name=p128 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2262.5 -330 2 0 {name=p129 sig_type=std_logic lab=vepulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 2502.5 -340 0 1 {name=M15
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
C {devices/lab_pin.sym} 2482.5 -222.5 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2457.5 -340 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2482.5 -252.5 0 0 {name=I14 value=0.5u}
C {devices/lab_pin.sym} 2482.5 -435 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2552.5 -340 2 0 {name=p133 sig_type=std_logic lab=vipulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 2802.5 -352.5 0 1 {name=M16
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
C {devices/lab_pin.sym} 2782.5 -232.5 0 0 {name=p134 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2757.5 -352.5 0 0 {name=p135 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2782.5 -262.5 0 0 {name=I15 value=500p}
C {devices/lab_pin.sym} 2782.5 -447.5 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1195 -282.5 2 0 {name=p48 sig_type=std_logic lab=W[2]}
C {devices/lab_pin.sym} 1195 -212.5 2 0 {name=p50 sig_type=std_logic lab=W[3]}
C {devices/lab_pin.sym} 1195 -242.5 2 0 {name=p53 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1195 -172.5 2 0 {name=p54 sig_type=std_logic lab=0}
C {tie_low.sym} 1045 -262.5 0 0 {name=x4}
C {devices/lab_pin.sym} 1195 -192.5 0 1 {name=p55 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1195 -262.5 0 1 {name=p62 sig_type=std_logic lab=aVDD}
C {tie_low.sym} 1045 -192.5 0 0 {name=x3}
C {devices/simulator_commands_shown.sym} 50 -320 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 2ms
.PRINT TRAN format=raw file=neuron_4syn_v1_tb.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO TR_singleton_filter=1 TR_amd=1
.SAVE
"}
C {devices/simulator_commands_shown.sym} 60 -690 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value=".option method=gear
.save x1.x1.x1[0].x2.vsin x1.x1.x1[1].x2.vsin x1.x1.x1[2].x2.vsin x1.x1.x1[3].x2.vsin
.save x1.x2.x1[0].x2.vsin x1.x2.x1[1].x2.vsin x1.x2.x1[2].x2.vsin x1.x2.x1[3].x2.vsin
.save x1.vmem monout exc spk1 ack1 syn_req nRes resetW
.control
  tran 0.01us 2ms
  write neuron_4syn_v1_tb.raw
  quit 0
.endc"}
C {devices/lab_pin.sym} 1947.5 -940 0 1 {name=p8 sig_type=std_logic lab=JExcWn[0]}
C {sky130_fd_pr/pfet_01v8.sym} 1917.5 -967.5 0 1 {name=M12
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
C {devices/lab_pin.sym} 1897.5 -847.5 0 0 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1872.5 -967.5 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1897.5 -877.5 0 0 {name=I11 value=1u}
C {devices/lab_pin.sym} 1897.5 -1062.5 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2157.5 -945 0 1 {name=p14 sig_type=std_logic lab=JExcWn[1]}
C {sky130_fd_pr/pfet_01v8.sym} 2127.5 -972.5 0 1 {name=M1
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
C {devices/lab_pin.sym} 2107.5 -852.5 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2082.5 -972.5 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2107.5 -882.5 0 0 {name=I1 value=1.2u}
C {devices/lab_pin.sym} 2107.5 -1067.5 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2382.5 -945 0 1 {name=p118 sig_type=std_logic lab=JExcWn[2]}
C {sky130_fd_pr/pfet_01v8.sym} 2352.5 -972.5 0 1 {name=M2
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
C {devices/lab_pin.sym} 2332.5 -852.5 0 0 {name=p120 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2307.5 -972.5 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2332.5 -882.5 0 0 {name=I2 value=1u}
C {devices/lab_pin.sym} 2332.5 -1067.5 0 0 {name=p123 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2607.5 -945 0 1 {name=p124 sig_type=std_logic lab=JExcWn[3]}
C {sky130_fd_pr/pfet_01v8.sym} 2577.5 -972.5 0 1 {name=M3
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
C {devices/lab_pin.sym} 2557.5 -852.5 0 0 {name=p125 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2532.5 -972.5 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2557.5 -882.5 0 0 {name=I3 value=1u}
C {devices/lab_pin.sym} 2557.5 -1067.5 0 0 {name=p127 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1502.5 -940 0 1 {name=p21 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 1472.5 -967.5 0 1 {name=M4
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
C {devices/lab_pin.sym} 1452.5 -847.5 0 0 {name=p26 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1427.5 -967.5 0 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1452.5 -877.5 0 0 {name=I4 value=25p}
C {devices/lab_pin.sym} 1452.5 -1062.5 0 0 {name=p39 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1717.5 -965 0 1 {name=p41 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1662.5 -832.5 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/isource.sym} 1662.5 -1022.5 0 0 {name=I16 value=1u}
C {sky130_fd_pr/nfet_01v8.sym} 1682.5 -952.5 0 1 {name=M5
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
C {devices/lab_pin.sym} 1662.5 -1052.5 0 0 {name=p45 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1502.5 -1282.5 0 1 {name=p46 sig_type=std_logic lab=JInhWp[0]}
C {sky130_fd_pr/pfet_01v8.sym} 1472.5 -1310 0 1 {name=M6
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
C {devices/lab_pin.sym} 1452.5 -1190 0 0 {name=p47 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1427.5 -1310 0 0 {name=p66 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1452.5 -1220 0 0 {name=I5 value=500p}
C {devices/lab_pin.sym} 1452.5 -1405 0 0 {name=p67 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1712.5 -1287.5 0 1 {name=p68 sig_type=std_logic lab=JInhWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 1682.5 -1315 0 1 {name=M7
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
C {devices/lab_pin.sym} 1662.5 -1195 0 0 {name=p69 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1637.5 -1315 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1662.5 -1225 0 0 {name=I6 value=500p}
C {devices/lab_pin.sym} 1662.5 -1410 0 0 {name=p72 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1937.5 -1287.5 0 1 {name=p74 sig_type=std_logic lab=JInhWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 1907.5 -1315 0 1 {name=M8
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
C {devices/lab_pin.sym} 1887.5 -1195 0 0 {name=p84 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1862.5 -1315 0 0 {name=p87 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1887.5 -1225 0 0 {name=I7 value=500p}
C {devices/lab_pin.sym} 1887.5 -1410 0 0 {name=p92 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2162.5 -1287.5 0 1 {name=p96 sig_type=std_logic lab=JInhWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 2132.5 -1315 0 1 {name=M14
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
C {devices/lab_pin.sym} 2112.5 -1195 0 0 {name=p97 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2087.5 -1315 0 0 {name=p98 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2112.5 -1225 0 0 {name=I13 value=500p}
C {devices/lab_pin.sym} 2112.5 -1410 0 0 {name=p99 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2432.5 -1287.5 0 1 {name=p100 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 2402.5 -1315 0 1 {name=M17
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
C {devices/lab_pin.sym} 2382.5 -1195 0 0 {name=p102 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2357.5 -1315 0 0 {name=p103 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2382.5 -1225 0 0 {name=I17 value=1u}
C {devices/lab_pin.sym} 2382.5 -1410 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2647.5 -1312.5 0 1 {name=p111 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 2592.5 -1180 0 0 {name=p112 sig_type=std_logic lab=0}
C {devices/isource.sym} 2592.5 -1370 0 0 {name=I18 value=300p}
C {sky130_fd_pr/nfet_01v8.sym} 2612.5 -1300 0 1 {name=M18
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
C {devices/lab_pin.sym} 2592.5 -1400 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 190 -912.5 0 0 {name=p31 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 190 -852.5 0 0 {name=V3 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 190 -802.5 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 157.5 -1135 0 0 {name=p81 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 157.5 -1075 0 0 {name=V6 value="pulse(0 1.8 35u 1ns 1ns 1ns 10us)"}
C {devices/lab_pin.sym} 417.5 -1125 0 0 {name=p91 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 417.5 -1065 0 0 {name=V14 value="pulse(0 1.8 1ns 15ns 1ns 29us 10ms 1)"}
C {devices/lab_pin.sym} 157.5 -1025 0 0 {name=p117 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 417.5 -1035 0 0 {name=p119 sig_type=std_logic lab=0}
