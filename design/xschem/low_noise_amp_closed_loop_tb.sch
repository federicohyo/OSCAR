v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {closed loop gain} 346.25 -195 0 0 0.4 0.4 {}
N 121.25 -720 121.25 -700 {
lab=0}
N 121.25 -810 121.25 -780 {
lab=VDD}
N 296.25 -732.5 326.25 -732.5 {
lab=VDD}
N 321.25 -702.5 321.25 -697.5 {
lab=bufp}
N 321.25 -697.5 321.25 -677.5 {
lab=bufp}
N 361.25 -732.5 391.25 -732.5 {
lab=bufp}
N 321.25 -827.5 321.25 -767.5 {
lab=VDD}
N 321.25 -692.5 371.25 -692.5 {
lab=bufp}
N 371.25 -732.5 371.25 -692.5 {
lab=bufp}
N 321.25 -677.5 321.25 -672.5 {
lab=bufp}
N 321.25 -767.5 321.25 -762.5 {
lab=VDD}
N 618.75 -378.75 618.75 -333.75 {
lab=0}
N 368.75 -390 368.75 -350 { lab=vcm}
N 368.75 -290 368.75 -250 { lab=0}
N 368.75 -420 368.75 -390 { lab=vcm}
N 368.75 -420 428.75 -420 { lab=vcm}
N 92.5 -458.75 92.5 -428.75 { lab=vin_signal}
N 92.5 -368.75 92.5 -328.75 { lab=vsen}
N 92.5 -268.75 92.5 -228.75 { lab=vcm}
N 92.5 -458.75 152.5 -458.75 { lab=vin_signal}
N 212.5 -458.75 322.5 -458.75 { lab=vin}
N 570 -440 618.75 -440 {
lab=vout}
N 618.75 -541.25 618.75 -440 {
lab=vout}
N 397.5 -541.25 397.5 -458.75 {
lab=vin}
N 423.75 -460 430 -460 {
lab=vin}
N 423.75 -460 423.75 -458.75 {
lab=vin}
N 321.25 -458.75 423.75 -458.75 {
lab=vin}
N 398.75 -548.75 473.75 -548.75 {
lab=vin}
N 397.5 -548.75 398.75 -548.75 {
lab=vin}
N 397.5 -548.75 397.5 -541.25 {
lab=vin}
N 533.75 -548.75 618.75 -548.75 {
lab=vout}
N 618.75 -548.75 618.75 -541.25 {
lab=vout}
N 470 -290 470 -250 { lab=0}
N 470 -380 470 -350 { lab=#net1}
N 428.75 -420 430 -420 {
lab=vcm}
C {devices/vsource.sym} 121.25 -750 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 121.25 -810 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 121.25 -700 0 0 {name=p96 sig_type=std_logic lab=0}
C {sky130_fd_pr/pfet_01v8.sym} 341.25 -732.5 0 1 {name=M6
L=0.3
W=3.0
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
C {devices/lab_pin.sym} 321.25 -612.5 0 0 {name=p63 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 296.25 -732.5 0 0 {name=p67 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 321.25 -642.5 0 0 {name=I5 value=100u}
C {devices/lab_pin.sym} 321.25 -827.5 0 0 {name=p70 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 391.25 -732.5 0 1 {name=p68 sig_type=std_logic lab=bufp}
C {devices/lab_pin.sym} 510 -380 0 1 {name=p9 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 618.75 -408.75 0 0 {name=C1 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 618.75 -333.75 0 0 {name=p14 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 618.75 -457.5 0 1 {name=p17 sig_type=std_logic lab=vout}
C {sky130_fd_pr/corner.sym} 630 -816.25 0 0 {name=CORNER only_toplevel=false corner=tt}
C {low_noise_amp.sym} 480 -440 0 0 {name=x1}
C {devices/lab_pin.sym} 490 -490 1 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/capa.sym} 321.25 -428.75 0 0 {name=C5
m=1
value=5p
footprint=1206
device="ceramic capacitor"}
C {devices/lab_wire.sym} 408.75 -420 0 0 {name=l4 sig_type=std_logic lab=vcm}
C {devices/vsource.sym} 368.75 -320 0 0 {name=V5 value=DC\{vcm\}}
C {devices/vsource.sym} 92.5 -298.75 0 0 {name=V4 value="sin(0 \{vac\} 1Meg) dc 0 ac 1"}
C {devices/capa.sym} 92.5 -398.75 2 0 {name=C4
m=1
value=1
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 92.5 -228.75 3 0 {name=l20 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 92.5 -348.75 3 0 {name=l24 sig_type=std_logic lab=vsen}
C {devices/res.sym} 182.5 -458.75 1 0 {name=R1
value=500
footprint=1206
device=resistor
m=1}
C {devices/lab_wire.sym} 132.5 -458.75 0 0 {name=l7 sig_type=std_logic lab=vin_signal}
C {devices/lab_pin.sym} 321.25 -398.75 0 1 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 368.75 -250 0 1 {name=p8 sig_type=std_logic lab=0}
C {devices/res.sym} 503.75 -548.75 1 0 {name=R3
value=5k
footprint=1206
device=resistor
m=1}
C {devices/lab_wire.sym} 268.75 -458.75 0 0 {name=l6 sig_type=std_logic lab=vin}
C {devices/netlist_not_shown.sym} 488.75 -817.5 0 0 {name=sIMULATION only_toplevel=false 

value="


* Circuit Parameters
.param iref = 100u
.param vdd  = 1.8
.param vss  = 0.0
.param vcm  = 0.8
.param vac  = 10m
.options TEMP = 65.0


* OP Parameters & Singals to save
.save all
+ @M.X1.XM1.msky130_fd_pr__pfet_01v8[id] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM1.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM1.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM2.msky130_fd_pr__pfet_01v8[id] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM3.msky130_fd_pr__nfet_01v8[id] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM3.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM3.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM4.msky130_fd_pr__nfet_01v8[id] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM4.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM4.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM5.msky130_fd_pr__pfet_01v8[id] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM5.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM5.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM6.msky130_fd_pr__nfet_01v8[id] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM6.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM6.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM7.msky130_fd_pr__pfet_01v8[id] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM7.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM7.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM7.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM8.msky130_fd_pr__pfet_01v8[id] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM8.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM8.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM9.msky130_fd_pr__nfet_01v8[id] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM9.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM9.msky130_fd_pr__nfet_01v8[gds]

*Simulations
.control
  ac dec 200 0.1 10G
  setplot ac1
  meas ac GBW when vdb(vout)=0
  meas ac DCG find vdb(vout) at=1k
  *meas ac PM find vp(vout) when vdb(vout)=0
  *print PM*180/PI
  *meas ac GM find vdb(vout) when vp(vout)=0
  plot vdb(vout) \{vp(vout)*180/PI\}
  write opamp_closeloop_ac1.raw
  
  reset
  tran 0.01u 11u
  setplot tran1
  plot v(vsen) v(vout)
  write opamp_closeloop_tran1.raw

  reset    
  noise v(vout) V4 dec 200 0.1 10G 1
  setplot noise1
  plot inoise_spectrum onoise_spectrum
  *print inoise_spectrum
  *print onoise_spectrum
  setplot noise2
  *plot inoise_total onoise_total
  print inoise_total
  print onoise_total
  write opamp_closeloop_noise.raw
  
  reset
  op
  setplot op1
  print vout  
  write opamp_closeloop_op1.raw
  
.endc

.end
"}
C {devices/isource.sym} 470 -320 0 0 {name=I0 value=DC\{iref\}}
C {devices/lab_pin.sym} 470 -250 0 1 {name=p1 sig_type=std_logic lab=0}
