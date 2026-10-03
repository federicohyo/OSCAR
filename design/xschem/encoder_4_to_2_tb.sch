v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 650 -760 1450 -360 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=4e-05
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="ack_neu[0]
ack_neu[1]
ack_neu[2]
ack_neu[3]
OUT;neu_addr[1],neu_addr[0]
neu_addr[0]
neu_addr[1]"
color="4 4 4 4 9 9 9"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
N 120 -150 120 -130 {
lab=0}
N 120 -240 120 -210 {
lab=ack_neu[0]}
N 120 -300 120 -280 {
lab=0}
N 120 -390 120 -360 {
lab=ack_neu[1]}
N 470 -70 500 -70 {
lab=ack_neu[0:3]}
N 880 -170 880 -150 {
lab=0}
N 880 -260 880 -230 {
lab=VDD}
N 190 -530 190 -510 {
lab=0}
N 190 -620 190 -590 {
lab=ack_neu[2]}
N 190 -680 190 -660 {
lab=0}
N 190 -770 190 -740 {
lab=ack_neu[3]}
C {devices/lab_pin.sym} 120 -240 0 0 {name=p20 sig_type=std_logic lab=ack_neu[0]}
C {devices/vsource.sym} 120 -180 0 0 {name=V1 value="pulse(0 1.8 1ns 2ns 1ns 2us 80us 1)"}
C {devices/lab_pin.sym} 120 -130 0 0 {name=p11 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 120 -390 0 0 {name=p1 sig_type=std_logic lab=ack_neu[1]}
C {devices/vsource.sym} 120 -330 0 0 {name=V2 value="pulse(0 1.8 10us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 120 -280 0 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 470 -70 2 1 {name=p74 sig_type=std_logic lab=ack_neu[0:3]}
C {devices/lab_pin.sym} 800 -70 2 0 {name=p76 sig_type=std_logic lab=neu_addr[0:1]}
C {devices/code.sym} 610 -260 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 450 -270 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/vsource.sym} 880 -200 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 880 -260 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 880 -150 0 0 {name=p7 sig_type=std_logic lab=0}
C {encoder_4_to_2.sym} 650 -50 0 0 {name=x1}
C {devices/lab_pin.sym} 190 -620 0 0 {name=p3 sig_type=std_logic lab=ack_neu[2]}
C {devices/vsource.sym} 190 -560 0 0 {name=V3 value="pulse(0 1.8 20us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 190 -510 0 0 {name=p4 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 190 -770 0 0 {name=p5 sig_type=std_logic lab=ack_neu[3]}
C {devices/vsource.sym} 190 -710 0 0 {name=V5 value="pulse(0 1.8 30us 2ns 1ns 2us 80us)"}
C {devices/lab_pin.sym} 190 -660 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 800 -30 0 1 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 800 -50 0 1 {name=p10 sig_type=std_logic lab=VDD}
C {devices/simulator_commands_shown.sym} 1010 -210 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value=".save all
.control
  tran 10ns 40us
  write encoder_4_to_2_tb.raw
  quit 0
.endc
"}
C {devices/simulator_commands_shown.sym} 1380 -210 0 0 {name=COMMANDS1
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 40us
.PRINT TRAN format=raw file=encoder_2_to_4.raw v(*) i(*)
.OPTION DEVICE GMIN=1.0e-14
.SAVE
"}
