__author__ = 'peterwills'
import numpy as np
import sys as sys
import pylab as plt

# fd parameters for radial diffusivity equation.
def reg(delr=0.1):
    """
    crteate a regular grid
    :param delr: grid delta r
    :return: r, dr
    """
    rseg = [0.1, 100.0]

    r = np.arange(rseg[0], rseg[1], delr)
    rreg = np.arange(rseg[0], rseg[1], delr)
    dr = np.ones(len(r)) * delr
    rp = np.ones(len(r))
    rpp = np.zeros(len(r))

    return r, rreg, dr, rp, rpp

def irreg_cluster(expand=1.0, delr=0.1):
    """
    create an irregular grid based on map function
    :param expand: how much to expand the grid for larger r. 1.0 is regular
    :param delr: starting interval
    :return: r, dr
    """
    rseg = [0.1, 500.0]                         # Interval for grid
    deps = 8.0                                  # step for uniform grid
    rreg = np.arange(rseg[0], rseg[1], deps)    # The uniform grid
    nreg = len(rreg)                            # number of nodes
    pwr = 1.0

    r, dr = np.zeros(100000), np.ones(100000)*deps
    rp, rpp = np.zeros(10000), np.zeros(10000)
    for (i, rr) in enumerate(rreg):
        lam = ((rreg[i] - rseg[0]) / (rseg[1] - rseg[0]))**pwr          # (0, 1) to the power
        rp[i] = pwr * ((rreg[i] - rseg[0]) / (rseg[1] - rseg[0]))**(pwr - 1)
        rpp[i] = pwr * (pwr - 1) / (rseg[1] - rseg[0]) * ((rreg[i] - rseg[0]) / (rseg[1] - rseg[0]))**(pwr - 2)
        r[i] = rseg[0] + lam * (rseg[1] - rseg[0])

    r = r[:nreg]
    dr = dr[:nreg]
    rp = rp[:nreg]
    rpp = rpp[:nreg]

    return r, rreg, dr, rp, rpp

# Time stepping for the model
# Time is measured in seconds.
tmax = 3600*24                            # seconds to run simulation
nt = 10
dt = int(tmax / nt)                       # time step in seconds
nstep = int(tmax / dt)                    # Number of steps to run
tvals = np.arange(0.0, tmax, dt)
tprev = 0.0

# r, dr = reg(delr=0.1)
r, rreg, dr, rp, rpp = irreg_cluster()

plt.figure(1)
ax = plt.subplot(1,3,1)
plt.title("Irregular Grid Map Jacobian rp")
plt.xlabel('r(m)')
plt.ylabel('rp')
plt.plot(r, rp, 'ro')
plt.grid()

plt.subplot(1,3,2, sharex=ax)
plt.title("Irregular Grid Map Jacobian rpp")
plt.xlabel('r(m)')
plt.ylabel('rpp')
plt.plot(r, rpp, 'ro')
plt.grid()


plt.subplot(1,3,3, sharex=ax)
plt.title("Irregular Grid vs Regular grid")
plt.xlabel('r(m)')
plt.ylabel('dr')
plt.plot(r, np.zeros(len(r)), 'ro', label='irregular')
plt.plot(rreg, np.ones(len(r)), 'bo', label='regular')
plt.grid()
plt.ylim([-0.5, 1.5])
plt.legend()
plt.show()

sys.exit()





"""
def irreg():

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
"""
"""
def irreg1(expand=1.0, delr=0.1):
    ""
    create a regular grid
    :param expand: how much to expand the grid for larger r. 1.0 is regular
    :param delr: starting interval
    :return: r, dr
    ""
    rseg = [0.1, 500.0]         # Interval for grid
    rp = rseg[0]
    sz, N = delr, 0
    r, dr = np.zeros(100000), np.zeros(100000)
    while rp < rseg[1]:
        r[N] = rp
        dr[N] = sz
        rp = rp + sz
        sz *= expand
        N += 1

    r = r[:N-1]
    dr = dr[:N-1]

    return r, dr
        """