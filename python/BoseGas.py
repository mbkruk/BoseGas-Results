'''
	usage: import BoseGas
	
	Provides common functions used in many scripts.
	
	Add absolute directory path of this module to PYTHONPATH environment variable to import it.
'''

import sys
import numpy as np
import time

def psi(x,k,alphas):
	return np.sum(alphas*np.exp(np.outer(2j*np.pi*x,k)),axis=1)

def periodicGauss2(x,mu,sigma,N):
	M = 3
	y = np.zeros_like(x)
	for n in range(-M,M+1):
		y += np.exp(-0.5*((x-mu-n)/sigma)**2)
	y /= np.sqrt(np.sqrt(np.pi)*sigma)
	return N*(y**2)

class MCData:

	def loadAlphas(self):
		if self.alphaIndex>=self.alphaCount:
			return None
		data = self.file.readline().split()
		re = np.array(data[:len(data)//2],dtype=np.float)
		im = np.array(data[len(data)//2:],dtype=np.float)
		alphas = np.vectorize(complex)(re,im)
		self.alphaIndex += 1
		return alphas

	def close(self):
		self.file.close()

	def __del__(self):
		self.close()

	def __init__(self,fname):
		file = open(fname,"r")
		self.N = int(file.readline())
		self.nmax = int(file.readline())
		self.gamma = float(file.readline())
		self.interactionType = file.readline()
		self.alphaIndex = 0
		self.alphaCount = int(file.readline())
		self.file = file
		file.readline()

class Status:

	def update(self,workDone,workTotal):
		if (workDone+1)%self.updateFrequency!=0:
			return
		eta = int((time.time()-self.t)/workDone*(workTotal-workDone)+0.5)
		hrs = eta//(60*60)
		mins = (eta%(60*60))//60
		secs = eta%60
		msg = "{:.2f} done, ETA = {:02d}:{:02d}:{:02d}".format(workDone/workTotal,hrs,mins,secs)
		if msg!=self.lastMessage:
			print(msg,flush=True)
			self.lastMessage = msg

	def __init__(self):
		self.lastMessage = ""
		self.updateFrequency = 1000
		self.t = time.time()
