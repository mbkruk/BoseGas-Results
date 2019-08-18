#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt
import BoseGas as bg

binCount = 101
bins = []

if not len(sys.argv) in [2,3]:
	print("usage: Plot.py <data> <output>")
	exit(1)

input = sys.argv[1]
if input.endswith(".txt.npy"):
	if len(sys.argv)==2:
		output = sys.argv[1].replace(".txt.npy",".pdf").replace("plt/data/","plt/").replace("plt/data2/","plt/mc-")
	locFluc = np.load(input)
else:
	output = None
	if input.endswith(".txt"):
		locFluc = np.loadtxt(input)
	else:
		locFluc = np.load(input)

if len(sys.argv)==3:
	output = sys.argv[2]

plt.ylabel("$\\frac{\Delta N}{N}$")
plt.xlabel("$\\frac{x}{L}$")
plt.plot(np.linspace(-0.5,0.5,len(locFluc),endpoint=False),locFluc,ls=' ',marker='.')

if output!=None:
	print(output,flush=True)
	plt.savefig(output)
else:
	plt.show()
