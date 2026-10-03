v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 950 -550 950 -530 {
lab=0}
N 950 -640 950 -610 {
lab=VDD}
N 660 -140 660 -100 { lab=0}
N 1110 -210 1110 -160 {
lab=0}
N 1110 -220 1110 -210 {
lab=0}
N 660 -210 660 -200 {
lab=vref}
N 670 -240 770 -240 {
lab=vref}
N 660 -240 670 -240 {
lab=vref}
N 660 -240 660 -210 {
lab=vref}
N 990 -280 1040 -280 {
lab=vout}
N 1350 -170 1350 -150 {
lab=0}
N 1350 -260 1350 -230 {
lab=en0}
N 1420 -170 1420 -150 {
lab=0}
N 1420 -260 1420 -230 {
lab=en1}
N 1490 -170 1490 -150 {
lab=0}
N 1490 -260 1490 -230 {
lab=en2}
N 1550 -170 1550 -150 {
lab=0}
N 1550 -260 1550 -230 {
lab=en3}
N 1200 -590 1230 -590 {
lab=VDD}
N 1230 -560 1230 -540 {
lab=bufp}
N 1270 -590 1300 -590 {
lab=bufp}
N 1230 -690 1230 -630 {
lab=VDD}
N 1230 -550 1280 -550 {
lab=bufp}
N 1280 -590 1280 -550 {
lab=bufp}
N 1230 -540 1230 -530 {
lab=bufp}
N 1230 -630 1230 -620 {
lab=VDD}
N 460 -320 460 -220 {
lab=vsen}
N 460 -320 520 -320 {
lab=vsen}
N 580 -320 670 -320 {
lab=vsen}
N 730 -320 770 -320 {
lab=vin}
N 520 -320 580 -320 {
lab=vsen}
N 1040 -280 1110 -280 {
lab=vout}
N 1060 -550 1060 -510 { lab=0}
N 1060 -640 1060 -610 {
lab=tunep}
N 1400 -580 1430 -580 {
lab=VDD}
N 1430 -550 1430 -530 {
lab=boostp}
N 1470 -580 1500 -580 {
lab=boostp}
N 1430 -680 1430 -620 {
lab=VDD}
N 1430 -540 1480 -540 {
lab=boostp}
N 1480 -580 1480 -540 {
lab=boostp}
N 1430 -530 1430 -520 {
lab=boostp}
N 1430 -620 1430 -610 {
lab=VDD}
N 1640 -580 1670 -580 {
lab=0}
N 1670 -550 1670 -530 {
lab=boostn}
N 1710 -580 1740 -580 {
lab=boostn}
N 1670 -680 1670 -620 {
lab=VDD}
N 1670 -540 1720 -540 {
lab=boostn}
N 1720 -580 1720 -540 {
lab=boostn}
N 1670 -530 1670 -520 {
lab=boostn}
N 1670 -620 1670 -610 {
lab=VDD}
C {devices/vsource.sym} 950 -580 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 950 -640 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 950 -530 0 0 {name=p96 sig_type=std_logic lab=0}
C {sky130_fd_pr/corner.sym} 640 -630 0 0 {name=CORNER1 only_toplevel=false corner=tt}
C {devices/vsource.sym} 660 -170 0 0 {name=V5 value=DC\{vcm\}}
C {devices/lab_pin.sym} 820 -390 2 1 {name=p1 sig_type=std_logic lab=bufp}
C {devices/lab_pin.sym} 1110 -160 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1110 -280 0 1 {name=p4 sig_type=std_logic lab=vout}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1110 -250 0 0 {name=C1 model=cap_mim_m3_1 W=22 L=22 MF=1 spiceprefix=X}
C {devices/lab_wire.sym} 460 -260 0 0 {name=l1 sig_type=std_logic lab=vsen}
C {devices/lab_pin.sym} 660 -100 0 0 {name=p2 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1060 -640 0 1 {name=p8 sig_type=std_logic lab=tunep}
C {devices/lab_pin.sym} 820 -370 2 1 {name=p11 sig_type=std_logic lab=tunep}
C {devices/simulator_commands.sym} 500 -630 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value="
* ngspice commands



* Circuit Parameters
*.param iref1 = 200u
.param iref = 200u
.param vdd  = 1.8
.param vss  = 0.0
.param vcm  = 0.8
.param vac  = 5u
.options TEMP = 35.0


* OP Parameters & Singals to save
.save all

+ @M.X1.XM2.msky130_fd_pr__pfet_01v8[id] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM1.msky130_fd_pr__pfet_01v8[id] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM1.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM1.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM11.msky130_fd_pr__pfet_01v8[id] @M.X1.XM11.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM11.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM11.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM11.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM11.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM11.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM7.msky130_fd_pr__pfet_01v8[id] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM7.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM7.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM9.msky130_fd_pr__nfet_01v8[id] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM9.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM9.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM10.msky130_fd_pr__nfet_01v8[id] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM10.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM10.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM12.msky130_fd_pr__pfet_01v8[id] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM12.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM12.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM16.msky130_fd_pr__nfet_01v8[id] @M.X1.XM16.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM16.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM16.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM16.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM16.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM16.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM12.msky130_fd_pr__pfet_01v8[id] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM12.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM12.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM12.msky130_fd_pr__pfet_01v8[gds] @M.X1.XM12.msky130_fd_pr__pfet_01v8[gdm]
+ @M.X1.XM8.msky130_fd_pr__pfet_01v8[id] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM8.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM8.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM15.msky130_fd_pr__pfet_01v8[id] @M.X1.XM15.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM15.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM15.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM15.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM15.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM15.msky130_fd_pr__pfet_01v8[gds] @M.X1.XM15.msky130_fd_pr__pfet_01v8[gdm]


*Simulations
.control
  ac dec 200 0.001 1G
  setplot ac1
  meas ac GBW when vdb(vout)=0
  meas ac DCG find vdb(vout) at=10
  meas ac PM find vp(vout) when vdb(vout)=0
  print PM*180/PI
  meas ac GM find vdb(vout) when vp(vout)=0
  plot vdb(vout) \{vp(vout)*180/PI\}
  write opamp_closeloop_ac1_v1.raw
  
  reset
  tran 1u 20m
  setplot tran1
  plot v(vsen) v(vout) 
  write opamp_closeloop_tran1.raw

  reset    
  noise v(vout) V8 dec 200 0.001 1G 1
  setplot noise1
  plot inoise_spectrum onoise_spectrum
  *print inoise_spectrum
  *print onoise_spectrum
  setplot noise2
  *plot inoise_total onoise_total
  print inoise_total
  print onoise_total
  write opamp_closeloop_noise_v1.raw
  
  reset
  op
  setplot op1
  print vout  
  write opamp_closeloop_op1_v1_fctoday.raw
  
.endc

.end
"}
C {devices/lab_wire.sym} 750 -320 3 0 {name=l2 sig_type=std_logic lab=vin}
C {devices/lab_pin.sym} 940 -360 2 0 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 940 -380 0 1 {name=p10 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} 1350 -200 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 1350 -150 0 0 {name=p13 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1350 -260 2 1 {name=p12 sig_type=std_logic lab=en0}
C {devices/vsource.sym} 1420 -200 0 0 {name=V4 value=1.8}
C {devices/lab_pin.sym} 1420 -150 0 0 {name=p14 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1420 -260 2 1 {name=p15 sig_type=std_logic lab=en1}
C {devices/vsource.sym} 1490 -200 0 0 {name=V6 value=1.8}
C {devices/lab_pin.sym} 1490 -150 0 0 {name=p16 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1490 -260 2 1 {name=p17 sig_type=std_logic lab=en2}
C {devices/vsource.sym} 1550 -200 0 0 {name=V7 value=1.8}
C {devices/lab_pin.sym} 1550 -150 0 0 {name=p18 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1550 -260 2 1 {name=p19 sig_type=std_logic lab=en3}
C {devices/lab_pin.sym} 860 -200 2 1 {name=p20 sig_type=std_logic lab=en0}
C {devices/lab_pin.sym} 860 -180 2 1 {name=p21 sig_type=std_logic lab=en1}
C {devices/lab_pin.sym} 860 -160 2 1 {name=p22 sig_type=std_logic lab=en2}
C {devices/lab_pin.sym} 860 -140 2 1 {name=p23 sig_type=std_logic lab=en3}
C {sky130_fd_pr/pfet_01v8.sym} 1250 -590 0 1 {name=M1
L=0.6
W=6
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=30
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 1230 -470 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1200 -590 0 0 {name=p25 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1230 -500 0 0 {name=I2 value=\{iref\}}
C {devices/lab_pin.sym} 1230 -690 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1300 -590 0 1 {name=p27 sig_type=std_logic lab=bufp}
C {devices/lab_wire.sym} 730 -240 3 0 {name=l3 sig_type=std_logic lab=vref}
C {devices/vsource.sym} 460 -190 0 0 {name=V8 value="sin(0 \{vac\} 100) dc 0 ac 1"}
C {sky130_fd_pr/res_generic_l1.sym} 700 -320 1 1 {name=R1
W=1
L=1
model=res_generic_l1
mult=1}
C {devices/lab_wire.sym} 460 -160 3 0 {name=l4 sig_type=std_logic lab=vref}
C {devices/vsource.sym} 1060 -580 0 0 {name=V3 value=0.4}
C {devices/lab_pin.sym} 1060 -510 0 0 {name=p5 sig_type=std_logic lab=0}
C {sky130_fd_pr/pfet_01v8.sym} 1450 -580 0 1 {name=M2
L=0.6
W=9
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 1430 -460 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1400 -580 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1430 -490 0 0 {name=I1 value=400u}
C {devices/lab_pin.sym} 1430 -680 0 0 {name=p28 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1500 -580 0 1 {name=p29 sig_type=std_logic lab=boostp}
C {low_noise_amp_fc_v2.sym} 870 -280 0 0 {name=x1}
C {devices/lab_pin.sym} 820 -430 0 0 {name=p30 sig_type=std_logic lab=boostp}
C {sky130_fd_pr/nfet_01v8.sym} 1690 -580 0 1 {name=M3
L=0.45
W=12
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 1670 -460 0 0 {name=p31 sig_type=std_logic lab=0}
C {devices/isource.sym} 1670 -490 0 0 {name=I3 value=200u}
C {devices/lab_pin.sym} 1670 -680 0 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1740 -580 0 1 {name=p34 sig_type=std_logic lab=boostn}
C {devices/lab_pin.sym} 1640 -580 0 0 {name=p32 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 820 -410 0 0 {name=p36 sig_type=std_logic lab=boostn}
