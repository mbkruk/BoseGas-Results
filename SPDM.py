#!/usr/bin/env python3

# Single Particle Density Matrix

import sys
import numpy as np
from scipy import sparse as spsparse

rhos = []

with open(sys.argv[1],"r") as f:
	data = f.read().split()
	N = int(data[0])
	nmax = int(data[1])
	gamma = float(data[2])
	interactionType = data[3]
	alphaCount = int(data[4])

	for aidx in range(alphaCount):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)
		rho = np.outer(np.conj(alphas),alphas)
		rhos.append(rho)

rhos = np.mean(np.array(rhos),axis=0)
l, v = np.linalg.eig(rhos)

print(np.sort(l.real))
