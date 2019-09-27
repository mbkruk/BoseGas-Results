#!/usr/bin/env python3

import sys
import numpy as np
import BoseGas as bg
from matplotlib import pyplot as plt
from scipy import optimize as spopt

plt.rcParams['figure.figsize'] = [8.5/2.54, 2.5]
plt.rcParams['axes.linewidth'] = 0.6
plt.rc('xtick', labelsize=7) 
plt.rc('ytick', labelsize=7)

fname = sys.argv[1]

ldx = np.load(fname)

fig, ax1 = plt.subplots()
left, bottom, width, height = [0.61, 0.3, 0.35, 0.35]
ax2 = fig.add_axes([left, bottom, width, height])

# hist

ax2.set_xlabel("$\Delta x$",fontsize=6,labelpad=-0.5)
ax2.set_ylabel("$p(\Delta x)$",fontsize=6,labelpad=-0.5)
ax2.tick_params(labelsize=5)
n, bins, labels = plt.hist(ldx,bins=51,density=True)

maxi = np.argmax(n)
delta0 = n[maxi]
mids = []
vals = []
maxh = 0.0
for i in range(len(n)):
	if i==maxi:
		continue
	mids.append((bins[i]+bins[i+1])/2)
	vals.append(n[i])
	maxh = max(n[i],maxh)

def gauss(x,mu,sigma,N):
	return N*np.exp(-0.5*((x-mu)/sigma)**2)/np.sqrt(np.pi)/sigma

def gaussp(x,mu,sigma,N):
	return gauss(x-1,mu,sigma,N)+gauss(x,mu,sigma,N)+gauss(x+1,mu,sigma,N)

xmax = (bins[maxi+1]+bins[maxi])/2

hp, hpcov = spopt.curve_fit(gaussp,mids,vals,p0=(xmax,0.002,0.5))
hu = np.sqrt(np.diag(hpcov))

print(hp)
print(hu,flush=True)

# sqrt

mds = 10
mdn = 100

dist = [list() for _ in range(mdn)]
y = []
for i in range(mdn,len(ldx),2*mdn):
	x = 0.0
	for j in range(mdn):
		x += ldx[i+j-mdn]
		dist[j].append(np.abs(x))
		if i==mdn:
			y.append(x)
dist = np.array(dist)
t = np.arange(mdn)+1

dist = dist[mds:]
t = t[mds:]

mdm = np.mean(dist,axis=1)
mdu = np.std(dist,axis=1,ddof=1)/np.sqrt(dist.shape[1])

def f(x,a,b):
	return b+np.sqrt(x/a)

mdp, mdpcov = spopt.curve_fit(f,t,mdm)

mdchi2red = np.sum(((f(t,*mdp)-mdm)/mdu)**2)/(len(t)-len(mdp))

print("MD chi^2_r =",mdchi2red,flush=True)

ax2.set_ylim((0,(maxh+min(delta0,2*maxh))/2*1.05))
x = np.linspace(np.min(ldx),np.max(ldx),256)
y = gauss(x,*hp)
ax2.plot(x,y,linewidth=1.0,label='Gaussian fit',c='orange')
ax2.legend(loc='upper left', fontsize=4.5,handlelength=0.5)

ax1.set_xlabel("MC steps",fontsize=9)
ax1.set_ylabel("$<|x|>$",fontsize=9, labelpad=-1)

ax1.errorbar(t,mdm,yerr=mdu,c='red',zorder=1)
x = np.linspace(0,mdn,256)
ax1.plot(x,f(x,*mdp),c='blue',linewidth=0.6,label='sqrt fit',zorder=0)
ax1.locator_params(axis='y', nbins=5)
ax1.legend(loc='upper left',fontsize=8) 

ax1.tick_params(direction='in')
ax2.tick_params(direction='in')

output = "inset-"+(fname.replace(".npy",".pdf"))
plt.savefig(output)
print(output,flush=True)
plt.tight_layout(rect=(0,-0.03,1.04,1.05))
plt.savefig('../figures/fig5.eps', dpi=1200)
plt.show()
