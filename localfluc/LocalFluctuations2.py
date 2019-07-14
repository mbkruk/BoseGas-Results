#!/usr/bin/env python3

import sys
import numpy as np
from scipy import optimize as spopt
import BoseGas as bg
from matplotlib import pyplot as plt

binCount = 101
bins = []

if len(sys.argv)!=2:
	print("usage: LocalFluctuations.py <data>")
	exit(1)

input = sys.argv[1]
output = "plt/"+input.replace("data/","data2/")

print(output,flush=True)

data = bg.MCData(input)

binSize = 4*(4*data.nmax)
x = np.linspace(-0.5,0.5,binSize*binCount,endpoint=False)
dx = 1.0/len(x)

searchRadius = len(x)//4
print("searchRadius =",searchRadius,(2*searchRadius+1)*dx,flush=True)

k = []
for i in range(-data.nmax,data.nmax+1):
	k.append(i)
k = np.array(k)

def calcMC(yy):
	dy = 0.5*dx*(yy+np.roll(yy,1))*x*x
	return np.sum(dy)

status = bg.Status(10)
for aidx in range(data.alphaCount//10):
	status.update(aidx,data.alphaCount//10)

	alphas = data.loadAlphas()

	y = np.abs(bg.psi(x,k,alphas))**2
	i0 = np.argmax(y)
	
	# x[len(x)//2]==0.0
	minMC = np.abs(calcMC(np.roll(y,len(x)//2-i0)))
	minJ0 = i0
	minDiff = 0
	
	for _ in range(200):
		j0 = minJ0+np.random.randint(-searchRadius,searchRadius)+np.random.randint(-searchRadius,searchRadius)
		yy = np.roll(y,len(x)//2-j0)
		mc = np.abs(calcMC(yy))
		if mc<minMC:
			minJ0 = (j0+len(x))%len(x)
			minDiff = j0-i0
			minMC = mc
	'''print("diff:",minDiff*dx,minMC,flush=True)
	yy = np.roll(y,len(x)//2-minJ0)
	plt.clf()
	plt.plot(x,yy)
	plt.show()'''
	
	i0 = minJ0
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

np.save(output,locFluc)
