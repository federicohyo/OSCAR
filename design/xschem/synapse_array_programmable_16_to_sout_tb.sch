v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Power up reset} 145 -455 0 0 0.4 0.4 {}
T {Excitatory syn} 1400 -790 0 0 0.4 0.4 {}
T {synapse address 4 bit encoded} 680 -30 0 0 0.4 0.4 {}
N 1110 -480 1260 -480 {
lab=sout}
N 1260 -420 1260 -380 {
lab=#net1}
N 165 -505 165 -485 {
lab=GND}
N 165 -595 165 -565 {
lab=resetW}
N 270 -290 270 -270 {
lab=GND}
N 270 -380 270 -350 {
lab=VDD}
N 170 -390 170 -360 {
lab=GND}
N 170 -360 170 -290 {
lab=GND}
N 1435 -630 1435 -610 {
lab=GND}
N 1435 -720 1435 -690 {
lab=vtaudpip}
N 1535 -630 1535 -610 {
lab=GND}
N 1535 -720 1535 -690 {
lab=vthrdpin}
N 1640 -640 1640 -620 {
lab=GND}
N 1640 -730 1640 -700 {
lab=vstddpin}
N 1310 -620 1310 -600 {
lab=GND}
N 1310 -710 1310 -680 {
lab=vspke}
N 1790 -640 1790 -620 {
lab=GND}
N 1790 -730 1790 -700 {
lab=vpulseextp}
N 710 -460 810 -460 {
lab=W[0:1]}
N 650 -460 710 -460 {
lab=W[0:1]}
N 650 -490 650 -460 {
lab=W[0:1]}
N 1785 -375 1785 -355 {
lab=GND}
N 1785 -465 1785 -435 {
lab=setW}
C {synapse_array_programmable_16_to_sout.sym} 960 -400 0 0 {name=x1}
C {devices/code_shown.sym} 530 -750 0 0 {name=SPICE only_toplevel=false value="

.save all

.control
tran 0.01us 500us
write synapse_array_programmable_16_to_sout_tb.raw
set appendwrite
plot setW resetW+2 x1.x2.x3.vsin+4 
.endc
"}
C {devices/res.sym} 1260 -350 0 0 {name=R1
value=1
footprint=1206
device=resistor
m=1}
C {devices/gnd.sym} 1260 -320 0 0 {name=l10 lab=GND value="0"}
C {devices/lab_pin.sym} 1200 -480 1 0 {name=p13 sig_type=std_logic lab=sout}
C {devices/ammeter.sym} 1260 -450 0 0 {name=Vmeas savecurrent=true}
C {devices/lab_pin.sym} 1110 -460 2 0 {name=p11 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1110 -440 2 0 {name=p12 sig_type=std_logic lab=VDD}
C {devices/code.sym} 270 -740 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice

* Power domains
VSTDCELL_PWR VPWR 0 DC 1.8
VSTDCELL_PB  VPB  0 DC 1.8
VSTDCELL_NB  VNB  0 DC 0
VSTDCELL_GND VGND 0 DC 0
.global VNB VGND VPB VPWR
)"}
C {sky130_fd_pr/corner.sym} 120 -740 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/gnd.sym} 165 -485 0 0 {name=l12 lab=GND value="0"}
C {devices/lab_pin.sym} 165 -595 0 0 {name=p51 sig_type=std_logic lab=resetW}
C {devices/vsource.sym} 165 -535 0 0 {name=V11 value="pulse(0 1.8 1ns 15ns 1ns 29us 200us 1)"}
C {devices/vsource.sym} 270 -320 0 0 {name=V2 value=1.8}
C {devices/gnd.sym} 270 -270 0 0 {name=l6 lab=GND value="0"}
C {devices/lab_pin.sym} 270 -380 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} 170 -290 0 0 {name=l9 lab=GND value="0"}
C {devices/lab_pin.sym} 170 -390 0 0 {name=p48 sig_type=std_logic lab=GND}
C {devices/vsource.sym} 1435 -660 0 0 {name=V7 value=1.5}
C {devices/gnd.sym} 1435 -610 0 0 {name=l8 lab=GND value="0"}
C {devices/lab_pin.sym} 1435 -720 0 0 {name=p16 sig_type=std_logic lab=vtaudpip}
C {devices/vsource.sym} 1535 -660 0 0 {name=V13 value=0.9}
C {devices/gnd.sym} 1535 -610 0 0 {name=l14 lab=GND value="0"}
C {devices/lab_pin.sym} 1535 -720 0 0 {name=p26 sig_type=std_logic lab=vthrdpin}
C {devices/vsource.sym} 1640 -670 0 0 {name=V10 value=0.47}
C {devices/gnd.sym} 1640 -620 0 0 {name=l11 lab=GND value="0"}
C {devices/lab_pin.sym} 1640 -730 0 0 {name=p39 sig_type=std_logic lab=vstddpin}
C {devices/vsource.sym} 1310 -650 0 1 {name=V12 value="pulse(0 1.8 10ns 1ns 1ns 1ns 20us 100)"}
C {devices/gnd.sym} 1310 -600 0 0 {name=l13 lab=GND value="0"}
C {devices/lab_pin.sym} 1310 -710 0 0 {name=p19 sig_type=std_logic lab=vspke}
C {devices/vsource.sym} 1790 -670 0 0 {name=V6 value=0.5}
C {devices/gnd.sym} 1790 -620 0 0 {name=l7 lab=GND value="0"}
C {devices/lab_pin.sym} 1790 -730 0 0 {name=p85 sig_type=std_logic lab=vpulseextp}
C {devices/lab_pin.sym} 810 -380 0 0 {name=p1 sig_type=std_logic lab=vspke}
C {devices/lab_pin.sym} 810 -360 0 0 {name=p2 sig_type=std_logic lab=vtaudpip
}
C {devices/lab_pin.sym} 810 -420 0 0 {name=p4 sig_type=std_logic lab=vthrdpin
}
C {devices/lab_pin.sym} 810 -480 0 0 {name=p5 sig_type=std_logic lab=vstddpin
}
C {devices/lab_pin.sym} 810 -320 0 0 {name=p7 sig_type=std_logic lab=vpulseextp}
C {devices/lab_pin.sym} 810 -400 0 0 {name=p3 sig_type=std_logic lab=resetW}
C {devices/bus_connect.sym} 650 -465 1 1 {name=l2 lab=W[1]}
C {devices/bus_connect.sym} 650 -485 1 1 {name=l5 lab=W[0]}
C {devices/lab_pin.sym} 670 -460 3 0 {name=p10 sig_type=std_logic lab=W[0:1]
}
C {devices/lab_pin.sym} 810 -340 0 0 {name=p8 sig_type=std_logic lab=setW}
C {devices/lab_pin.sym} 1650 -440 2 0 {name=p9 sig_type=std_logic lab=W[1]}
C {devices/lab_pin.sym} 1650 -370 2 0 {name=p14 sig_type=std_logic lab=W[0]}
C {devices/lab_pin.sym} 1650 -400 2 0 {name=p6 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1650 -330 2 0 {name=p15 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1650 -420 2 0 {name=p17 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1650 -350 2 0 {name=p18 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} 1785 -355 0 0 {name=l1 lab=GND value="0"}
C {devices/lab_pin.sym} 1785 -465 0 0 {name=p20 sig_type=std_logic lab=setW}
C {devices/vsource.sym} 1785 -405 0 0 {name=V1 value="pulse(0 1.8 1ns 30ns 1ns 60us 120us 2)"}
C {tie_low.sym} 1500 -350 0 0 {name=x3}
C {tie_low.sym} 1500 -420 0 0 {name=x2}
C {devices/lab_pin.sym} 1160 -170 2 0 {name=p21 sig_type=std_logic lab=syn_addr[2]}
C {devices/lab_pin.sym} 1160 -130 2 0 {name=p23 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1160 -60 2 0 {name=p24 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1160 -150 2 0 {name=p25 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1160 -80 2 0 {name=p27 sig_type=std_logic lab=VDD}
C {tie_low.sym} 1010 -80 0 0 {name=x4}
C {tie_low.sym} 1010 -150 0 0 {name=x5}
C {devices/lab_pin.sym} 720 -180 2 0 {name=p28 sig_type=std_logic lab=syn_addr[0]}
C {devices/lab_pin.sym} 720 -110 2 0 {name=p29 sig_type=std_logic lab=syn_addr[1]}
C {devices/lab_pin.sym} 720 -140 2 0 {name=p30 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 720 -70 2 0 {name=p31 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 720 -160 2 0 {name=p32 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 720 -90 2 0 {name=p33 sig_type=std_logic lab=VDD}
C {tie_low.sym} 570 -90 0 0 {name=x6}
C {tie_hi.sym} 570 -160 0 0 {name=x7}
C {devices/lab_pin.sym} 1160 -100 2 0 {name=p22 sig_type=std_logic lab=syn_addr[3]}
C {devices/lab_pin.sym} 810 -440 0 0 {name=p34 sig_type=std_logic lab=syn_addr[0:3]}
