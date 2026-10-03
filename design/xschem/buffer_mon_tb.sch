v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 550 -525 550 -505 {
lab=0}
N 550 -615 550 -585 {
lab=VDD}
N 750 -535 780 -535 {
lab=bufmonn}
N 750 -585 750 -535 {
lab=bufmonn}
N 750 -585 820 -585 {
lab=bufmonn}
N 820 -585 820 -565 {
lab=bufmonn}
N 820 -505 820 -480 {
lab=0}
N 815 -535 845 -535 {
lab=0}
N 845 -535 845 -500 {
lab=0}
N 820 -500 845 -500 {
lab=0}
N 940 -595 985 -595 {
lab=VDD}
N 940 -625 940 -595 {
lab=VDD}
N 940 -625 980 -625 {
lab=VDD}
N 980 -565 980 -545 {
lab=bufmonp}
N 980 -555 1045 -555 {
lab=bufmonp}
N 1045 -595 1045 -555 {
lab=bufmonp}
N 1020 -595 1045 -595 {
lab=bufmonp}
N 980 -650 980 -625 {
lab=VDD}
C {buffer_mon.sym} 650 -245 0 0 {name=x1}
C {sky130_fd_pr/corner.sym} 137.5 -602.5 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/vsource.sym} 550 -555 0 0 {name=V2 value=1.8
}
C {devices/lab_pin.sym} 550 -615 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 550 -505 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 800 -225 0 1 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 750 -585 0 0 {name=p72 sig_type=std_logic lab=bufmonn}
C {devices/lab_pin.sym} 820 -480 0 0 {name=p73 sig_type=std_logic lab=0}
C {devices/isource.sym} 820 -615 0 0 {name=I7 value=500p}
C {devices/lab_pin.sym} 820 -645 0 0 {name=p97 sig_type=std_logic lab=VDD}
C {devices/simulator_commands.sym} 335 -585 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value="
* ngspice commands
.save all

.save @m.x1.xm2.msky130_fd_pr__nfet_01v8[id]
.save @m.x1.xm2.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm3.msky130_fd_pr__nfet_01v8[id]
.save @m.x1.xm3.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm4.msky130_fd_pr__nfet_01v8[id]
.save @m.x1.xm4.msky130_fd_pr__nfet_01v8[gm]


.save @m.x1.xm1.msky130_fd_pr__pfet_01v8[id]
.save @m.x1.xm1.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[id]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[gm]


.save @m.x2.xm4.msky130_fd_pr__nfet_01v8[id]
.save @m.x2.xm4.msky130_fd_pr__nfet_01v8[gm]
.save @m.x2.xm3.msky130_fd_pr__nfet_01v8[id]
.save @m.x2.xm3.msky130_fd_pr__nfet_01v8[gm]

.save @m.x2.xm1.msky130_fd_pr__pfet_01v8[id]
.save @m.x2.xm1.msky130_fd_pr__pfet_01v8[gm]
.save @m.x2.xm5.msky130_fd_pr__pfet_01v8[id]
.save @m.x2.xm5.msky130_fd_pr__pfet_01v8[gm]
.save @m.x2.xm2.msky130_fd_pr__pfet_01v8[id]
.save @m.x2.xm2.msky130_fd_pr__pfet_01v8[gm]


.control
op
write buffer_mon_tb.raw

dc vin 0 1.8 0.01
plot outn outp
*frequency sweep over Vin to find bandwith and gain
ac dec 10 1 1MEG
plot db(outp/in)
plot db(outn/in)
.endc
"}
C {devices/lab_pin.sym} 800 -245 2 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 500 -245 0 0 {name=p3 sig_type=std_logic lab=bufmonn}
C {devices/vsource.sym} 385 -210 0 0 {name=Vin value="DC 0.403 AC 1m"
}
C {devices/lab_pin.sym} 385 -240 0 0 {name=p4 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 385 -180 0 0 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 500 -265 0 0 {name=p6 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 800 -265 2 0 {name=p7 sig_type=std_logic lab=outn}
C {sky130_fd_pr/nfet_01v8.sym} 800 -535 0 0 {name=M1
L=0.5
W=1.0
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {buffer_mon_p.sym} 650 -350 0 0 {name=x2}
C {devices/lab_pin.sym} 1045 -595 0 1 {name=p8 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 980 -485 0 0 {name=p9 sig_type=std_logic lab=0}
C {devices/isource.sym} 980 -515 0 0 {name=I1 value=500p}
C {devices/lab_pin.sym} 980 -650 0 0 {name=p10 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 1000 -595 0 1 {name=M2
L=0.30
W=1.0
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {devices/lab_pin.sym} 500 -370 2 1 {name=p11 sig_type=std_logic lab=bufmonp}
C {devices/lab_pin.sym} 800 -350 2 0 {name=p12 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 800 -330 0 1 {name=p13 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 500 -350 0 0 {name=p14 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 800 -370 2 0 {name=p15 sig_type=std_logic lab=outp}
