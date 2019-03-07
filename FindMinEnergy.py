#!/usr/bin/env python3

'''
	usage: FindMinEnergy.py <particle count> <interaction strength>

	Find number of extra mode pairs for which energy reaches minimum.
	Interaction strength should be negative real number.
	Defalt interaction type is gaussian.
'''

import sys
import subprocess

print("extra mode pairs".rjust(16),"energy".rjust(16),flush=True)

def findMin(N,gamma):
	extra = 0
	energies = []
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

N = float(sys.argv[1])
gamma = float(sys.argv[2])

min = findMin(N,gamma)
if min>0:
	print(min,flush=True)
else:
	print("none",flush=True)
