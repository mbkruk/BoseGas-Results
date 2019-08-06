#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt

x, y = np.loadtxt(sys.argv[1]).T

def f(x,a):
	return np.sqrt(x/a)

popt, pcov = spopt.curve_fit(f,x,y)

plt.scatter(x,y)
plt.scatter(x,f(x,*popt),marker='x')
plt.show()
