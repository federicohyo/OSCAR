v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 60 -110 60 -70 { lab=GND}
N 60 -210 60 -170 { lab=vss}
N 160 -210 160 -170 { lab=vdd}
N 160 -110 160 -70 { lab=vss}
N 260 -300 260 -270 { lab=vin_signal}
N 670 -130 670 -90 { lab=vss}
N 670 -220 670 -190 { lab=#net1}
N 260 -210 260 -170 { lab=vsen}
N 260 -110 260 -70 { lab=vcm}
N 450 -490 510 -490 { lab=vin}
N 440 -490 440 -300 { lab=vin}
N 440 -490 450 -490 { lab=vin}
N 260 -300 320 -300 { lab=vin_signal}
N 490 -300 550 -300 { lab=vin}
N 720 -490 770 -490 { lab=vout}
N 490 -190 490 -150 { lab=vss}
N 490 -300 490 -250 { lab=vin}
N 710 -220 710 -200 { lab=vss}
N 920 -280 920 -250 { lab=vout}
N 920 -190 920 -140 { lab=vss}
N 570 -230 570 -190 { lab=vcm}
N 570 -130 570 -90 { lab=vss}
N 570 -260 570 -230 { lab=vcm}
N 570 -260 630 -260 { lab=vcm}
N 380 -300 490 -300 { lab=vin}
N 770 -490 850 -490 { lab=vout}
N 510 -490 660 -490 { lab=vin}
N 690 -360 690 -330 { lab=vdd}
N 610 -300 630 -300 { lab=#net2}
N 860 -280 880 -280 { lab=vout}
N 850 -490 920 -490 { lab=vout}
N 920 -490 920 -280 { lab=vout}
N 880 -280 920 -280 { lab=vout}
N 770 -280 800 -280 { lab=#net3}
C {devices/vsource.sym} 60 -140 0 0 {name=V1 value=DC\{vss\}}
C {devices/vsource.sym} 160 -140 0 0 {name=V2 value=DC\{vdd\}}
C {devices/gnd.sym} 60 -70 0 0 {name=l14 lab=GND}
C {devices/vsource.sym} 260 -140 0 0 {name=V4 value="sin(0 \{vac\} 1Meg) dc 0 ac 1"}
C {devices/capa.sym} 260 -240 2 0 {name=C4
m=1
value=1
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 160 -210 1 0 {name=l15 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 60 -210 1 0 {name=l16 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 160 -70 3 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 260 -70 3 0 {name=l20 sig_type=std_logic lab=vcm}
C {devices/isource.sym} 670 -160 0 0 {name=I0 value=DC\{iref\}}
C {devices/lab_pin.sym} 670 -90 3 0 {name=l22 sig_type=std_logic lab=vss}
C {devices/lab_wire.sym} 260 -190 3 0 {name=l24 sig_type=std_logic lab=vsen}
C {devices/res.sym} 350 -300 1 0 {name=R1
value=500
footprint=1206
device=resistor
m=1}
C {devices/res.sym} 690 -490 1 0 {name=R3
value=5k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 490 -150 3 0 {name=l28 sig_type=std_logic lab=vss
}
C {devices/capa.sym} 490 -220 0 0 {name=C5
m=1
value=5p
footprint=1206
device="ceramic capacitor"}
C {devices/netlist_not_shown.sym} 110 -470 0 0 {name=SIMULATION only_toplevel=false 

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
  ac dec 100 1k 10G
  setplot ac1
  meas ac GBW when vdb(vout)=0
  meas ac DCG find vdb(vout) at=1k
  *meas ac PM find vp(vout) when vdb(vout)=0
  *print PM*180/PI
  *meas ac GM find vdb(vout) when vp(vout)=0
  plot vdb(vout) \{vp(vout)*180/PI\}
  *write opamp_closeloop_rpad_ac1.raw
  
  reset
  tran 0.01u 11u
  setplot tran1
  plot v(vsen) v(vout)
  *write opamp_closeloop_rpad_tran1.raw

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
  *write opamp_closeloop_rpad_noise.raw
  
  reset
  op
  setplot op1
  print vout  
  *write opamp_closeloop_rapd_op1.raw
  
.endc

.end
"}
C {devices/lab_pin.sym} 710 -200 3 0 {name=l1 sig_type=std_logic lab=vss}
C {devices/capa.sym} 920 -220 0 0 {name=C1
m=1
value=20p
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 920 -140 3 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/lab_wire.sym} 900 -280 0 0 {name=p3 sig_type=std_logic lab=vout}
C {devices/lab_pin.sym} 570 -90 3 0 {name=p5 sig_type=std_logic lab=vss}
C {devices/lab_wire.sym} 610 -260 0 0 {name=p4 sig_type=std_logic lab=vcm}
C {devices/vsource.sym} 570 -160 0 0 {name=V5 value=DC\{vcm\}}
C {devices/lab_wire.sym} 530 -300 0 0 {name=p6 sig_type=std_logic lab=vin}
C {devices/lab_wire.sym} 300 -300 0 0 {name=p7 sig_type=std_logic lab=vin_signal}
C {devices/lab_pin.sym} 690 -360 1 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/res.sym} 580 -300 1 0 {name=R2
value=150
footprint=1206
device=resistor
m=1}
C {devices/res.sym} 830 -280 1 0 {name=R4
value=150
footprint=1206
device=resistor
m=1}
C {low_noise_amp.sym} 680 -280 0 0 {name=x1}
C {sky130_fd_pr/corner.sym} 265 -480 0 0 {name=CORNER only_toplevel=false corner=tt}
