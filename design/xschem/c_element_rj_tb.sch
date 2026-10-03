v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1360 -630 2160 -230 {flags=graph
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
node="va
vb
nc1porta
nc1portb
nc1portc"
color="6 5 8 10 16"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
T {Power up reset} 405 -225 0 0 0.4 0.4 {}
T {c elements with fan-out of 3} 630 -760 0 0 0.4 0.4 {}
N 60 -280 60 -260 {
lab=0}
N 60 -370 60 -340 {
lab=VA}
N 60 -120 60 -100 {
lab=0}
N 60 -210 60 -180 {
lab=VB}
N 365 -125 365 -105 {
lab=0}
N 365 -215 365 -185 {
lab=nRes}
N 660 -130 660 -110 {
lab=0}
N 660 -220 660 -190 {
lab=VDD}
N 650 -380 680 -380 {
lab=VA}
N 640 -360 680 -360 {
lab=VB}
N 640 -340 680 -340 {
lab=nRes}
N 1070 -370 1090 -370 {
lab=c_rj}
N 1070 -370 1070 -330 {
lab=c_rj}
N 1070 -330 1090 -330 {
lab=c_rj}
N 1070 -300 1090 -290 {
lab=c_rj}
N 1070 -330 1070 -300 {
lab=c_rj}
N 980 -380 1070 -380 {
lab=c_rj}
N 1070 -380 1070 -370 {
lab=c_rj}
N 1170 -370 1210 -370 {
lab=nc1porta}
N 1170 -330 1200 -330 {
lab=nc1portb}
N 1170 -290 1210 -290 {
lab=nc1portc}
C {devices/lab_pin.sym} 60 -370 0 0 {name=p1 sig_type=std_logic lab=VA}
C {devices/vsource.sym} 60 -310 0 0 {name=V1 value="dc 0 pulse(0 1.8 1ns 1ns 1ns 7ns 14ns)"}
C {devices/lab_pin.sym} 60 -210 0 0 {name=p2 sig_type=std_logic lab=VB}
C {devices/vsource.sym} 60 -150 0 0 {name=V3 value="dc 0 pulse(0 1.8 1ns 1ns 1ns 9ns 18ns)"}
C {devices/lab_pin.sym} 365 -215 0 0 {name=p51 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 365 -155 0 0 {name=V4 value="dc 0 pulse(1.8 0 2ns 1ns 1ns 20ns 2us)"}
C {sky130_fd_pr/corner.sym} 880 -620 0 0 {name=CORNER only_toplevel=false corner=ss}
C {devices/vsource.sym} 660 -160 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 660 -220 0 0 {name=p15 sig_type=std_logic lab=VDD}
C {c_element_rj.sym} 830 -360 0 0 {name=x1}
C {devices/lab_pin.sym} 650 -380 0 0 {name=p3 sig_type=std_logic lab=VA}
C {devices/lab_pin.sym} 640 -360 0 0 {name=p5 sig_type=std_logic lab=VB}
C {devices/lab_pin.sym} 640 -340 0 0 {name=p41 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 980 -340 2 0 {name=p7 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 980 -360 0 1 {name=p9 sig_type=std_logic lab=0}
C {sky130_stdcells/inv_1.sym} 1130 -370 0 0 {name=x2 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1130 -290 0 0 {name=x3 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1130 -330 0 0 {name=x4 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1210 -370 0 1 {name=p26 sig_type=std_logic lab=nc1porta}
C {devices/lab_pin.sym} 1200 -330 0 1 {name=p27 sig_type=std_logic lab=nc1portb}
C {devices/lab_pin.sym} 1210 -290 0 1 {name=p28 sig_type=std_logic lab=nc1portc}
C {devices/code.sym} 730 -620 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {devices/lab_pin.sym} 1040 -380 1 0 {name=p46 sig_type=std_logic lab=c_rj}
C {devices/lab_pin.sym} 60 -100 0 0 {name=p4 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 60 -260 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 365 -105 0 0 {name=p8 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 660 -110 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/simulator_commands_shown.sym} 40 -750 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value=".save all
.control
  tran 0.1ns 200ns
  write c_element_rj_tb.raw
  quit 0
.endc
"}
C {devices/simulator_commands_shown.sym} 40 -510 0 0 {name=COMMANDS1
simulator=xyce
only_toplevel=false 
value=".TRAN 0.1ns 200ns
.PRINT TRAN format=raw file=c_element_rj_tb.raw v(*) i(*)
"}
