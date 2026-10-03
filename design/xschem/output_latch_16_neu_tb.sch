v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1220 -490 2020 -90 {flags=graph
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
node="ACK_I;ack_addr[0],ack_addr[1],ack_addr[2],ack_addr[3],ack_addr[4],ack_addr[5],ack_addr[6],ack_addr[7],ack_addr[8],ack_addr[9],ack_addr[10],ack_addr[11],ack_addr[12],ack_addr[13],ack_addr[14],ack_addr[15]
ACK_S;ack_addr_latched[0],ack_addr_latched[1],ack_addr_latched[2],ack_addr_latched[3],ack_addr_latched[4],ack_addr_latched[5],ack_addr_latched[6],ack_addr_latched[7],ack_addr_latched[8],ack_addr_latched[9],ack_addr_latched[10],ack_addr_latched[11],ack_addr_latched[12],ack_addr_latched[13],ack_addr_latched[14],ack_addr_latched[15]"
color="17 17"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
T {Power up reset} 100 -730 0 0 0.4 0.4 {}
N 750 -250 750 -230 {
lab=0}
N 750 -340 750 -310 {
lab=nRes}
N 620 -250 620 -230 {
lab=0}
N 620 -340 620 -310 {
lab=VDD}
C {devices/code.sym} 30 -160 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 160 -160 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/simulator_commands_shown.sym} 340 -150 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 500us
.PRINT TRAN format=raw file=output_latch_16_neu_tb.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
C {devices/lab_pin.sym} 750 -340 0 0 {name=p31 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 750 -280 0 0 {name=V3 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 750 -230 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 360 -650 2 0 {name=p23 sig_type=std_logic lab=ack_addr[0]}
C {devices/vsource.sym} 360 -620 0 1 {name=V1 value="pulse(0 1.8 25ns 1ns 1ns 13us 26us 100)"}
C {devices/lab_pin.sym} 360 -590 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 350 -560 2 0 {name=p2 sig_type=std_logic lab=ack_addr[1]}
C {devices/vsource.sym} 350 -530 0 1 {name=V5 value="pulse(0 1.8 1ns 1ns 1ns 9us 18us 100)"}
C {devices/lab_pin.sym} 350 -500 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 350 -480 2 0 {name=p4 sig_type=std_logic lab=ack_addr[2]}
C {devices/vsource.sym} 350 -450 0 1 {name=V6 value="pulse(0 1.8 3ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 350 -420 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 350 -390 2 0 {name=p7 sig_type=std_logic lab=ack_addr[3]}
C {devices/vsource.sym} 350 -360 0 1 {name=V7 value="pulse(0 1.8 4ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 350 -330 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 670 -430 0 0 {name=p5 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 620 -340 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 620 -280 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 620 -230 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 670 -450 2 1 {name=p11 sig_type=std_logic lab=ack_addr[0:15]}
C {devices/lab_pin.sym} 970 -450 2 0 {name=p12 sig_type=std_logic lab=ack_addr_latched[0:15]}
C {output_latch_16_neu.sym} 820 -430 0 0 {name=x1}
C {devices/lab_pin.sym} 760 -890 2 0 {name=p13 sig_type=std_logic lab=ack_addr[4]}
C {devices/vsource.sym} 760 -860 0 1 {name=V4 value="pulse(0 1.8 25ns 1ns 1ns 13us 26us 100)"}
C {devices/lab_pin.sym} 760 -830 0 0 {name=p14 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 750 -800 2 0 {name=p15 sig_type=std_logic lab=ack_addr[5]}
C {devices/vsource.sym} 750 -770 0 1 {name=V8 value="pulse(0 1.8 2ns 1ns 1ns 9us 18us 100)"}
C {devices/lab_pin.sym} 750 -740 0 0 {name=p16 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 750 -710 2 0 {name=p17 sig_type=std_logic lab=ack_addr[6]}
C {devices/vsource.sym} 750 -680 0 1 {name=V9 value="pulse(0 1.8 5ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 750 -650 0 0 {name=p18 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 750 -630 2 0 {name=p19 sig_type=std_logic lab=ack_addr[7]}
C {devices/vsource.sym} 750 -600 0 1 {name=V10 value="pulse(0 1.8 4ns 1ns 1ns 11us 22us 100)"}
C {devices/lab_pin.sym} 750 -570 0 0 {name=p20 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1150 -890 2 0 {name=p21 sig_type=std_logic lab=ack_addr[8]}
C {devices/vsource.sym} 1150 -860 0 1 {name=V11 value="pulse(0 1.8 7ns 1ns 1ns 14us 28us 100)"}
C {devices/lab_pin.sym} 1150 -830 0 0 {name=p22 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1150 -800 2 0 {name=p24 sig_type=std_logic lab=ack_addr[9]}
C {devices/vsource.sym} 1150 -770 0 1 {name=V12 value="pulse(0 1.8 7ns 1ns 1ns 11us 22us 100)"}
C {devices/lab_pin.sym} 1150 -740 0 0 {name=p25 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1150 -710 2 0 {name=p26 sig_type=std_logic lab=ack_addr[10]}
C {devices/vsource.sym} 1150 -680 0 1 {name=V13 value="pulse(0 1.8 5ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 1150 -650 0 0 {name=p27 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1150 -630 2 0 {name=p28 sig_type=std_logic lab=ack_addr[11]}
C {devices/vsource.sym} 1150 -600 0 1 {name=V14 value="pulse(0 1.8 4ns 1ns 1ns 7us 14us 100)"}
C {devices/lab_pin.sym} 1150 -570 0 0 {name=p29 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1510 -890 2 0 {name=p30 sig_type=std_logic lab=ack_addr[12]}
C {devices/vsource.sym} 1510 -860 0 1 {name=V15 value="pulse(0 1.8 23ns 1ns 1ns 12us 24us 100)"}
C {devices/lab_pin.sym} 1510 -830 0 0 {name=p33 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1510 -800 2 0 {name=p34 sig_type=std_logic lab=ack_addr[13]}
C {devices/vsource.sym} 1510 -770 0 1 {name=V16 value="pulse(0 1.8 2ns 1ns 1ns 5us 10us 100)"}
C {devices/lab_pin.sym} 1510 -740 0 0 {name=p35 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1510 -710 2 0 {name=p36 sig_type=std_logic lab=ack_addr[14]}
C {devices/vsource.sym} 1510 -680 0 1 {name=V17 value="pulse(0 1.8 3ns 1ns 1ns 33us 66us 100)"}
C {devices/lab_pin.sym} 1510 -650 0 0 {name=p37 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1510 -630 2 0 {name=p38 sig_type=std_logic lab=ack_addr[15]}
C {devices/vsource.sym} 1510 -600 0 1 {name=V18 value="pulse(0 1.8 4ns 1ns 1ns 17us 34us 100)"}
C {devices/lab_pin.sym} 1510 -570 0 0 {name=p39 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 970 -410 0 1 {name=p40 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 970 -430 0 1 {name=p41 sig_type=std_logic lab=VDD}
