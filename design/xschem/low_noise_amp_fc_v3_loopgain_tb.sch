v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 430 -950 430 -930 {
lab=0}
N 430 -1040 430 -1010 {
lab=VDD}
N 920 -550 920 -500 {
lab=0}
N 920 -560 920 -550 {
lab=0}
N 800 -620 850 -620 {
lab=vout}
N 800 -980 830 -980 {
lab=VDD}
N 830 -950 830 -930 {
lab=bufp}
N 870 -980 900 -980 {
lab=bufp}
N 830 -1080 830 -1020 {
lab=VDD}
N 830 -940 880 -940 {
lab=bufp}
N 880 -980 880 -940 {
lab=bufp}
N 830 -930 830 -920 {
lab=bufp}
N 830 -1020 830 -1010 {
lab=VDD}
N 270 -660 270 -560 {
lab=vsen}
N 270 -660 330 -660 {
lab=vsen}
N 390 -660 480 -660 {
lab=vsen}
N 540 -660 580 -660 {
lab=vin}
N 330 -660 390 -660 {
lab=vsen}
N 850 -620 920 -620 {
lab=vout}
N 550 -1000 580 -1000 {
lab=VDD}
N 580 -970 580 -950 {
lab=tunep}
N 620 -1000 650 -1000 {
lab=tunep}
N 580 -1100 580 -1040 {
lab=VDD}
N 580 -960 630 -960 {
lab=tunep}
N 630 -1000 630 -960 {
lab=tunep}
N 580 -950 580 -940 {
lab=tunep}
N 580 -1040 580 -1030 {
lab=VDD}
N 1210 -980 1240 -980 {
lab=VDD}
N 1240 -950 1240 -930 {
lab=vb2}
N 1280 -980 1310 -980 {
lab=vb2}
N 1240 -1080 1240 -1020 {
lab=VDD}
N 1240 -940 1290 -940 {
lab=vb2}
N 1290 -980 1290 -940 {
lab=vb2}
N 1240 -930 1240 -920 {
lab=vb2}
N 1240 -1020 1240 -1010 {
lab=VDD}
N 1000 -990 1030 -990 {
lab=VDD}
N 1030 -960 1030 -940 {
lab=vb1}
N 1070 -990 1100 -990 {
lab=vb1}
N 1030 -1090 1030 -1030 {
lab=VDD}
N 1030 -950 1080 -950 {
lab=vb1}
N 1080 -990 1080 -950 {
lab=vb1}
N 1030 -940 1030 -930 {
lab=vb1}
N 1030 -1030 1030 -1020 {
lab=VDD}
N 620 -180 620 -140 { lab=0}
N 630 -510 630 -460 {
lab=vr}
N 620 -470 620 -430 {
lab=vr}
N 620 -470 630 -470 {
lab=vr}
N 630 -280 630 -250 {
lab=#net1}
N 630 -250 630 -240 {
lab=#net1}
N 670 -430 670 -310 {
lab=#net2}
N 630 -400 630 -340 {
lab=#net2}
N 550 -510 630 -510 {
lab=vr}
N 620 -310 630 -310 {
lab=#net1}
N 620 -430 630 -430 {
lab=vr}
N 620 -310 620 -260 {
lab=#net1}
N 620 -260 630 -260 {
lab=#net1}
N 550 -240 630 -240 {
lab=#net1}
N 550 -510 550 -360 {
lab=vr}
N 550 -300 550 -240 {
lab=#net1}
N 560 -580 560 -510 {
lab=vr}
N 560 -580 580 -580 {
lab=vr}
N 270 -440 270 -400 { lab=0}
N 630 -380 670 -380 {
lab=#net2}
N 270 -500 550 -500 {
lab=vr}
C {devices/vsource.sym} 430 -980 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 430 -1040 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 430 -930 0 0 {name=p96 sig_type=std_logic lab=0}
C {sky130_fd_pr/corner.sym} 240 -1020 0 0 {name=CORNER1 only_toplevel=false corner=tt}
C {devices/lab_pin.sym} 630 -730 2 1 {name=p1 sig_type=std_logic lab=bufp}
C {devices/lab_pin.sym} 920 -500 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 920 -620 0 1 {name=p4 sig_type=std_logic lab=vout}
C {sky130_fd_pr/cap_mim_m3_1.sym} 920 -590 0 0 {name=C1 model=cap_mim_m3_1 W=22 L=22 MF=1 spiceprefix=X}
C {devices/lab_wire.sym} 270 -600 0 0 {name=l1 sig_type=std_logic lab=vsen}
C {devices/simulator_commands.sym} 100 -1020 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value="
* ngspice commands



* Circuit Parameters
*.param iref1 = 200u
.param iref = 6u
.param vdd  = 1.8
.param vss  = 0.0
.param vcm  = 0.8
.param vac  = 5u
.options TEMP = 35.0


* OP Parameters & Singals to save
.save all


+ @M.X1.XM2.msky130_fd_pr__pfet_01v8[id] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM2.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM2.msky130_fd_pr__pfet_01v8[gds] @M.X1.XM2.msky130_fd_pr__pfet_01v8[cgs]
+ @M.X1.XM1.msky130_fd_pr__pfet_01v8[id] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM1.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM1.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM1.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM5.msky130_fd_pr__pfet_01v8[id] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM5.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM5.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM5.msky130_fd_pr__pfet_01v8[gds]


+ @M.X1.XM3.msky130_fd_pr__nfet_01v8[id] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM3.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM3.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM3.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM6.msky130_fd_pr__nfet_01v8[id] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM6.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM6.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM6.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM4.msky130_fd_pr__nfet_01v8[id] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM4.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM4.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM4.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM9.msky130_fd_pr__nfet_01v8[id] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM9.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM9.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM9.msky130_fd_pr__nfet_01v8[gds]

+ @M.X1.XM10.msky130_fd_pr__nfet_01v8[id] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM10.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM10.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM10.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM15.msky130_fd_pr__nfet_01v8[id] @M.X1.XM15.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM15.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM15.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM15.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM15.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM15.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM12.msky130_fd_pr__nfet_01v8[id] @M.X1.XM12.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM12.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM12.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM12.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM12.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM12.msky130_fd_pr__nfet_01v8[gds]
+ @M.X1.XM7.msky130_fd_pr__nfet_01v8[id] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vth] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vgs] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vds] @M.X1.XM7.msky130_fd_pr__nfet_01v8[vdsat] @M.X1.XM7.msky130_fd_pr__nfet_01v8[gm] @M.X1.XM7.msky130_fd_pr__nfet_01v8[gds]

+ @M.X1.XM16.msky130_fd_pr__pfet_01v8[id] @M.X1.XM16.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM16.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM16.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM16.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM16.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM16.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM27.msky130_fd_pr__pfet_01v8[id] @M.X1.XM27.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM27.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM27.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM27.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM27.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM27.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM17.msky130_fd_pr__pfet_01v8[id] @M.X1.XM17.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM17.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM17.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM17.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM17.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM17.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM24.msky130_fd_pr__pfet_01v8[id] @M.X1.XM24.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM24.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM24.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM24.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM24.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM24.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM25.msky130_fd_pr__pfet_01v8[id] @M.X1.XM25.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM25.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM25.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM25.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM25.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM25.msky130_fd_pr__pfet_01v8[gds]
+ @M.X1.XM26.msky130_fd_pr__pfet_01v8[id] @M.X1.XM26.msky130_fd_pr__pfet_01v8[vth] @M.X1.XM26.msky130_fd_pr__pfet_01v8[vgs] @M.X1.XM26.msky130_fd_pr__pfet_01v8[vds] @M.X1.XM26.msky130_fd_pr__pfet_01v8[vdsat] @M.X1.XM26.msky130_fd_pr__pfet_01v8[gm] @M.X1.XM26.msky130_fd_pr__pfet_01v8[gds]



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
  tran 1u 120m
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
  print frequency inoise_spectrum onoise_spectrum > noise_data.csv
  write opamp_closeloop_noise_v1.raw
  
  reset
  op
  setplot op1
  print vout  
  write opamp_closeloop_op1_v3_fctoday.raw
  
.endc

.end
"}
C {devices/lab_wire.sym} 560 -660 3 0 {name=l2 sig_type=std_logic lab=vin}
C {devices/lab_pin.sym} 750 -700 2 0 {name=p9 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 750 -720 0 1 {name=p10 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 850 -980 0 1 {name=M1
L=0.3
W=3.0
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=120
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 830 -860 0 0 {name=p24 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 800 -980 0 0 {name=p25 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 830 -890 0 0 {name=I2 value=\{iref\}}
C {devices/lab_pin.sym} 830 -1080 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 900 -980 0 1 {name=p27 sig_type=std_logic lab=bufp}
C {devices/vsource.sym} 270 -530 0 0 {name=V8 value="sin(0 \{vac\} 100) dc 0 ac 1"}
C {sky130_fd_pr/res_generic_l1.sym} 510 -660 1 1 {name=R1
W=2
L=1
model=res_generic_l1
mult=1}
C {sky130_fd_pr/pfet_01v8.sym} 600 -1000 0 1 {name=M2
L=3.0
W=1.0
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 580 -880 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 550 -1000 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 580 -910 0 0 {name=I1 value=280n}
C {devices/lab_pin.sym} 580 -1100 0 0 {name=p28 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 630 -770 0 0 {name=p30 sig_type=std_logic lab=vb2}
C {devices/lab_pin.sym} 630 -790 0 0 {name=p36 sig_type=std_logic lab=vb1}
C {low_noise_amp_fc_v3.sym} 680 -620 0 0 {name=x1}
C {devices/lab_pin.sym} 1240 -860 0 0 {name=p31 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1210 -980 0 0 {name=p32 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1240 -890 0 0 {name=I3 value=510n}
C {devices/lab_pin.sym} 1240 -1080 0 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1310 -980 0 1 {name=p34 sig_type=std_logic lab=vb2}
C {devices/lab_pin.sym} 650 -1000 0 1 {name=p5 sig_type=std_logic lab=tunep}
C {devices/lab_pin.sym} 630 -750 0 0 {name=p11 sig_type=std_logic lab=tunep}
C {sky130_fd_pr/pfet_01v8.sym} 1050 -990 0 1 {name=M4
L=3.0
W=1.0
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/lab_pin.sym} 1030 -870 0 0 {name=p37 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1000 -990 0 0 {name=p38 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 1030 -900 0 0 {name=I4 value=100n}
C {devices/lab_pin.sym} 1030 -1090 0 0 {name=p39 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1100 -990 0 1 {name=p40 sig_type=std_logic lab=vb1}
C {sky130_fd_pr/pfet_01v8.sym} 1260 -980 0 1 {name=M3
L=3.0
W=1.0
ad="'W * 0.29'" pd="'2 * (W + 0.29)'"
as="'W * 0.29'" ps="'2 * (W + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
nf=1 mult=1
model=pfet_01v8
spiceprefix=X}
C {devices/vsource.sym} 620 -210 0 0 {name=V1 value=DC\{vcm\}}
C {devices/lab_pin.sym} 620 -140 0 0 {name=p8 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 550 -330 2 0 {name=C6 model=cap_mim_m3_1 W=8 L=8 MF=1 spiceprefix=X}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 650 -430 0 1 {name=M12
W=1
L=3.0
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8_hvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_hvt.sym} 650 -310 2 0 {name=M15
W=1
L=3.0
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8_hvt
spiceprefix=X
}
C {devices/lab_wire.sym} 560 -530 0 0 {name=l3 sig_type=std_logic lab=vr}
C {devices/vsource.sym} 270 -470 0 0 {name=V4 value=DC\{vcm\}}
C {devices/lab_pin.sym} 270 -400 0 0 {name=p15 sig_type=std_logic lab=0}
