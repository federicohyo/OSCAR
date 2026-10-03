v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Trim input pulse
 to about 0.5ns width} 140 -330 0 0 0.4 0.4 {}
T {Stretch input pulse
 controlled by bias setting} 570 -330 0 0 0.4 0.4 {}
N 510 -220 540 -220 {
lab=vpulseshort}
N 510 -240 540 -240 {
lab=vpulseextp}
N 120 -240 150 -240 {
lab=vspk}
N 130 -240 130 -200 {
lab=vspk}
N 130 -200 230 -200 {
lab=vspk}
N 440 -220 510 -220 {
lab=vpulseshort}
N 230 -200 320 -200 {
lab=vspk}
N 230 -240 320 -240 {
lab=#net1}
C {spike_extender.sym} 690 -220 0 0 {name=x1}
C {devices/lab_pin.sym} 840 -240 2 0 {name=p1 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 840 -200 2 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 510 -240 1 0 {name=p3 sig_type=std_logic lab=vpulseextp}
C {devices/lab_pin.sym} 120 -240 0 0 {name=p4 sig_type=std_logic lab=vspk}
C {devices/lab_pin.sym} 840 -220 2 0 {name=p5 sig_type=std_logic lab=spkext}
C {sky130_stdcells/clkdlybuf4s50_1.sym} 190 -240 0 0 {name=x3 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 460 -220 1 0 {name=p9 sig_type=std_logic lab=vpulseshort}
C {devices/iopin.sym} 90 -450 0 0 {name=p16 lab=GND
}
C {devices/iopin.sym} 90 -430 0 0 {name=p19 lab=VDD}
C {devices/ipin.sym} 85 -485 2 0 {name=p6 lab=vspk


}
C {devices/opin.sym} 235 -435 2 0 {name=p7 lab=spkext


}
C {devices/ipin.sym} 175 -485 2 0 {name=p10 lab=vpulseextp


}
C {sky130_stdcells/nor2b_1.sym} 380 -220 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
