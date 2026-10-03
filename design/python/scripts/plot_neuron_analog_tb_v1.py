import matplotlib.pyplot as plt 
from rawread import *

arrs, plots = rawread('../netlists/neuron_analog_fb_tb_v1.raw')
print(arrs)

arrs[0].dtype.names

fig = plt.figure()
plt.subplot(4,1,1)
plt.plot(arrs[0]['TIME'], arrs[0]['V(VMEM2)'], label='vmem')
plt.plot(arrs[0]['TIME'], arrs[0]['V(MONOUT)'], label='monout')
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(4,1,2)
plt.plot(arrs[0]['TIME'], arrs[0]['V(VSPKI)'], label='spki')
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(4,1,3)
plt.plot(arrs[0]['TIME'], arrs[0]['V(VSPKE)'], label='spke')
plt.plot(arrs[0]['TIME'], arrs[0]['V(NET4)'], label='NET4 IHN')
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])

plt.subplot(4,1,4)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X16:SPKE)'], label='SPKIHN')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X16:NET1)'], label='D[0] IHN')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X16:NET2)'], label='D[1] IHN')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X16:NET3)'], label='D[3] IHN')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X16:NET4)'], label='D[2] IHN')
plt.ylabel("Voltage [V]")

plt.xlabel("Time [s]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])


plt.show()

