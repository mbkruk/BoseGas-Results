#!/usr/bin/env python3

import sys
import numpy as np
import BoseGas as bg
from matplotlib import pyplot as plt
from scipy import optimize as spopt

fname = sys.argv[1]

ldx = np.load(fname)
print(ldx)

eps = 1e-9

n0 = np.sum(np.abs(ldx)<eps)/len(ldx)

nzldx = []
for x in ldx:
	if np.abs(x)>=eps:
		nzldx.append(x)

print("n0 =",n0,flush=True)

plt.xlabel("$\Delta x$")
plt.ylabel("$p(\Delta x)$")
n, bins, labels = plt.hist(ldx,bins=101,density=True)

maxi = np.argmax(n)
mids = []
vals = []
maxh = 0.0
for i in range(len(n)):
	if i==maxi:
		continue
	mids.append((bins[i]+bins[i+1])/2)
	vals.append(n[i])
	maxh = max(n[i],maxh)

def gauss(x,mu,sigma,N):
	return N*np.exp(-0.5*((x-mu)/sigma)**2)/np.sqrt(2*np.pi)/sigma

def gaussp(x,mu,sigma,N):
	return gauss(x-1,mu,sigma,N)+gauss(x,mu,sigma,N)+gauss(x+1,mu,sigma,N)

xmax = (bins[maxi+1]+bins[maxi])/2

p, pcov = spopt.curve_fit(gaussp,mids,vals,p0=(xmax,np.std(nzldx),1.0-n0))
u = np.sqrt(np.diag(pcov))

print("mu =",p[0]," sigma =",p[1]," n =",p[2])
print(u,flush=True)
print("len =",len(n),len(bins))

h = bins[maxi+1]-bins[maxi]

n0 = (n[maxi]-h*gauss(p[0],*p))/np.sum(n)
print("n0' =",n0,flush=True)

x = np.linspace(np.min(ldx),np.max(ldx),256)
y = gauss(x,*p)

plt.ylim((0,maxh*1.1))

plt.plot(x,y)

plt.show()
