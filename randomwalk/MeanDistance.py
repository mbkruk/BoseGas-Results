#!/usr/bin/env python3

import sys
import numpy as np
import BoseGas as bg
from matplotlib import pyplot as plt
from scipy import optimize as spopt

n = 100

fname = sys.argv[1]

ldx = np.load(fname)

print(len(ldx))

dist = [list() for _ in range(n)]
y = []
for i in range(n,len(ldx),2*n):
	x = 0.0
	for j in range(n):
		x += ldx[i+j-n]
		dist[j].append(np.abs(x))
		if i==n:
			y.append(x)
dist = np.array(dist)
print(dist.shape,flush=True)
t = np.arange(n)+1
m = np.mean(dist,axis=1)
u = np.std(dist,axis=1,ddof=1)
print(m.shape,flush=True)

def f(x,a):
	return np.sqrt(x/a)

popt, pcov = spopt.curve_fit(f,t,m)

plt.xlabel("MC steps")
plt.ylabel("$<|x|>$")

plt.errorbar(t,m,yerr=u)
#plt.plot(t,y)
x = np.linspace(0,n,256)
plt.plot(x,f(x,*popt))

plt.show()
