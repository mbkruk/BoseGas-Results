#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt

nmax, ratio = np.loadtxt(sys.argv[1]).T

what = sys.argv[2]

# beta = 0.58/nmax/nmax
# nmax = sqrt(0.58/beta)

oldbeta = 0.58/nmax/nmax
newbeta = ratio*oldbeta
effconst = ratio*0.58#/nmax/nmax*nmax*nmax

def f(x,a,b):
	return np.power(x/a,b)

if what=="newbeta/nmax":
	x, y, popt  = newbeta, nmax, (1/18,-0.5)
elif what=="effconst":
	x, y, popt  = nmax, effconst, (18,0.5)

popt, pcov = spopt.curve_fit(f,x,y,p0=popt)

print(*popt,flush=True)

if what=="effconst":
	plt.axhline(y=0.58,color="black", linestyle='dashed')
	plt.xlabel('$n_{max}$')
	plt.ylabel('$\\beta n_{max}^2$')

plt.scatter(x,y)
if what=="newbeta/nmax":
	plt.scatter(oldbeta,nmax)

#plt.scatter(x,f(x,*popt),marker='x')
plt.show()
