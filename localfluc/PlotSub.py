#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt

plt.rcParams['figure.figsize'] = [8.5/2.54, 8.5/2.54]
plt.rcParams['axes.linewidth'] = 0.6
plt.rc('xtick', labelsize=7) 
plt.rc('ytick', labelsize=7)


data1 = np.loadtxt("data/n1-e12-contact.mc.out.txt")
data2 = np.loadtxt("data/n3-e12-contact.mc.out.txt")
data3 = np.loadtxt("data/n1-e4-dipole-0.060.mc.out.txt")
data4 = np.loadtxt("data/n3-e4-dipole-0.060.mc.out.txt")


x1 = np.linspace(-0.5,0.5,len(data1),endpoint=False)
x2 = np.linspace(-0.5,0.5,len(data2),endpoint=False)
x3 = np.linspace(-0.5,0.5,len(data3),endpoint=False)
x4 = np.linspace(-0.5,0.5,len(data4),endpoint=False)


ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3,sharex=ax1)
ax4 = plt.subplot(2,2,4,sharex=ax2)
size=10
ax1.scatter(x1,data1,marker='.',c="blue",s=size)
ax2.scatter(x2,data2,marker='.',c="blue",s=size)
ax3.scatter(x3,data3,marker='.',c="blue",s=size)
ax4.scatter(x4,data4,marker='.',c="blue",s=size)

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)

ax1.set_ylabel("$\Delta N/N$",fontsize=9,labelpad=-0.5)
ax3.set_ylabel("$\Delta N/N$", fontsize=9,labelpad=-0.5)
ax3.set_xlabel("$x/L$", fontsize=9,labelpad=-1)
ax4.set_xlabel("$x/L$", fontsize=9,labelpad=-1)

ax1.tick_params(direction='in')
ax2.tick_params(direction='in')
ax3.tick_params(direction='in')
ax4.tick_params(direction='in')


plt.tight_layout(rect=(-0.04,-0.04,1.04,1.04))
plt.subplots_adjust(wspace=0.22, hspace=0.12)
plt.savefig('../figures/fig6.eps', dpi=1200)
plt.show()
