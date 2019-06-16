#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt
import BoseGas as bg

binCount = 101
bins = []

if len(sys.argv)!=2:
	print("usage: Plot.py <data>")
	exit(1)

input = sys.argv[1]
output = sys.argv[1].replace(".txt.npy",".pdf").replace("plt/data/","plt/")

locFluc = np.load(input)

plt.ylabel("$\\frac{\Delta N}{N}$")
plt.xlabel("$\\frac{x}{L}$")
plt.plot(np.linspace(-0.5,0.5,len(locFluc),endpoint=False),locFluc,ls=' ',marker='.')

print(output,flush=True)
plt.savefig(output)
