v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1320 -270 1360 -270 {
lab=gc}
N 990 -230 1020 -230 {
lab=ack_out}
N 990 -230 990 -190 {
lab=ack_out}
N 990 -190 1310 -190 {
lab=ack_out}
N 1320 -360 1360 -360 {
lab=ack_outi[0:1]}
N 1360 -380 1360 -360 {
lab=ack_outi[0:1]}
N 890 -480 890 -340 {
lab=gc}
N 890 -340 1020 -340 {
lab=gc}
N 990 -360 1020 -360 {
lab=rc[0:1]}
N 990 -420 990 -360 {
lab=rc[0:1]}
N 990 -430 990 -420 {
lab=rc[0:1]}
C {arbiter_three_2.sym} 1170 -330 0 0 {name=x3}
C {c_element_rj.sym} 1170 -250 0 0 {name=x11}
C {devices/lab_pin.sym} 1020 -250 0 0 {name=p7 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 1310 -190 2 0 {name=p10 sig_type=std_logic lab=ack_out}
C {devices/lab_pin.sym} 280 -380 0 0 {name=p200 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1320 -230 2 0 {name=p11 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1320 -250 2 0 {name=p12 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1360 -270 2 0 {name=p13 sig_type=std_logic lab=gc}
C {devices/bus_connect.sym} 1360 -380 1 1 {name=l25 lab=ack_outi[0]}
C {devices/bus_connect.sym} 1360 -360 1 1 {name=l26 lab=ack_outi[1]}
C {devices/lab_pin.sym} 1340 -360 3 1 {name=p194 sig_type=std_logic lab=ack_outi[0:1]}
C {devices/bus_connect.sym} 990 -430 1 1 {name=l24 lab=rc[1]}
C {devices/lab_pin.sym} 890 -475 2 1 {name=p192 sig_type=std_logic lab=gc}
C {devices/bus_connect.sym} 990 -420 3 1 {name=l27 lab=rc[0]}
C {devices/lab_pin.sym} 990 -380 0 1 {name=p193 sig_type=std_logic lab=rc[0:1]}
C {arbiter_three_8.sym} 430 -440 0 0 {name=x4}
C {arbiter_three_8.sym} 430 -170 0 0 {name=x5}
C {devices/lab_pin.sym} 1320 -340 2 0 {name=p5 sig_type=std_logic lab=req_out}
C {c_element_rj.sym} 430 -360 0 0 {name=x1}
C {c_element_rj.sym} 430 -90 0 0 {name=x2}
C {devices/lab_pin.sym} 580 -430 0 1 {name=p71 sig_type=std_logic lab=ack_neu[0:7]}
C {devices/lab_pin.sym} 580 -410 2 0 {name=p72 sig_type=std_logic lab=rc[0]}
C {devices/lab_pin.sym} 580 -470 2 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 580 -450 2 0 {name=p2 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 580 -200 2 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 580 -180 2 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 580 -360 2 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 580 -340 2 0 {name=p14 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 580 -90 2 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 580 -70 2 0 {name=p9 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 280 -360 0 0 {name=p15 sig_type=std_logic lab=rc[0]}
C {devices/lab_pin.sym} 1020 -270 0 0 {name=p16 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 280 -110 0 0 {name=p17 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 280 -430 0 0 {name=p73 sig_type=std_logic lab=gc0}
C {devices/lab_pin.sym} 580 -380 2 0 {name=p18 sig_type=std_logic lab=gc0}
C {devices/lab_pin.sym} 280 -340 0 0 {name=p95 sig_type=std_logic lab=ack_outi[0]}
C {devices/lab_pin.sym} 280 -450 2 1 {name=p19 sig_type=std_logic lab=req_neu[0:7]}
C {devices/lab_pin.sym} 280 -470 0 0 {name=p20 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 580 -160 0 1 {name=p21 sig_type=std_logic lab=ack_neu[8:15]}
C {devices/lab_pin.sym} 280 -180 2 1 {name=p22 sig_type=std_logic lab=req_neu[8:15]}
C {devices/lab_pin.sym} 280 -200 0 0 {name=p23 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 280 -160 0 0 {name=p75 sig_type=std_logic lab=gc1}
C {devices/lab_pin.sym} 580 -110 2 0 {name=p24 sig_type=std_logic lab=gc1}
C {devices/lab_pin.sym} 280 -90 0 0 {name=p84 sig_type=std_logic lab=rc[1]}
C {devices/lab_pin.sym} 280 -70 0 0 {name=p79 sig_type=std_logic lab=ack_outi[1]}
C {devices/lab_pin.sym} 580 -140 2 0 {name=p74 sig_type=std_logic lab=rc[1]}
C {devices/iopin.sym} 240 -620 0 0 {name=p34 lab=VDD}
C {devices/iopin.sym} 240 -590 0 0 {name=p35 lab=GND}
C {devices/ipin.sym} 470 -620 0 0 {name=p69 lab=req_neu[0:15]}
C {devices/opin.sym} 330 -590 0 0 {name=p25 lab=ack_neu[0:15]}
C {devices/ipin.sym} 570 -640 0 0 {name=p26 lab=nRes}
C {devices/ipin.sym} 610 -620 0 0 {name=p67 lab=ack_out}
C {devices/opin.sym} 530 -590 0 0 {name=p68 lab=req_out}
C {devices/lab_pin.sym} 1320 -300 2 0 {name=p27 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1320 -320 2 0 {name=p28 sig_type=std_logic lab=VDD}
