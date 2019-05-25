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
	plt.scatter(mcX,mcF,marker='v',label='MC ideal',c="black",s=10)
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='v',label='MC ideal',c="black")

mcX = []
mcU = []
mcY = []
mcF = []

evX = []
evY = []
evF = []

for n in range(1,25+1):
	with open("repulsive/0.5"+sys.argv[1]+"/contact/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-1].split()
		mcX.append(n)
		mcY.append(float(data[2]))
		mcU.append(float(data[3]))
		mcF.append(float(data[4]))
	with open("repulsive/0.5"+sys.argv[1]+"/contact/ev/results/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		evX.append(n)
		evY.append(float(data[-2]))
		evF.append(float(data[-1]))

if sys.argv[2]=='f':
	plt.scatter(mcX,mcF,marker='x',label='MC',c="blue")
	plt.scatter(evX,evF,marker='.',label='EV',c="lightgreen")
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='x',label='MC',c="blue")
	plt.errorbar(evX,evY,marker='.',ls=' ',label='EV',c="lightgreen")

mcX = []
mcU = []
mcY = []
mcF = []

evX = []
evY = []
evF = []

for n in range(1,25+1):
	with open("repulsive/0.5"+sys.argv[1]+"/0.025/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-2*n-4].split()
		mcX.append(n)
		mcY.append(float(data[2]))
		mcU.append(float(data[3]))
		mcF.append(float(data[4]))
	with open("repulsive/0.5"+sys.argv[1]+"/0.025/ev/results/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		evX.append(n)
		evY.append(float(data[-2]))
		evF.append(float(data[-1]))

if sys.argv[2]=='f':
	plt.scatter(mcX,mcF,marker='x',label='MC dd 0.025',c="red")
	plt.scatter(evX,evF,marker='.',label='EV dd 0.025', c="indianred")
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='x',label='MC dd 0.025',c="red")
	plt.errorbar(evX,evY,marker='.',ls=' ',label='EV dd 0.025', c="indianred")

plt.xlabel('$N_{max}$')
if sys.argv[2]=='f':
	plt.ylabel("$\\sqrt{Var[n_0]}$")
else:
	plt.ylabel('$<n_0>$')
plt.legend()

plt.show()
