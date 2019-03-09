#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

with open(sys.argv[1],"r") as f:
	data = f.read().split()
	N = int(data[0])
	nmax = int(data[1])
	gamma = float(data[2])

	re = []
	im = []

	for i in range(2*nmax+1):
		re.append(float(data[3+i]))
	for i in range(2*nmax+1):
		im.append(float(data[4+2*nmax+i]))
	alphas = np.vectorize(complex)(re,im)

k = []
for i in range(-nmax,nmax+1):
	k.append(i)
k = np.array(k)

def psi(x):
	return np.sum(alphas*np.exp(np.outer(2j*np.pi*x,k)),axis=1)

#def psi(x):
#	y = np.zeros_like(x,dtype=np.complex)
#	for j in range(2*nmax+1):
#		y += alphas[j]*np.exp((2j*np.pi*(j-nmax))*x)
#	return y

x = np.linspace(-0.5,0.5,1000)
plt.plot(x,np.abs(psi(x))**2)
plt.show()
