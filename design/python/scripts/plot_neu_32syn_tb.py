import matplotlib.pyplot as plt 
from rawread import *

arrs, plots = rawread('../netlists/neuron_32syn_tb_xyce.raw')
print(arrs)

arrs[0].dtype.names

fig = plt.figure()
plt.subplot(7,1,1)
plt.plot(arrs[0]['TIME'], arrs[0]['V(MONOUT)'], label='VMEM')
plt.plot(arrs[0]['TIME'], arrs[0]['V(SYN_REQ)'], label='SPK')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(7,1,2)
plt.plot(arrs[0]['TIME'], arrs[0]['V(SETW)'], label='SETW')
plt.plot(arrs[0]['TIME'], arrs[0]['V(RESETW)'], label='RESETW')
plt.plot(arrs[0]['TIME'], arrs[0]['V(EXC)'], label='EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:NET1)'], label='SINP')
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(7,1,3)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET13)'], label='Syn12EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:D[12])']-0.01, label='D[12]EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:NET13)'], label='Syn12INH')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:D[12])']+0.01, label='D[12]INH')
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(7,1,4)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X26:NET1)']-0.01, label='W0EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X26:NET4)']-0.02, label='W1EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X26:NET3)']-0.03, label='W2EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X26:NET2)']-0.04, label='W3EXC')
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(7,1,5)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:NET1)']-0.01, label='W0INH')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:NET3)']-0.02, label='W1INH')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:NET4)']-0.03, label='W2INH')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:NET5)']-0.04, label='W3INH')
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(7,1,6)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:X3:VSIN)']-0.01, label='VSINEXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:SPKE)']-0.01, label='VSPKE')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:NET13)'], label='Syn12INH')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:X3:NET3)'], label='VsinInhON')
#plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:D[0])']-0.01, label='D[0]INH')
#plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:D[1])']-0.02, label='D[1]INH')
#plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:D[2])']-0.03, label='D[2]INH')
#plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:D[3])']-0.04, label='D[3]INH')
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(7,1,7)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X26:X3:VSIN)']-0.01, label='VSINEXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X2:X26:X3:VSIN)']-0.01, label='VSININH')
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.show()

