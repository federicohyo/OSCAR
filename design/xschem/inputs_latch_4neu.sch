v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 200 -445 275 -445 {
lab=req_inp}
N 200 -495 200 -445 {
lab=req_inp}
N 125 -495 200 -495 {
lab=req_inp}
N 200 -445 200 -215 {
lab=req_inp}
N 200 -365 275 -365 {
lab=req_inp}
N 200 -285 275 -285 {
lab=req_inp}
N 200 -180 280 -180 {
lab=req_inp}
N 200 -215 200 -180 {
lab=req_inp}
N 455 -445 500 -445 {
lab=syn_addr_latched[0:3]}
N 455 -365 495 -365 {
lab=neu_addr_latched[0:1]}
N 455 -285 490 -285 {
lab=exc_latched}
N 600 -180 620 -180 {
lab=req_in_array}
C {sky130_stdcells/dfrtp_1.sym} 365 -425 0 0 {name=x2[0:3] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/dfrtp_1.sym} 365 -345 0 0 {name=x1[0:1] VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/dfrtp_1.sym} 365 -265 0 0 {name=x3 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 275 -345 0 0 {name=p46 lab=neu_addr_in[0:1]

}
C {devices/ipin.sym} 125 -495 0 0 {name=p1 lab=req_inp

}
C {devices/ipin.sym} 275 -425 0 0 {name=p45 lab=syn_addr_in[0:3]

}
C {devices/ipin.sym} 275 -265 0 0 {name=p47 lab=exc_in

}
C {sky130_stdcells/inv_1.sym} 320 -180 0 0 {name=x7 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 400 -180 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 480 -180 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 560 -180 0 0 {name=x4 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 120 -400 0 0 {name=p31 lab=nRes}
C {devices/lab_pin.sym} 120 -400 2 0 {name=p32 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 275 -405 2 1 {name=p2 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 275 -325 2 1 {name=p3 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 275 -245 2 1 {name=p4 sig_type=std_logic lab=nRes}
C {devices/opin.sym} 500 -445 0 0 {name=p5 lab=syn_addr_latched[0:3]

}
C {devices/opin.sym} 495 -365 0 0 {name=p6 lab=neu_addr_latched[0:1]

}
C {devices/opin.sym} 490 -285 0 0 {name=p7 lab=exc_latched

}
C {devices/opin.sym} 620 -180 0 0 {name=p8 lab=req_in_array

}
C {devices/iopin.sym} 125 -155 0 0 {name=p9 lab=VDD

}
C {devices/iopin.sym} 125 -135 0 0 {name=p10 lab=GND

}
