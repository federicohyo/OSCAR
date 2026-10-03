v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1100 -830 1660 -40 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=5e-05
divx=5
subdivx=1
xlabmag=0.5
ylabmag=0.5
node="A;a[0],a[1]
d[0]
d[1]
d[2]
d[3]"
color="7 6 6 6 6"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
N 470 -60 470 -40 {
lab=0}
N 470 -150 470 -120 {
lab=A[0]}
N 470 -210 470 -190 {
lab=0}
N 470 -300 470 -270 {
lab=A[1]}
N 720 -50 720 -30 {
lab=0}
N 720 -140 720 -110 {
lab=VDD}
N 990 -60 990 -40 {
lab=0}
N 990 -150 990 -120 {
lab=nReq}
C {devices/code.sym} 170 -430 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 10 -430 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 470 -150 0 0 {name=p19 sig_type=std_logic lab=A[0]}
C {devices/lab_pin.sym} 470 -300 0 0 {name=p39 sig_type=std_logic lab=A[1]}
C {devices/vsource.sym} 470 -90 0 1 {name=V3 value="pulse(0 1.8 10ns 1ns 1ns 20us 40us)"}
C {devices/vsource.sym} 470 -240 0 1 {name=V4 value="pulse(0 1.8 10ns 1ns 1ns 10us 20us)"}
C {devices/vsource.sym} 720 -80 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 720 -140 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 990 -90 0 1 {name=V1 value="pulse(1.8 0 3ns 1ns 1ns 1us 2us)"}
C {devices/lab_pin.sym} 990 -150 0 0 {name=p8 sig_type=std_logic lab=nReq}
C {decoder_2_to_4.sym} 800 -310 0 0 {name=x2}
C {devices/lab_pin.sym} 650 -320 2 1 {name=p13 sig_type=std_logic lab=A[0:1]}
C {devices/lab_pin.sym} 950 -280 2 0 {name=p5 sig_type=std_logic lab=D[0:3]}
C {devices/simulator_commands_shown.sym} 60 -605 0 0 {name=COMMANDS
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.01us 50us
.PRINT TRAN format=raw file=decoder_2_to_4_tb.raw v(*) i(*)
"}
C {devices/simulator_commands_shown.sym} 700 -625 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value="
.save all
.control
  tran 0.01us 100us
  write decoder_2_to_4_tb.raw
  quit 0
.endc
"}
C {devices/lab_pin.sym} 470 -190 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 470 -40 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 720 -30 0 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 990 -40 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 650 -340 0 0 {name=p4 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 950 -320 0 1 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 950 -340 0 1 {name=p7 sig_type=std_logic lab=VDD}
