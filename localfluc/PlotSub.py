#!/usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as spopt


data1 = np.load("plt/data2/n3-e2-contact.txt.npy")
data2 = np.load("plt/data2/n5-e2-contact.txt.npy")
data3 = np.load("plt/data2/n3-e2-dipole-0.060.txt.npy")
data4 = np.load("plt/data2/n5-e2-dipole-0.060.txt.npy")

x1 = np.linspace(-0.5,0.5,len(data1),endpoint=False)
x2 = np.linspace(-0.5,0.5,len(data2),endpoint=False)
x3 = np.linspace(-0.5,0.5,len(data3),endpoint=False)
x4 = np.linspace(-0.5,0.5,len(data4),endpoint=False)


ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3,sharex=ax1)
ax4 = plt.subplot(2,2,4,sharex=ax2)

ax1.scatter(x1,data1,marker='.',c="blue")
ax2.scatter(x2,data2,marker='.',c="blue")
ax3.scatter(x3,data3,marker='.',c="blue")
ax4.scatter(x4,data4,marker='.',c="blue")

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)

ax1.set_ylabel("$\\frac{\Delta N}{N}$",fontsize=14)
ax3.set_ylabel("$\\frac{\Delta N}{N}$", fontsize=14)
ax3.set_xlabel("$\\frac{x}{L}$", fontsize=14)
ax4.set_xlabel("$\\frac{x}{L}$", fontsize=14)

ax1.text(-0.53,0.37,'$\\beta$=0.0644',fontsize=12)
ax3.text(-0.53,0.35,'$\\beta$=0.0644',fontsize=12)

ax2.text(-0.53,0.62,'$\\beta$=0.0232',fontsize=12)
ax4.text(-0.53,0.59,'$\\beta$=0.0232',fontsize=12)


plt.tight_layout()
plt.show()
