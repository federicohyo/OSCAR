v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1010 -450 1810 -50 {flags=graph
y1=-0.86
y2=2
ypos1=-0.288
ypos2=2.572
divy=5
subdivy=1
unity=1
x1=0
x2=2e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="\\"i(vdd) -1e5 *\\"
vspk
extended
x1.vpulseshort
x1.x1.net1"
color="9 5 6 8 4"
dataset=-1
unitx=1
logx=0
logy=0
digital=1}
T {delay pulse} 650 -710 0 0 0.4 0.4 {}
N 140 -450 140 -430 {
lab=0}
N 140 -540 140 -510 {
lab=VDD}
N 670 -450 670 -430 {
lab=0}
N 670 -540 670 -510 {
lab=vpulseextackp}
N 440 -450 440 -430 {
lab=0}
N 440 -540 440 -510 {
lab=vspk}
N 710 -570 740 -570 {
lab=vpulseextackp}
N 720 -570 720 -520 {
lab=vpulseextackp}
N 670 -520 720 -520 {
lab=vpulseextackp}
N 670 -620 670 -600 {
lab=VDD}
N 670 -600 670 -570 {
lab=VDD}
C {devices/code.sym} 200 -730 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice

* Power domains
VSTDCELL_PWR VPWR 0 DC 1.8
VSTDCELL_PB  VPB  0 DC 1.8
VSTDCELL_NB  VNB  0 DC 0
VSTDCELL_GND VGND 0 DC 0
.global VNB VGND VPB VPWR
)"}
C {sky130_fd_pr/corner.sym} 40 -730 0 0 {name=CORNER only_toplevel=true corner=ss}
C {devices/vsource.sym} 140 -480 0 0 {name=Vdd value=1.8}
C {devices/lab_pin.sym} 140 -540 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 600 -250 2 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 600 -210 2 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 740 -570 0 1 {name=p100 sig_type=std_logic lab=vpulseextackp}
C {devices/lab_pin.sym} 300 -250 2 1 {name=p3 sig_type=std_logic lab=vpulseextackp}
C {devices/vsource.sym} 440 -480 0 1 {name=Vin value="pulse(0 1.8 1ns 1ns 1ns 1ns 10us)"}
C {devices/lab_pin.sym} 440 -540 0 0 {name=p19 sig_type=std_logic lab=vspk}
C {devices/lab_pin.sym} 300 -230 0 0 {name=p4 sig_type=std_logic lab=vspk}
C {devices/lab_pin.sym} 600 -230 2 0 {name=p5 sig_type=std_logic lab=extended}
C {devices/lab_pin.sym} 670 -430 0 0 {name=p6 sig_type=std_logic lab=0

}
C {devices/lab_pin.sym} 440 -430 0 0 {name=p7 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 140 -430 0 0 {name=p8 sig_type=std_logic lab=0}
C {sky130_fd_pr/pfet_01v8.sym} 690 -570 0 1 {name=M6
L=2
W=1
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 670 -620 0 0 {name=p10 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 670 -480 0 0 {name=Ibias value=0.5u}
C {devices/simulator_commands_shown.sym} 360 -880 0 0 {name=COMMANDS2
simulator=xyce
only_toplevel=false 
value="
.TRAN 0.1ns 20ns
.PRINT TRAN format=raw file=spike_extender_tb.raw v(*) i(*)
"}
C {devices/simulator_commands_shown.sym} 1010 -880 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value=".option method=gear
.save all
.control
  let I_vec = vector(10)
  let T_vec = vector(10)
  let idx = 0
  foreach Ibiasc 0.5u 0.4u 0.3u 0.2u 0.1u 90n 80n 70n 50n 25n
    alter Ibias $Ibiasc
    tran 0.01ns 1000ns

    write spike_extender_tb.raw
    set appendwrite

    meas tran t_pulse trig extended val=0.9 rise=1 targ extended val=0.9 fall=1
    let I_vec[idx] = $Ibiasc
    let T_vec[idx] = t_pulse
    let idx = idx + 1
  end
  plot T_vec vs I_vec xlog ylog
  quit 0
.endc
"
spice_ignore=true}
C {devices/simulator_commands_shown.sym} 1010 -1100 0 0 {name=COMMANDS3
simulator=ngspice
only_toplevel=false 
value=".option method=gear
.save all
.control
  tran 0.01ns 20ns
  write spike_extender_tb.raw
  meas tran t_pulse trig extended val=0.9 rise=1 targ extended val=0.9 fall=1
.endc
"}
C {spike_extender_with_trimming.sym} 450 -230 0 0 {name=x1}
