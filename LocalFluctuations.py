#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt

binCount = 40
bins = []

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

	binSize = 4*(4*nmax)
	x = np.linspace(-0.5,0.5,binSize*binCount,endpoint=False)

	k = []
	for i in range(-nmax,nmax+1):
		k.append(i)
	k = np.array(k)

	for aidx in range(alphaCount):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)

		y = np.abs(psi(x,k,alphas))**2
		i0 = np.argmax(y)
		x0 = x[i0]
		idx = np.array(list(range(len(x))))
		idx = ((idx+len(idx)//2-i0)%len(idx))//binSize
		binIdx = [[] for _ in range(binCount)]
		for i in range(len(idx)):
			binIdx[idx[i]].append(i)
		y1 = np.roll(y,1)
		dx = 1.0/len(x)
		dy = 0.5*dx*(y+y1)
		bin = np.array([0.0]*binCount)
		for j in range(len(bin)):
			bin[j] = np.sum(dy[binIdx[j]])
		bins.append(bin)

bins = np.array(bins)
locFluc = np.std(bins,axis=0)/np.mean(bins,axis=0)

plt.ylabel("$\\frac{\Delta N}{N}$")
plt.xlabel("$\\frac{x}{L}$")
plt.plot(np.linspace(-0.5,0.5,binCount,endpoint=False),locFluc,ls=' ',marker='o')
plt.show()
