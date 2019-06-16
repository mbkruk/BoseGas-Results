#!/usr/bin/env python3

#Usage: FindminPlot.py <interaction type> <width/energy>
import sys
import numpy as np
from matplotlib import pyplot as plt

def wid(t):
	return 1.0/(np.power(2.0*np.pi,1.5)*99.0*t)

def ene(t):
	return np.pi*99.0*99.0*100.0*x*x

fig, ax1 = plt.subplots()


ax1.set_xlabel('$|g|$', fontsize=14)

if sys.argv[1]=="width":
	ax1.set_ylabel('$\lambda/L$', fontsize=14)
	left, bottom, width, height = [0.5, 0.45, 0.43, 0.47]
elif sys.argv[1]=="energy":
	ax1.set_ylabel('$|E_{min}|/\epsilon$',fontsize=14)
	left, bottom, width, height = [0.2, 0.45, 0.3, 0.4]

ax2 = fig.add_axes([left, bottom, width, height])

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

delta=(gammasc[11]-gammasc[0])/20
x = np.linspace(gammasc[0]-delta,gammasc[11]+delta,1000)
if sys.argv[1]=="width":
	y = wid(x)
	ax1.errorbar(gammasc,mccsig,yerr=mccsigstd,ls=' ',marker='v',label='MC simulations',c="red")
elif sys.argv[1]=="energy":
	y=ene(x)
	ax1.errorbar(gammasc,mccene,yerr=mccenestd,ls=' ',marker='v',label='MC simulations',c="red")
ax1.plot(x,y,c="blue", label='Gauss ansatz')


wolfsig=[]
wolfene=[]
for n in range(1,12+1):
	with open("dipole-0.025/wolfram/e-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		data = data[-2].split()
		wolfsig.append(float(data[0]))
		wolfene.append((-1.0)*float(data[1]))
if sys.argv[1]=="width":
	ax2.errorbar(gammasd,wolfsig,ls=' ',marker='x',label='Gauss ansatz',c="blue",markersize='8')
	ax2.errorbar(gammasd,mcdsig,yerr=mcdsigstd,ls=' ',marker='v',label='MC simulations',c="red")
elif sys.argv[1]=="energy":
	ax2.errorbar(gammasd,wolfene,ls=' ',marker='x',label='Gauss ansatz',c="blue",markersize='8')
	ax2.errorbar(gammasd,mcdene,yerr=mcdsigstd,ls=' ',marker='v',label='MC simulations',c="red")

if sys.argv[1]=="width":
	ax1.legend(loc='lower left',fontsize=11)
	ax2.legend(loc='upper right', fontsize='small')
elif sys.argv[1]=="energy":
	ax1.legend(loc='lower right',fontsize=11)
	ax2.legend(loc='upper left', fontsize='small')

ax1.tick_params(labelsize=11)
plt.tight_layout()
plt.show()