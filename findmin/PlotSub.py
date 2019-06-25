#!/usr/bin/env python3

#Usage: FindminPlot.py <interaction type> <width/energy>
import sys
import numpy as np
from matplotlib import pyplot as plt

def wid(t):
	return 1.0/(np.power(2.0*np.pi,1.5)*99.0*t)

def ene(t):
	return np.pi*99.0*99.0*100.0*x*x

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

delta=(gammasc[11]-gammasc[0])/20
x = np.linspace(gammasc[0]-delta,gammasc[11]+delta,1000)
ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3,sharex=ax1)
ax4 = plt.subplot(2,2,4,sharex=ax2)

y=ene(x)
ax1.errorbar(gammasc,mccene,yerr=mccenestd,ls=' ',marker='v',label='MC simulations',c="red")
ax1.plot(x,y,c="blue", label='Gauss ansatz')


ax2.errorbar(gammasd,wolfene,ls=' ',marker='x',label='Gauss ansatz',c="blue",markersize='8')
ax2.errorbar(gammasd,mcdene,yerr=mcdsigstd,ls=' ',marker='v',label='MC simulations',c="red")


y = wid(x)
ax3.errorbar(gammasc,mccsig,yerr=mccsigstd,ls=' ',marker='v',label='MC simulations',c="red")
ax3.plot(x,y,c="blue", label='Gauss ansatz')

ax4.errorbar(gammasd,wolfsig,ls=' ',marker='x',label='Gauss ansatz',c="blue",markersize='8')
ax4.errorbar(gammasd,mcdsig,yerr=mcdsigstd,ls=' ',marker='v',label='MC simulations',c="red")

ax1.tick_params(labelsize=10)
ax2.tick_params(labelsize=10)
ax3.tick_params(labelsize=10)
ax4.tick_params(labelsize=10)


plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)

ax1.set_ylabel('$|E_{min}|/\epsilon$',fontsize=14)
ax3.set_ylabel('$\lambda/L$', fontsize=14)
ax3.set_xlabel('$|g|$', fontsize=14)
ax4.set_xlabel('$|g|$', fontsize=14)

ax1.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=1, fontsize=12)
ax2.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=1,fontsize=12)
plt.subplots_adjust(top=0.9, right=0.97)
plt.show()