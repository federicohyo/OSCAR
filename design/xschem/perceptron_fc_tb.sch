v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1850 -1430 2650 -1030 {flags=graph
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
node="\\"x1.d;x1.d[7],x1.d[6],x1.d[5],x1.d[4],x1.d[3],x1.d[2],x1.d[1],x1.d[0]\\"
win
sdone
clk
nres"
color="5 4 4 4 6"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
B 2 1850 -990 2650 -590 {flags=graph
y1=-0.013
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
node="spk_in[1]
spk_in[0]
req_out
x1.sinp0"
color="4 5 6 7"
dataset=-1
unitx=1
logx=0
logy=0
}
T {Neuron biases} 20 -780 0 0 0.4 0.4 {}
T {Excitatory syn} 360 -1240 0 0 0.4 0.4 {}
T {Power up reset} 120 -1010 0 0 0.4 0.4 {}
T {Enable} 620 -1020 0 0 0.4 0.4 {}
N 170 -640 170 -620 {
lab=GND}
N 170 -730 170 -700 {
lab=ifrefn}
N 90 -640 90 -620 {
lab=GND}
N 90 -730 90 -700 {
lab=ifleakn}
N 370 -630 370 -610 {
lab=GND}
N 370 -720 370 -690 {
lab=ifahwp}
N 290 -630 290 -610 {
lab=GND}
N 290 -720 290 -690 {
lab=ifnmdap}
N 480 -630 480 -610 {
lab=GND}
N 480 -720 480 -690 {
lab=ifdcp}
N 600 -630 600 -610 {
lab=GND}
N 600 -720 600 -690 {
lab=ifahthrp}
N 720 -630 720 -610 {
lab=GND}
N 720 -720 720 -690 {
lab=ifthrp}
N 840 -630 840 -610 {
lab=GND}
N 840 -720 840 -690 {
lab=ifcascn}
N 970 -630 970 -610 {
lab=GND}
N 970 -720 970 -690 {
lab=ifahtaun}
N 510 -860 510 -840 {
lab=GND}
N 510 -950 510 -920 {
lab=VDD}
N 395 -1080 395 -1060 {
lab=GND}
N 395 -1170 395 -1140 {
lab=vtaudpip}
N 495 -1080 495 -1060 {
lab=GND}
N 495 -1170 495 -1140 {
lab=vthrdpin}
N 600 -1090 600 -1070 {
lab=GND}
N 600 -1180 600 -1150 {
lab=vstddpin}
N 210 -1090 210 -1070 {
lab=GND}
N 210 -1180 210 -1150 {
lab=Spk_in[0]}
N 410 -960 410 -930 {
lab=GND}
N 410 -930 410 -860 {
lab=GND}
N 600 -860 600 -840 {
lab=GND}
N 600 -950 600 -920 {
lab=aVDD}
N 160 -870 160 -850 {
lab=GND}
N 160 -960 160 -930 {
lab=nRes}
N 690 -880 690 -860 {
lab=GND}
N 690 -970 690 -940 {
lab=Enable}
N 865 -1340 865 -1320 {
lab=GND}
N 865 -1430 865 -1400 {
lab=sDone}
N 1125 -1350 1125 -1330 {
lab=GND}
N 1125 -1440 1125 -1410 {
lab=Clk}
N 1360 -1345 1360 -1325 {
lab=GND}
N 1360 -1435 1360 -1405 {
lab=Win}
N 1250 -960 1260 -960 {
lab=vtaudpip}
N 1250 -940 1260 -940 {
lab=vthrdpin}
N 1250 -1000 1260 -1000 {
lab=sDone}
N 1250 -1020 1260 -1020 {
lab=Clk}
N 1240 -1020 1250 -1020 {
lab=Clk}
N 210 -1260 210 -1240 {
lab=GND}
N 210 -1350 210 -1320 {
lab=Spk_in[1]}
N 1560 -1050 1640 -1050 {
lab=Req_out}
C {devices/vsource.sym} 170 -670 0 0 {name=V8 value=0.4}
C {devices/gnd.sym} 170 -620 0 0 {name=l9 lab=GND value="0"}
C {devices/lab_pin.sym} 170 -730 0 0 {name=p45 sig_type=std_logic lab=ifrefn}
C {devices/vsource.sym} 90 -670 0 0 {name=V9 value=0.4}
C {devices/gnd.sym} 90 -620 0 0 {name=l10 lab=GND value="0"}
C {devices/lab_pin.sym} 90 -730 0 0 {name=p46 sig_type=std_logic lab=ifleakn}
C {devices/vsource.sym} 370 -660 0 0 {name=V16 value=1.8}
C {devices/gnd.sym} 370 -610 0 0 {name=l15 lab=GND value="0"}
C {devices/lab_pin.sym} 370 -720 0 0 {name=p33 sig_type=std_logic lab=ifahwp}
C {devices/vsource.sym} 290 -660 0 0 {name=V18 value=0.0}
C {devices/gnd.sym} 290 -610 0 0 {name=l17 lab=GND value="0"}
C {devices/lab_pin.sym} 290 -720 0 0 {name=p40 sig_type=std_logic lab=ifnmdap}
C {devices/vsource.sym} 480 -660 0 0 {name=V19 value=1.8}
C {devices/gnd.sym} 480 -610 0 0 {name=l18 lab=GND value="0"}
C {devices/lab_pin.sym} 480 -720 0 0 {name=p41 sig_type=std_logic lab=ifdcp}
C {devices/vsource.sym} 600 -660 0 0 {name=V21 value=1.8}
C {devices/gnd.sym} 600 -610 0 0 {name=l21 lab=GND value="0"}
C {devices/lab_pin.sym} 600 -720 0 0 {name=p42 sig_type=std_logic lab=ifahthrp}
C {devices/vsource.sym} 720 -660 0 0 {name=V22 value=1.8}
C {devices/gnd.sym} 720 -610 0 0 {name=l22 lab=GND value="0"}
C {devices/lab_pin.sym} 720 -720 0 0 {name=p43 sig_type=std_logic lab=ifthrp}
C {devices/vsource.sym} 840 -660 0 0 {name=V23 value=0.0}
C {devices/gnd.sym} 840 -610 0 0 {name=l23 lab=GND value="0"}
C {devices/lab_pin.sym} 840 -720 0 0 {name=p44 sig_type=std_logic lab=ifcascn}
C {devices/vsource.sym} 970 -660 0 0 {name=V24 value=0.0}
C {devices/gnd.sym} 970 -610 0 0 {name=l24 lab=GND value="0"}
C {devices/lab_pin.sym} 970 -720 0 0 {name=p47 sig_type=std_logic lab=ifahtaun}
C {devices/vsource.sym} 510 -890 0 0 {name=V2 value=1.8}
C {devices/gnd.sym} 510 -840 0 0 {name=l5 lab=GND value="0"}
C {devices/lab_pin.sym} 510 -950 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 395 -1110 0 0 {name=V7 value=1.5}
C {devices/gnd.sym} 395 -1060 0 0 {name=l8 lab=GND value="0"}
C {devices/lab_pin.sym} 395 -1170 0 0 {name=p16 sig_type=std_logic lab=vtaudpip}
C {devices/vsource.sym} 495 -1110 0 0 {name=V13 value=0.9}
C {devices/gnd.sym} 495 -1060 0 0 {name=l14 lab=GND value="0"}
C {devices/lab_pin.sym} 495 -1170 0 0 {name=p26 sig_type=std_logic lab=vthrdpin}
C {devices/vsource.sym} 600 -1120 0 0 {name=V10 value=0.47}
C {devices/gnd.sym} 600 -1070 0 0 {name=l11 lab=GND value="0"}
C {devices/lab_pin.sym} 600 -1180 0 0 {name=p39 sig_type=std_logic lab=vstddpin}
C {devices/vsource.sym} 210 -1120 0 1 {name=V12 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/gnd.sym} 210 -1070 0 0 {name=l13 lab=GND value="0"}
C {devices/gnd.sym} 410 -860 0 0 {name=l4 lab=GND value="0"}
C {devices/lab_pin.sym} 410 -960 0 0 {name=p48 sig_type=std_logic lab=GND}
C {devices/vsource.sym} 600 -890 0 0 {name=V4 value=1.8}
C {devices/gnd.sym} 600 -840 0 0 {name=l3 lab=GND value="0"}
C {devices/lab_pin.sym} 600 -950 0 0 {name=p57 sig_type=std_logic lab=aVDD}
C {devices/gnd.sym} 160 -850 0 0 {name=l12 lab=GND value="0"}
C {devices/lab_pin.sym} 160 -960 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 160 -900 0 0 {name=V11 value="pulse(1.8 0 0ns 1ns 1ns 100ns 1ms 1)"}
C {devices/lab_pin.sym} 1560 -980 2 0 {name=p1 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1560 -960 2 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1560 -940 2 0 {name=p3 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1260 -1060 0 0 {name=p4 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1260 -780 0 0 {name=p5 sig_type=std_logic lab=ifleakn}
C {devices/lab_pin.sym} 1260 -800 0 0 {name=p6 sig_type=std_logic lab=ifrefn}
C {devices/lab_pin.sym} 1260 -900 0 0 {name=p7 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 1260 -860 0 0 {name=p8 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 1260 -920 0 0 {name=p9 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 1260 -880 0 0 {name=p10 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 1260 -760 0 0 {name=p11 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 1260 -840 0 0 {name=p12 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 1260 -820 0 0 {name=p13 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 1255 -960 0 0 {name=p14 sig_type=std_logic lab=vtaudpip}
C {devices/lab_pin.sym} 1255 -940 0 0 {name=p15 sig_type=std_logic lab=vthrdpin}
C {devices/lab_pin.sym} 1260 -980 0 0 {name=p17 sig_type=std_logic lab=vstddpin}
C {devices/lab_pin.sym} 1350 -1090 2 0 {name=p18 sig_type=std_logic lab=Spk_in[0:1]}
C {devices/lab_pin.sym} 1620 -1050 1 0 {name=p20 sig_type=std_logic lab=Req_out}
C {sky130_stdcells/inv_1.sym} 1680 -1050 0 0 {name=x13 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1760 -1050 0 0 {name=x2 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1800 -1050 3 0 {name=p21 sig_type=std_logic lab=Ack_in}
C {devices/lab_pin.sym} 1560 -760 2 0 {name=p22 sig_type=std_logic lab=Ack_in}
C {devices/gnd.sym} 690 -860 0 0 {name=l1 lab=GND value="0"}
C {devices/lab_pin.sym} 690 -970 0 0 {name=p23 sig_type=std_logic lab=Enable}
C {devices/vsource.sym} 690 -910 0 0 {name=V1 value="pulse(1.8 0 1ns 1us 1us 1us 1ms 1)"}
C {devices/lab_pin.sym} 1560 -780 2 0 {name=p24 sig_type=std_logic lab=Enable}
C {devices/vsource.sym} 865 -1370 0 1 {name=V3 value="pulse(0 1.8 300ns 1ns 1ns 10ns 10us 1)"}
C {devices/gnd.sym} 865 -1320 0 0 {name=l2 lab=GND value="0"}
C {devices/lab_pin.sym} 865 -1430 0 0 {name=p25 sig_type=std_logic lab=sDone}
C {devices/lab_pin.sym} 1255 -1000 0 0 {name=p27 sig_type=std_logic lab=sDone}
C {devices/vsource.sym} 1125 -1380 0 1 {name=V5 value="pulse(0 1.8 200ns 1ns 1ns 5ns 10ns 8)"}
C {devices/gnd.sym} 1125 -1330 0 0 {name=l6 lab=GND value="0"}
C {devices/lab_pin.sym} 1125 -1440 0 0 {name=p28 sig_type=std_logic lab=Clk}
C {devices/lab_pin.sym} 1245 -1020 0 0 {name=p29 sig_type=std_logic lab=Clk}
C {devices/vsource.sym} 1360 -1375 0 1 {name=V6 value="pulse(0 1.8 200ns 1ns 1ns 10ns 20ns 4)"}
C {devices/gnd.sym} 1360 -1325 0 0 {name=l7 lab=GND value="0"}
C {devices/lab_pin.sym} 1360 -1435 0 0 {name=p30 sig_type=std_logic lab=Win}
C {devices/lab_pin.sym} 1260 -1040 0 0 {name=p31 sig_type=std_logic lab=Win}
C {devices/code.sym} 280 -1420 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice)"}
C {sky130_fd_pr/corner.sym} 410 -1420 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/code_shown.sym} 700 -1250 0 0 {name=SPICE only_toplevel=false value="

.save all

.control
tran 10ns 1ms
write perceptron_fc_tb.raw
set appendwrite
*plot Req_out+4 Ack_in+4 x1.x3.vmem+2 x1.x4.vsin
quit 0
.endc
"}
C {perceptron_fc.sym} 1410 -910 0 0 {name=x1}
C {devices/vsource.sym} 210 -1290 0 1 {name=V14 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/gnd.sym} 210 -1240 0 0 {name=l19 lab=GND value="0"}
C {devices/lab_pin.sym} 210 -1350 0 0 {name=p32 sig_type=std_logic lab=Spk_in[1]}
C {devices/lab_pin.sym} 210 -1180 0 0 {name=p19 sig_type=std_logic lab=Spk_in[0]}
