v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Power up reset} 170 -550 0 0 0.4 0.4 {}
N 970 -590 970 -570 {
lab=GND}
N 970 -680 970 -650 {
lab=VDD}
N 880 -670 880 -640 {
lab=GND}
N 880 -640 880 -570 {
lab=GND}
N 210 -400 210 -380 {
lab=GND}
N 210 -490 210 -460 {
lab=nRes}
N 495 -600 495 -580 {
lab=GND}
N 495 -690 495 -660 {
lab=clk}
N 730 -595 730 -575 {
lab=GND}
N 730 -685 730 -655 {
lab=Da}
N 545 -400 545 -380 {
lab=GND}
N 545 -490 545 -460 {
lab=sDone}
N 980 -260 1020 -260 {
lab=clk}
N 980 -280 1020 -280 {
lab=Da}
N 1000 -220 1020 -220 {
lab=sDone}
N 1320 -280 1340 -280 {
lab=D[0:3]}
N 1320 -260 1350 -260 {
lab=Dout}
C {devices/code_shown.sym} 1150 -600 0 0 {name=SPICE only_toplevel=false value="

.save all

.control
tran 0.01us 500us
write dflip_flop_chain_fc_tb.raw
set appendwrite
plot D0 D1+2 D2+4 D3+6
.endc
"}
C {devices/vsource.sym} 970 -620 0 0 {name=V2 value=1.8}
C {devices/gnd.sym} 970 -570 0 0 {name=l5 lab=GND value="0"}
C {devices/lab_pin.sym} 970 -680 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} 880 -570 0 0 {name=l1 lab=GND value="0"}
C {devices/lab_pin.sym} 880 -670 0 0 {name=p36 sig_type=std_logic lab=GND}
C {devices/gnd.sym} 210 -380 0 0 {name=l12 lab=GND value="0"}
C {devices/lab_pin.sym} 210 -490 0 0 {name=p51 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 210 -430 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 1ms 1)"}
C {devices/vsource.sym} 495 -630 0 1 {name=V18 value="pulse(0 1.8 10ns 1ns 1ns 5us 10us)"}
C {devices/gnd.sym} 495 -580 0 0 {name=l17 lab=GND value="0"}
C {devices/lab_pin.sym} 495 -690 0 0 {name=p42 sig_type=std_logic lab=clk}
C {devices/vsource.sym} 730 -625 0 1 {name=V19 value="pulse(0 1.8 10ns 1ns 1ns 10us 20us)"}
C {devices/gnd.sym} 730 -575 0 0 {name=l18 lab=GND value="0"}
C {devices/lab_pin.sym} 730 -685 0 0 {name=p43 sig_type=std_logic lab=Da}
C {devices/code.sym} 970 -470 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice

* Power domains
VSTDCELL_PWR VPWR 0 DC 1.8
VSTDCELL_PB  VPB  0 DC 1.8
VSTDCELL_NB  VNB  0 DC 0
VSTDCELL_GND VGND 0 DC 0
.global VNB VGND VPB VPWR
)"}
C {sky130_fd_pr/corner.sym} 810 -470 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/vsource.sym} 545 -430 0 1 {name=V1 value="pulse(1.8 0 40ns 1ns 1ns 5us 10us)"}
C {devices/gnd.sym} 545 -380 0 0 {name=l2 lab=GND value="0"}
C {devices/lab_pin.sym} 545 -490 0 0 {name=p8 sig_type=std_logic lab=sDone}
C {dflip_flop_chain_4_fc.sym} 1170 -250 0 0 {name=x5}
C {devices/lab_pin.sym} 985 -260 0 0 {name=p5 sig_type=std_logic lab=clk}
C {devices/lab_pin.sym} 980 -280 0 0 {name=p17 sig_type=std_logic lab=Da}
C {devices/lab_pin.sym} 1020 -240 0 0 {name=p18 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1000 -220 0 0 {name=p19 sig_type=std_logic lab=sDone}
C {devices/lab_pin.sym} 1335 -280 2 0 {name=p1 sig_type=std_logic lab=D[0:3]
}
C {devices/lab_pin.sym} 1345 -260 2 0 {name=p2 sig_type=std_logic lab=Dout

}
