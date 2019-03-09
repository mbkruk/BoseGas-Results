#!/usr/bin/env python3

help = '''
	usage: FindMinEnergy.py <particle count> <interaction strength>

	Find number of extra mode pairs for which energy reaches minimum.
	Interaction strength should be negative real number.
	Defalt interaction type is gaussian.
'''

import sys
import subprocess
import random
import numpy as np

def findMinConstGamma(N,gamma):
	extra = 0
	energies = []
	print("extra mode pairs".rjust(16),"energy".rjust(16),flush=True)
	while extra<10:
		result = subprocess.run(["bgmc","-N",str(N),"-g",str(gamma),"-n","1","-e",str(extra)],stdout=subprocess.PIPE)
		E = float(result.stdout.decode("utf-8").split('\n')[-2].split()[6])
		if len(energies)==3:
			energies = energies[1:]
		energies.append(E)
		print(str(extra).rjust(16),str(E).rjust(16),flush=True)
		if len(energies)==3:
			if energies[2]>energies[1] and energies[1]>energies[0]:
				return 0
			elif energies[0]>energies[1] and energies[2]>energies[1]:
				return extra-1
		extra += 1
	return 0

def findRangeConstExtraModes(N,extraModePairs):
	maxIter = 12
	gammaMul = 2.0
	gamma = -(1.0+random.random())/1000.0
	maxMinGamma = float('-inf')
	minMaxGamma = float('inf')
	data = {-1:[],0:[],1:[]}
	def step(gamma):
		result = subprocess.run(["bgmc","-N",str(N),"-g",str(gamma),"-n","1","-e",str(extraModePairs-1)],stdout=subprocess.PIPE)
		E0 = float(result.stdout.decode("utf-8").split('\n')[-2].split()[6])
		result = subprocess.run(["bgmc","-N",str(N),"-g",str(gamma),"-n","1","-e",str(extraModePairs)],stdout=subprocess.PIPE)
		E1 = float(result.stdout.decode("utf-8").split('\n')[-2].split()[6])
		result = subprocess.run(["bgmc","-N",str(N),"-g",str(gamma),"-n","1","-e",str(extraModePairs+1)],stdout=subprocess.PIPE)
		E2 = float(result.stdout.decode("utf-8").split('\n')[-2].split()[6])
		if E0<E1 and E1<E2:
			order = 1
		elif E2>E1 and E2>E1:
			order = 0
		elif E0>E1 and E1>E2:
			order = -1
		else:
			# shouldn't happen
			order = 0
		print(str(gamma).rjust(16),order,[E0,E1,E2],flush=True)
		return order
	order = step(gamma)
	data[order].append(gamma)
	if order!=0:
		print("find opposite",flush=True)
		for _ in range(maxIter):
			gamma *= gammaMul**order
			newOrder = step(gamma)
			data[newOrder].append(gamma)
			if order*newOrder<0:
				break
	else:
		oldGamma = gamma
		print("find -1",flush=True)
		for _ in range(maxIter):
			gamma *= gammaMul
			newOrder = step(gamma)
			data[newOrder].append(gamma)
			if newOrder==-1:
				break
		gamma = oldGamma
		print("find 1",flush=True)
		for _ in range(maxIter):
			gamma /= gammaMul
			newOrder = step(gamma)
			data[newOrder].append(gamma)
			if newOrder==1:
				break
	if len(data[-1])==0 or len(data[1])==0:
		return (float('-inf'),float('inf'))
	if len(data[0])==0:
		print("find 0",flush=True)
		a = np.min(data[1])
		b = np.max(data[-1])
		for _ in range(maxIter):
			c = (a+b)/2.0
			order = step(c)
			data[order].append(c)
			if order==0:
				break
			elif order==1:
				a = c
			else:
				b = c
	if len(data[0])==0:
		return (np.max(data[-1]),np.min(data[1]))

	print("find lower bound",flush=True)
	a = np.min(data[0])
	b = np.max(data[-1])
	for _ in range(maxIter):
		c = (a+b)/2.0
		order = step(c)
		data[order].append(c)
		if order<0:
			b = c
		else:
			a = c

	print("find upper bound",flush=True)
	a = np.min(data[1])
	b = np.max(data[0])
	for _ in range(maxIter):
		c = (a+b)/2.0
		order = step(c)
		data[order].append(c)
		if order>0:
			a = c
		else:
			b = c

	return (np.min(data[0]),np.max(data[0]))

if len(sys.argv)!=3:
	print(help)
	exit(1)

N = float(sys.argv[1])
const = float(sys.argv[2])

'''min = findMinConstGamma(N,const)
if min>0:
	print(min,flush=True)
else:
	print("none",flush=True)'''

range = findRangeConstExtraModes(N,const)
print(range,flush=True)
