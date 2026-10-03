v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 650 -460 1450 -60 {flags=graph
y1=0.0000001

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=u
x1=0
x2=1.8
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
node=i(vd1)
color=5
dataset=-1
unitx=1
logx=0
logy=0
y2=0.00014}
B 2 640 -880 1440 -480 {flags=graph
y1=0

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=k


divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
node="\\"1 i(vd1) deriv() /\\""
color=8
dataset=-1
unitx=1
logx=0
logy=0
y2=60000000000
x2=1.8
x1=0}
T {https://www.youtube.com/watch?v=fggf9DeVN5k} 80 -830 0 0 0.4 0.4 {}
N 350 -230 350 -190 {
lab=D}
N 350 -80 350 -40 {
lab=0}
N 260 -160 310 -160 {
lab=G}
N 350 -160 420 -160 {
lab=0}
N 60 -200 60 -170 {
lab=D}
N 160 -200 160 -170 {
lab=G}
N 60 -110 60 -80 {
lab=0}
N 160 -110 160 -80 {
lab=0}
C {devices/code_shown.sym} 42.3828125 -739.6484375 0 0 {name=Xyce only_toplevel=false value="

*.dc VD 0 1.8 0.01 VG 0 1.8 0.2
.dc VG 0 1.8 0.01
.print dc format=raw file=transistor_tb.raw v(*) i(*)"}
C {sky130_fd_pr/corner.sym} 110 -520 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 350 -40 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 60 -200 0 0 {name=p3 sig_type=std_logic lab=D}
C {devices/vsource.sym} 60 -140 0 0 {name=VD value=1.8}
C {devices/ammeter.sym} 350 -100 0 0 {name=VD1 savecurrent=true}
C {devices/lab_pin.sym} 160 -200 0 0 {name=p2 sig_type=std_logic lab=G}
C {devices/vsource.sym} 160 -140 0 0 {name=VG value=0}
C {devices/lab_pin.sym} 60 -80 0 0 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 160 -80 0 0 {name=p6 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 260 -160 0 0 {name=p4 sig_type=std_logic lab=G}
C {sky130_fd_pr/nfet_01v8.sym} 330 -160 0 0 {name=M2
L=1
W=1
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
C {devices/lab_pin.sym} 420 -160 2 0 {name=p7 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 350 -230 0 0 {name=p8 sig_type=std_logic lab=D}
