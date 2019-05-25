#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt

def load(fname):
	with open(fname) as f:
		data = f.read().replace("*^","E").split()
		data = [float(x) for x in data]
	return data

exact = load("fit/fit-N=100-beta=0.03625-exact.txt")
good = load("fit/fit-N=100-beta=0.03625-cf-ok.txt")
more = load("fit/fit-N=100-beta=0.03625-cf+1.txt")
less = load("fit/fit-N=100-beta=0.03625-cf-1.txt")

x = list(range(len(exact)))

marker = '.'
alpha = 1.0

plt.scatter(x,exact,label="exact")
plt.scatter(x,good,label="$K_{max}=4$ (optimal)",marker=marker,alpha=alpha)
plt.scatter(x,more,label="$K_{max}=5$",marker=marker,alpha=alpha)
plt.scatter(x,less,label="$K_{max}=3$",marker=marker,alpha=alpha)
plt.legend()
plt.show()
