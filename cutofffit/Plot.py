#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt

def load(fname):
	with open(fname) as f:
		data = f.read().replace("*^","E").split()
		data = [float(x) for x in data]
	return data

exact = load("fit-N=100-beta=0.03625-exact.txt")
good = load("fit-N=100-beta=0.03625-cf-ok.txt")
more = load("fit-N=100-beta=0.03625-cf+1.txt")
less = load("fit-N=100-beta=0.03625-cf-1.txt")

x = list(range(len(exact)))

marker = '.'
alpha = 1.0

plt.scatter(x,exact,label="exact",marker=marker,c='black', s=50)
plt.scatter(x,good,label="$n_{max}=4$ (optimal)",marker=marker,alpha=alpha,c='lime',s=50)
plt.scatter(x,more,label="$n_{max}=5$",marker=marker,alpha=alpha,c='red',s=50)
plt.scatter(x,less,label="$n_{max}=3$",marker=marker,alpha=alpha,c='blue',s=50)
plt.legend(fontsize=15)
plt.xlabel('$N_{ex}$',fontsize=16)
plt.ylabel('$P(N_{ex})$',fontsize=16)
plt.ylim(bottom=0,top=0.017)
plt.tight_layout()
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.show()
