v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1310 -460 2110 -60 {flags=graph
y1=0.4
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
node="nres
ACK_I;ack_addr[0],ack_addr[1],ack_addr[2],ack_addr[3]
ACK_L;ack_addr_latched[0],ack_addr_latched[1],ack_addr_latched[2],ack_addr_latched[3]
ack_addr_latched[0]
ack_addr_latched[1]
ack_addr_latched[2]
ack_addr_latched[3]
ack_addr[0]
ack_addr[1]
ack_addr[2]
ack_addr[3]"
color="5 10 8 10 10 10 10 13 13 13 13"
dataset=-1
unitx=1
logx=0
logy=0
digital=1
}
T {Power up reset} 80 -680 0 0 0.4 0.4 {}
N 730 -220 730 -200 {
lab=0}
N 730 -310 730 -280 {
lab=nRes}
N 600 -220 600 -200 {
lab=0}
N 600 -310 600 -280 {
lab=VDD}
C {devices/code.sym} 10 -110 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 140 -110 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/simulator_commands_shown.sym} 320 -100 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 100us
.PRINT TRAN format=raw file=output_latch_4_neu_tb.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
C {output_latch_4_neu.sym} 800 -400 0 0 {name=x1}
C {devices/lab_pin.sym} 730 -310 0 0 {name=p31 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 730 -250 0 0 {name=V3 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 730 -200 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 340 -600 2 0 {name=p23 sig_type=std_logic lab=ack_addr[0]}
C {devices/vsource.sym} 340 -570 0 1 {name=V1 value="pulse(0 1.8 25ns 1ns 1ns 13us 26us 100)"}
C {devices/lab_pin.sym} 340 -540 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 330 -510 2 0 {name=p2 sig_type=std_logic lab=ack_addr[1]}
C {devices/vsource.sym} 330 -480 0 1 {name=V5 value="pulse(0 1.8 1ns 1ns 1ns 9us 18us 100)"}
C {devices/lab_pin.sym} 330 -450 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 330 -430 2 0 {name=p4 sig_type=std_logic lab=ack_addr[2]}
C {devices/vsource.sym} 330 -400 0 1 {name=V6 value="pulse(0 1.8 3ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 330 -370 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 330 -340 2 0 {name=p7 sig_type=std_logic lab=ack_addr[3]}
C {devices/vsource.sym} 330 -310 0 1 {name=V7 value="pulse(0 1.8 4ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 330 -280 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 650 -400 0 0 {name=p5 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 600 -310 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 600 -250 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 600 -200 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 650 -420 2 1 {name=p11 sig_type=std_logic lab=ack_addr[0:3]}
C {devices/lab_pin.sym} 950 -420 2 0 {name=p12 sig_type=std_logic lab=ack_addr_latched[0:3]}
C {devices/lab_pin.sym} 950 -380 0 1 {name=p13 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 950 -400 0 1 {name=p14 sig_type=std_logic lab=VDD}
