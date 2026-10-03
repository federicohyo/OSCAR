v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 190 -120 190 -80 {
lab=QN}
N 190 -120 310 -190 {
lab=QN}
N 310 -210 310 -190 {
lab=QN}
N 310 -210 360 -210 {
lab=QN}
N 190 -190 190 -160 {
lab=Q}
N 190 -160 310 -80 {
lab=Q}
N 310 -80 310 -60 {
lab=Q}
N 310 -60 360 -60 {
lab=Q}
N 140 -40 190 -40 {
lab=rst}
N 140 -230 190 -230 {
lab=set}
C {sky130_stdcells/nor2_1.sym} 250 -210 0 0 {name=x1 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/nor2_1.sym} 250 -60 0 0 {name=x2 VGND=GND VNB=GND VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/ipin.sym} 140 -230 0 0 {name=p1 lab=set}
C {devices/ipin.sym} 140 -40 0 0 {name=p2 lab=rst}
C {devices/opin.sym} 360 -60 0 0 {name=p3 lab=Q}
C {devices/opin.sym} 360 -210 0 0 {name=p4 lab=QN}
C {devices/iopin.sym} 140 -310 0 0 {name=p5 lab=VDD}
C {devices/iopin.sym} 140 -290 0 0 {name=p6 lab=GND}
