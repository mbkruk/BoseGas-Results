#!/usr/bin/env python3

help = '''
	usage: FindMinEnergy.py <particle count> <extra mode pairs>
	Interaction strength range for which energy reaches minimum.
	Defalt interaction type is gaussian.
'''

import sys
import subprocess
import random
import numpy as np

if len(sys.argv)!=3 and len(sys.argv)!=4:
	print(help)
	exit(1)

if len(sys.argv)==4:
    options = ["-I",sys.argv[3]]
else:
    options = []

N = float(sys.argv[1])
extraModePairs = int(sys.argv[2])
maxIter = 20
gammaMul = 2.0
#gamma = -(1.0+random.random())/1000.0
gamma = -0.017242898991634857*(1.0+(random.random()-0.5)/10)
maxMinGamma = float('-inf')
minMaxGamma = float('inf')
data = {-1:[],0:[],1:[]}

def finish(*range):
	print(range,flush=True)
	print((range[0]+range[1])/2.0,flush=True)
	exit()

def step(gamma):
	cmpl = [0,0,0]
	fails = 0
	lines = 0
	while True:
		result = subprocess.run(["bgmc","-c","-N",str(N),"-S","1024","-g",str(gamma),"-n","1","-e",str(extraModePairs),*options],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		data = result.stdout.decode("utf-8").split('\n')
		lines += len(data)-1
		data = data[-2].split()
		cmp = [float(x) for x in data]
		valid = True
		if cmp[0]>0.0 and cmp[1]>0.0:
			order = 2
		elif cmp[0]<0.0 and cmp[1]>0.0:
			order = 1
		elif cmp[0]<0.0 and cmp[1]<0.0:
			order = 0
		else:
			# shouldn't happen
			fails += 1
			valid = False
		if valid:
			cmpl[order] += 1
		scmpl = sorted(cmpl)
		if scmpl[-1]-scmpl[-2]>2:
			break
	order = np.argmax(cmpl)-1
	print(str(gamma).rjust(16),order,cmpl,lines,fails,flush=True)
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
	finish(float('-inf'),float('inf'))

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
	finish(np.max(data[-1]),np.min(data[1]))

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

finish((np.max(data[-1])+np.min(data[0]))/2,(np.max(data[0])+np.min(data[1]))/2)
