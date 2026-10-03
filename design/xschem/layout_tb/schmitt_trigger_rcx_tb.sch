v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 810 -610 1610 -210 {flags=graph
y1=-0.016
y2=1.9
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.8
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=y
color=4
dataset=-1
unitx=1
logx=0
logy=0
sweep=a}
B 2 810 -1030 1610 -630 {flags=graph
y1=-5.2e-07
y2=3.4e-05
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.2e-05
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="\\"i(vdd); 0 i(vdd) -\\""
color=5
dataset=-1
unitx=1
logx=0
logy=0
}
N 190 -440 190 -420 {
lab=A}
N 550 -370 550 -350 {
lab=VDD}
N 550 -270 550 -255 {
lab=GND}
C {schmitt_trigger.sym} 590 -310 0 0 {name=x1
schematic=schmitt_trigger_rcx
spice_sym_def="tcleval(.include [abs_sym_path schmitt_trigger_rcx.spice])"
tclcommand="textwindow [abs_sym_path schmitt_trigger_rcx.spice]"}
C {devices/vdd.sym} 190 -270 0 0 {name=l3 lab=VDD}
C {devices/vsource.sym} 190 -240 0 0 {name=Vdd value=1.8 savecurrent=false}
C {devices/gnd.sym} 190 -210 0 0 {name=l4 lab=GND}
C {devices/gnd.sym} 190 -360 0 0 {name=l5 lab=GND}
C {devices/vsource.sym} 190 -390 0 0 {name=Vin value="pulse(0 1.8 0u 5u 5u 1u 12u)" savecurrent=false}
C {devices/simulator_commands_shown.sym} 400 -570 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value=".option method=gear
.save all
.control
  tran 0.1u 12u
  write schmitt_trigger_rcx_tb.raw
 * quit 0
.endc"}
C {sky130_fd_pr/corner.sym} 160 -600 0 0 {name=CORNER only_toplevel=false corner=ss}
C {devices/lab_pin.sym} 510 -310 0 0 {name=p1 lab=A}
C {devices/lab_pin.sym} 610 -310 0 1 {name=p2 lab=Y}
C {devices/lab_pin.sym} 190 -440 0 1 {name=p4 lab=A}
C {devices/lab_pin.sym} 550 -370 0 1 {name=p3 lab=VDD}
C {devices/lab_pin.sym} 550 -255 0 1 {name=p5 lab=GND}
