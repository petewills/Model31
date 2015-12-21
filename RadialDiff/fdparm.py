__author__ = 'peterwills'
import numpy as np
import sys as sys
import pylab as plt

# fd parameters for radial diffusivity equation.

"""
# First grid point at zero is a fake boundary point. Also last point at rmax+1
dr = 20.0                    # meters
rmax = 100.0                # meters
NR = int(rmax / dr) + 1


r = np.arange(0.0, rmax+2*dr, dr)
rinv = np.zeros(NR+1)
rinv[1:NR+1] = 1.0 / r[1:NR+1]

"""
def reg(delr=0.1):
    """
    crteate a regular grid
    :param delr: grid delta r
    :return: r, dr
    """
    rseg = [0.1, 100.0]

    r = np.arange(rseg[0], rseg[1], delr)
    dr = np.ones(len(r)) * delr

    return r, dr

def irreg():
    """
    Create an irregular grid
    :return:
    """
    # First node is first physical point in the model
    #
    rseg = [0.1, 2.0, 10.0, 100.0, 1000.0]          # at nodes
    drseg   = [0.5, 1.0,  10.0,   100.0,   1000.0]  # also at nodes
    nseg = 10                                       # single segment n - applies to all segments
                                      # single segment n - applies to all segments
    Nseg = len(rseg) - 1                            # Number of segments
    r, dr = np.zeros(Nseg*(nseg-1)), np.zeros(Nseg*(nseg-1))
    for i in range(Nseg):
        lr, ur = rseg[i], rseg[i+1]
        ldr, udr = drseg[i], drseg[i+1]
        temp, tempr = [], []
        for j in range(nseg-1):
            lamb = (float(j) / float(nseg-2)) **1.6        # 0 to 1
            temp.append((1.0-lamb) * ldr + lamb * udr)
        norm = np.sum(temp)
        tot = lr
        tempr = [lr]
        for j in range(nseg-1):
            temp[j] *= (ur - lr) / norm
        for j in range(nseg-1):
            tot += temp[j]
            tempr.append(tot)
        r[(nseg-1)*i:(nseg-1)*(i+1)] = tempr[:nseg-1]
    for j in range(len(dr)-1):
        dr[j] = r[j+1] - r[j]
    dr[-1] = dr[-2]

    return r, dr


# Time stepping for the model
# Time is measured in seconds.
tmax = 3600*24*10                            # seconds to run simulation
dt = 10000                                 # time step in seconds
nstep = int(tmax / dt)                      # Number of steps to run
tvals = np.arange(0.0, tmax, dt)
tprev = 0.0

r, dr = reg(delr=0.1)

plt.figure(1)
plt.title("Irregular Grid")
plt.xlabel('r(m)')
plt.ylabel('dr(m)')
#
plt.plot(r, dr, 'ro')
plt.grid()
plt.show()



