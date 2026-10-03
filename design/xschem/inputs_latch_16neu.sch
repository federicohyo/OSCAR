v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 190 -425 265 -425 {
lab=req_inp}
N 190 -475 190 -425 {
lab=req_inp}
N 115 -475 190 -475 {
lab=req_inp}
N 190 -425 190 -195 {
lab=req_inp}
N 190 -345 265 -345 {
lab=req_inp}
N 190 -265 265 -265 {
lab=req_inp}
N 190 -160 270 -160 {
lab=req_inp}
N 190 -195 190 -160 {
lab=req_inp}
N 445 -425 490 -425 {
lab=syn_addr_latched[0:3]}
N 445 -345 485 -345 {
lab=neu_addr_latched[0:3]}
N 445 -265 480 -265 {
lab=exc_latched}
N 590 -160 610 -160 {
lab=req_in_array}
C {sky130_stdcells/dfrtp_1.sym} 355 -405 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/dfrtp_1.sym} 355 -325 0 0 {name=x1[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/dfrtp_1.sym} 355 -245 0 0 {name=x3 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 265 -325 0 0 {name=p46 lab=neu_addr_in[0:3]

}
C {devices/ipin.sym} 115 -475 0 0 {name=p1 lab=req_inp

}
C {devices/ipin.sym} 265 -405 0 0 {name=p45 lab=syn_addr_in[0:3]

}
C {devices/ipin.sym} 265 -245 0 0 {name=p47 lab=exc_in

}
C {sky130_stdcells/inv_1.sym} 310 -160 0 0 {name=x7 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 390 -160 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 470 -160 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 550 -160 0 0 {name=x4 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 110 -380 0 0 {name=p31 lab=nRes}
C {devices/lab_pin.sym} 110 -380 2 0 {name=p32 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 265 -385 2 1 {name=p2 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 265 -305 2 1 {name=p3 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 265 -225 2 1 {name=p4 sig_type=std_logic lab=nRes}
C {devices/opin.sym} 490 -425 0 0 {name=p5 lab=syn_addr_latched[0:3]

}
C {devices/opin.sym} 485 -345 0 0 {name=p6 lab=neu_addr_latched[0:3]

}
C {devices/opin.sym} 480 -265 0 0 {name=p7 lab=exc_latched

}
C {devices/opin.sym} 610 -160 0 0 {name=p8 lab=req_in_array

}
C {devices/iopin.sym} 135 -85 0 0 {name=p9 lab=VDD

}
C {devices/iopin.sym} 135 -65 0 0 {name=p10 lab=GND

}
