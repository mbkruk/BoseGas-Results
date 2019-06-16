#!/usr/bin/env python3

import sys
import numpy as np
from scipy import optimize as spopt
import BoseGas as bg

binCount = 101
bins = []

if len(sys.argv)!=2:
	print("usage: LocalFluctuations.py <data>")
	exit(1)

input = sys.argv[1]
output = "plt/"+input

data = bg.MCData(input)

binSize = 4*(4*data.nmax)
x = np.linspace(-0.5,0.5,binSize*binCount,endpoint=False)

k = []
for i in range(-data.nmax,data.nmax+1):
	k.append(i)
k = np.array(k)

status = bg.Status()
for aidx in range(data.alphaCount):
	status.update(aidx,data.alphaCount)

	alphas = data.loadAlphas()

	y = np.abs(bg.psi(x,k,alphas))**2
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

print(output,flush=True)

np.save(output,locFluc)
