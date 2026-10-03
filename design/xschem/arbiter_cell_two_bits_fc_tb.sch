v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 1915 -680 2715 -280 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0.002
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="gc1
gc0
nreq_neu0
nreq_neu1
nack_neu0
nack_neu1"
color="19 4 7 12 10 6"
dataset=-1
unitx=1
logx=0
logy=0
}
T {Neuron biases} 356.25 -354.375 0 0 0.4 0.4 {}
T {Neurons are driven by injection current ifdc} 380 -1177.5 0 0 0.4 0.4 {}
T {Neuron biases} 150 -270 0 0 0.4 0.4 {}
T {Power up reset} 1210 -260 0 0 0.4 0.4 {}
N 1658.75 -430.625 1658.75 -410.625 {
lab=0}
N 1658.75 -520.625 1658.75 -490.625 {
lab=aVDD}
N 730 -980 760 -980 {
lab=nreq_neu0}
N 370 -590 430 -590 {
lab=nack_neu1}
N 370 -980 430 -980 {
lab=nack_neu0}
N 930 -880 940 -880 {
lab=req_neu0}
N 940 -880 1040 -880 {
lab=req_neu0}
N 930 -830 950 -830 {
lab=req_neu1}
N 950 -860 950 -830 {
lab=req_neu1}
N 950 -860 1040 -860 {
lab=req_neu1}
N 830 -880 850 -880 {
lab=nreq_neu0}
N 830 -980 830 -880 {
lab=nreq_neu0}
N 760 -980 830 -980 {
lab=nreq_neu0
.IC=VDD}
N 730 -590 770 -590 {
lab=nreq_neu1}
N 850 -740 850 -650 {
lab=nreq_neu1}
N 760 -650 850 -650 {
lab=nreq_neu1}
N 760 -650 760 -590 {
lab=nreq_neu1}
N 1010 -900 1040 -900 {
lab=ack_out
.IC=GND}
N 875 -550 875 -530 {
lab=vmem1}
N 755 -550 875 -550 {
lab=vmem1}
N 730 -550 755 -550 {
lab=vmem1}
N 875 -470 875 -445 {
lab=0}
N 300 -220 300 -190 {
lab=vrefn}
N 220 -220 220 -190 {
lab=vleakn}
N 500 -210 500 -180 {
lab=ifahwp}
N 420 -210 420 -180 {
lab=ifnmdap}
N 610 -210 610 -180 {
lab=ifdcp}
N 730 -210 730 -180 {
lab=ifahthrp}
N 850 -210 850 -180 {
lab=ifthrp}
N 970 -210 970 -180 {
lab=ifcascn}
N 1100 -210 1100 -180 {
lab=ifahtaun}
N 1250 -210 1250 -180 {
lab=nRes}
N 65 -90 1255 -90 {
lab=0}
N 1255 -120 1255 -90 {
lab=0}
N 1245 -120 1255 -120 {
lab=0}
N 1095 -120 1095 -90 {
lab=0}
N 1095 -120 1105 -120 {
lab=0}
N 975 -120 975 -90 {
lab=0}
N 965 -120 975 -120 {
lab=0}
N 845 -120 855 -120 {
lab=0}
N 845 -120 845 -90 {
lab=0}
N 225 -110 225 -90 {
lab=0}
N 225 -130 225 -110 {
lab=0}
N 215 -130 225 -130 {
lab=0}
N 295 -130 305 -130 {
lab=0}
N 295 -130 295 -90 {
lab=0}
N 415 -120 435 -120 {
lab=0}
N 435 -120 435 -90 {
lab=0}
N 495 -120 505 -120 {
lab=0}
N 505 -120 505 -90 {
lab=0}
N 605 -120 615 -120 {
lab=0}
N 615 -120 615 -90 {
lab=0}
N 725 -120 735 -120 {
lab=0}
N 735 -120 735 -90 {
lab=0}
N 905 -1065 905 -1040 {
lab=0}
N 775 -940 905 -940 {
lab=vmem0}
N 905 -980 905 -940 {
lab=vmem0}
N 765 -940 775 -940 {
lab=vmem0}
N 730 -940 765 -940 {
lab=vmem0}
N 850 -830 850 -740 {
lab=nreq_neu1}
C {arbiter_cell_two_bits_fc.sym} 1190 -860 0 0 {name=x1}
C {devices/vsource.sym} 1658.75 -460.625 0 0 {name=V2 value=\{aVDD\}}
C {devices/lab_pin.sym} 1658.75 -520.625 0 0 {name=p35 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1286.875 -1052.5 2 0 {name=p5 sig_type=std_logic lab=nack_neu0}
C {devices/lab_pin.sym} 1340 -860 2 0 {name=p49 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 985 -880 1 0 {name=p2 sig_type=std_logic lab=req_neu0}
C {devices/lab_pin.sym} 950 -830 3 0 {name=p3 sig_type=std_logic lab=req_neu1}
C {neuron_analog_fc.sym} 580 -890 0 0 {name=x3}
C {devices/lab_pin.sym} 830 -980 1 0 {name=p8 sig_type=std_logic lab=nreq_neu0}
C {devices/lab_pin.sym} 770 -590 2 0 {name=p9 sig_type=std_logic lab=nreq_neu1}
C {neuron_analog_fc.sym} 580 -500 0 0 {name=x4}
C {devices/lab_pin.sym} 430 -450 0 0 {name=p10 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 430 -430 0 0 {name=p11 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 430 -570 0 0 {name=p12 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 430 -550 0 0 {name=p13 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 430 -530 0 0 {name=p14 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 430 -510 0 0 {name=p16 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 430 -490 0 0 {name=p17 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 430 -470 0 0 {name=p18 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 430 -410 0 0 {name=p19 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 430 -840 0 0 {name=p20 sig_type=std_logic lab=vleakn}
C {devices/lab_pin.sym} 430 -820 0 0 {name=p22 sig_type=std_logic lab=vrefn}
C {devices/lab_pin.sym} 430 -960 0 0 {name=p23 sig_type=std_logic lab=ifnmdap}
C {devices/lab_pin.sym} 430 -940 0 0 {name=p24 sig_type=std_logic lab=ifahwp}
C {devices/lab_pin.sym} 430 -920 0 0 {name=p25 sig_type=std_logic lab=ifdcp}
C {devices/lab_pin.sym} 430 -900 0 0 {name=p26 sig_type=std_logic lab=ifahthrp}
C {devices/lab_pin.sym} 430 -880 0 0 {name=p27 sig_type=std_logic lab=ifthrp}
C {devices/lab_pin.sym} 430 -860 0 0 {name=p28 sig_type=std_logic lab=ifcascn}
C {devices/lab_pin.sym} 430 -800 0 0 {name=p29 sig_type=std_logic lab=ifahtaun}
C {devices/code_shown.sym} 1529.375 -1096.875 0 0 {name=SPICE only_toplevel=false value="

.TRAN 0.01us 2ms 
.PRINT TRAN format=raw file=arbiter_cell_two_bits_fc_xyce.raw v(*) i(*)

.param aVDD = 1.8V
.options timeint reltol=5e-3 abstol=1e-3
* Continuation Options
.options nonlin continuation=gmin

"}
C {devices/code.sym} 1279.375 -542.5 0 0 {name=stdcell_lib only_toplevel=true value="tcleval(
* Standard cell simulation files
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
)"}
C {sky130_fd_pr/corner.sym} 1119.375 -542.5 0 0 {name=CORNER only_toplevel=true corner=tt}
C {devices/lab_pin.sym} 1869.375 -237.5 2 0 {name=p32 sig_type=std_logic lab=ack_out}
C {devices/lab_pin.sym} 1549.375 -237.5 0 0 {name=p38 sig_type=std_logic lab=req_out}
C {devices/lab_pin.sym} 730 -530 2 0 {name=p52 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -920 2 0 {name=p53 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -960 2 0 {name=p54 sig_type=std_logic lab=sinp0}
C {devices/lab_pin.sym} 730 -570 2 0 {name=p55 sig_type=std_logic lab=sinp1}
C {sky130_stdcells/inv_1.sym} 1246.875 -1052.5 0 0 {name=x6 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1246.875 -992.5 0 0 {name=x7 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1340 -880 2 0 {name=p58 sig_type=std_logic lab=gc0}
C {devices/lab_pin.sym} 1340 -900 2 0 {name=p59 sig_type=std_logic lab=gc1}
C {sky130_stdcells/inv_1.sym} 890 -880 0 0 {name=x8 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 890 -830 0 0 {name=x9 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1589.375 -237.5 0 0 {name=x5 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1669.375 -237.5 0 0 {name=x10 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {c_element_rj.sym} 580 -1060 0 0 {name=x14}
C {devices/lab_pin.sym} 730 -1040 2 0 {name=p78 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -1080 2 0 {name=p82 sig_type=std_logic lab=ack_cel0}
C {devices/lab_pin.sym} 430 -1080 0 0 {name=p84 sig_type=std_logic lab=nRes}
C {c_element_rj.sym} 580 -690 0 0 {name=x11}
C {devices/lab_pin.sym} 730 -670 2 0 {name=p34 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 730 -710 2 0 {name=p61 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 430 -710 0 0 {name=p62 sig_type=std_logic lab=nRes}
C {devices/lab_pin.sym} 430 -690 0 0 {name=p39 sig_type=std_logic lab=req_neu1}
C {devices/lab_pin.sym} 430 -1060 0 0 {name=p63 sig_type=std_logic lab=req_neu0}
C {devices/lab_pin.sym} 1206.875 -1052.5 0 0 {name=p56 sig_type=std_logic lab=ack_cel0}
C {devices/lab_pin.sym} 1206.875 -992.5 0 0 {name=p57 sig_type=std_logic lab=ack_cel1}
C {devices/lab_pin.sym} 370 -590 0 0 {name=p30 sig_type=std_logic lab=nack_neu1}
C {devices/lab_pin.sym} 370 -980 0 0 {name=p31 sig_type=std_logic lab=nack_neu0}
C {devices/lab_pin.sym} 430 -1040 0 0 {name=p60 sig_type=std_logic lab=gc0}
C {devices/lab_pin.sym} 430 -670 0 0 {name=p64 sig_type=std_logic lab=gc1}
C {devices/lab_pin.sym} 730 -1060 2 0 {name=p37 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 730 -690 2 0 {name=p65 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 730 -900 2 0 {name=p48 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 730 -510 2 0 {name=p50 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1010 -900 1 0 {name=p1 sig_type=std_logic lab=ack_out}
C {devices/lab_pin.sym} 1286.875 -992.5 2 0 {name=p4 sig_type=std_logic lab=nack_neu1}
C {devices/lab_pin.sym} 900 -940 2 0 {name=p6 sig_type=std_logic lab=vmem0}
C {devices/lab_pin.sym} 875 -550 2 0 {name=p7 sig_type=std_logic lab=vmem1}
C {devices/lab_pin.sym} 1658.75 -412.5 3 0 {name=p67 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 875 -500 2 0 {name=C1 model=cap_mim_m3_1 W=11 L=11 MF=1 spiceprefix=X}
C {devices/vsource.sym} 300 -160 0 0 {name=V13 value=0.4}
C {devices/lab_pin.sym} 300 -220 0 0 {name=p47 sig_type=std_logic lab=vrefn}
C {devices/vsource.sym} 220 -160 0 0 {name=V14 value=0}
C {devices/lab_pin.sym} 220 -220 0 0 {name=p79 sig_type=std_logic lab=vleakn}
C {devices/vsource.sym} 500 -150 0 0 {name=V16 value=1.8}
C {devices/lab_pin.sym} 500 -210 0 0 {name=p80 sig_type=std_logic lab=ifahwp}
C {devices/vsource.sym} 420 -150 0 0 {name=V18 value=0}
C {devices/lab_pin.sym} 420 -210 0 0 {name=p81 sig_type=std_logic lab=ifnmdap}
C {devices/vsource.sym} 610 -150 0 0 {name=V19 value=1.6}
C {devices/lab_pin.sym} 610 -210 0 0 {name=p83 sig_type=std_logic lab=ifdcp}
C {devices/vsource.sym} 730 -150 0 0 {name=V21 value=1.8}
C {devices/lab_pin.sym} 730 -210 0 0 {name=p85 sig_type=std_logic lab=ifahthrp}
C {devices/vsource.sym} 850 -150 0 0 {name=V22 value=1.8}
C {devices/lab_pin.sym} 850 -210 0 0 {name=p86 sig_type=std_logic lab=ifthrp}
C {devices/vsource.sym} 970 -150 0 0 {name=V23 value=0}
C {devices/lab_pin.sym} 970 -210 0 0 {name=p87 sig_type=std_logic lab=ifcascn}
C {devices/vsource.sym} 1100 -150 0 0 {name=V24 value=0}
C {devices/lab_pin.sym} 1100 -210 0 0 {name=p88 sig_type=std_logic lab=ifahtaun}
C {devices/lab_pin.sym} 1250 -210 0 0 {name=p93 sig_type=std_logic lab=nRes}
C {devices/vsource.sym} 1250 -150 0 0 {name=V26 value="pulse(1.8 0 1ns 1us 1us 1us 10ms 1)"}
C {devices/lab_pin.sym} 70 -90 0 0 {name=p94 sig_type=std_logic lab=0}
C {sky130_fd_pr/cap_mim_m3_1.sym} 905 -1010 0 0 {name=C2 model=cap_mim_m3_1 W=11 L=11 MF=1 spiceprefix=X}
C {tie_low.sym} 1190 -740 0 0 {name=x2}
C {tie_low.sym} 1190 -650 0 0 {name=x12}
C {devices/lab_pin.sym} 1340 -760 2 0 {name=p33 sig_type=std_logic lab=sinp0}
C {devices/lab_pin.sym} 1340 -670 2 0 {name=p40 sig_type=std_logic lab=sinp1}
C {devices/lab_pin.sym} 1330 -650 2 0 {name=p43 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1340 -740 2 0 {name=p44 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 875 -445 2 0 {name=p15 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 905 -1065 2 0 {name=p45 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1340 -720 2 0 {name=p41 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1340 -630 2 0 {name=p42 sig_type=std_logic lab=0}
C {sky130_stdcells/inv_1.sym} 1749.375 -237.5 0 0 {name=x13 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {sky130_stdcells/inv_1.sym} 1829.375 -237.5 0 0 {name=x15 VGND=0 VNB=0 VPB=aVDD VPWR=aVDD prefix=sky130_fd_sc_hd__ }
C {devices/lab_pin.sym} 1340 -840 2 0 {name=p21 sig_type=std_logic lab=aVDD}
C {devices/lab_pin.sym} 1340 -820 2 0 {name=p36 sig_type=std_logic lab=0}
