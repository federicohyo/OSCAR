v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 70 -1220 1210 -630 {flags=graph
y1=0

ypos1=-0.14585673
ypos2=3.4100731

subdivy=1
unity=1
x1=0
x2=2e-07
divx=5
subdivx=1


node="clk
req_cpu
ack_cpu
a
req[0]
ack[0]
b
req[1]
ack[1]
c
req[2]
ack[2]
d
req[3]
ack[3]"
color="19 5 5 6 6 6 9 9 9 11 11 11 12 12 12"
dataset=-1
unitx=1
logx=0
logy=0
digital=1
xlabmag=1
ylabmag=1
divy=5
y2=2}
T {CPU circuit emulation

Sample request line and delay for one clock cycle (currently running at 200 MHz)} 860 -600 0 0 0.4 0.4 {}
T {Arbiter under test} 1340 -920 0 0 0.4 0.4 {}
T {Input request generation and acknowledgement handling} 1130 -280 0 0 0.4 0.4 {}
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
N 1290 -150 1350 -150 {
lab=#net2}
N 1350 -170 1350 -150 {
lab=#net2}
N 770 -30 770 -10 {
lab=0}
N 770 -120 770 -90 {
lab=D}
N 500 -30 500 -10 {
lab=0}
N 500 -110 500 -80 {
lab=C}
N 1630 -790 1680 -790 {
lab=#net3}
N 1630 -810 1680 -810 {
lab=#net4}
N 370 -420 370 -400 {
lab=0}
N 370 -510 370 -480 {
lab=VDD}
C {devices/vsource.sym} 770 -210 0 0 {name=V3 value="dc 0 pulse(0 1.8 2ns 1ns 1ns 1ns 60ns)"}
C {devices/lab_pin.sym} 770 -160 0 0 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1650 -130 0 1 {name=p7 sig_type=std_logic lab=req[0:3]}
C {devices/vsource.sym} 500 -210 0 0 {name=V2 value="dc 0 pulse(0 1.8 2ns 1ns 1ns 1ns 50ns)"}
C {devices/lab_pin.sym} 500 -160 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 520 -510 0 0 {name=p3 sig_type=std_logic lab=clk}
C {devices/vsource.sym} 520 -450 0 0 {name=V1 value="dc 0 pulse(0 1.8 1ns 1ns 1ns 1.5ns 5ns)"}
C {devices/lab_pin.sym} 520 -400 0 0 {name=p6 sig_type=std_logic lab=0}
C {sky130_fd_pr/corner.sym} 110 -290 0 0 {name=CORNER only_toplevel=false corner=ff}
C {devices/code.sym} 110 -500 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {devices/simulator_commands_shown.sym} 490 -1340 0 0 {name=COMMANDS2
simulator=xyce
only_toplevel=false 
value=".TRAN 0.02ns 200ns
.PRINT TRAN format=raw file=arbiter_four_bits_tb.raw v(*) i(*)
"}
C {devices/simulator_commands_shown.sym} 90 -1340 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value=".save all
.control
 tran 0.02ns 200ns
 write arbiter_four_bits_tb.raw
 quit 0
.endc
"}
C {devices/lab_pin.sym} 1140 -430 2 1 {name=p10 sig_type=std_logic lab=req_cpu}
C {devices/lab_pin.sym} 1560 -450 2 0 {name=p11 sig_type=std_logic lab=ack_cpu}
C {devices/lab_pin.sym} 1140 -480 2 1 {name=p12 sig_type=std_logic lab=clk}
C {srlatch.sym} 1500 -160 0 0 {name=x4[0:3]}
C {devices/lab_pin.sym} 1210 -150 0 0 {name=p13 sig_type=std_logic lab=ack[0:3]}
C {sky130_stdcells/clkdlybuf4s50_1.sym} 1250 -150 0 0 {name=x6[0:3] VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
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
C {devices/lab_pin.sym} 1350 -190 0 0 {name=p14 sig_type=std_logic lab=A,B,C,D}
C {arbiter_two_bits.sym} 1830 -780 0 0 {name=x3}
C {devices/lab_pin.sym} 1330 -810 0 0 {name=p15 lab=req[0:3]}
C {devices/lab_pin.sym} 1980 -790 0 1 {name=p21 lab=ack_cpu}
C {devices/lab_pin.sym} 1980 -810 0 1 {name=p22 lab=req_cpu}
C {devices/lab_pin.sym} 1330 -790 0 0 {name=p23 lab=ack[0:3]}
C {arbiter_two_bits.sym} 1480 -780 0 0 {name=x1[0:1]}
C {devices/vsource.sym} 770 -60 0 0 {name=V5 value="dc 0 pulse(0 1.8 2ns 1ns 1ns 1ns 20ns)"}
C {devices/lab_pin.sym} 770 -10 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/vsource.sym} 500 -60 0 0 {name=V6 value="dc 0 pulse(0 1.8 2ns 1ns 1ns 1ns 70ns)"}
C {devices/lab_pin.sym} 500 -10 0 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 500 -110 0 0 {name=p9 sig_type=std_logic lab=C}
C {devices/lab_pin.sym} 770 -120 0 0 {name=p24 sig_type=std_logic lab=D}
C {devices/lab_pin.sym} 1630 -750 0 1 {name=p25 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1980 -750 0 1 {name=p26 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1980 -770 0 1 {name=p27 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1630 -770 0 1 {name=p28 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 370 -510 0 0 {name=p29 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 370 -450 0 0 {name=VDD value=1.8}
C {devices/lab_pin.sym} 370 -400 0 0 {name=p30 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1650 -190 0 1 {name=p31 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1650 -170 0 1 {name=p32 sig_type=std_logic lab=0}
