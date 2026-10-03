import matplotlib.pyplot as plt 
from rawread import *

arrs, plots = rawread('../netlists/neuron_32syn_v1_tb.raw')
print(arrs)

arrs[0].dtype.names

fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(arrs[0]['TIME'], arrs[0]['V(MONOUT)'], label='vmem')
plt.plot(arrs[0]['TIME'], arrs[0]['V(SPK1)'], label='SPK')

plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:NET13)'], label='NET13')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X27:SPKE)'], label='SPKE')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(2,1,2)
plt.plot(arrs[0]['TIME'], arrs[0]['V(EXC)'], label='EXC')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X27:NET2)'], label='D[0]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X27:NET1)'], label='D[1]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X27:NET3)'], label='D[2]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X27:NET4)'], label='D[3]')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X27:X3:NET1)'], label='D[3]')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.show()

