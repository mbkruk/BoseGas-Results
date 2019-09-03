#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt

def load(fname):
	with open(fname) as f:
		data = f.read().replace("*^","E").split()
		data = [float(x) for x in data]
	return data

plt.rcParams['figure.figsize'] = [8.5/2.54, 2.5]
plt.rcParams['axes.linewidth'] = 0.6

exact = load("fit-N=100-beta=0.03625-exact.txt")
good = load("fit-N=100-beta=0.03625-cf-ok.txt")
more = load("fit-N=100-beta=0.03625-cf+1.txt")
less = load("fit-N=100-beta=0.03625-cf-1.txt")

x = list(range(len(exact)))

marker = '.'
alpha = 1.0
size = 10

plt.scatter(x,exact,label="exact",marker=marker,c='black', s=size)
plt.scatter(x,good,label="$n_{max}=4$ (optimal)",marker=marker,alpha=alpha,c='lime',s=size)
plt.scatter(x,more,label="$n_{max}=5$",marker=marker,alpha=alpha,c='red',s=size)
plt.scatter(x,less,label="$n_{max}=3$",marker=marker,alpha=alpha,c='blue',s=size)
plt.legend(fontsize=8)
plt.xlabel('$N_{ex}$',fontsize=9,labelpad=-0.5)
plt.ylabel('$P(N_{ex})$',fontsize=9,labelpad=-0.2)
plt.ylim(bottom=0,top=0.017)
plt.tight_layout(rect=(-0.08,-0.08,1.04,1.05))
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)
plt.locator_params(axis='y', nbins=5) 
plt.savefig('../figures/fig1.eps', dpi=1200)
plt.show()
