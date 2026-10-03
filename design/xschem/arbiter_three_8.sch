v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 760 -440 790 -440 {
lab=gc0}
N 430 -420 460 -420 {
lab=rc[0]}
N 430 -400 460 -400 {
lab=ack_outi[0]}
N 760 -200 790 -200 {
lab=gc1}
N 430 -180 460 -180 {
lab=rc[1]}
N 430 -160 460 -160 {
lab=ack_outi[1]}
N 1340 -280 1380 -280 {
lab=gc}
N 1010 -240 1040 -240 {
lab=ack_out}
N 1010 -240 1010 -200 {
lab=ack_out}
N 1010 -200 1330 -200 {
lab=ack_out}
N 1340 -390 1380 -390 {
lab=ack_outi[0:1]}
N 1380 -410 1380 -390 {
lab=ack_outi[0:1]}
N 1010 -390 1040 -390 {
lab=rc[0:1]}
N 1010 -450 1010 -390 {
lab=rc[0:1]}
N 1010 -460 1010 -450 {
lab=rc[0:1]}
N 800 -470 840 -470 {
lab=ack_neu[0:3]}
N 840 -530 840 -510 {
lab=ack_neu[0:3]}
N 840 -490 840 -470 {
lab=ack_neu[0:3]}
N 840 -510 840 -490 {
lab=ack_neu[0:3]}
N 760 -470 800 -470 {
lab=ack_neu[0:3]}
N 290 -510 320 -510 {
lab=req_neu[0:3]}
N 290 -570 290 -510 {
lab=req_neu[0:3]}
N 290 -580 290 -570 {
lab=req_neu[0:3]}
N 290 -630 290 -580 {
lab=req_neu[0:3]}
N 320 -510 460 -510 {
lab=req_neu[0:3]}
N 820 -240 860 -240 {
lab=ack_neu[4:7]}
N 860 -300 860 -280 {
lab=ack_neu[4:7]}
N 860 -260 860 -240 {
lab=ack_neu[4:7]}
N 860 -280 860 -260 {
lab=ack_neu[4:7]}
N 760 -240 820 -240 {
lab=ack_neu[4:7]}
N 290 -280 320 -280 {
lab=req_neu[4:7]}
N 290 -340 290 -280 {
lab=req_neu[4:7]}
N 290 -350 290 -340 {
lab=req_neu[4:7]}
N 290 -400 290 -350 {
lab=req_neu[4:7]}
N 320 -280 460 -280 {
lab=req_neu[4:7]}
C {arbiter_three_4.sym} 610 -500 0 0 {name=x1}
C {arbiter_three_4.sym} 610 -270 0 0 {name=x2}
C {arbiter_three_2.sym} 1190 -360 0 0 {name=x3}
C {c_element_rj.sym} 610 -420 0 0 {name=x4}
C {devices/lab_pin.sym} 790 -440 2 0 {name=p14 sig_type=std_logic lab=gc0}
C {devices/lab_pin.sym} 760 -400 2 0 {name=p16 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 760 -420 2 0 {name=p17 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 460 -440 0 0 {name=p22 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 430 -400 0 0 {name=p95 sig_type=std_logic lab=ack_outi[0]}
C {devices/lab_pin.sym} 430 -420 0 0 {name=p97 sig_type=std_logic lab=rc[0]}
C {c_element_rj.sym} 610 -180 0 0 {name=x5}
C {devices/lab_pin.sym} 790 -200 2 0 {name=p15 sig_type=std_logic lab=gc1}
C {devices/lab_pin.sym} 760 -160 2 0 {name=p18 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 760 -180 2 0 {name=p19 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 460 -200 0 0 {name=p23 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 430 -180 0 0 {name=p84 sig_type=std_logic lab=rc[1]}
C {devices/lab_pin.sym} 430 -160 0 0 {name=p79 sig_type=std_logic lab=ack_outi[1]}
C {c_element_rj.sym} 1190 -260 0 0 {name=x11}
C {devices/lab_pin.sym} 1040 -260 0 0 {name=p7 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 1330 -200 2 0 {name=p10 sig_type=std_logic lab=ack_out}
C {devices/lab_pin.sym} 1040 -280 0 0 {name=p200 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 1340 -240 2 0 {name=p11 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1380 -280 2 0 {name=p13 sig_type=std_logic lab=gc}
C {devices/bus_connect.sym} 1380 -410 1 1 {name=l25 lab=ack_outi[0]}
C {devices/bus_connect.sym} 1380 -390 1 1 {name=l26 lab=ack_outi[1]}
C {devices/lab_pin.sym} 1360 -390 3 1 {name=p194 sig_type=std_logic lab=ack_outi[0:1]}
C {devices/lab_pin.sym} 1340 -370 2 0 {name=p5 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 1040 -370 0 0 {name=p1 sig_type=std_logic lab=gc}
C {devices/bus_connect.sym} 1010 -460 1 1 {name=l24 lab=rc[1]}
C {devices/bus_connect.sym} 1010 -450 3 1 {name=l27 lab=rc[0]}
C {devices/lab_pin.sym} 1010 -410 0 1 {name=p193 sig_type=std_logic lab=rc[0:1]}
C {devices/bus_connect.sym} 840 -530 1 1 {name=l17 lab=ack_neu[0]}
C {devices/bus_connect.sym} 840 -510 1 1 {name=l18 lab=ack_neu[1]}
C {devices/lab_pin.sym} 820 -470 3 1 {name=p50 sig_type=std_logic lab=ack_neu[0:3]}
C {devices/bus_connect.sym} 840 -490 1 1 {name=l1 lab=ack_neu[2]}
C {devices/bus_connect.sym} 840 -470 1 1 {name=l2 lab=ack_neu[3]}
C {devices/lab_pin.sym} 760 -490 2 0 {name=p2 sig_type=std_logic lab=rc[0]}
C {devices/lab_pin.sym} 760 -530 2 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 760 -510 2 0 {name=p4 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 760 -300 2 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 760 -280 2 0 {name=p8 sig_type=std_logic lab=GND}
C {devices/bus_connect.sym} 290 -580 1 1 {name=l15 lab=req_neu[1]}
C {devices/bus_connect.sym} 290 -570 3 1 {name=l16 lab=req_neu[0]}
C {devices/lab_pin.sym} 290 -510 2 1 {name=p41 sig_type=std_logic lab=req_neu[0:3]}
C {devices/bus_connect.sym} 290 -610 3 1 {name=l7 lab=req_neu[2]}
C {devices/bus_connect.sym} 290 -630 3 1 {name=l8 lab=req_neu[3]}
C {devices/lab_pin.sym} 460 -530 0 0 {name=p9 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 460 -490 0 0 {name=p20 sig_type=std_logic lab=gc0}
C {devices/bus_connect.sym} 860 -300 1 1 {name=l3 lab=ack_neu[4]}
C {devices/bus_connect.sym} 860 -280 1 1 {name=l4 lab=ack_neu[5]}
C {devices/lab_pin.sym} 840 -240 3 1 {name=p21 sig_type=std_logic lab=ack_neu[4:7]}
C {devices/bus_connect.sym} 860 -260 1 1 {name=l5 lab=ack_neu[6]}
C {devices/bus_connect.sym} 860 -240 1 1 {name=l6 lab=ack_neu[7]}
C {devices/lab_pin.sym} 760 -260 2 0 {name=p24 sig_type=std_logic lab=rc[1]}
C {devices/bus_connect.sym} 290 -350 1 1 {name=l9 lab=req_neu[5]}
C {devices/bus_connect.sym} 290 -340 3 1 {name=l10 lab=req_neu[4]}
C {devices/lab_pin.sym} 290 -300 0 1 {name=p25 sig_type=std_logic lab=req_neu[4:7]}
C {devices/bus_connect.sym} 290 -380 3 1 {name=l11 lab=req_neu[6]}
C {devices/bus_connect.sym} 290 -400 3 1 {name=l12 lab=req_neu[7]}
C {devices/lab_pin.sym} 460 -300 0 0 {name=p26 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 460 -260 0 0 {name=p27 sig_type=std_logic lab=gc1}
C {devices/ipin.sym} 160 -120 0 0 {name=p67 lab=ack_out}
C {devices/opin.sym} 40 -50 0 0 {name=p68 lab=req_out}
C {devices/ipin.sym} 160 -150 0 0 {name=p69 lab=req_neu[0:7]}
C {devices/opin.sym} 40 -80 0 0 {name=p28 lab=ack_neu[0:7]}
C {devices/ipin.sym} 160 -180 0 0 {name=p29 lab=nRes}
C {devices/iopin.sym} 40 -250 0 0 {name=p30 lab=VDD}
C {devices/iopin.sym} 40 -220 0 0 {name=p31 lab=GND}
C {devices/lab_pin.sym} 1340 -350 2 0 {name=p32 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1340 -330 2 0 {name=p33 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1340 -260 2 0 {name=p34 sig_type=std_logic lab=VDD}
