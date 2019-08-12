#!/usr/bin/env python3

import sys
import numpy as np
from scipy import optimize as spopt
import BoseGas as bg
from matplotlib import pyplot as plt

binCount = 101
bins = []

if len(sys.argv)!=3 or not sys.argv[2] in ["save","plot"]:
	print("usage: LocalFluctuations.py <data> <save/plot>")
	exit(1)

input = sys.argv[1]
output = "plt/"+input.replace("data/","data2/")

plot = sys.argv[2]=="plot"

print(output,flush=True)

data = bg.MCData(input)

binSize = 4*(4*data.nmax)
x = np.linspace(-0.5,0.5,binSize*binCount,endpoint=False)
dx = 1.0/len(x)

k = []
for i in range(-data.nmax,data.nmax+1):
	k.append(i)
k = np.array(k)

status = bg.Status()
for aidx in range(data.alphaCount):
	status.update(aidx,data.alphaCount)

	alphas = data.loadAlphas()

	y = np.abs(bg.psi(x,k,alphas))**2

	mc = np.sum((np.array([np.cos(2*np.pi*x),np.sin(2*np.pi*x)])*y.T).T,axis=0)
	#print("mcv",mc,flush=True)
	
	i0 = np.argmin(np.abs(x-np.arctan2(mc[1],mc[0])/(2*np.pi)))
	
	if plot:
		yy = np.roll(y,len(x)//2-i0)
		plt.clf()
		plt.plot(x,y)
		plt.plot(x,yy)
		plt.show()
	
	x0 = x[i0]
	idx = np.array(list(range(len(x))))
	idx = ((idx+len(idx)//2-i0)%len(idx))//binSize
	binIdx = [[] for _ in range(binCount)]
	for i in range(len(idx)):
		binIdx[idx[i]].append(i)
	y1 = np.roll(y,1)

	dy = 0.5*dx*(y+y1)
	bin = np.array([0.0]*binCount)
	for j in range(len(bin)):
		bin[j] = np.sum(dy[binIdx[j]])
	bins.append(bin)

bins = np.array(bins)
locFluc = np.std(bins,axis=0)/np.mean(bins,axis=0)

if not plot:
	np.save(output,locFluc)
