#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt

if len(sys.argv)!=2:
	exit(1)

def psi(x,k,alphas):
	return np.sum(alphas*np.exp(np.outer(2j*np.pi*x,k)),axis=1)

def periodicGauss2(x,mu,sigma):
	M = 2
	y = np.zeros_like(x)
	for n in range(-M,M+1):
		y += np.exp(-0.5*((x-mu-n)/sigma)**2)
	y /= np.sqrt(np.sqrt(np.pi)*sigma)
	return N*(y**2)

with open(sys.argv[1],"r") as f:
	data = f.read().split()
	N = int(data[0])
	nmax = int(data[1])
	gamma = float(data[2])
	interactionType = data[3]
	alphaCount = int(data[4])

	x = np.linspace(-0.5,0.5,1000)
	k = []
	for i in range(-nmax,nmax+1):
		k.append(i)
	k = np.array(k)

	sigma=[]

	for aidx in range(alphaCount):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)

		y = np.abs(psi(x,k,alphas))**2

		estSigma = N/np.sqrt(np.pi)/np.max(y)
		estMu = x[np.argmax(y)]

		popt, pcov = spopt.curve_fit(periodicGauss2,x,y,p0=(estMu,estSigma))

		if np.sqrt(pcov[1,1])/popt[1] < 0.01 :
			sigma.append(popt[1])
	
sigmas= np.array(sigma)

print("sigma =",np.mean(sigmas),"+/-",np.std(sigmas,axis=0),flush=True)