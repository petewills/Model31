from RadialDiff import library as lib

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
import parm as prm


# lib.testei(fig=2)
nday = 100.0
tv = np.arange(3600, nday * 3600*24, 3600)

x, y = 100.0, 0.0
P1 = lib.onewell_times( x, y, prm.D, prm.p0, prm.pi, tv)


x, y = 10.0, 0.0
P2 = lib.onewell_times( x, y, prm.D, prm.p0, prm.pi, tv)

x, y = 0.1, 0.0
P3 = lib.onewell_times( x, y, prm.D, prm.p0, prm.p, tv)

plt.figure(1)
plt.plot(tv/3600.0/24, P1, 'r-', label='100 meters')
plt.plot(tv/3600.0/24, P2, 'b-', label='10 meters')
plt.plot(tv/3600.0/24, P3, 'k-', label='0.1 meters')
plt.grid()
plt.ylim([0,15])
plt.title("Pressure at origin")
plt.xlabel('Time(days)')
plt.legend()


xv = np.arange(0.1, 300.0, 0.1)
yv = xv * 0.0

T = 20.0                            # in days
P1 = lib.onewell_xy(xv, yv, prm.D, prm.p0, prm.pi, T * 24.0 * 3600.0)
T = 40.0                            # in days
P2 = lib.onewell_xy(xv, yv, prm.D, prm.p0, prm.pi, T * 24.0 * 3600.0)
T = 80.0                            # in days
P3 = lib.onewell_xy(xv, yv, prm.D, prm.p0, prm.pi, T * 24.0 * 3600.0)

plt.figure(2)
plt.plot(xv, P1, 'r-', label='20 days')
plt.plot(xv, P2, 'b-', label= '40 days')
plt.plot(xv, P3, 'k-', label='80 days')

plt.grid()
plt.ylim([0,15])
plt.title("Pressure at distances from well")
plt.xlabel('x(meters)')
plt.legend()
plt.show()
