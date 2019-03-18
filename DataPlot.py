#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

mcX = []
mcF = []
mcU = []
mcY = []

for n in range(1,25+1):
	with open("idealgas/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-1].split()
		mcX.append(n)
		mcY.append(float(data[2]))
		mcU.append(float(data[3]))
		mcF.append(float(data[4]))

if sys.argv[2]=='f':
	plt.scatter(mcX,mcF,marker='x',label='MC ideal')
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='x',label='MC ideal')

mcX = []
mcU = []
mcY = []
mcF = []

evX = []
evY = []
evF = []

for n in range(1,25+1):
	with open("repulsive/"+sys.argv[1]+"/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-1].split()
		mcX.append(n)
		mcY.append(float(data[2]))
		mcU.append(float(data[3]))
		mcF.append(float(data[4]))
	with open("repulsive/"+sys.argv[1]+"/ev/results/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		evX.append(n)
		evY.append(float(data[-2]))
		evF.append(float(data[-1]))

if sys.argv[2]=='f':
	plt.scatter(mcX,mcF,marker='.',label='MC')
	plt.scatter(evX,evF,marker='.',label='EV')
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='.',label='MC')
	plt.errorbar(evX,evY,marker='.',ls=' ',label='EV')

plt.xlabel('$N_{max}$')
if sys.argv[2]=='f':
	plt.ylabel("$\\sqrt{Var[n_0]}$")
else:
	plt.ylabel('$<n_0>$')
plt.legend()

plt.show()
