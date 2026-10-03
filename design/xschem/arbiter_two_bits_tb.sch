v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 70 -1040 1200 -660 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-07
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="clk
req
ack
a
reqa
acka
b
reqb
ackb"
color="19 5 5 6 6 6 9 9 9"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
T {CPU circuit emulation

Sample request line and delay for one clock cycle (currently running at 200 MHz)} 860 -600 0 0 0.4 0.4 {}
T {Arbiter under test} 1340 -1020 0 0 0.4 0.4 {}
T {Input request generation and handshake} 860 -350 0 0 0.4 0.4 {}
N 770 -180 770 -160 {
lab=0}
N 770 -270 770 -240 {
lab=B}
N 500 -180 500 -160 {
lab=0}
N 500 -260 500 -230 {
lab=A}
N 520 -420 520 -400 {
lab=0}
N 520 -510 520 -480 {
lab=clk}
N 1320 -450 1350 -450 {
lab=#net1}
N 1350 -450 1350 -430 {
lab=#net1}
N 1350 -430 1380 -430 {
lab=#net1}
N 1140 -480 1140 -450 {
lab=clk}
N 1380 -470 1380 -450 {
lab=clk}
N 1140 -470 1380 -470 {
lab=clk}
N 790 -420 790 -400 {
lab=0}
N 790 -510 790 -480 {
lab=rst}
N 1310 -190 1370 -190 {
lab=#net2}
N 1370 -210 1370 -190 {
lab=#net2}
N 350 -420 350 -400 {
lab=0}
N 350 -510 350 -480 {
lab=VDD}
C {devices/vsource.sym} 770 -210 0 0 {name=V3 value="dc 0 pulse(0 1.8 2ns 1ns 1ns 1ns 18ns)"}
C {devices/lab_pin.sym} 770 -160 0 0 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1670 -170 0 1 {name=p7 sig_type=std_logic lab=reqA,reqB}
C {devices/vsource.sym} 500 -210 0 0 {name=V2 value="dc 0 pulse(0 1.8 2ns 1ns 1ns 1ns 14ns)"}
C {devices/lab_pin.sym} 500 -160 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 520 -510 0 0 {name=p3 sig_type=std_logic lab=clk}
C {devices/vsource.sym} 520 -450 0 0 {name=V1 value="dc 0 pulse(0 1.8 1ns 1ns 1ns 1.5ns 5ns)"}
C {devices/lab_pin.sym} 520 -400 0 0 {name=p6 sig_type=std_logic lab=0}
C {sky130_fd_pr/corner.sym} 110 -290 0 0 {name=CORNER only_toplevel=false corner=ss}
C {devices/code.sym} 110 -500 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {devices/simulator_commands_shown.sym} 510 -1140 0 0 {name=COMMANDS2
simulator=xyce
only_toplevel=false 
value=".TRAN 0.01us 200ns
.PRINT TRAN format=raw file=arbiter_two_bits_tb.raw v(*) i(*)
"}
C {devices/simulator_commands_shown.sym} 110 -1170 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value=".save all
.control
 tran 0.1ns 200ns
 write arbiter_two_bits_tb.raw
 quit 0
.endc
"}
C {devices/lab_pin.sym} 1140 -430 2 1 {name=p10 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 1560 -450 2 0 {name=p11 sig_type=std_logic lab=ack}
C {devices/lab_pin.sym} 1140 -480 2 1 {name=p12 sig_type=std_logic lab=clk}
C {srlatch.sym} 1520 -200 0 0 {name=x4[0:1]}
C {devices/lab_pin.sym} 1230 -190 0 0 {name=p13 sig_type=std_logic lab=ackA,ackB}
C {sky130_stdcells/clkdlybuf4s50_1.sym} 1270 -190 0 0 {name=x6[0:1] VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 500 -260 0 0 {name=p4 sig_type=std_logic lab=A}
C {devices/lab_pin.sym} 770 -270 0 0 {name=p16 sig_type=std_logic lab=B}
C {sky130_stdcells/dfrtn_1.sym} 1230 -430 0 0 {name=x8 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/dfrtn_1.sym} 1470 -430 0 0 {name=x2 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 790 -510 0 0 {name=p17 sig_type=std_logic lab=rst}
C {devices/vsource.sym} 790 -450 0 0 {name=V4 value="dc 0 pulse(0 1.8 1ns 1ns 1ns 2000ns 600000ns)"
lab=rst}
C {devices/lab_pin.sym} 790 -400 0 0 {name=p18 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1140 -410 0 0 {name=p19 sig_type=std_logic lab=rst}
C {devices/lab_pin.sym} 1380 -410 0 0 {name=p20 sig_type=std_logic lab=rst}
C {devices/lab_pin.sym} 1370 -230 0 0 {name=p14 sig_type=std_logic lab=A,B}
C {arbiter_two_bits.sym} 1510 -780 0 0 {name=x3}
C {devices/lab_pin.sym} 1360 -810 0 0 {name=p15 lab=reqA,reqB}
C {devices/lab_pin.sym} 1660 -790 0 1 {name=p21 lab=ack}
C {devices/lab_pin.sym} 1660 -810 0 1 {name=p22 lab=req}
C {devices/lab_pin.sym} 1360 -790 0 0 {name=p23 lab=ackA,ackB}
C {devices/lab_pin.sym} 1670 -210 0 1 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1670 -230 0 1 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1660 -750 0 1 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1660 -770 0 1 {name=p24 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 350 -510 0 0 {name=p25 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 350 -450 0 0 {name=VDD value=1.8}
C {devices/lab_pin.sym} 350 -400 0 0 {name=p26 sig_type=std_logic lab=0}
