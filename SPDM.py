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

	re = []
	im = []

	for i in range(2*nmax+1):
		re.append(float(data[4+i]))
	for i in range(2*nmax+1):
		im.append(float(data[5+2*nmax+i]))
	alphas = np.vectorize(complex)(re,im)

print(alphas)

rho = np.outer(np.conj(alphas),alphas)

l, v = np.linalg.eig(rho)
print(np.abs(alphas[nmax])**2)
print(np.max(l.real))
