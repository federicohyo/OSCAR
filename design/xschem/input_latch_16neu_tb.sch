v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1430 -510 2230 -110 {flags=graph
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
node="reqin
reqin_ar
SYN_I;syn_addr[0],syn_addr[1],syn_addr[2],syn_addr[3]
SYN_L;syn_addr_latched[0],syn_addr_latched[1],syn_addr_latched[2],syn_addr_latched[3]
NEU_I;neu_addr[0],neu_addr[1],neu_addr[2],neu_addr[3]
NEU_L;neu_addr_latched[0],neu_addr_latched[1],neu_addr_latched[2],neu_addr_latched[3]"
color="13 13 9 9 11 11"
dataset=-1
unitx=1
logx=0
logy=0
digital=1
}
T {Power up reset} 70 -720 0 0 0.4 0.4 {}
N 160 -510 160 -480 {
lab=REQIN}
N 160 -650 160 -620 {
lab=exc}
N 160 -270 160 -250 {
lab=0}
N 160 -360 160 -330 {
lab=nRes}
N 1040 -310 1080 -310 {
lab=syn_addr_latched[0:3]}
N 1040 -290 1070 -290 {
lab=neu_addr_latched[0:3]}
N 1040 -270 1070 -270 {
lab=exc_ar}
N 1040 -250 1070 -250 {
lab=REQIN_ar}
C {devices/code.sym} 50 -160 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 180 -160 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/vsource.sym} 160 -450 0 1 {name=V12 value="pulse(0 1.8 3ns 1ns 1ns 1us 2us 100)"}
C {devices/lab_pin.sym} 160 -510 0 0 {name=p19 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 160 -420 0 0 {name=p94 sig_type=std_logic lab=0}
C {devices/vsource.sym} 880 -400 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 880 -430 0 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 880 -370 0 0 {name=p42 sig_type=std_logic lab=0}
C {devices/vsource.sym} 160 -590 0 1 {name=V25 value="pulse(0 1.8 25ns 1ns 1ns 1.8ms 3.6ms 1)"}
C {devices/lab_pin.sym} 160 -650 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 160 -560 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 160 -360 0 0 {name=p31 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 160 -300 0 0 {name=V3 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 160 -250 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 430 -620 2 0 {name=p23 sig_type=std_logic lab=syn_addr[0]}
C {devices/vsource.sym} 430 -590 0 1 {name=V1 value="pulse(0 1.8 25ns 1ns 1ns 13us 26us 100)"}
C {devices/lab_pin.sym} 430 -560 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 420 -530 2 0 {name=p2 sig_type=std_logic lab=syn_addr[1]}
C {devices/vsource.sym} 420 -500 0 1 {name=V5 value="pulse(0 1.8 1ns 1ns 1ns 9us 18us 100)"}
C {devices/lab_pin.sym} 420 -470 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 420 -450 2 0 {name=p4 sig_type=std_logic lab=syn_addr[2]}
C {devices/vsource.sym} 420 -420 0 1 {name=V6 value="pulse(0 1.8 3ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 420 -390 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 420 -360 2 0 {name=p7 sig_type=std_logic lab=syn_addr[3]}
C {devices/vsource.sym} 420 -330 0 1 {name=V7 value="pulse(0 1.8 4ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 420 -300 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 880 -620 2 0 {name=p9 sig_type=std_logic lab=neu_addr[0]}
C {devices/vsource.sym} 880 -590 0 1 {name=V8 value="pulse(0 1.8 3ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 880 -560 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 880 -540 2 0 {name=p11 sig_type=std_logic lab=neu_addr[1]}
C {devices/vsource.sym} 880 -510 0 1 {name=V9 value="pulse(0 1.8 4ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 880 -480 0 0 {name=p12 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 740 -230 0 0 {name=p13 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 740 -310 0 0 {name=p14 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 740 -270 0 0 {name=p15 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 740 -290 2 1 {name=p16 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 740 -250 2 1 {name=p17 sig_type=std_logic lab=neu_addr[0:3]}
C {devices/lab_pin.sym} 1070 -250 0 1 {name=p18 sig_type=std_logic lab=REQIN_ar}
C {devices/lab_pin.sym} 1070 -270 0 1 {name=p20 sig_type=std_logic lab=exc_ar}
C {devices/lab_pin.sym} 1080 -310 2 0 {name=p21 sig_type=std_logic lab=syn_addr_latched[0:3]}
C {devices/lab_pin.sym} 1070 -290 2 0 {name=p22 sig_type=std_logic lab=neu_addr_latched[0:3]}
C {devices/simulator_commands_shown.sym} 360 -150 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 100us
.PRINT TRAN format=raw file=input_latch_16neu_tb.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
C {devices/lab_pin.sym} 1250 -620 2 0 {name=p5 sig_type=std_logic lab=neu_addr[2]}
C {devices/vsource.sym} 1250 -590 0 1 {name=V2 value="pulse(0 1.8 3ns 1ns 1ns 11us 22us 100)"}
C {devices/lab_pin.sym} 1250 -560 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1250 -540 2 0 {name=p25 sig_type=std_logic lab=neu_addr[3]}
C {devices/vsource.sym} 1250 -510 0 1 {name=V4 value="pulse(0 1.8 4ns 1ns 1ns 9us 18us 100)"}
C {devices/lab_pin.sym} 1250 -480 0 0 {name=p26 sig_type=std_logic lab=0}
C {inputs_latch_16neu.sym} 890 -260 0 0 {name=x1}
C {devices/lab_pin.sym} 1040 -210 0 1 {name=p27 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1040 -230 0 1 {name=p28 sig_type=std_logic lab=VDD}
C {devices/simulator_commands_shown.sym} 360 -10 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value=".save all
.control
  tran 0.01us 100us
  write input_latch_16neu_tb.raw
  quit 0
.endc
"}
