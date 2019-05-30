#!/usr/bin/env python3

import sys
import numpy as np
import BoseGas as bg
from matplotlib import pyplot as plt
from scipy import optimize as spopt

fname = sys.argv[1]

ldx = np.load(fname)

plt.xlabel("$\Delta x$")
plt.ylabel("$p(\Delta x)$")
n, bins, labels = plt.hist(ldx,bins=101,density=True)

mids = []
vals = []
maxh = 0.0
for i in range(len(n)//2):
	mids.append((bins[i]+bins[i+1])/2)
	vals.append(n[i])
	mids.append((bins[-i-1]+bins[-i-2])/2)
	vals.append(n[-i-1])
	maxh = max(max(n[i],n[-i-1]),maxh)

def gauss(x,mu,sigma,N):
	return N*np.exp(-0.5*((x-mu)/sigma)**2)/np.sqrt(np.pi)/sigma

def gaussp(x,mu,sigma,N):
	return gauss(x-1,mu,sigma,N)+gauss(x,mu,sigma,N)+gauss(x+1,mu,sigma,N)

p, pcov = spopt.curve_fit(gaussp,mids,vals,p0=(0.0,0.1,0.5))
u = np.sqrt(np.diag(pcov))

print(p)
print(u,flush=True)
print("len =",len(n),len(bins))

midi = len(n)//2
h = bins[midi+1]-bins[midi]

n0 = (n[midi]-h*gauss(0,*p))/np.sum(n)
print("n0 =",n0,flush=True)

x = np.linspace(np.min(ldx),np.max(ldx),256)
y = gauss(x,*p)

plt.ylim((0,maxh*1.1))

plt.plot(x,y)

plt.show()
