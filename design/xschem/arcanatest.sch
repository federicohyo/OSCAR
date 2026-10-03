v {xschem version=3.4.7RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1700 -805 2500 -405 {flags=graph
y1=1.7888889
y2=3.7888889
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0.00037101433
x2=0.0013710144
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
P 4 1 -260 -660 {}
T {Neuron driven by excitatory synapse} 940 -845 0 0 0.4 0.4 {}
T {some small delay
} 1340 -535 0 0 0.4 0.4 {}
T {# OPTION LINSOL TYPE=AztecOO PREC_TYPE=IFPACK} 135 -225 0 0 0.4 0.4 {}
T {Neuron biases} 270 -1170 0 0 0.4 0.4 {}
T {Inhibitory syn} 1107.5 -1167.5 0 0 0.4 0.4 {}
T {Excitatory syn} 2005 -1162.5 0 0 0.4 0.4 {}
T {Pulse Extender Syn} 1885 -367.5 0 0 0.4 0.4 {}
N 490 -665 490 -635 {
lab=syn_req}
N 1270 -600 1280 -600 {
lab=0}
N 1270 -620 1280 -620 {
lab=aVDD}
N 1270 -680 1340 -680 {
lab=monout}
N 1270 -580 1340 -580 {
lab=spk1}
N 910 -745 950 -745 {
lab=spk1}
N 890 -765 950 -765 {
lab=ack1}
N 960 -640 970 -640 {
lab=W[0:3]}
N 960 -660 970 -660 {
lab=ifdcp}
N 960 -680 970 -680 {
lab=JExcWp[0:3]}
N 960 -580 970 -580 {
lab=syn_addr[0:3]}
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
N 75 -1025 105 -1025 {
lab=0}
N 100 -995 100 -990 {
lab=0}
N 100 -990 100 -970 {
lab=0}
N 140 -1025 170 -1025 {
lab=vleakn}
N 100 -970 100 -965 {
lab=0}
N 100 -1060 100 -1055 {
lab=vleakn}
N 100 -1065 100 -1060 {
lab=vleakn}
N 100 -965 100 -905 {
lab=0}
N 75 -1025 75 -965 {
lab=0}
N 75 -965 100 -965 {
lab=0}
N 100 -1060 155 -1060 {
lab=vleakn}
N 155 -1060 155 -1025 {
lab=vleakn}
N 305 -1030 335 -1030 {
lab=VDD}
N 330 -1000 330 -995 {
lab=ifdcp}
N 330 -995 330 -975 {
lab=ifdcp}
N 370 -1030 400 -1030 {
lab=ifdcp}
N 330 -1125 330 -1065 {
lab=VDD}
N 330 -990 380 -990 {
lab=ifdcp}
N 380 -1030 380 -990 {
lab=ifdcp}
N 330 -975 330 -970 {
lab=ifdcp}
N 330 -1065 330 -1060 {
lab=VDD}
N 535 -1025 565 -1025 {
lab=0}
N 560 -995 560 -990 {
lab=0}
N 560 -990 560 -970 {
lab=0}
N 600 -1025 630 -1025 {
lab=vrefn}
N 560 -970 560 -965 {
lab=0}
N 560 -1060 560 -1055 {
lab=vrefn}
N 560 -1065 560 -1060 {
lab=vrefn}
N 560 -965 560 -905 {
lab=0}
N 535 -1025 535 -965 {
lab=0}
N 535 -965 560 -965 {
lab=0}
N 560 -1060 615 -1060 {
lab=vrefn}
N 615 -1060 615 -1025 {
lab=vrefn}
N 1775 -1005 1805 -1005 {
lab=0}
N 1800 -975 1800 -970 {
lab=0}
N 1800 -970 1800 -950 {
lab=0}
N 1840 -1005 1870 -1005 {
lab=JExcWp[0]}
N 1800 -950 1800 -945 {
lab=0}
N 1800 -1040 1800 -1035 {
lab=JExcWp[0]}
N 1800 -1045 1800 -1040 {
lab=JExcWp[0]}
N 1800 -945 1800 -885 {
lab=0}
N 1775 -1005 1775 -945 {
lab=0}
N 1775 -945 1800 -945 {
lab=0}
N 1800 -1040 1855 -1040 {
lab=JExcWp[0]}
N 1855 -1040 1855 -1005 {
lab=JExcWp[0]}
N 1980 -1000 2010 -1000 {
lab=0}
N 2005 -970 2005 -965 {
lab=0}
N 2005 -965 2005 -945 {
lab=0}
N 2045 -1000 2075 -1000 {
lab=JExcWp[1]}
N 2005 -945 2005 -940 {
lab=0}
N 2005 -1035 2005 -1030 {
lab=JExcWp[1]}
N 2005 -1040 2005 -1035 {
lab=JExcWp[1]}
N 2005 -940 2005 -880 {
lab=0}
N 1980 -1000 1980 -940 {
lab=0}
N 1980 -940 2005 -940 {
lab=0}
N 2005 -1035 2060 -1035 {
lab=JExcWp[1]}
N 2060 -1035 2060 -1000 {
lab=JExcWp[1]}
N 2180 -995 2210 -995 {
lab=0}
N 2205 -965 2205 -960 {
lab=0}
N 2205 -960 2205 -940 {
lab=0}
N 2245 -995 2275 -995 {
lab=JExcWp[2]}
N 2205 -940 2205 -935 {
lab=0}
N 2205 -1030 2205 -1025 {
lab=JExcWp[2]}
N 2205 -1035 2205 -1030 {
lab=JExcWp[2]}
N 2205 -935 2205 -875 {
lab=0}
N 2180 -995 2180 -935 {
lab=0}
N 2180 -935 2205 -935 {
lab=0}
N 2205 -1030 2260 -1030 {
lab=JExcWp[2]}
N 2260 -1030 2260 -995 {
lab=JExcWp[2]}
N 2380 -990 2410 -990 {
lab=0}
N 2405 -960 2405 -955 {
lab=0}
N 2405 -955 2405 -935 {
lab=0}
N 2445 -990 2475 -990 {
lab=JExcWp[3]}
N 2405 -935 2405 -930 {
lab=0}
N 2405 -1025 2405 -1020 {
lab=JExcWp[3]}
N 2405 -1030 2405 -1025 {
lab=JExcWp[3]}
N 2405 -930 2405 -870 {
lab=0}
N 2380 -990 2380 -930 {
lab=0}
N 2380 -930 2405 -930 {
lab=0}
N 2405 -1025 2460 -1025 {
lab=JExcWp[3]}
N 2460 -1025 2460 -990 {
lab=JExcWp[3]}
N 810 -1010 840 -1010 {
lab=VDD}
N 835 -980 835 -975 {
lab=JInhWn[0]}
N 835 -975 835 -955 {
lab=JInhWn[0]}
N 875 -1010 905 -1010 {
lab=JInhWn[0]}
N 835 -1105 835 -1045 {
lab=VDD}
N 835 -970 885 -970 {
lab=JInhWn[0]}
N 885 -1010 885 -970 {
lab=JInhWn[0]}
N 835 -955 835 -950 {
lab=JInhWn[0]}
N 835 -1045 835 -1040 {
lab=VDD}
N 1020 -1015 1050 -1015 {
lab=VDD}
N 1045 -985 1045 -980 {
lab=JInhWn[1]}
N 1045 -980 1045 -960 {
lab=JInhWn[1]}
N 1085 -1015 1115 -1015 {
lab=JInhWn[1]}
N 1045 -1110 1045 -1050 {
lab=VDD}
N 1045 -975 1095 -975 {
lab=JInhWn[1]}
N 1095 -1015 1095 -975 {
lab=JInhWn[1]}
N 1045 -960 1045 -955 {
lab=JInhWn[1]}
N 1045 -1050 1045 -1045 {
lab=VDD}
N 1225 -1015 1255 -1015 {
lab=VDD}
N 1250 -985 1250 -980 {
lab=JInhWn[2]}
N 1250 -980 1250 -960 {
lab=JInhWn[2]}
N 1290 -1015 1320 -1015 {
lab=JInhWn[2]}
N 1250 -1110 1250 -1050 {
lab=VDD}
N 1250 -975 1300 -975 {
lab=JInhWn[2]}
N 1300 -1015 1300 -975 {
lab=JInhWn[2]}
N 1250 -960 1250 -955 {
lab=JInhWn[2]}
N 1250 -1050 1250 -1045 {
lab=VDD}
N 1430 -1015 1460 -1015 {
lab=VDD}
N 1455 -985 1455 -980 {
lab=JInhWn[3]}
N 1455 -980 1455 -960 {
lab=JInhWn[3]}
N 1495 -1015 1525 -1015 {
lab=JInhWn[3]}
N 1455 -1110 1455 -1050 {
lab=VDD}
N 1455 -975 1505 -975 {
lab=JInhWn[3]}
N 1505 -1015 1505 -975 {
lab=JInhWn[3]}
N 1455 -960 1455 -955 {
lab=JInhWn[3]}
N 1455 -1050 1455 -1045 {
lab=VDD}
N 1740 -1305 1770 -1305 {
lab=VDD}
N 1765 -1275 1765 -1270 {
lab=vtaup}
N 1765 -1270 1765 -1250 {
lab=vtaup}
N 1805 -1305 1835 -1305 {
lab=vtaup}
N 1765 -1400 1765 -1340 {
lab=VDD}
N 1765 -1265 1815 -1265 {
lab=vtaup}
N 1815 -1305 1815 -1265 {
lab=vtaup}
N 1765 -1250 1765 -1245 {
lab=vtaup}
N 1765 -1340 1765 -1335 {
lab=VDD}
N 1950 -1290 1980 -1290 {
lab=0}
N 1975 -1260 1975 -1255 {
lab=0}
N 1975 -1255 1975 -1235 {
lab=0}
N 2015 -1290 2045 -1290 {
lab=vthrdn}
N 1975 -1235 1975 -1230 {
lab=0}
N 1975 -1325 1975 -1320 {
lab=vthrdn}
N 1975 -1330 1975 -1325 {
lab=vthrdn}
N 1975 -1230 1975 -1170 {
lab=0}
N 1950 -1290 1950 -1230 {
lab=0}
N 1950 -1230 1975 -1230 {
lab=0}
N 1975 -1325 2030 -1325 {
lab=vthrdn}
N 2030 -1325 2030 -1290 {
lab=vthrdn}
N 850 -1315 880 -1315 {
lab=VDD}
N 875 -1285 875 -1280 {
lab=vthrdp}
N 875 -1280 875 -1260 {
lab=vthrdp}
N 915 -1315 945 -1315 {
lab=vthrdp}
N 875 -1410 875 -1350 {
lab=VDD}
N 875 -1275 925 -1275 {
lab=vthrdp}
N 925 -1315 925 -1275 {
lab=vthrdp}
N 875 -1260 875 -1255 {
lab=vthrdp}
N 875 -1350 875 -1345 {
lab=VDD}
N 1060 -1300 1090 -1300 {
lab=0}
N 1085 -1270 1085 -1265 {
lab=0}
N 1085 -1265 1085 -1245 {
lab=0}
N 1125 -1300 1155 -1300 {
lab=vtaun}
N 1085 -1245 1085 -1240 {
lab=0}
N 1085 -1335 1085 -1330 {
lab=vtaun}
N 1085 -1340 1085 -1335 {
lab=vtaun}
N 1085 -1240 1085 -1180 {
lab=0}
N 1060 -1300 1060 -1240 {
lab=0}
N 1060 -1240 1085 -1240 {
lab=0}
N 1085 -1335 1140 -1335 {
lab=vtaun}
N 1140 -1335 1140 -1300 {
lab=vtaun}
N 1770 -222.5 1800 -222.5 {
lab=VDD}
N 1795 -192.5 1795 -187.5 {
lab=vepulseextp}
N 1795 -187.5 1795 -167.5 {
lab=vepulseextp}
N 1835 -222.5 1865 -222.5 {
lab=vepulseextp}
N 1795 -317.5 1795 -257.5 {
lab=VDD}
N 1795 -182.5 1845 -182.5 {
lab=vepulseextp}
N 1845 -222.5 1845 -182.5 {
lab=vepulseextp}
N 1795 -167.5 1795 -162.5 {
lab=vepulseextp}
N 1795 -257.5 1795 -252.5 {
lab=VDD}
N 2060 -232.5 2090 -232.5 {
lab=VDD}
N 2085 -202.5 2085 -197.5 {
lab=vipulseextp}
N 2085 -197.5 2085 -177.5 {
lab=vipulseextp}
N 2125 -232.5 2155 -232.5 {
lab=vipulseextp}
N 2085 -327.5 2085 -267.5 {
lab=VDD}
N 2085 -192.5 2135 -192.5 {
lab=vipulseextp}
N 2135 -232.5 2135 -192.5 {
lab=vipulseextp}
N 2085 -177.5 2085 -172.5 {
lab=vipulseextp}
N 2085 -267.5 2085 -262.5 {
lab=VDD}
N 2360 -245 2390 -245 {
lab=VDD}
N 2385 -215 2385 -210 {
lab=bufmonp}
N 2385 -210 2385 -190 {
lab=bufmonp}
N 2425 -245 2455 -245 {
lab=bufmonp}
N 2385 -340 2385 -280 {
lab=VDD}
N 2385 -205 2435 -205 {
lab=bufmonp}
N 2435 -245 2435 -205 {
lab=bufmonp}
N 2385 -190 2385 -185 {
lab=bufmonp}
N 2385 -280 2385 -275 {
lab=VDD}
N 1270 -640 1280 -640 {lab=dVDD}
N 1270 -660 1280 -660 {lab=0}
C {devices/vsource.sym} 585 -615 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 585 -645 0 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/vsource.sym} 490 -605 0 1 {name=V12 value="pulse(0 1.8 1u 1ns 1ns 10ns 1us)"}
C {devices/lab_pin.sym} 490 -665 0 0 {name=p19 sig_type=std_logic lab=syn_req}
C {devices/code.sym} 40 -680 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 165 -675 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 1280 -660 2 0 {name=p3 sig_type=std_logic lab=0}
C {c_element_rj.sym} 1100 -765 0 0 {name=x2}
C {devices/lab_pin.sym} 1250 -785 2 0 {name=p56 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 950 -785 0 0 {name=p85 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 970 -300 0 0 {name=p10 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 960 -320 0 0 {name=p6 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 970 -560 0 0 {name=p7 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 970 -600 0 0 {name=p187 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 960 -640 0 0 {name=p29 sig_type=std_logic lab=W[0:3]}
C {devices/lab_pin.sym} 960 -580 0 0 {name=p61 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 960 -660 0 0 {name=p62 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 960 -500 0 0 {name=p63 sig_type=std_logic lab=resetW}
C {devices/lab_pin.sym} 970 -420 0 0 {name=p64 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 970 -480 0 0 {name=p65 sig_type=std_logic lab=syn_req}
C {devices/lab_pin.sym} 970 -520 0 0 {name=p70 sig_type=std_logic lab=vepulseextp}
C {devices/lab_pin.sym} 970 -540 0 0 {name=p71 sig_type=std_logic lab=vipulseextp}
C {devices/lab_pin.sym} 960 -440 0 0 {name=p73 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 970 -360 0 0 {name=p76 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 1330 -680 1 0 {name=p77 sig_type=std_logic lab=monout}
C {devices/lab_pin.sym} 1500 -450 2 0 {name=p86 sig_type=std_logic lab=ack1}
C {sky130_stdcells/inv_1.sym} 1380 -450 0 0 {name=x16 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1460 -450 0 0 {name=x18 VGND=0 VNB=0 VPB=dVDD VPWR=dVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1340 -450 0 0 {name=p88 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 890 -765 0 0 {name=p79 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 1340 -580 2 0 {name=p78 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 910 -745 0 0 {name=p80 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 1280 -600 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1250 -745 2 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 490 -575 0 0 {name=p94 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1420 -650 0 1 {name=C1 model=cap_mim_m3_1 W=11 L=11 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 1420 -620 0 0 {name=p48 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 585 -585 0 0 {name=p93 sig_type=std_logic lab=0}
C {devices/vsource.sym} 690 -615 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 690 -645 0 0 {name=p57 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 690 -585 0 0 {name=p95 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1280 -620 0 1 {name=p5 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1280 -640 0 1 {name=p109 sig_type=std_logic lab=dVDD}
C {devices/lab_pin.sym} 1250 -765 0 1 {name=p4 sig_type=std_logic lab=dVDD}
C {neuron_32syn_v1.sym} 1120 -490 0 0 {name=x1}
C {devices/lab_pin.sym} 960 -680 0 0 {name=p18 sig_type=std_logic lab=JExcWp[0:3]}
C {devices/lab_pin.sym} 970 -620 2 1 {name=p30 sig_type=std_logic lab=JInhWn[0:3]}
C {devices/title.sym} 240 -160 0 0 {name=l1 author="Stijn van Himste"}
C {devices/vsource.sym} 780 -615 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 780 -645 0 0 {name=p87 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 780 -585 0 0 {name=p92 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 960 -460 0 0 {name=p8 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 970 -400 0 0 {name=p9 sig_type=std_logic lab=vtaup}
C {devices/lab_pin.sym} 970 -380 0 0 {name=p11 sig_type=std_logic lab=vthrdp}
C {devices/lab_pin.sym} 960 -340 0 0 {name=p12 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 885 -987.5 0 1 {name=p13 sig_type=std_logic lab=JInhWn[0]}
C {devices/lab_pin.sym} 1855 -1022.5 0 1 {name=p14 sig_type=std_logic lab=JExcWp[0]}
C {devices/lab_pin.sym} 170 -1025 0 1 {name=p51 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 100 -905 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/isource.sym} 100 -1095 0 0 {name=I8 value=100p}
C {sky130_fd_pr/nfet_01v8.sym} 120 -1025 0 1 {name=M9
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
C {devices/lab_pin.sym} 100 -1125 0 0 {name=p101 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 350 -1030 0 1 {name=M10
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
C {devices/lab_pin.sym} 330 -910 0 0 {name=p89 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 305 -1030 0 0 {name=p90 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 330 -940 0 0 {name=I9 value=500p}
C {devices/lab_pin.sym} 330 -1125 0 0 {name=p104 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 400 -1030 0 1 {name=p105 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 560 -905 0 0 {name=p106 sig_type=std_logic lab=0}
C {devices/isource.sym} 560 -1095 0 0 {name=I10 value=100p}
C {sky130_fd_pr/nfet_01v8.sym} 580 -1025 0 1 {name=M11
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
C {devices/lab_pin.sym} 560 -1125 0 0 {name=p107 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 630 -1025 0 1 {name=p110 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 1800 -885 0 0 {name=p119 sig_type=std_logic lab=0}
C {devices/isource.sym} 1800 -1075 0 0 {name=I13 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 1820 -1005 0 1 {name=M14
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
C {devices/lab_pin.sym} 1800 -1105 0 0 {name=p121 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1095 -982.5 0 1 {name=p41 sig_type=std_logic lab=JInhWn[1]}
C {devices/lab_pin.sym} 2005 -880 0 0 {name=p45 sig_type=std_logic lab=0}
C {devices/isource.sym} 2005 -1070 0 0 {name=I1 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 2025 -1000 0 1 {name=M1
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
C {devices/lab_pin.sym} 2005 -1100 0 0 {name=p46 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1300 -982.5 0 1 {name=p96 sig_type=std_logic lab=JInhWn[2]}
C {devices/lab_pin.sym} 2205 -875 0 0 {name=p98 sig_type=std_logic lab=0}
C {devices/isource.sym} 2205 -1065 0 0 {name=I2 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 2225 -995 0 1 {name=M2
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
C {devices/lab_pin.sym} 2205 -1095 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1505 -987.5 0 1 {name=p17 sig_type=std_logic lab=JInhWn[3]}
C {devices/lab_pin.sym} 2405 -870 0 0 {name=p111 sig_type=std_logic lab=0}
C {devices/isource.sym} 2405 -1060 0 0 {name=I3 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 2425 -990 0 1 {name=M3
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
C {devices/lab_pin.sym} 2405 -1090 0 0 {name=p112 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 855 -1010 0 1 {name=M12
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
C {devices/lab_pin.sym} 835 -890 0 0 {name=p20 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 810 -1010 0 0 {name=p21 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 835 -920 0 0 {name=I11 value=1u}
C {devices/lab_pin.sym} 835 -1105 0 0 {name=p114 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2060 -1027.5 0 1 {name=p26 sig_type=std_logic lab=JExcWp[1]}
C {sky130_fd_pr/pfet_01v8.sym} 1065 -1015 0 1 {name=M4
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
C {devices/lab_pin.sym} 1045 -895 0 0 {name=p113 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1020 -1015 0 0 {name=p115 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1045 -925 0 0 {name=I4 value=1u}
C {devices/lab_pin.sym} 1045 -1110 0 0 {name=p116 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2260 -1022.5 0 1 {name=p117 sig_type=std_logic lab=JExcWp[2]}
C {sky130_fd_pr/pfet_01v8.sym} 1270 -1015 0 1 {name=M5
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
C {devices/lab_pin.sym} 1250 -895 0 0 {name=p118 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1225 -1015 0 0 {name=p120 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1250 -925 0 0 {name=I5 value=1u}
C {devices/lab_pin.sym} 1250 -1110 0 0 {name=p122 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2460 -1012.5 0 1 {name=p123 sig_type=std_logic lab=JExcWp[3]}
C {sky130_fd_pr/pfet_01v8.sym} 1475 -1015 0 1 {name=M6
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
C {devices/lab_pin.sym} 1455 -895 0 0 {name=p124 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1430 -1015 0 0 {name=p125 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1455 -925 0 0 {name=I6 value=1u}
C {devices/lab_pin.sym} 1455 -1110 0 0 {name=p126 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1815 -1277.5 0 1 {name=p33 sig_type=std_logic lab=vtaup}
C {sky130_fd_pr/pfet_01v8.sym} 1785 -1305 0 1 {name=M7
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
C {devices/lab_pin.sym} 1765 -1185 0 0 {name=p44 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1740 -1305 0 0 {name=p47 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1765 -1215 0 0 {name=I7 value=10p}
C {devices/lab_pin.sym} 1765 -1400 0 0 {name=p69 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2030 -1302.5 0 1 {name=p72 sig_type=std_logic lab=vthrdn}
C {devices/lab_pin.sym} 1975 -1170 0 0 {name=p84 sig_type=std_logic lab=0}
C {devices/isource.sym} 1975 -1360 0 0 {name=I16 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 1995 -1290 0 1 {name=M8
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
C {devices/lab_pin.sym} 1975 -1390 0 0 {name=p39 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 925 -1287.5 0 1 {name=p140 sig_type=std_logic lab=vthrdp}
C {sky130_fd_pr/pfet_01v8.sym} 895 -1315 0 1 {name=M17
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
C {devices/lab_pin.sym} 875 -1195 0 0 {name=p141 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 850 -1315 0 0 {name=p142 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 875 -1225 0 0 {name=I17 value=780p}
C {devices/lab_pin.sym} 875 -1410 0 0 {name=p143 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1140 -1312.5 0 1 {name=p144 sig_type=std_logic lab=vtaun}
C {devices/lab_pin.sym} 1085 -1180 0 0 {name=p145 sig_type=std_logic lab=0}
C {devices/isource.sym} 1085 -1370 0 0 {name=I18 value=1p}
C {sky130_fd_pr/nfet_01v8.sym} 1105 -1300 0 1 {name=M18
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
C {devices/lab_pin.sym} 1085 -1400 0 0 {name=p146 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2450 -245 0 1 {name=p42 sig_type=std_logic lab=bufmonp}
C {sky130_fd_pr/pfet_01v8.sym} 1815 -222.5 0 1 {name=M13
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
C {devices/lab_pin.sym} 1795 -105 0 0 {name=p43 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1770 -222.5 0 0 {name=p52 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1795 -135 0 0 {name=I12 value=2u}
C {devices/lab_pin.sym} 1795 -317.5 0 0 {name=p128 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1865 -222.5 2 0 {name=p129 sig_type=std_logic lab=vepulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 2105 -232.5 0 1 {name=M15
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
C {devices/lab_pin.sym} 2085 -115 0 0 {name=p130 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2060 -232.5 0 0 {name=p131 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2085 -145 0 0 {name=I14 value=2u}
C {devices/lab_pin.sym} 2085 -327.5 0 0 {name=p132 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 2155 -232.5 2 0 {name=p133 sig_type=std_logic lab=vipulseextp}
C {sky130_fd_pr/pfet_01v8.sym} 2405 -245 0 1 {name=M16
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
C {devices/lab_pin.sym} 2385 -125 0 0 {name=p134 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 2360 -245 0 0 {name=p135 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 2385 -155 0 0 {name=I15 value=500p}
C {devices/lab_pin.sym} 2385 -340 0 0 {name=p136 sig_type=std_logic lab=VDD}
C {devices/code_shown.sym} 90 -490 0 0 {name=Xyce only_toplevel=false value="
.include arcanatest.cir
.TRAN 0.01us 0.1ms 
.PRINT TRAN format=raw file=arcanatest.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.OPTION LINSOL TYPE=AztecOO TR_singleton_filter=1 TR_amd=1
.SAVE
"}
C {devices/code_shown.sym} -230 -475 0 0 {name=SPICE only_toplevel=false value="
*.include arcanatest.cir
*.save all
*.tran 0.01us 0.1ms
*.write arcanatest.raw
"}
