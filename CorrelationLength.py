#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import BoseGas as bg

if len(sys.argv)!=2:
	exit(1)

data = bg.MCData(sys.argv[1])

resol = 32
x = np.linspace(-0.5,0.5,resol)

k = []
for i in range(-data.nmax,data.nmax+1):
	k.append(i)
k = np.array(k)

values = []

status = bg.Status()

for aidx in range(data.alphaCount):
	status.update(aidx,data.alphaCount)
	alphas = data.loadAlphas()
	values.append(np.outer(np.conj(bg.psi(x,k,alphas)),bg.psi(x,k,alphas)))

values = np.array(values)

X, Y = np.meshgrid(x,x)

m = np.abs(np.mean(values,axis=0))
#s = np.abs(np.std(values,axis=0))

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X,Y,m)
#ax.plot_surface(X,Y,s)
plt.show()
