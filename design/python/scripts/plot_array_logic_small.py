import matplotlib.pyplot as plt 
from rawread import *

arrs, plots = rawread('../../netlists/neuron_synapse_array_with_input_output_logic_tb_v1_small.raw')
print(arrs)

arrs[0].dtype.names


print(arrs[0]['V(NEU_ADDR[0])']) # 0 
print(arrs[0]['V(NEU_ADDR[1])']) # 1

fig = plt.figure()
#plt.subplot(7,1,1)
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[0]:NET1)'], label='VMEM0')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:NET1)'], label='VMEM1')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[2]:NET1)'], label='VMEM2')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[3]:NET1)'], label='VMEM3')
plt.plot(arrs[0]['TIME'], arrs[0]['V(REQ)'], label='SPK')
plt.plot(arrs[0]['TIME'], arrs[0]['V(ACK)'], label='ACK')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])



print(arrs[0]['V(SYN_ADDR[0])']) # 1 
print(arrs[0]['V(SYN_ADDR[1])']) # 0 
print(arrs[0]['V(SYN_ADDR[2])']) # 1
print(arrs[0]['V(SYN_ADDR[3])']) # 0 



fig = plt.figure()
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[0]:X2:VSIN)'], label='VSIN0')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[1]:X2:VSIN)'], label='VSIN1')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[2]:X2:VSIN)'], label='VSIN2')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[3]:X2:VSIN)'], label='VSIN3')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[4]:X2:VSIN)'], label='VSIN4')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[5]:X2:VSIN)'], label='VSIN5')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[6]:X2:VSIN)'], label='VSIN6')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[7]:X2:VSIN)'], label='VSIN7')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[8]:X2:VSIN)'], label='VSIN8')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[9]:X2:VSIN)'], label='VSIN9')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[10]:X2:VSIN)'], label='VSIN10')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[11]:X2:VSIN)'], label='VSIN11')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[12]:X2:VSIN)'], label='VSIN12')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[13]:X2:VSIN)'], label='VSIN13')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[14]:X2:VSIN)'], label='VSIN14')
plt.plot(arrs[0]['TIME'], arrs[0]['V(X1:X1:X4[1]:X1:X1[15]:X2:VSIN)'], label='VSIN15')
plt.xlabel("Time [s]")
plt.ylabel("Vmem [V]")
plt.legend(loc="best")
plt.xlim([min(arrs[0]['TIME']), max(arrs[0]['TIME'])])


## synaps number 5

# exc
# print(arrs[0]['V(EXC)'])
