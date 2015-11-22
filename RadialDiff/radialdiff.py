__author__ = 'nlpwi4'
import parm as prm
import numpy as np
import library as lib
import pylab as plt

"""
Compute pressures using the radial diffusion equation, for input into ndi
Used to simulate pressure in 31-08
Creates an ascii version of an int file
"""

ofile = open("pressure.dat", "w")

# s = phi * mu * c * r^2 / (4 * k * t)
# P = q * mu / (4*pi*h) Ei*-s)
mb = prm.k / prm.mu
D = prm.phi * prm.c / (4.0 * mb)
daystep = 5

xwell = 511258
ywell = 6246989
tlim = [1, 20]         # in days
nt = tlim[1] - tlim[0]

rmax = 300.0            # generate data out to this radius
dx = 10.0
nx = int(2.0 * rmax / dx) + 1

P = np.zeros([nt+1, nx, nx])
for (it, t) in enumerate(range(tlim[0], tlim[1])):
    dt = ((t-1) * daystep + 1) * 3600 * 24
    for i in range(nx):
        x = (xwell - rmax) + float(i) * dx
        for j in range(nx):
            y = (ywell - rmax) + float(j) * dx
            r = np.sqrt((x-xwell)**2 + (y-ywell)**2)
            s = D * r**2 / (dt)
            P[t, i, j] =  prm.pi - prm.p0 * lib.ei(s) / 1000 / 1000        # In MPa
            # print x, y, t, it, s, r, prm.p0

plt.figure(1)
nx = int(np.sqrt(nt))
t = tlim[0]
ind = tlim[0]
ip = 1
for i in range(nx):
    for j in range(nx):
        if ip>1:
            plt.subplot(nx, nx, ip, sharex=ax, sharey=ax)
        else:
            ax = plt.subplot(nx, nx, ip)
        plt.imshow(np.transpose(P[ind]), origin='lower', clim=[4,prm.pi])
        plt.colorbar()
        fr = plt.gca()
        fr.axes.get_xaxis().set_visible(False)
        fr.axes.get_yaxis().set_visible(False)
        fr.text(0.5, 0.85, 'Day '+str(t), transform=fr.transAxes, fontsize=12, horizontalalignment='center')
        t += daystep
        ind += 1
        ip += 1
plt.show()

ofile.close()



