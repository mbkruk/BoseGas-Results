#!/usr/bin/env python3

#Usage: FindminPlot.py <interaction type> <width/energy>
import sys
import numpy as np
from matplotlib import pyplot as plt

def wid(t):
	return 1.0/(np.power(2.0,0.5)*np.power(np.pi,1.5)*99.0*t)

def ene(t):
	return np.pi*99.0*99.0*100.0*x*x/4.0

plt.rcParams['figure.figsize'] = [8.5/2.54, 10/2.54]
plt.rcParams['axes.linewidth'] = 0.6

mccsig=[]
mccsigstd=[]
mccene=[]
mccenestd=[]

mcdsig=[]
mcdsigstd=[]
mcdene=[]
mcdenestd=[]

gammasc=[]
gammasd=[]

for n in range(1,12+1):
	with open("contact/mc/e-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		mccsigstd.append(float(data[-2]))
		mccsig.append(float(data[-3]))

for n in range(1,12+1):
	with open("dipole-0.025/mc/e-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		mcdsigstd.append(float(data[-2]))
		mcdsig.append(float(data[-3]))
		
for n in range(1,12+1):
	with open("contact/mc/e-{}.in".format(n),"r") as f:
		data = f.read().split('\n')
		gammasc.append((-1.0)*float(data[2]))
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-2*n-6].split()
		mccene.append((-1.0)*float(data[5]))
		mccenestd.append(float(data[7]))

for n in range(1,12+1):
	with open("dipole-0.025/mc/e-{}.in".format(n),"r") as f:
		data = f.read().split('\n')
		gammasd.append((-1.0)*float(data[2]))
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-2*n-6].split()
		mcdene.append((-1.0)*float(data[5]))
		mcdenestd.append(float(data[7]))

wolfsig=[]
wolfene=[]
for n in range(1,12+1):
	with open("dipole-0.025/wolfram/e-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		data = data[-2].split()
		wolfsig.append(float(data[0]))
		wolfene.append((-1.0)*float(data[1]))
#zmiana jednostek
gammasc = [2*n for n in gammasc]
gammasd = [2*n for n in gammasd]

delta=(gammasc[11]-gammasc[0])/20
x = np.linspace(gammasc[0]-delta,gammasc[11]+delta,1000)
ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3,sharex=ax1)
ax4 = plt.subplot(2,2,4,sharex=ax2)

y=ene(x)
ax1.errorbar(gammasc,mccene,yerr=mccenestd,ls=' ',marker='v',label='MC simulations',c="red",markersize='5',elinewidth=1.1)
ax1.plot(x,y,c="blue", label='Gaussian ansatz',linewidth=0.8)


ax2.errorbar(gammasd,wolfene,ls=' ',marker='x',label='Gaussian ansatz',c="blue",markersize='5')
ax2.errorbar(gammasd,mcdene,yerr=mcdsigstd,ls=' ',marker='v',label='MC simulations',c="red",markersize='5',elinewidth=1.1)


y = wid(x)
ax3.errorbar(gammasc,mccsig,yerr=mccsigstd,ls=' ',marker='v',label='MC simulations',c="red",markersize='5',elinewidth=1.1)
ax3.plot(x,y,c="blue", label='Gaussian ansatz',linewidth=0.8)

ax4.errorbar(gammasd,wolfsig,ls=' ',marker='x',label='Gaussian ansatz',c="blue",markersize='5',elinewidth=1.1)
ax4.errorbar(gammasd,mcdsig,yerr=mcdsigstd,ls=' ',marker='v',label='MC simulations',c="red",markersize='5',elinewidth=1.1)

ax1.tick_params(labelsize=6)
ax2.tick_params(labelsize=6)
ax3.tick_params(labelsize=6)
ax4.tick_params(labelsize=6)

ax1.locator_params(axis='y', nbins=5)
ax2.locator_params(axis='y', nbins=5)
ax3.locator_params(axis='y', nbins=5)
ax4.locator_params(axis='y', nbins=5)



plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)

ax1.set_ylabel('$|E_{min}|/\epsilon$',fontsize=9,labelpad=-1)
ax3.set_ylabel('$\lambda/L$', fontsize=9,labelpad=-1)
ax3.set_xlabel('$|g|$', fontsize=9)
ax4.set_xlabel('$|g|$', fontsize=9)

ax1.tick_params(direction='in')
ax2.tick_params(direction='in')
ax3.tick_params(direction='in')
ax4.tick_params(direction='in')

ax1.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=1, fontsize=8)
ax2.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=1,fontsize=8)
plt.subplots_adjust(top=0.9, right=0.98, wspace=0.25, hspace=0.12)
plt.savefig('../figures/fig4.eps', dpi=1200)
plt.show()