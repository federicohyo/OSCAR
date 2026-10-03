v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1630 -1420 3250 -340 {flags=graph
y1=0
y2=1
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=4.5e-05
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="OUT;neu_addr[3],neu_addr[2],neu_addr[1],neu_addr[0]
ack_neu[0]
ack_neu[1]
ack_neu[2]
ack_neu[3]
ack_neu[4]
ack_neu[5]
ack_neu[6]
ack_neu[7]
ack_neu[8]
ack_neu[9]
ack_neu[10]
ack_neu[11]
ack_neu[12]
ack_neu[13]
ack_neu[14]
ack_neu[15]"
color="5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
N 420 -340 450 -340 {
lab=ack_neu[0:15]}
N 140 -660 140 -640 {
lab=0}
N 140 -750 140 -720 {
lab=ack_neu[0]}
N 830 -440 830 -420 {
lab=0}
N 830 -530 830 -500 {
lab=VDD}
N 140 -810 140 -790 {
lab=0}
N 140 -900 140 -870 {
lab=ack_neu[1]}
N 140 -960 140 -940 {
lab=0}
N 140 -1050 140 -1020 {
lab=ack_neu[2]}
N 140 -1120 140 -1100 {
lab=0}
N 140 -1210 140 -1180 {
lab=ack_neu[3]}
N 440 -660 440 -640 {
lab=0}
N 440 -750 440 -720 {
lab=ack_neu[4]}
N 440 -810 440 -790 {
lab=0}
N 440 -900 440 -870 {
lab=ack_neu[5]}
N 440 -960 440 -940 {
lab=0}
N 440 -1050 440 -1020 {
lab=ack_neu[6]}
N 440 -1120 440 -1100 {
lab=0}
N 440 -1210 440 -1180 {
lab=ack_neu[7]}
N 730 -660 730 -640 {
lab=0}
N 730 -750 730 -720 {
lab=ack_neu[8]}
N 730 -810 730 -790 {
lab=0}
N 730 -900 730 -870 {
lab=ack_neu[9]}
N 730 -960 730 -940 {
lab=0}
N 730 -1050 730 -1020 {
lab=ack_neu[10]}
N 730 -1120 730 -1100 {
lab=0}
N 730 -1210 730 -1180 {
lab=ack_neu[11]}
N 1030 -660 1030 -640 {
lab=0}
N 1030 -750 1030 -720 {
lab=ack_neu[12]}
N 1030 -810 1030 -790 {
lab=0}
N 1030 -900 1030 -870 {
lab=ack_neu[13]}
N 1030 -960 1030 -940 {
lab=0}
N 1030 -1050 1030 -1020 {
lab=ack_neu[14]}
N 1030 -1120 1030 -1100 {
lab=0}
N 1030 -1210 1030 -1180 {
lab=ack_neu[15]}
C {devices/lab_pin.sym} 420 -340 2 1 {name=p74 sig_type=std_logic lab=ack_neu[0:15]}
C {devices/lab_pin.sym} 750 -340 2 0 {name=p76 sig_type=std_logic lab=neu_addr[0:3]}
C {encoder_16_to_4.sym} 600 -320 0 0 {name=x1}
C {devices/code.sym} 560 -530 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 400 -540 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 140 -750 0 0 {name=p20 sig_type=std_logic lab=ack_neu[0]}
C {devices/vsource.sym} 140 -690 0 0 {name=V1 value="pulse(0 1.8 2us 2ns 1ns 2us 80us)"}
C {devices/vsource.sym} 830 -470 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 830 -530 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 140 -640 0 0 {name=p11 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 140 -900 0 0 {name=p1 sig_type=std_logic lab=ack_neu[1]}
C {devices/vsource.sym} 140 -840 0 0 {name=V2 value="pulse(0 1.8 4us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 140 -790 0 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 140 -1050 0 0 {name=p3 sig_type=std_logic lab=ack_neu[2]}
C {devices/vsource.sym} 140 -990 0 0 {name=V3 value="pulse(0 1.8 6us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 140 -940 0 0 {name=p4 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 140 -1210 0 0 {name=p5 sig_type=std_logic lab=ack_neu[3]}
C {devices/vsource.sym} 140 -1150 0 0 {name=V5 value="pulse(0 1.8 8us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 140 -1100 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 830 -420 0 0 {name=p7 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 440 -750 0 0 {name=p9 sig_type=std_logic lab=ack_neu[4]}
C {devices/vsource.sym} 440 -690 0 0 {name=V6 value="pulse(0 1.8 10us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 440 -640 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 440 -900 0 0 {name=p12 sig_type=std_logic lab=ack_neu[5]}
C {devices/vsource.sym} 440 -840 0 0 {name=V7 value="pulse(0 1.8 12us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 440 -790 0 0 {name=p13 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 440 -1050 0 0 {name=p14 sig_type=std_logic lab=ack_neu[6]}
C {devices/vsource.sym} 440 -990 0 0 {name=V8 value="pulse(0 1.8 14us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 440 -940 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 440 -1210 0 0 {name=p16 sig_type=std_logic lab=ack_neu[7]}
C {devices/vsource.sym} 440 -1150 0 0 {name=V9 value="pulse(0 1.8 16us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 440 -1100 0 0 {name=p17 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -750 0 0 {name=p18 sig_type=std_logic lab=ack_neu[8]}
C {devices/vsource.sym} 730 -690 0 0 {name=V10 value="pulse(0 1.8 18us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 730 -640 0 0 {name=p19 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -900 0 0 {name=p21 sig_type=std_logic lab=ack_neu[9]}
C {devices/vsource.sym} 730 -840 0 0 {name=V11 value="pulse(0 1.8 20us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 730 -790 0 0 {name=p22 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -1050 0 0 {name=p23 sig_type=std_logic lab=ack_neu[10]}
C {devices/vsource.sym} 730 -990 0 0 {name=V12 value="pulse(0 1.8 22us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 730 -940 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -1210 0 0 {name=p25 sig_type=std_logic lab=ack_neu[11]}
C {devices/vsource.sym} 730 -1150 0 0 {name=V13 value="pulse(0 1.8 24us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 730 -1100 0 0 {name=p26 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1030 -750 0 0 {name=p27 sig_type=std_logic lab=ack_neu[12]}
C {devices/vsource.sym} 1030 -690 0 0 {name=V14 value="pulse(0 1.8 26us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 1030 -640 0 0 {name=p28 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1030 -900 0 0 {name=p29 sig_type=std_logic lab=ack_neu[13]}
C {devices/vsource.sym} 1030 -840 0 0 {name=V15 value="pulse(0 1.8 28us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 1030 -790 0 0 {name=p30 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1030 -1050 0 0 {name=p31 sig_type=std_logic lab=ack_neu[14]}
C {devices/vsource.sym} 1030 -990 0 0 {name=V16 value="pulse(0 1.8 30us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 1030 -940 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1030 -1210 0 0 {name=p33 sig_type=std_logic lab=ack_neu[15]}
C {devices/vsource.sym} 1030 -1150 0 0 {name=V17 value="pulse(0 1.8 32us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 1030 -1100 0 0 {name=p34 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 750 -300 0 1 {name=p35 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 750 -320 0 1 {name=p36 sig_type=std_logic lab=VDD}
C {devices/simulator_commands_shown.sym} 950 -330 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value=".save all
.control
  tran 0.01us 45us
  write encoder_16_to_4_tb.raw
  quit 0
.endc
"}
C {devices/simulator_commands_shown.sym} 940 -510 0 0 {name=COMMANDS1
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 45us
.PRINT TRAN format=raw file=encoder_16_to_4.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.SAVE
"}
