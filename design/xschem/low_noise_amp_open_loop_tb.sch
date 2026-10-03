v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 82.5 -87.5 82.5 -50 { lab=GND}
N 82.5 -187.5 82.5 -147.5 { lab=vss}
N 170 -187.5 170 -147.5 { lab=vdd}
N 170 -87.5 170 -50 { lab=vss}
N 480 -200 480 -160 { lab=vss}
N 270 -285 270 -247.5 { lab=vin}
N 580 -200 580 -160 { lab=vss}
N 270 -187.5 270 -147.5 { lab=vsen}
N 270 -87.5 270 -50 { lab=vcm}
N 160 -380 290 -380 { lab=ve}
N 230 -570 290 -570 { lab=ve}
N 220 -570 220 -380 { lab=ve}
N 220 -570 230 -570 { lab=ve}
N 40 -380 100 -380 { lab=vcm}
N 350 -380 400 -380 { lab=vin}
N 400 -380 460 -380 { lab=vin}
N 400 -270 400 -230 { lab=vss}
N 400 -380 400 -330 { lab=vin}
N 580 -300 580 -260 { lab=#net1}
N 618.75 -300 618.75 -280 { lab=vss}
N 730 -360 730 -340 { lab=vout}
N 680 -360 730 -360 { lab=vout}
N 730 -280 730 -250 { lab=vss}
N 598.75 -440 598.75 -410 { lab=vdd}
N 490 -340 540 -340 { lab=vcm}
N 480 -340 480 -260 { lab=vcm}
N 480 -340 490 -340 { lab=vcm}
N 460 -380 540 -380 { lab=vin}
N 540 -570 730 -570 { lab=vout}
N 730 -570 730 -360 { lab=vout}
N 290 -570 480 -570 { lab=ve}
N 578.75 -300 580 -300 {}
N 678.75 -360 681.25 -360 {}
C {devices/vsource.sym} 82.5 -117.5 0 0 {name=V1 value=DC\{vss\}}
C {devices/vsource.sym} 170 -117.5 0 0 {name=V2 value=DC\{vdd\}}
C {devices/vsource.sym} 480 -230 0 0 {name=V3 value=DC\{vcm\}}
C {devices/gnd.sym} 82.5 -50 0 0 {name=l14 lab=GND}
C {devices/vsource.sym} 270 -117.5 0 0 {name=V4 value="sin(0 \{vac\} 1Meg) dc 0 ac 1"}
C {devices/capa.sym} 270 -217.5 2 0 {name=C4
m=1
value=1
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 170 -187.5 1 0 {name=l15 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 82.5 -187.5 1 0 {name=l16 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 170 -50 3 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 480 -160 3 0 {name=l19 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 270 -50 3 0 {name=l20 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 270 -285 1 0 {name=l21 sig_type=std_logic lab=vin}
C {devices/isource.sym} 580 -230 0 0 {name=I0 value=DC\{iref\}}
C {devices/lab_pin.sym} 580 -160 3 0 {name=l22 sig_type=std_logic lab=vss}
C {devices/lab_wire.sym} 270 -175 3 0 {name=l24 sig_type=std_logic lab=vsen}
C {devices/res.sym} 130 -380 1 0 {name=R1
value=500
footprint=1206
device=resistor
m=1}
C {devices/res.sym} 320 -380 1 0 {name=R2
value=1G
footprint=1206
device=resistor
m=1}
C {devices/res.sym} 510 -570 1 0 {name=R3
value=5k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 40 -380 0 0 {name=l25 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 202.5 -380 0 0 {name=l26 sig_type=std_logic lab=ve

}
C {devices/lab_pin.sym} 400 -230 3 0 {name=l28 sig_type=std_logic lab=vss
}
C {devices/capa.sym} 400 -300 0 0 {name=C5
m=1
value=5p
footprint=1206
device="ceramic capacitor"}
C {devices/netlist_not_shown.sym} 30 -550 0 0 {name=SIMULATION only_toplevel=false 

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

*Simulation
.control
  
  ac dec 100 1 10G
  setplot ac1
  meas ac GBW when vdb(vout)=0
  meas ac DCG find vdb(vout) at=1
  meas ac PM find vp(vout) when vdb(vout)=0
  print PM*180/PI
  meas ac GM find vdb(vout) when vp(vout)=0
  plot vdb(vout) \{vp(vout)*180/PI\}
  write opamp_openloop_ac1.raw

  reset
  op
  setplot op1
  write opamp_openloop_op1.raw

.endc

.end
"}
C {devices/lab_pin.sym} 618.75 -280 3 0 {name=l1 sig_type=std_logic lab=vss}
C {devices/capa.sym} 730 -310 0 0 {name=C1
m=1
value=20p
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 730 -250 3 0 {name=l2 sig_type=std_logic lab=vss}
C {devices/lab_wire.sym} 722.5 -360 0 0 {name=l3 sig_type=std_logic lab=vout

}
C {devices/lab_pin.sym} 598.75 -440 1 0 {name=l4 sig_type=std_logic lab=vdd}
C {devices/lab_wire.sym} 522.5 -340 0 0 {name=l5 sig_type=std_logic lab=vcm

}
C {devices/lab_wire.sym} 472.5 -380 0 0 {name=l6 sig_type=std_logic lab=vin

}
C {low_noise_amp.sym} 588.75 -360 0 0 {name=x1}
C {sky130_fd_pr/corner.sym} 31.25 -723.75 0 0 {name=CORNER only_toplevel=false corner=tt}
