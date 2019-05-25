#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt

if len(sys.argv)!=2:
	print("usage: WavePlot.py <BGMC output file>")
	print("Plots wave function and fits gaussian function to it with sigma = standard deviation, mu = mean.")
	exit(1)

with open(sys.argv[1],"r") as f:
	data = f.read().split()
	N = int(data[0])
	nmax = int(data[1])
	gamma = float(data[2])
	interactionType = data[3]
	alphaCount = int(data[4])

if interactionType=="contact":
	for aidx in range(1):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)
else:
	for aidx in range(1):
		re = []
		im = []
		for i in range(2*nmax+1):
			re.append(float(data[5+2*nmax+1+(2*nmax+1)*2*aidx+i]))
		for i in range(2*nmax+1):
			im.append(float(data[5+2*nmax+1+(2*nmax+1)*(2*aidx+1)+i]))
		alphas = np.vectorize(complex)(re,im)


k = []
for i in range(-nmax,nmax+1):
	k.append(i)
k = np.array(k)

def psi(x):
	return np.sum(alphas*np.exp(np.outer(2j*np.pi*x,k)),axis=1)

def periodicGauss2(x,mu,sigma):
	M = 2
	y = np.zeros_like(x)
	for n in range(-M,M+1):
		y += np.exp(-0.5*((x-mu-n)/sigma)**2)
	y /= np.sqrt(np.sqrt(np.pi)*sigma)
	return N*(y**2)

#def psi(x):
#	y = np.zeros_like(x,dtype=np.complex)
#	for j in range(2*nmax+1):
#		y += alphas[j]*np.exp((2j*np.pi*(j-nmax))*x)
#	return y

x = np.linspace(-0.5,0.5,1000)
y = np.abs(psi(x))**2
plt.plot(x,y)

estSigma = N/np.sqrt(np.pi)/np.max(y)
estMu = x[np.argmax(y)]

popt, pcov = spopt.curve_fit(periodicGauss2,x,y,p0=(estMu,estSigma))

#print(popt,flush=True)
print("mu =",popt[0],"+/-",np.sqrt(pcov[0,0]),flush=True)
print("sigma =",popt[1],"+/-",np.sqrt(pcov[1,1]),flush=True)

y = periodicGauss2(x,popt[0],popt[1])
plt.plot(x,y)

plt.show()
