v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1280 -210 1320 -210 {
lab=gc}
N 950 -170 980 -170 {
lab=ack_out}
N 950 -170 950 -130 {
lab=ack_out}
N 950 -130 1270 -130 {
lab=ack_out}
N 730 -370 760 -370 {
lab=gc0}
N 730 -60 760 -60 {
lab=gc1}
N 400 -350 430 -350 {
lab=rc[0]}
N 400 -330 430 -330 {
lab=ack_outi[0]}
N 400 -40 430 -40 {
lab=rc[1]}
N 400 -20 430 -20 {
lab=ack_outi[1]}
N 1280 -320 1330 -320 {
lab=ack_outi[0:1]}
N 1330 -350 1330 -320 {
lab=ack_outi[0:1]}
N 950 -320 980 -320 {
lab=rc[0:1]}
N 950 -380 950 -320 {
lab=rc[0:1]}
N 950 -390 950 -380 {
lab=rc[0:1]}
N 730 -460 770 -460 {
lab=ack_neu[0:1]}
N 770 -480 770 -460 {
lab=ack_neu[0:1]}
N 730 -160 770 -160 {
lab=ack_neu[2:3]}
N 770 -180 770 -160 {
lab=ack_neu[2:3]}
N 300 -580 300 -440 {
lab=gc0}
N 300 -440 430 -440 {
lab=gc0}
N 400 -460 430 -460 {
lab=req_neu[0:1]}
N 400 -520 400 -460 {
lab=req_neu[0:1]}
N 400 -530 400 -520 {
lab=req_neu[0:1]}
N 300 -280 300 -140 {
lab=gc1}
N 300 -140 430 -140 {
lab=gc1}
N 400 -160 430 -160 {
lab=req_neu[2:3]}
N 400 -220 400 -160 {
lab=req_neu[2:3]}
N 400 -230 400 -220 {
lab=req_neu[2:3]}
C {devices/ipin.sym} 140 -90 0 0 {name=p2 lab=ack_out}
C {devices/opin.sym} 40 -60 0 0 {name=p3 lab=req_out}
C {devices/ipin.sym} 140 -120 0 0 {name=p4 lab=req_neu[0:3]}
C {devices/opin.sym} 40 -30 0 0 {name=p8 lab=ack_neu[0:3]}
C {devices/ipin.sym} 140 -150 0 0 {name=p9 lab=nRes}
C {c_element_rj.sym} 1130 -190 0 0 {name=x11}
C {c_element_rj.sym} 580 -350 0 0 {name=x4}
C {c_element_rj.sym} 580 -40 0 0 {name=x5}
C {devices/lab_pin.sym} 980 -190 0 0 {name=p7 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 1270 -130 2 0 {name=p10 sig_type=std_logic lab=ack_out}
C {devices/lab_pin.sym} 980 -210 0 0 {name=p200 sig_type=std_logic lab=nRes}
C {devices/iopin.sym} 50 -210 0 0 {name=p34 lab=VDD}
C {devices/iopin.sym} 50 -180 0 0 {name=p35 lab=GND}
C {devices/lab_pin.sym} 1320 -210 2 0 {name=p13 sig_type=std_logic lab=gc}
C {devices/lab_pin.sym} 760 -370 2 0 {name=p14 sig_type=std_logic lab=gc0}
C {devices/lab_pin.sym} 760 -60 2 0 {name=p15 sig_type=std_logic lab=gc1}
C {devices/lab_pin.sym} 730 -400 2 0 {name=p16 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 730 -420 2 0 {name=p17 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 730 -20 2 0 {name=p18 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 730 -40 2 0 {name=p19 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 430 -370 0 0 {name=p22 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 430 -60 0 0 {name=p23 sig_type=std_logic lab=nRes}
C {arbiter_three_2.sym} 1130 -290 0 0 {name=x1}
C {arbiter_three_2.sym} 580 -430 0 0 {name=x2}
C {arbiter_three_2.sym} 580 -130 0 0 {name=x3}
C {devices/lab_pin.sym} 1280 -300 2 0 {name=p1 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 980 -300 0 0 {name=p5 sig_type=std_logic lab=gc}
C {devices/lab_pin.sym} 1300 -320 3 1 {name=p194 sig_type=std_logic lab=ack_outi[0:1]}
C {devices/bus_connect.sym} 1330 -350 1 1 {name=l25 lab=ack_outi[0]}
C {devices/bus_connect.sym} 1330 -330 1 1 {name=l26 lab=ack_outi[1]}
C {devices/bus_connect.sym} 950 -390 1 1 {name=l24 lab=rc[1]}
C {devices/bus_connect.sym} 950 -380 3 1 {name=l27 lab=rc[0]}
C {devices/lab_pin.sym} 950 -340 0 1 {name=p193 sig_type=std_logic lab=rc[0:1]}
C {devices/bus_connect.sym} 770 -480 1 1 {name=l17 lab=ack_neu[0]}
C {devices/bus_connect.sym} 770 -460 1 1 {name=l18 lab=ack_neu[1]}
C {devices/lab_pin.sym} 750 -460 3 1 {name=p50 sig_type=std_logic lab=ack_neu[0:1]}
C {devices/bus_connect.sym} 770 -180 1 1 {name=l21 lab=ack_neu[2]}
C {devices/bus_connect.sym} 770 -160 1 1 {name=l22 lab=ack_neu[3]}
C {devices/lab_pin.sym} 750 -160 3 1 {name=p77 sig_type=std_logic lab=ack_neu[2:3]}
C {devices/lab_pin.sym} 730 -140 2 0 {name=p184 sig_type=std_logic lab=rc[1]}
C {devices/lab_pin.sym} 730 -440 2 0 {name=p89 sig_type=std_logic lab=rc[0]}
C {devices/lab_pin.sym} 400 -330 0 0 {name=p95 sig_type=std_logic lab=ack_outi[0]}
C {devices/lab_pin.sym} 400 -350 0 0 {name=p97 sig_type=std_logic lab=rc[0]}
C {devices/bus_connect.sym} 400 -530 1 1 {name=l15 lab=req_neu[1]}
C {devices/lab_pin.sym} 300 -575 2 1 {name=p93 sig_type=std_logic lab=gc0}
C {devices/bus_connect.sym} 400 -520 3 1 {name=l16 lab=req_neu[0]}
C {devices/lab_pin.sym} 400 -480 0 1 {name=p41 sig_type=std_logic lab=req_neu[0:1]}
C {devices/bus_connect.sym} 400 -230 1 1 {name=l20 lab=req_neu[3]}
C {devices/lab_pin.sym} 300 -275 2 1 {name=p71 sig_type=std_logic lab=gc1}
C {devices/bus_connect.sym} 400 -220 3 1 {name=l23 lab=req_neu[2]}
C {devices/lab_pin.sym} 400 -180 0 1 {name=p76 sig_type=std_logic lab=req_neu[2:3]}
C {devices/lab_pin.sym} 400 -40 0 0 {name=p84 sig_type=std_logic lab=rc[1]}
C {devices/lab_pin.sym} 400 -20 0 0 {name=p79 sig_type=std_logic lab=ack_outi[1]}
C {devices/lab_pin.sym} 730 -330 2 0 {name=p6 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 730 -350 2 0 {name=p20 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 730 -100 2 0 {name=p21 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 730 -120 2 0 {name=p24 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1280 -260 2 0 {name=p25 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1280 -280 2 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1280 -170 2 0 {name=p27 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1280 -190 2 0 {name=p28 sig_type=std_logic lab=VDD}
