#!/usr/bin/env python3

#Usage: FindminPlot.py <interaction type> <width/energy>
import sys
import numpy as np
from matplotlib import pyplot as plt

def wid(t):
	return 1.0/(np.power(2.0*np.pi,1.5)*99.0*t)

def ene(t):
	return np.pi*99.0*99.0*100.0*x*x

mcsig=[]
mcsigstd=[]
mcene=[]
mcenestd=[]

for n in range(1,12+1):
	with open(sys.argv[1]+"/mc/e-{}.out".format(n),"r") as f:
		data = f.read().split('\n')
		mcsigstd.append(float(data[-2]))
		mcsig.append(float(data[-3]))
		


gammas=[]

for n in range(1,12+1):
	with open(sys.argv[1]+"/mc/e-{}.in".format(n),"r") as f:
		data = f.read().split('\n')
		gammas.append((-1.0)*float(data[2]))
		if len(data[-1])==0:
			data = data[:-1]
		data = data[-2*n-6].split()
		mcene.append((-1.0)*float(data[5]))
		mcenestd.append(float(data[7]))

if sys.argv[1]=="contact":
	delta=(gammas[11]-gammas[0])/20
	x = np.linspace(gammas[0]-delta,gammas[11]+delta,1000)
	if sys.argv[2]=="width":
		y = wid(x)
		plt.errorbar(gammas,mcsig,yerr=mcsigstd,ls=' ',marker='.',label='MC simulations',c="red")
		plt.ylabel('Gauss width $\sigma$')
	elif sys.argv[2]=="energy":
		y=ene(x)
		plt.errorbar(gammas,mcene,yerr=mcenestd,ls=' ',marker='.',label='MC simulations',c="red")
		plt.ylabel('Energy $|E_{min}|$')
	plt.plot(x,y,c="blue", label='Gauss ansatz')
else:
	wolfsig=[]
	wolfene=[]
	for n in range(1,12+1):
		with open(sys.argv[1]+"/wolfram/e-{}.out".format(n),"r") as f:
			data = f.read().split('\n')
			data = data[-2].split()
			wolfsig.append(float(data[0]))
			wolfene.append(float(data[1]))
	if sys.argv[2]=="width":
		plt.errorbar(gammas,mcsig,yerr=mcsigstd,ls=' ',marker='x',label='MC simulations',c="red")
		plt.errorbar(gammas,wolfsig,ls=' ',marker='x',label='variational',c="blue")
		plt.ylabel('Gauss width $\sigma$')
	elif sys.argv[2]=="energy":
		plt.errorbar(gammas,mcene,yerr=mcsigstd,ls=' ',marker='x',label='MC simulations',c="red")
		plt.errorbar(gammas,wolfene,ls=' ',marker='x',label='Gauss ansatz',c="blue")
		plt.ylabel('Energy $|E_{min}|$')

plt.xlabel('Interaction strength $|g|$')
plt.legend()
plt.show()