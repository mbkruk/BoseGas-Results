#!/usr/bin/env python3

import os
import glob
import json

target = "data.json"

def loadG(fname):
	with open(fname) as f:
		data = f.read().split('\n')
		for i in range(-1,-len(data),-1):
			if data[i]:
				return float(data[i])
	raise "no gamma"

def loadE():
	data = {}
	for file in glob.glob("e-*.out"):
		if not os.path.isfile(file):
			continue
		extra = int(file[2:-4])
		gamma = loadG(file)
		data[extra] = gamma
	return data

cwd = os.getcwd()

data = {}

os.chdir("contact/python")
data["contact"] = loadE()
os.chdir(cwd)

data["dipole"] = {}
for path in glob.glob("dipole-*"):
	if not os.path.isdir(path):
		continue
	width = path[7:]
	os.chdir(path+"/python")
	data["dipole"][width] = loadE()
	os.chdir(cwd)

print(target)

with open(target,"w") as f:
	f.write(json.dumps(data,separators=(',', ': '),indent="\t"))
