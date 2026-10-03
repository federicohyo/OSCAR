import matplotlib.pyplot as plt 
from rawread import *

arrs, plots = rawread('../netlists/neuron_4syn_v1_tb.raw')
#print(arrs)

#arrs[0].dtype.names

fig = plt.figure()
plt.subplot(4,1,1)
plt.plot(arrs[0]['TIME'], arrs[0]['V(SPK1)'], label='SPK')

plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET2)'], label='NET3 - syn addr 10')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X5:SPKE)'], label='SPKE')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(4,1,2)
plt.plot(arrs[0]['TIME'], arrs[0]['V(MONOUT)'], label='vmem')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:NET1)'], label='VMEM')
plt.plot(arrs[0]['TIME'], arrs[0]['V(EXC)'], label='EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X5:NET2)'], label='D[0]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X5:NET1)'], label='D[1]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X5:NET3)'], label='D[2]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X5:NET4)'], label='D[3]')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(4,1,3)
#plt.plot(arrs[0]['TIME'], -arrs[0]['I(X1:X3:IFDC)'], label='IFDC')
#plt.plot(arrs[0]['TIME'], -arrs[0]['I(X1:X3:ILEAK)'], label='ILEAK')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:NET2)'], label='NET2')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:NREQ_NEU1)'], label='NREQ')
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])


plt.subplot(4,1,4)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET1)'], label='Req D[0]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET2)'], label='Req D[1]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET3)'], label='Req D[2]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET4)'], label='Req D[3]')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])



plt.show()

