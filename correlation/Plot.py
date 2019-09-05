#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['figure.figsize'] = [8.5/2.54, 2.5]
plt.rcParams['axes.linewidth'] = 0.6
plt.rc('xtick', labelsize=7) 
plt.rc('ytick', labelsize=7)

fig, ax1 = plt.subplots()
ax2 = fig.add_axes([0.68, 0.69, 0.3, 0.27])

eX, eY =np.loadtxt('ideal/idealexact-n-9.csv', unpack=True,delimiter=',')
cX, cY =np.loadtxt('ideal/idealclass-n-9.csv', unpack=True,delimiter=',')
ax2.set_rasterization_zorder(2) 
ax2.plot(eX,eY, label='exact', linewidth=0.7,c='black',zorder=0)
ax2.plot(cX,cY, alpha=0.55, label='cf',c="lime",zorder=1)
ax2.set_xlabel('$x/L$', fontsize=6.5, labelpad=-0.15)
ax2.set_ylabel('$g_1(x)$', fontsize=6.5)
ax2.tick_params(labelsize=5)
ax2.legend(loc='upper right',fontsize=5.5, handlelength=0.5)
ax2.text(-0.46,0.78,'(a)',fontsize=9)
g1=[]
g2=[]
g3=[]

X=[]

size=20
iX, iY =np.loadtxt('ideal/analytic.csv', unpack=True,delimiter=',')

ax1.plot(iX,iY, label='ideal analytic', linestyle='dashed',c="black",zorder=1,linewidth=1.0)

ax3 = fig.add_axes([0.68, 0.31, 0.3, 0.27])
nmax, ratios=np.loadtxt('cutoffBetaRatio.txt', unpack=True,delimiter=' ')
effconst = ratios*0.58
ax3.axhline(y=0.58,color="black", linestyle='dashed', label='old',zorder=1,linewidth=1.0)
ax3.scatter(nmax,effconst,s=5, label='new',zorder=2)
ax3.set_xlabel('$n_{max}$',fontsize=6.5,labelpad=-1)
ax3.set_ylabel('$\\beta n_{max}^2$',fontsize=6.5)
ax3.tick_params(labelsize=5)
ax3.legend(loc='lower right',fontsize=5.5)
ax3.text(2.5,0.75,'(b)',fontsize=9)

for n in range(4,15+1):
	with open("ideal/mc/rightcutoff/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		X.append(n)
		g1.append(float(data[-1]))

X = [n*n/0.58/ratios[n-2] for n in X]
ax1.scatter(X,g1, marker='s', label='ideal MC',c='black',s=size,zorder=2)

for n in range(4,15+1):
	with open("0.1/contact/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		g2.append(float(data[-1]))

for n in range(4,15+1):
	with open("0.1/dipole-0.06/n-{}.out".format(n),"r") as f:
		data = f.read().split()
		g3.append(float(data[-1]))

ax1.scatter(X,g2, marker='x', label='contact MC',c='blue',s=size,zorder=2)
ax1.scatter(X,g3, marker='v', label='dd $l_{\perp}$=0.06 MC',c='indianred',s=size,zorder=2)
ax1.set_xlabel('$k_B T/\epsilon$',fontsize=9, labelpad=-0.5)
ax1.set_ylabel('$L_\phi/L$',fontsize=9,labelpad=-1)
ax1.locator_params(axis='y', nbins=5) 
ax1.legend(fontsize=6,loc='upper right', bbox_to_anchor=(0.5, 0.99))
plt.tight_layout(rect=(-0.04,-0.06,1.04,1.05))
plt.savefig('../figures/fig3.eps',rasterized=True,dpi=1200)
plt.show()