#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt
import BoseGas as bg

binCount = 101
bins = []

locFluc = []
for i in range(1,len(sys.argv)):
	input = sys.argv[i]
	if input.endswith(".txt"):
		lf = np.loadtxt(input)
	else:
		lf = np.load(input)
	locFluc.append((lf,input))

plt.ylabel("$\\frac{\Delta N}{N}$")
plt.xlabel("$\\frac{x}{L}$")

for lf, label in locFluc:
	plt.plot(np.linspace(-0.5,0.5,len(lf),endpoint=False),lf,ls=' ',marker='.',label=label)
plt.legend()

plt.show()
