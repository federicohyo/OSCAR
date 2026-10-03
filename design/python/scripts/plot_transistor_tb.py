import matplotlib.pyplot as plt 
from rawread import *
from scipy.optimize import curve_fit

plt.rcParams['text.usetex'] = True

arrs, plots = rawread('../netlists/transistor_tb.raw')
print(arrs)

arrs[0].dtype.names

def si(x, A, B):
    return A+(x*B)**2

def wi(x, A, B): # this is your 'straight line' y=f(x)
    return  A* np.exp(B*x)

popt, pcov = curve_fit(wi, arrs[0]['sweep'][0:30], arrs[0]['I(VD1)'][0:30]) # your data x, y to fit
popti, pcovi = curve_fit(si, arrs[0]['sweep'][35::], arrs[0]['I(VD1)'][35::]) # your data x, y to fit

dy = np.zeros(arrs[0]['I(VD1)'].shape, np.float)
dy[0:-1] = np.diff(arrs[0]['I(VD1)'])/np.diff(arrs[0]['sweep'])
dy[-1] = (arrs[0]['I(VD1)'][-1] - arrs[0]['I(VD1)'][-2])/(arrs[0]['sweep'][-1] - arrs[0]['sweep'][-2])

igr = np.gradient(arrs[0]['I(VD1)'])

fig = plt.figure()
#plt.subplot(2,1,1)
plt.plot(arrs[0]['sweep'], arrs[0]['I(VD1)'], '.')
plt.plot(arrs[0]['sweep'][0:70], wi(arrs[0]['sweep'][0:70], *popt), 'r-', label="$I_{d} = A  e^{V_{g}B}$" ) 
plt.plot(arrs[0]['sweep'], si(arrs[0]['sweep'], *popti), 'g-', label="$I_{d} = A + (V_{g}B)^{2} $" )
plt.yscale("log")
plt.ylabel(r'$I_{d}$', fontsize=26)
plt.xlabel(r'$V_{g}$', fontsize=26)
plt.gca().yaxis.grid(True, which="both", linewidth=1)
plt.yticks(fontsize=26)
plt.xticks(fontsize=26)
#plt.legend(loc="best", fontsize=16)
#plt.xlim([0.00, 1.8])

fig = plt.figure()
#plt.subplot(2,1,2)
plt.plot(arrs[0]['I(VD1)'], dy)
plt.xlabel(r'$I_{d}$', fontsize=26)
plt.ylabel(r'$g_{m}$', fontsize=26)
plt.gca().yaxis.grid(True, which="both", linewidth=1)
plt.gca().xaxis.grid(True, which="both", linewidth=1)
plt.yscale("log")
plt.xscale("log")
plt.yticks(fontsize=26)
plt.xticks(fontsize=26)
#
#plt.xlim([0.1, 1.8])



plt.show()

