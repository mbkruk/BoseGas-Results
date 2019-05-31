#!/usr/bin/env python3

import sys
import numpy as np
import BoseGas as bg
from matplotlib import pyplot as plt
from scipy import optimize as spopt

resolution = 1024
offset = int(sys.argv[2])
n = int(sys.argv[3])
step = int(sys.argv[3])

fname = sys.argv[1]

data = bg.MCData(fname)

k = [i for i in range(-data.nmax,data.nmax+1)]
x = np.linspace(-0.5,0.5,resolution)

alphas = []
for aidx in range(offset+step*n):
	alphas.append(data.loadAlphas())

y = np.abs(bg.psi(x,k,alphas[offset]))**2
x0 = x[np.argmax(y)]

status = bg.Status()
status.frequency = n//10
for aidx in range(offset,offset+step*n,step):
	index = (aidx-offset)//step
	status.update(index,n)

	y = np.abs(bg.psi(x+x0,k,alphas[aidx]))**2

	plt.clf()
	#plt.xlabel("$\frac{x}{L}$")
	#plt.ylabel("$|\psi(\frac{x}{L})|^2$")
	plt.xlim((-0.5,0.5))
	plt.ylim((0,750))
	plt.plot(x,y)
	plt.savefig("img/{:04d}.png".format(index))
