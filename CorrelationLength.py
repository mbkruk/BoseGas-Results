#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize as spopt

if len(sys.argv)!=2:
	exit(1)

def psi(x,k,alphas):
	return np.sum(alphas*np.exp(np.outer(2j*np.pi*x,k)),axis=1)


with open(sys.argv[1],"r") as f:
	data = f.read().split()
	N = int(data[0])
	nmax = int(data[1])
	gamma = float(data[2])
	interactionType = data[3]
	alphaCount = int(data[4])

	resol = 64
	x = np.linspace(-0.5,0.5,resol)

	k = []
	for i in range(-nmax,nmax+1):
		k.append(i)
	k = np.array(k)
	
	values = np.zeros_like(x)
	values = np.outer(values,values)

	for aidx in range(alphaCount):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)

		values += np.abs(np.outer(psi(x,k,alphas),psi(x,k,alphas)))

values = values/alphaCount

X, Y = np.meshgrid(x,x)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X,Y,values)
plt.show()
