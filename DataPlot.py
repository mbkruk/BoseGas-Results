#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

mcX = []
mcF = []
mcU = []
mcY = []

size=8

for n in range(1,22+1):
	with open("idealgas/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-1].split()
		mcX.append(n)
		mcY.append(float(data[2]))
		mcU.append(float(data[3]))
		mcF.append(float(data[4]))

mcX = [n*n/0.58 for n in mcX]

if sys.argv[2]=='f':
	plt.errorbar(mcX,mcF,marker='v',ls=' ',label='MC ideal',c="black",markersize=size)
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='v',label='MC ideal',c="black",markersize=size)

mcX = []
mcU = []
mcY = []
mcF = []

evX = []
evY = []
evF = []

for n in range(1,22+1):
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

mcX = [n*n/0.58 for n in mcX]
evX = [n*n/0.58 for n in evX]

if sys.argv[2]=='f':
	plt.errorbar(mcX,mcF,marker='x',ls=' ',label='MC',c="blue",markersize=size)
	plt.errorbar(evX,evF,marker='.',ls=' ',label='EV',c="mediumturquoise",markersize=1.2*size)
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='x',label='MC',c="blue",markersize=size)
	plt.errorbar(evX,evY,marker='.',ls=' ',label='EV',c="mediumturquoise",markersize=1.2*size)

mcX = []
mcU = []
mcY = []
mcF = []

evX = []
evY = []
evF = []

for n in range(1,22+1):
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

mcX = [n*n/0.58 for n in mcX]
evX = [n*n/0.58 for n in evX]

plt.xscale("log")

if sys.argv[2]=='f':
	plt.errorbar(mcX,mcF,marker='x',ls=' ',label='MC dd $l_{\perp}$=0.025',c="red",markersize=size)
	plt.errorbar(evX,evF,marker='.',ls=' ',label='EV dd $l_{\perp}$=0.025', c="indianred",markersize=1.2*size)
else:
	plt.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='x',label='MC dd $l_{\perp}$=0.025',c="red",markersize=size)
	plt.errorbar(evX,evY,marker='.',ls=' ',label='EV dd $l_{\perp}$=0.025', c="indianred",markersize=1.2*size)

plt.xlabel('$k_B T/\epsilon$',fontsize=16)
if sys.argv[2]=='f':
	plt.ylabel("$\\sqrt{Var[n_0]}$",fontsize=16)
	plt.legend(fontsize=11,loc='upper right')
else:
	plt.ylabel('$<n_0>$',fontsize=16)
	plt.legend(fontsize=12,loc='lower left')

plt.tight_layout()
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.show()
