#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

g1=[]
g2=[]
g3=[]

X=[]

for n in range(4,15+1):
	with open("0.025/"+sys.argv[1]+"/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		X.append(n)
		g1.append(float(data[-1]))

X = [n*n/0.58 for n in X]
plt.scatter(X,g1, marker='.', label='g=0.05',c='black',s=70)

for n in range(4,15+1):
	with open("0.075/"+sys.argv[1]+"/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		g2.append(float(data[-1]))

plt.scatter(X,g2, marker='x', label='g=0.15',c='blue')

for n in range(4,15+1):
	with open("0.125/"+sys.argv[1]+"/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		g3.append(float(data[-1]))

plt.scatter(X,g3, marker='v', label='g=0.25',c='red')

plt.xlabel('$k_B T$')
plt.ylabel('$\Delta$ l')
plt.legend()
plt.show()