#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

if len(sys.argv)!=6:
	print("usage: Plot.py <exact> <good> <more> <less> <output>",flush=True)
	exit(1)

def load(fname):
	with open(fname) as f:
		data = f.read().replace("*^","E").split()
		data = [float(x) for x in data]
	return data

plt.rcParams['figure.figsize'] = [8.5/2.54, 2.5]
plt.rcParams['axes.linewidth'] = 0.6

exact = load(sys.argv[1])
good = load(sys.argv[2])
more = load(sys.argv[3])
less = load(sys.argv[4])

x = list(range(len(exact)))

marker = '.'
alpha = 1.0
size = 10

fig, ax = plt.subplots()

ax.scatter(x,exact,label="exact",marker=marker,c='black', s=size)
ax.scatter(x,good,label="$n_{max}=4$ (optimal)",marker=marker,alpha=alpha,c='lime',s=size)
ax.scatter(x,more,label="$n_{max}=5$",marker=marker,alpha=alpha,c='indianred',s=size)
ax.scatter(x,less,label="$n_{max}=3$",marker=marker,alpha=alpha,c='blue',s=size)
ax.legend(fontsize=8)
plt.xlabel('$N_{ex}$',fontsize=9,labelpad=-0.5)
plt.ylabel('$P(N_{ex})$',fontsize=9,labelpad=-0.2)
plt.ylim(bottom=0,top=0.017)
plt.tight_layout(rect=(-0.08,-0.08,1.04,1.05))
plt.xticks(fontsize=7)
ax.tick_params(direction='in')
plt.yticks(fontsize=7)
plt.locator_params(axis='y', nbins=5)
plt.savefig(sys.argv[5], dpi=1200)
