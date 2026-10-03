v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 460 -210 510 -210 {
lab=#net1}
N 460 -380 500 -380 {
lab=#net2}
N 590 -210 750 -210 {
lab=#net3}
N 750 -220 750 -210 {
lab=#net3}
N 750 -220 780 -220 {
lab=#net3}
N 700 -210 700 -110 {
lab=#net3}
N 700 -110 780 -110 {
lab=#net3}
N 480 -320 480 -210 {
lab=#net1}
N 480 -330 480 -320 {
lab=#net1}
N 480 -330 780 -330 {
lab=#net1}
N 660 -460 780 -460 {
lab=#net1}
N 660 -460 660 -330 {
lab=#net1}
N 610 -150 780 -150 {
lab=#net4}
N 610 -380 610 -150 {
lab=#net4}
N 610 -370 780 -370 {
lab=#net4}
N 580 -380 610 -380 {
lab=#net4}
N 490 -500 780 -500 {
lab=#net2}
N 490 -500 490 -380 {
lab=#net2}
N 680 -260 780 -260 {
lab=#net2}
N 680 -500 680 -260 {
lab=#net2}
N 900 -480 940 -480 {
lab=#net5}
N 900 -130 940 -130 {
lab=#net6}
N 900 -240 940 -240 {
lab=#net7}
N 900 -350 940 -350 {
lab=#net8}
N 470 -50 520 -50 {
lab=#net9}
C {devices/ipin.sym} 105 -80 0 0 {name=p17 lab=A[0:1]


}
C {devices/opin.sym} 135 -70 0 0 {name=p21 lab=D[0:3]}
C {devices/lab_pin.sym} 380 -210 0 0 {name=p65 sig_type=std_logic lab=A[0]}
C {devices/lab_pin.sym} 380 -380 0 0 {name=p66 sig_type=std_logic lab=A[1]}
C {sky130_stdcells/inv_1.sym} 420 -210 0 0 {name=x3 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 420 -380 0 0 {name=x7 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 540 -380 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 550 -210 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 980 -480 0 0 {name=x10 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 980 -350 0 0 {name=x11 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 980 -240 0 0 {name=x12 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 980 -130 0 0 {name=x13 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1020 -480 2 0 {name=p6 sig_type=std_logic lab=D[0]}
C {devices/lab_pin.sym} 1020 -350 2 0 {name=p7 sig_type=std_logic lab=D[1]}
C {devices/lab_pin.sym} 1020 -240 2 0 {name=p8 sig_type=std_logic lab=D[2]}
C {devices/lab_pin.sym} 1020 -130 2 0 {name=p9 sig_type=std_logic lab=D[3]}
C {sky130_stdcells/nand2_1.sym} 840 -240 0 0 {name=x4 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} 840 -130 0 0 {name=x5 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} 840 -350 0 0 {name=x6 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nand2_1.sym} 840 -480 0 0 {name=x8 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 235 -110 0 0 {name=p1 lab=REQ_IN


}
C {devices/opin.sym} 275 -110 0 0 {name=p2 lab=REQ_OUT}
C {devices/lab_pin.sym} 390 -50 0 0 {name=p3 sig_type=std_logic lab=REQ_IN}
C {sky130_stdcells/inv_1.sym} 430 -50 0 0 {name=x9 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 560 -50 0 0 {name=x14 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 760 -50 2 0 {name=p4 sig_type=std_logic lab=REQ_OUT}
C {sky130_stdcells/inv_1.sym} 640 -50 0 0 {name=x15 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 720 -50 0 0 {name=x16 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/iopin.sym} 65 -230 0 0 {name=p5 lab=VDD}
C {devices/iopin.sym} 65 -200 0 0 {name=p10 lab=GND}
