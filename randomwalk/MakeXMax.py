#!/usr/bin/env python3

import sys
import numpy as np
import BoseGas as bg
from matplotlib import pyplot as plt

resolution = 1024
fname = sys.argv[1]
output = fname.replace(".txt",".npy")
if len(sys.argv)>=3:
	begin = float(sys.argv[2])
else:
	begin = 0

data = bg.MCData(fname)

print("cout: ",data.alphaCount,flush=True)

k = [i for i in range(-data.nmax,data.nmax+1)]
xx = np.linspace(-0.5,0.5,resolution)
shift = np.array([-1,0,1])

xmax = []
status = bg.Status()
for aidx in range(data.alphaCount):
	status.update(aidx,data.alphaCount)
	alphas = data.loadAlphas()
	if aidx<begin*data.alphaCount:
		continue
	y = np.abs(bg.psi(xx,k,alphas))**2
	x0 = xx[np.argmax(y)]
	x = x0+2*xx/resolution
	y = np.abs(bg.psi(x,k,alphas))**2
	x0 = x[np.argmax(y)]+shift
	x0 = x0[np.argmin(np.abs(x0))]
	xmax.append(x0)
xmax = np.array(xmax)

ldx = []
for i in range(1,len(xmax)):
	dx = (xmax[i]-xmax[i-1])+shift
	ldx.append(dx[np.argmin(np.abs(dx))])
ldx = np.array(ldx)

np.save(output,ldx)
