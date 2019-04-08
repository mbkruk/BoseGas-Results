#!/usr/bin/env python3

# Single Particle Density Matrix

import sys
import numpy as np
from scipy import sparse as spsparse

with open(sys.argv[1],"r") as f:
	data = f.read().split()
	N = int(data[0])
	nmax = int(data[1])
	gamma = float(data[2])
	interactionType = data[3]
	alphaCount = int(data[4])

	print("alphaCount =",alphaCount)
	print("2*nmax+1 =",2*nmax+1)

	for aidx in range(alphaCount):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)
		rho = np.outer(np.conj(alphas),alphas)
		l, v = np.linalg.eig(rho)
		n0 = np.abs(alphas[nmax])**2
		rhoMax = np.max(l.real)
		print(aidx,n0/rhoMax,n0,rhoMax,flush=True)
		a, b = np.sum(l.real), np.sum(np.abs(alphas)**2)
		if np.abs(a/N-1.0)>1e-3 or np.abs(b/N-1.0)>1e-3:
			print("error",a,b)
