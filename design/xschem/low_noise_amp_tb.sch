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
N 806.25 -378.75 806.25 -333.75 {
lab=0}
N 368.75 -290 368.75 -250 { lab=0}
N 368.75 -420 428.75 -420 { lab=vcm}
N 92.5 -458.75 92.5 -428.75 { lab=#net1}
N 92.5 -368.75 92.5 -328.75 { lab=vsen}
N 92.5 -268.75 92.5 -228.75 { lab=vcm}
N 212.5 -458.75 322.5 -458.75 { lab=vin}
N 397.5 -541.25 397.5 -458.75 {
lab=vin}
N 398.75 -548.75 473.75 -548.75 {
lab=vin}
N 397.5 -548.75 398.75 -548.75 {
lab=vin}
N 397.5 -548.75 397.5 -541.25 {
lab=vin}
N 533.75 -548.75 618.75 -548.75 {
lab=vout}
N 418.125 -458.75 418.125 -438.75 {
lab=vin}
N 792.5 -548.75 792.5 -438.125 {
lab=vout}
N 618.75 -548.75 792.5 -548.75 {
lab=vout}
N 755.625 -438.75 792.5 -438.75 {
lab=vout}
N 792.5 -438.75 806.25 -438.75 {
lab=vout}
N 428.75 -420 430 -420 {
lab=vcm}
N 430 -420 430 -418.75 {
lab=vcm}
N 418.125 -438.75 456.25 -438.75 {
lab=vin}
N 430 -418.75 456.25 -418.75 {
lab=vcm}
N 288.75 -756.25 318.75 -756.25 {
lab=VDD}
N 313.75 -726.25 313.75 -721.25 {
lab=bufp}
N 313.75 -721.25 313.75 -701.25 {
lab=bufp}
N 353.75 -756.25 383.75 -756.25 {
lab=bufp}
N 313.75 -851.25 313.75 -791.25 {
lab=VDD}
N 313.75 -716.25 363.75 -716.25 {
lab=bufp}
N 363.75 -756.25 363.75 -716.25 {
lab=bufp}
N 313.75 -701.25 313.75 -696.25 {
lab=bufp}
N 313.75 -791.25 313.75 -786.25 {
lab=VDD}
N 382.5 -458.75 397.5 -458.75 {
lab=vin}
N 397.5 -458.75 417.5 -458.75 {
lab=vin}
N 417.5 -458.75 418.125 -458.75 {
lab=vin}
N 280 -420 370 -420 {
lab=vcm}
N 238.75 -421.25 280 -421.25 {
lab=vcm}
N 280 -421.25 280 -420 {
lab=vcm}
N 368.75 -360 368.75 -350 {
lab=vcm}
N 368.75 -420 368.75 -358.75 {
lab=vcm}
N 321.25 -458.75 382.5 -458.75 {
lab=vin}
N 92.5 -458.75 153.75 -458.75 {
lab=#net1}
N 311.25 -558.75 358.75 -558.75 {
lab=vin}
N 358.75 -558.75 358.75 -458.75 {
lab=vin}
C {devices/vsource.sym} 121.25 -750 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 121.25 -810 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 121.25 -700 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 756.25 -418.75 0 1 {name=p9 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 806.25 -408.75 0 0 {name=C1 model=cap_mim_m3_1 W=25 L=25 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 806.25 -333.75 0 0 {name=p14 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 792.5 -478.75 0 1 {name=p17 sig_type=std_logic lab=vout}
C {sky130_fd_pr/corner.sym} 630 -816.25 0 0 {name=CORNER only_toplevel=false corner=tt}
C {devices/lab_pin.sym} 756.25 -458.75 1 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 408.75 -420 0 0 {name=l4 sig_type=std_logic lab=vcm}
C {devices/vsource.sym} 368.75 -320 0 0 {name=V5 value=DC\{vcm\}}
C {devices/vsource.sym} 92.5 -298.75 0 0 {name=V4 value="sin(0 \{vac\} 100) dc 0 ac 1"}
C {devices/lab_pin.sym} 92.5 -228.75 3 0 {name=l20 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 92.5 -348.75 3 0 {name=l24 sig_type=std_logic lab=vsen}
C {devices/lab_pin.sym} 368.75 -250 0 1 {name=p8 sig_type=std_logic lab=0}
C {devices/res.sym} 503.75 -548.75 1 0 {name=R3
value=5k
footprint=1206
device=resistor
m=1}
C {devices/lab_wire.sym} 268.75 -458.75 0 0 {name=l6 sig_type=std_logic lab=vin}
C {devices/netlist_not_shown.sym} 488.75 -807.5 0 0 {name=sIMULATION only_toplevel=false 

value="


* Circuit Parameters
.param iref = 500p
.param vdd  = 1.8
.param vss  = 0.0
.param vcm  = 0.8
.param vac  = 1m
.options TEMP = 65.0


* OP Parameters & Singals to save
.save all
+ @M.X1.XM4.msky130_fd_pr__pfet_01v8[id] @M.X1.XM4.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM4.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM4.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM4.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM4.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM4.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM2.msky130_fd_pr__pfet_01v8[id] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM3.msky130_fd_pr__pfet_01v8[id] @M.X1.XM3.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM3.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM3.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM3.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM3.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM3.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM1.msky130_fd_pr__nfet_01v8[id] @M.X1.XM1.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM1.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM1.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM1.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM1.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM1.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM5.msky130_fd_pr__nfet_01v8[id] @M.X1.XM5.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM5.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM5.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM5.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM5.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM5.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM6.msky130_fd_pr__nfet_01v8[id] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM6.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM6.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM7.msky130_fd_pr__nfet_01v8[id] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM7.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM7.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM8.msky130_fd_pr__pfet_01v8[id] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM8.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM8.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM8.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM9.msky130_fd_pr__pfet_01v8[id] @M.X1.XM9.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM9.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM9.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM9.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM9.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM9.msky130_fd_pr__pfet_01v8[gds]

*Simulations

.control
  ac dec 100 1k 10G
  setplot ac1
  meas ac GBW when vdb(vout)=0
  meas ac DCG find vdb(vout) at=1k
  *meas ac PM find vp(vout) when vdb(vout)=0
  *print PM*180/PI
  *meas ac GM find vdb(vout) when vp(vout)=0
  plot vdb(vout) \{vp(vout)*180/PI\}
  write opamp_closeloop_ac1.raw
  
  reset
  tran 0.1u 20m
  setplot tran1
  plot v(vsen) v(vout)
  write opamp_closeloop_tran1.raw

  reset    
  noise v(vout) V4 dec 100 1k 10G 1
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
  write opamp_closeloop_op1_today.raw
  
.endc

.end
"}
C {low_noise_amp_v1.sym} 606.25 -438.75 0 0 {name=x1}
C {devices/lab_pin.sym} 456.25 -458.75 3 1 {name=p1 sig_type=std_logic lab=bufp}
C {sky130_fd_pr/pfet_01v8.sym} 333.75 -756.25 0 1 {name=M6
L=4
W=5
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 288.75 -756.25 0 0 {name=p67 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 313.75 -666.25 0 0 {name=I7 value=\{iref\}}
C {devices/lab_pin.sym} 313.75 -851.25 0 0 {name=p70 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 383.75 -756.25 0 1 {name=p68 sig_type=std_logic lab=bufp}
C {sky130_fd_pr/cap_mim_m3_1.sym} 280 -390 0 0 {name=C4 model=cap_mim_m3_1 W=5 L=5 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 280 -360 0 1 {name=p2 sig_type=std_logic lab=0}
C {devices/res.sym} 240 -390 0 0 {name=R1
value=10
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 240 -360 0 1 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 313.75 -636.25 0 0 {name=p7 sig_type=std_logic lab=0}
C {devices/capa.sym} 92.5 -398.75 2 0 {name=C6
m=1
value=2
footprint=1206
device="ceramic capacitor"}
C {devices/capa.sym} 311.25 -528.75 0 0 {name=C5
m=1
value=5p
footprint=1206
device="ceramic capacitor"}
C {devices/res.sym} 185 -458.75 1 0 {name=R2
value=10
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 311.25 -498.75 0 1 {name=p5 sig_type=std_logic lab=0}
