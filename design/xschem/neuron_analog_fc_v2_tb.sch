v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1380 -630 2180 -230 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.001
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="vmem1
spk1"
color="7 8"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=1}
T {Neuron biases} 495 -775 0 0 0.4 0.4 {}
N 155 -555 155 -535 {
lab=0}
N 155 -645 155 -615 {
lab=VDD}
N 300 -630 330 -630 {
lab=0}
N 325 -600 325 -595 {
lab=0}
N 325 -595 325 -575 {
lab=0}
N 365 -630 395 -630 {
lab=vleakn}
N 325 -575 325 -570 {
lab=0}
N 325 -665 325 -660 {
lab=vleakn}
N 325 -670 325 -665 {
lab=vleakn}
N 325 -570 325 -510 {
lab=0}
N 300 -630 300 -570 {
lab=0}
N 300 -570 325 -570 {
lab=0}
N 325 -665 380 -665 {
lab=vleakn}
N 380 -665 380 -630 {
lab=vleakn}
N 530 -635 560 -635 {
lab=VDD}
N 555 -605 555 -600 {
lab=ifdcp}
N 555 -600 555 -580 {
lab=ifdcp}
N 595 -635 625 -635 {
lab=ifdcp}
N 555 -730 555 -670 {
lab=VDD}
N 555 -595 605 -595 {
lab=ifdcp}
N 605 -635 605 -595 {
lab=ifdcp}
N 555 -580 555 -575 {
lab=ifdcp}
N 555 -670 555 -665 {
lab=VDD}
N 760 -630 790 -630 {
lab=0}
N 785 -600 785 -595 {
lab=0}
N 785 -595 785 -575 {
lab=0}
N 825 -630 855 -630 {
lab=vrefn}
N 785 -575 785 -570 {
lab=0}
N 785 -665 785 -660 {
lab=vrefn}
N 785 -670 785 -665 {
lab=vrefn}
N 785 -570 785 -510 {
lab=0}
N 760 -630 760 -570 {
lab=0}
N 760 -570 785 -570 {
lab=0}
N 785 -665 840 -665 {
lab=vrefn}
N 840 -665 840 -630 {
lab=vrefn}
N 455 -270 547.5 -270 {
lab=spk1}
N 985 -600 985 -580 {
lab=0}
N 985 -690 985 -660 {
lab=nRes}
C {neuron_analog_fc_v2.sym} 505 -390 0 0 {name=x1}
C {devices/simulator_commands_shown.sym} 1605 -155 0 0 {name=COMMANDS1
simulator=ngspice
only_toplevel=false 
value="
.save all
.control
tran 0.01us 1ms
write neuron_analog_fb_tb_v2.raw
set appendwrite
.endc
"}
C {devices/vsource.sym} 155 -585 0 0 {name=V2 value=1.8}
C {devices/lab_pin.sym} 155 -645 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 155 -535 0 0 {name=p96 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 395 -630 0 1 {name=p46 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 325 -510 0 0 {name=p15 sig_type=std_logic lab=0}
C {devices/isource.sym} 325 -700 0 0 {name=I3 value=100f}
C {sky130_fd_pr/nfet_01v8.sym} 345 -630 0 1 {name=M4
L=2.0
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
C {devices/lab_pin.sym} 325 -730 0 0 {name=p64 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 575 -635 0 1 {name=M6
L=1.0
W=2.0
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
C {devices/lab_pin.sym} 555 -515 0 0 {name=p63 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 530 -635 0 0 {name=p67 sig_type=std_logic lab=VDD}
C {devices/isource.sym} 555 -545 0 0 {name=I5 value=500p}
C {devices/lab_pin.sym} 555 -730 0 0 {name=p70 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 625 -635 0 1 {name=p68 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 785 -510 0 0 {name=p65 sig_type=std_logic lab=0}
C {devices/isource.sym} 785 -700 0 0 {name=I4 value=500p}
C {sky130_fd_pr/nfet_01v8.sym} 805 -630 0 1 {name=M5
L=1
W=0.65
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
C {devices/lab_pin.sym} 785 -730 0 0 {name=p66 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 855 -630 0 1 {name=p41 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 355 -380 0 0 {name=p1 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 355 -420 0 0 {name=p2 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 355 -360 0 0 {name=p3 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 655 -400 0 1 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 655 -420 0 1 {name=p5 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 485 -157.5 0 0 {name=p178 sig_type=std_logic lab=ack_cel1}
C {sky130_stdcells/inv_1.sym} 525 -157.5 0 0 {name=x16 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 565 -157.5 2 0 {name=p179 sig_type=std_logic lab=nack_cel1}
C {devices/lab_pin.sym} 355 -400 0 0 {name=p24 sig_type=std_logic lab=nack_cel1}
C {devices/lab_pin.sym} 655 -380 2 0 {name=p165 sig_type=std_logic lab=nspk_tmp1}
C {devices/lab_pin.sym} 655 -360 0 1 {name=p166 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 707.5 -270 2 0 {name=p167 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 355 -270 0 0 {name=p168 sig_type=std_logic lab=nspk_tmp1}
C {sky130_stdcells/inv_1.sym} 587.5 -270 0 0 {name=x6 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 667.5 -270 0 0 {name=x10 VGND=0 VNB=0 VPB=VDD VPWR=VDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 507.5 -270 3 0 {name=p169 sig_type=std_logic lab=spk1}
C {schmitt_trigger.sym} 435 -270 0 0 {name=x14}
C {devices/lab_pin.sym} 395 -230 2 0 {name=p170 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 395 -310 2 0 {name=p171 sig_type=std_logic lab=VDD}
C {c_element_rj.sym} 547.5 -70 0 0 {name=x15}
C {devices/lab_pin.sym} 397.5 -70 0 0 {name=p172 sig_type=std_logic lab=ack1}
C {devices/lab_pin.sym} 397.5 -50 0 0 {name=p173 sig_type=std_logic lab=spk1}
C {devices/lab_pin.sym} 697.5 -90 2 0 {name=p174 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 397.5 -90 0 0 {name=p175 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 697.5 -70 2 0 {name=p176 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 697.5 -50 0 1 {name=p177 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 985 -690 0 0 {name=p83 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 985 -630 0 0 {name=V11 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 985 -580 0 0 {name=p98 sig_type=std_logic lab=0}
C {sky130_fd_pr/corner.sym} 1020 -430 0 0 {name=CORNER only_toplevel=false corner=tt}
C {devices/code.sym} 890 -430 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice)"}
C {devices/simulator_commands_shown.sym} 895 -145 0 0 {name=COMMANDS2
simulator=Xyce
only_toplevel=false 
value="
.TRAN 0.01us 1ms
.PRINT TRAN format=raw file=neuron_analog_fb_tb_v2.raw v(*) i(*)
.OPTION LINSOL TYPE=AztecOO PREC_TYPE=Ifpack
"}
