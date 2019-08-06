#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
import BoseGas as bg

def FindNearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

if len(sys.argv)!=2:
	exit(1)

data = bg.MCData(sys.argv[1])

resol = 401
x = np.linspace(-0.5,0.5,resol)

k = []
for i in range(-data.nmax,data.nmax+1):
	k.append(i)
k = np.array(k)

values = np.zeros(resol,dtype=complex)
densityValues = np.zeros(resol,dtype=float)

status = bg.Status()

for aidx in range(data.alphaCount):
	status.update(aidx,data.alphaCount)
	alphas = data.loadAlphas()
	psix = np.array(bg.psi(x,k,alphas))
	densityValues += np.abs(psix)**2
	values += np.conj(bg.psi(0.0,k,alphas))*psix

values = np.abs(values) / data.alphaCount 
densityValues = np.sqrt(densityValues / data.alphaCount)
values = np.divide(values,densityValues[list(x).index(0)]*densityValues)
#plt.plot(x,values)
#plt.show()

tab1 = values[: list(x).index(0)+1]
tab2 = values[list(x).index(0):]
hmax1 = max(tab1)/2.0
hmax2 = max(tab2)/2.0

print(x[FindNearest(tab1,hmax1)])
print(x[list(x).index(0)+FindNearest(tab2,hmax2)])
print((np.abs(x[list(x).index(0)+FindNearest(tab2,hmax2)]-x[FindNearest(tab1,hmax1)]))/2.0)