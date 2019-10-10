import numpy as np

g0 = -0.017447805261483047

v = np.linspace(g0*0.9,g0*1.1,21)

def cmds(v,extra):
	skip = 216+11*(extra-13)
	for i in range(len(v)):
		g = v[i]
		print("echo \"{2} {1}\" > {0} && bgmc -N 100 -n 1 -e {2} -g {1} -B 1 -s {3} >> {0}".format("energies/{:02}+{}.txt".format(i,extra),g,extra,skip))

cmds(v,14)
cmds(v,13)
cmds(v,12)
