v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Power up reset} 675 -275 0 0 0.4 0.4 {}
N 180 -90 200 -90 {
lab=RESET_B}
N 180 -90 180 -80 {
lab=RESET_B}
N 695 -325 695 -305 {
lab=GND}
N 695 -415 695 -385 {
lab=RESET_B}
N 800 -110 800 -90 {
lab=GND}
N 800 -200 800 -170 {
lab=VDD}
N 700 -210 700 -180 {
lab=GND}
N 700 -180 700 -110 {
lab=GND}
N 785 -415 785 -395 {
lab=GND}
N 785 -505 785 -475 {
lab=CLK}
C {sky130_stdcells/dfrtp_1.sym} 290 -110 0 0 {name=x5 VGND=VGND VNB=VNB VPB=VPB VPWR=VPWR prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 200 -110 0 0 {name=p7 sig_type=std_logic lab=D0}
C {devices/lab_pin.sym} 200 -130 0 0 {name=p20 sig_type=std_logic lab=CLK}
C {devices/lab_pin.sym} 180 -80 0 0 {name=p1 sig_type=std_logic lab=RESET_B}
C {devices/code_shown.sym} 340 -430 0 0 {name=SPICE only_toplevel=false value="

.save all

.control
tran 0.01us 500us
write dflip_flop_tb.raw
set appendwrite
plot D0 Q+2 CLK+4 RESET_B+6
.endc
"}
C {devices/code.sym} 190 -380 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice

* Power domains
VSTDCELL_PWR VPWR 0 DC 1.8
VSTDCELL_PB  VPB  0 DC 1.8
VSTDCELL_NB  VNB  0 DC 0
VSTDCELL_GND VGND 0 DC 0
.global VNB VGND VPB VPWR
)"}
C {sky130_fd_pr/corner.sym} 30 -380 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 380 -130 2 0 {name=p2 sig_type=std_logic lab=Q}
C {devices/gnd.sym} 695 -305 0 0 {name=l12 lab=GND value="0"}
C {devices/lab_pin.sym} 695 -415 0 0 {name=p51 sig_type=std_logic lab=RESET_B}
C {devices/vsource.sym} 695 -355 0 0 {name=V11 value="pulse(1.8 0 1ns 15ns 1ns 29us 200us 2)"}
C {devices/vsource.sym} 800 -140 0 0 {name=V2 value=1.8}
C {devices/gnd.sym} 800 -90 0 0 {name=l6 lab=GND value="0"}
C {devices/lab_pin.sym} 800 -200 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} 700 -110 0 0 {name=l9 lab=GND value="0"}
C {devices/lab_pin.sym} 700 -210 0 0 {name=p48 sig_type=std_logic lab=GND}
C {devices/gnd.sym} 785 -395 0 0 {name=l1 lab=GND value="0"}
C {devices/lab_pin.sym} 785 -505 0 0 {name=p3 sig_type=std_logic lab=CLK}
C {devices/vsource.sym} 785 -445 0 0 {name=V1 value="pulse(0 1.8 1ns 30ns 1ns 60us 120us 2)"}
C {devices/lab_pin.sym} 1190 -150 2 0 {name=p9 sig_type=std_logic lab=D0}
C {tie_hi.sym} 1040 -130 0 0 {name=x1}
C {devices/lab_pin.sym} 1190 -110 2 0 {name=p6 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1190 -130 2 0 {name=p17 sig_type=std_logic lab=VDD}
