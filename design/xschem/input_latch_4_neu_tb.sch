v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1260 -540 2060 -140 {flags=graph
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
SYN_L;syn_addr_latched[0],syn_addr_latched[1],syn_addr_latched[2],syn_addr_latched[3]
SYN_I;syn_addr[0],syn_addr[1],syn_addr[2],syn_addr[3]
nres
exc
exc_ar
NEU_L;neu_addr_latched[0],neu_addr_latched[1]
NEU_I;neu_addr[0],neu_addr[1]"
color="8 4 5 7 6 10 17 9 9"
dataset=-1
unitx=1
logx=0
logy=0
digital=1
}
B 2 1270 -980 2070 -580 {flags=graph
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
reqin_ar"
color="17 5"
dataset=-1
unitx=1
logx=0
logy=0
digital=0}
T {Power up reset} 10 -680 0 0 0.4 0.4 {}
N 100 -470 100 -440 {
lab=REQIN}
N 100 -610 100 -580 {
lab=exc}
N 100 -230 100 -210 {
lab=0}
N 100 -320 100 -290 {
lab=nRes}
N 990 -270 1020 -270 {
lab=syn_addr_latched[0:3]}
N 990 -250 1020 -250 {
lab=neu_addr_latched[0:1]}
N 990 -230 1020 -230 {
lab=exc_ar}
N 990 -210 1020 -210 {
lab=REQIN_ar}
C {devices/code.sym} -10 -120 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 120 -120 0 0 {name=CORNER only_toplevel=true corner=tt}
C {inputs_latch_4neu.sym} 840 -220 0 0 {name=x1}
C {devices/vsource.sym} 100 -410 0 1 {name=V12 value="pulse(0 1.8 3ns 1ns 1ns 1us 2us 100)"}
C {devices/lab_pin.sym} 100 -470 0 0 {name=p19 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 100 -380 0 0 {name=p94 sig_type=std_logic lab=0}
C {devices/vsource.sym} 820 -360 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 820 -390 0 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 820 -330 0 0 {name=p42 sig_type=std_logic lab=0}
C {devices/vsource.sym} 100 -550 0 1 {name=V25 value="pulse(0 1.8 25ns 1ns 1ns 1.8ms 3.6ms 1)"}
C {devices/lab_pin.sym} 100 -610 0 0 {name=p75 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 100 -520 0 0 {name=p82 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 100 -320 0 0 {name=p31 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 100 -260 0 0 {name=V3 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 100 -210 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 370 -580 2 0 {name=p23 sig_type=std_logic lab=syn_addr[0]}
C {devices/vsource.sym} 370 -550 0 1 {name=V1 value="pulse(0 1.8 25ns 1ns 1ns 13us 26us 100)"}
C {devices/lab_pin.sym} 370 -520 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 370 -490 2 0 {name=p2 sig_type=std_logic lab=syn_addr[1]}
C {devices/vsource.sym} 370 -460 0 1 {name=V5 value="pulse(0 1.8 1ns 1ns 1ns 9us 18us 100)"}
C {devices/lab_pin.sym} 370 -430 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 370 -410 2 0 {name=p4 sig_type=std_logic lab=syn_addr[2]}
C {devices/vsource.sym} 370 -380 0 1 {name=V6 value="pulse(0 1.8 3ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 370 -350 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 370 -320 2 0 {name=p7 sig_type=std_logic lab=syn_addr[3]}
C {devices/vsource.sym} 370 -290 0 1 {name=V7 value="pulse(0 1.8 4ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 370 -260 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 820 -580 2 0 {name=p9 sig_type=std_logic lab=neu_addr[0]}
C {devices/vsource.sym} 820 -550 0 1 {name=V8 value="pulse(0 1.8 3ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 820 -520 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 820 -500 2 0 {name=p11 sig_type=std_logic lab=neu_addr[1]}
C {devices/vsource.sym} 820 -470 0 1 {name=V9 value="pulse(0 1.8 4ns 1ns 1ns 10us 20us 100)"}
C {devices/lab_pin.sym} 820 -440 0 0 {name=p12 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 690 -190 0 0 {name=p13 sig_type=std_logic lab=exc}
C {devices/lab_pin.sym} 690 -270 0 0 {name=p14 sig_type=std_logic lab=REQIN}
C {devices/lab_pin.sym} 690 -230 0 0 {name=p15 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 690 -250 2 1 {name=p16 sig_type=std_logic lab=syn_addr[0:3]}
C {devices/lab_pin.sym} 690 -210 2 1 {name=p17 sig_type=std_logic lab=neu_addr[0:1]}
C {devices/lab_pin.sym} 1020 -210 0 1 {name=p18 sig_type=std_logic lab=REQIN_ar}
C {devices/lab_pin.sym} 1020 -230 0 1 {name=p20 sig_type=std_logic lab=exc_ar}
C {devices/lab_pin.sym} 1020 -270 2 0 {name=p21 sig_type=std_logic lab=syn_addr_latched[0:3]}
C {devices/lab_pin.sym} 1020 -250 2 0 {name=p22 sig_type=std_logic lab=neu_addr_latched[0:1]}
C {devices/simulator_commands_shown.sym} 310 -110 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 100us
.PRINT TRAN format=raw file=input_latch_4_neu_tb.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
C {devices/lab_pin.sym} 990 -170 0 1 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 990 -190 0 1 {name=p24 sig_type=std_logic lab=VDD}
C {devices/simulator_commands_shown.sym} 310 40 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value=".save all
.control
  tran 0.01us 100us
  write input_latch_4_neu_tb.raw
  quit 0
.endc
"}
