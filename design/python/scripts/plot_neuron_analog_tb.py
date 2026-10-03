import matplotlib.pyplot as plt 
from rawread import *

arrs, plots = rawread('../netlists/neuron_analog_fb_tb_xyce.raw')
print(arrs)

arrs[0].dtype.names

fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(arrs[0]['TIME'], arrs[0]['V(VMEM0)'], label='vmem (ifdc=1.6V)')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])
plt.subplot(2,1,2)
plt.plot(arrs[0]['TIME'], arrs[0]['V(VSPKE)'], '--', label='inp spike')
plt.plot(arrs[0]['TIME'], arrs[0]['V(VMEM1)'] , label = "vmem")
plt.plot(arrs[0]['TIME'], arrs[0]['V(X4:VSIN)'], label="vsin")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")

plt.show()

