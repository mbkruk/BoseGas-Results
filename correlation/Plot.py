#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

g1=[]
g2=[]
g3=[]

X=[]
iX, iY =np.loadtxt('ideal/analytic.csv', unpack=True,delimiter=',')

plt.plot(iX,iY, label='ideal analytic', linestyle='dashed',c="black",zorder=1)
ratios=[]
nmax=[]
nmax, ratios=np.loadtxt('cutoffBetaRatio.txt', unpack=True,delimiter=' ')

for n in range(4,15+1):
	with open("ideal/mc/rightcutoff/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		X.append(n)
		g1.append(float(data[-1]))

X = [n*n/0.58/ratios[n-2] for n in X]
plt.scatter(X,g1, marker='s', label='ideal mc',c='black',s=70,zorder=2)

for n in range(4,15+1):
	with open("0.1/contact/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		g2.append(float(data[-1]))

for n in range(4,15+1):
	with open("0.1/dipole-0.06/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		g3.append(float(data[-1]))

plt.scatter(X,g2, marker='x', label='contact MC',c='blue',s=70,zorder=2)
plt.scatter(X,g3, marker='v', label='ddi l=0.06 MC',c='red',s=70,zorder=2)

plt.xlabel('$k_B T$')
plt.ylabel('$L_\phi$')
plt.legend()
plt.show()