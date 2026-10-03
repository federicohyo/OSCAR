v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1410 -1410 2240 -20 {flags=graph


ypos1=-0.41147219
ypos2=4.1496732
divy=1

unity=1
x1=0
x2=0.0001
divx=1
subdivx=4


node="A;a[3],a[2],a[1],a[0]
d[0]
d[1]
d[2]
d[3]
d[4]
d[5]
d[6]
d[7]
d[8]
d[9]
d[10]
d[11]
d[12]
d[13]
d[14]
d[15]"
color="7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7"

unitx=1
logx=0
logy=0
digital=1

rainbow=1



y1=0.
y2=2
subdivy=1
dataset=-1
xlabmag=1
ylabmag=1}
N 380 -790 380 -770 {
lab=0}
N 380 -880 380 -850 {
lab=A[2]}
N 380 -940 380 -920 {
lab=0}
N 380 -1030 380 -1000 {
lab=A[3]}
N 380 -490 380 -470 {
lab=0}
N 380 -580 380 -550 {
lab=A[0]}
N 380 -640 380 -620 {
lab=0}
N 380 -730 380 -700 {
lab=A[1]}
N 630 -480 630 -460 {
lab=0}
N 630 -570 630 -540 {
lab=VDD}
N 900 -490 900 -470 {
lab=0}
N 900 -580 900 -550 {
lab=req}
N 530 -830 580 -830 {
lab=A[0:3]}
C {devices/vsource.sym} 380 -820 0 1 {name=V12 value="pulse(0 1.8 10ns 1ns 1ns 40us 80us)"}
C {devices/lab_pin.sym} 380 -580 0 0 {name=p19 sig_type=std_logic lab=A[0]}
C {devices/vsource.sym} 380 -970 0 1 {name=V5 value="pulse(0 1.8 10ns 1ns 1ns 80us 160us)"}
C {devices/lab_pin.sym} 380 -730 0 0 {name=p39 sig_type=std_logic lab=A[1]}
C {devices/vsource.sym} 380 -520 0 1 {name=V3 value="pulse(0 1.8 10ns 1ns 1ns 10us 20us)"}
C {devices/lab_pin.sym} 380 -1030 0 0 {name=p1 sig_type=std_logic lab=A[3]}
C {devices/vsource.sym} 380 -670 0 1 {name=V4 value="pulse(0 1.8 10ns 1ns 1ns 20us 40us)"}
C {devices/lab_pin.sym} 380 -880 0 0 {name=p2 sig_type=std_logic lab=A[2]}
C {devices/code.sym} 380 -1290 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice)"}
C {devices/vsource.sym} 630 -510 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 630 -570 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 900 -520 0 1 {name=V1 value="pulse(0 1.8 3ns 1ns 1ns 1us 2us)"}
C {devices/lab_pin.sym} 900 -580 0 0 {name=p8 sig_type=std_logic lab=req}
C {decoder_4_to_16.sym} 730 -800 0 0 {name=x1}
C {devices/lab_pin.sym} 535 -830 2 1 {name=p13 sig_type=std_logic lab=A[0:3]}
C {devices/lab_pin.sym} 580 -810 0 0 {name=p3 sig_type=std_logic lab=req}
C {devices/lab_pin.sym} 880 -810 2 0 {name=p4 sig_type=std_logic lab=req_syn}
C {devices/lab_pin.sym} 880 -830 2 0 {name=p5 sig_type=std_logic lab=D[0:15]}
C {devices/simulator_commands_shown.sym} 640 -1125 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value="
.save all
.control
tran 0.01us 200us
write decoder_4_to_16_tb.raw
quit 0
.endc
"}
C {devices/lab_pin.sym} 380 -920 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 380 -770 0 0 {name=p7 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 380 -620 0 0 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 380 -470 0 0 {name=p10 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 880 -770 0 1 {name=p11 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 900 -470 0 0 {name=p12 sig_type=std_logic lab=0}
C {devices/simulator_commands_shown.sym} 630 -1265 0 0 {name=COMMANDS2
simulator=Xyce
only_toplevel=false 
value="
.TRAN 0.01us 200us
.PRINT TRAN format=raw file=decoder_4_to_16_tb.raw v(*) i(*)
"}
C {sky130_fd_pr/corner.sym} 230 -1290 0 0 {name=CORNER1 only_toplevel=false corner=tt}
C {devices/lab_pin.sym} 880 -790 0 1 {name=p14 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 630 -460 0 0 {name=p15 sig_type=std_logic lab=0}
