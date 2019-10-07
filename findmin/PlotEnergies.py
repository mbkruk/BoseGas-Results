#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

dextra = {}

for i in range(1,len(sys.argv)):
	f = open(sys.argv[i])
	data = f.read().split('\n')
	header = data[0].split()
	extra = int(header[0])
	gamma = float(header[1])
	E = None
	uE = None
	for line in data:
		line = line.split()
		if len(line)<7:
			continue
		if line[0]=="total":
			E = float(line[5])
			uE = float(line[6])
			break
	if not extra in dextra:
		dextra[extra] = []
	dextra[extra].append((gamma,E,uE))
	f.close()

data = {}

for k, v in dextra.items():
	print(k,flush=True)
	gamma = []
	E = []
	uE = []
	for g, e, ue in v:
		gamma.append(g)
		E.append(e)
		uE.append(ue)
	data[k] = (np.array(gamma),np.array(E),np.array(uE))

ref = 13
w = data[ref]

for k, v in data.items():
	if k==ref:
		continue
	plt.errorbar(v[0],v[1]-w[1],yerr=np.sqrt(v[2]**2+w[2]**2),label="$E_{{{}}}-E_{{{}}}$".format(k,ref))

plt.legend()
plt.show()
