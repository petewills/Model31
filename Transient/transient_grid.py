__author__ = 'peterwills'
"""
Compute hall plots and other things from a transient well solution.
Reference: infohost.nmy.edu/~petro/faculty/Engler524/PET524-7-transient.pdf
"""

import numpy as np
import pylab as plt
from scipy.ndimage import filters
from scipy.signal import gaussian
import sys as sys
import library as lib
import parm as prm

fault = 'NULL'
fault = 1.0

# lib.testei(fig=2)
# sparse set of times for a grid of obs wells around injection well at origin
tv = [1, 2, 4, 8, 16, 32, 64, 126, 256]
rv = np.arange(-30.0, 30.0, 0.5)
nx, nt = len(rv), len(tv)
#for k in range(nt):
#    tv[k] *= 24*3600
P = np.zeros([nt, nx, nx])
for (i, x) in enumerate(rv):
    for (j, y) in enumerate(rv):
        Ptemp = lib.onewell_times( x, y, prm.D, prm.p0, prm.pi, tv, fault=fault)
        for k in range(nt):
            P[k, i, j] = Ptemp[k]

print 'done numerics'
plt.figure(1)
ax=plt.subplot(3,3,1)
for k in range(nt):
    plt.imshow(P[k], vmin=4.0, vmax=10.0)
    plt.colorbar()
    if k < nt-1:
        plt.subplot(3,3,k+1, sharex=ax, sharey=ax)
plt.show()

# Hall plot
nday = 100
tv = np.arange(24.0*3600.0, nday*24.0*3600.0, 24.0*3600.0)
x = 0.05
y = 0.0
fault = 'NULL'
P = lib.onewell_times( x, y, prm.D, prm.p0, prm.pi, tv, fault=fault)
intP = 0.0
intQ = 0.0
intPv = []
intQv = []
plt.figure(2)
for i in range(nt):
    intP += P[i]
    intQ += prm.q*3600*24
    intPv.append(intP)
    intQv.append(intQ)
plt.plot(intQv, intPv, 'bo-', label='No Fault')

#plt.plot(tv, P, 'r-')
fault = 0.06
P = lib.onewell_times( x, y, prm.D, prm.p0, prm.pi, tv, fault=fault)
intP = 0.0
intQ = 0.0
intPv = []
intQv = []
for i in range(nt):
    intP += P[i]
    intQ += prm.q*3600*24
    print intQ, intP
    intPv.append(intP)
    intQv.append(intQ)
plt.plot(intQv, intPv, 'ro-', label='Fault')
plt.legend()
plt.show()
