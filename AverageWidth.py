#!/usr/bin/env python3

import sys
import numpy as np
#from matplotlib import pyplot as plt
from scipy import optimize as spopt
import BoseGas as bg

if len(sys.argv)!=2:
	print("usage: AverageWidth.py <MC output data file>")
	print("Compute average and standard deviation of wave packet profiles.")
	exit(1)

data = bg.MCData(sys.argv[1])

xx = np.linspace(-0.5,0.5,512)
k = []
for i in range(-data.nmax,data.nmax+1):
	k.append(i)
k = np.array(k)

def pg2(x,mu,sigma):
	return bg.periodicGauss2(x,mu,sigma,data.N)

def findSigma(alphas):
	y = np.abs(bg.psi(xx,k,alphas))**2
	estMu = xx[np.argmax(y)]
	x = xx+estMu
	y = np.abs(bg.psi(x,k,alphas))**2
	estSigma = data.N/np.sqrt(np.pi)/np.max(y)
	popt, pcov = spopt.curve_fit(pg2,x,y,p0=(estMu,estSigma))
	x = xx+popt[0]
	y = np.abs(bg.psi(x,k,alphas))**2
	popt, pcov = spopt.curve_fit(pg2,x,y,p0=(popt[0],popt[1]))
	return popt[1], np.sqrt(pcov[1,1])

sigmas = []

status = bg.Status()

for aidx in range(data.alphaCount):
	status.update(aidx,data.alphaCount)
	
	alphas = data.loadAlphas()
	m, u = findSigma(alphas)

	if u/m < 0.01:
		sigmas.append(m)

sigmas = np.array(sigmas)

print("sample count:",data.alphaCount)
print("accepted:",len(sigmas),len(sigmas)/data.alphaCount)
print(np.mean(sigmas),flush=True)
print(np.std(sigmas),flush=True)
