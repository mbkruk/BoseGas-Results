#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

g1=[]
g2=[]
g3=[]

X=[]
iX, iY =np.loadtxt('ideal/analytic.csv', unpack=True,delimiter=',')

plt.plot(iX,iY, label='ideal analytic')

for n in range(4,15+1):
	with open("ideal/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		X.append(n)
		g1.append(float(data[-1]))

X = [n*n/0.58 for n in X]
plt.scatter(X,g1, marker='x', label='ideal mc',c='red',s=70)


plt.xlabel('$k_B T$')
plt.ylabel('$L_\phi$')
plt.legend()
plt.show()