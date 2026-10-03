v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 430 -130 450 -130 {
lab=a[0]}
N 140 -270 310 -270 {
lab=y[3]}
N 220 -270 220 -150 {
lab=y[3]}
N 220 -150 310 -150 {
lab=y[3]}
N 270 -230 310 -230 {
lab=y[2]}
N 250 -110 310 -110 {
lab=y[1]}
N 240 -60 420 -60 {
lab=y[0]}
N 430 -250 450 -250 {
lab=a[1]}
C {devices/opin.sym} 60 -100 0 0 {name=p17 lab=a[0:1]}
C {devices/ipin.sym} 100 -130 0 0 {name=p26 lab=y[0:3]


}
C {devices/lab_pin.sym} 450 -250 0 1 {name=p3 lab=a[1]}
C {devices/lab_pin.sym} 450 -130 0 1 {name=p1 lab=a[0]}
C {devices/lab_pin.sym} 140 -270 0 0 {name=p2 lab=y[3]}
C {devices/lab_pin.sym} 270 -230 0 0 {name=p4 lab=y[2]}
C {devices/lab_pin.sym} 250 -110 0 0 {name=p5 lab=y[1]}
C {devices/lab_pin.sym} 240 -60 0 0 {name=p6 lab=y[0]}
C {sky130_stdcells/or2_0.sym} 370 -250 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/or2_0.sym} 370 -130 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/iopin.sym} 60 -80 0 0 {name=p7 lab=VDD}
C {devices/iopin.sym} 60 -60 0 0 {name=p8 lab=GND}
