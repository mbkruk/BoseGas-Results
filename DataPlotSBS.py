#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

plt.rc('xtick', labelsize=7) 
plt.rc('ytick', labelsize=7) 
plt.rcParams['axes.linewidth'] = 0.6

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17/2.54,2.5))

aX = []
aY = []
fX = []
fY = []

aX, aY =np.loadtxt('idealgas/analytic/avgdata.csv', unpack=True,delimiter=',')
aX = [1/n for n in aX]
fX, fY =np.loadtxt('idealgas/analytic/flucdata.csv', unpack=True,delimiter=',')
fX = [1/n for n in fX]


imcX = []
imcF = []
imcU = []
imcY = []

size=5

for n in range(1,22+1):
	with open("idealgas/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-1].split()
		imcX.append(n)
		imcY.append(float(data[2]))
		imcU.append(float(data[3]))
		imcF.append(float(data[4]))

imcX = [n*n/0.58 for n in imcX]


ax2.errorbar(imcX,imcF,marker='v',ls=' ',label='ideal MC',c="black",markersize=size)
ax2.plot(fX,fY, linestyle='dashed',c="black", label="ideal analytic",linewidth=1.0)

ax1.errorbar(imcX,imcY,yerr=imcU,ls=' ',marker='v',label='ideal MC',c="black",markersize=size)
ax1.plot(aX,aY, linestyle='dashed',c="black", label="ideal analytic",linewidth=1.0)

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


ax2.errorbar(mcX,mcF,marker='x',ls=' ',label='contact MC',c="blue",markersize=size)
ax2.errorbar(evX,evF,marker='.',ls=' ',label='contact EV',c="mediumturquoise",markersize=1.2*size)

ax1.errorbar(mcX,mcY,yerr=mcU,ls=' ',marker='x',label='contact MC',c="blue",markersize=size)
ax1.errorbar(evX,evY,marker='.',ls=' ',label='contact EV',c="mediumturquoise",markersize=1.2*size)

dmcX = []
dmcU = []
dmcY = []
dmcF = []

devX = []
devY = []
devF = []

for n in range(1,22+1):
	with open("repulsive/0.5"+sys.argv[1]+"/0.025/mc/n-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-2*n-4].split()
		dmcX.append(n)
		dmcY.append(float(data[2]))
		dmcU.append(float(data[3]))
		dmcF.append(float(data[4]))
	with open("repulsive/0.5"+sys.argv[1]+"/0.025/ev/results/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		devX.append(n)
		devY.append(float(data[-2]))
		devF.append(float(data[-1]))

dmcX = [n*n/0.58 for n in dmcX]
devX = [n*n/0.58 for n in devX]

ax1.set_xscale("log")
ax2.set_xscale("log")

ax1.tick_params(direction='in')
ax2.tick_params(direction='in')
ax1.tick_params(direction='in',which='minor')
ax2.tick_params(direction='in',which='minor')

ax2.errorbar(dmcX,dmcF,marker='x',ls=' ',label='dd $l_{\perp}$=0.025 MC',c="indianred",markersize=size)
ax2.errorbar(devX,devF,marker='.',ls=' ',label='dd $l_{\perp}$=0.025 EV', c="red",markersize=1.2*size)

ax1.errorbar(dmcX,dmcY,yerr=dmcU,ls=' ',marker='x',label='dd $l_{\perp}$=0.025 MC',c="indianred",markersize=size)
ax1.errorbar(devX,devY,marker='.',ls=' ',label='dd $l_{\perp}$=0.025 EV', c="red",markersize=1.2*size)

ax2.set_xlabel('$k_\mathit{B} T/\epsilon$',fontsize=9, labelpad=-0.5)
ax1.set_xlabel('$k_\mathit{B} T/\epsilon$',fontsize=9, labelpad=-0.5)

ax2.set_ylabel("$\\sqrt{Var[n_0]}$",fontsize=9)
ax2.legend(fontsize=5.6,loc='upper left')

ax1.set_ylabel('$<n_0>$',fontsize=9, labelpad=-2)
ax1.legend(fontsize=5.6,loc='lower left')

plt.tight_layout(rect=(-0.021,-0.07,1.02,1.06))
fig.subplots_adjust(wspace=0.21)
plt.savefig('figures/fig2.eps', dpi=1200)
plt.show()
