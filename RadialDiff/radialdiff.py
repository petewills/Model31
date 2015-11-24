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
# P = q * mu / (4*pi*k*h) Ei*-s)
mb = prm.k / prm.mu
exfac = 500.0
D = prm.phi * prm.c / (4.0 * mb) * exfac

Pup_days = 74                   # Days of pressure-up
daystep = 1

xwell = 511258
ywell = 6246989
tlim = [1, 74]         # in days
nt = tlim[1] - tlim[0]

rmax = 250.0            # generate data out to this radius
dx = 5.0
nxmap = int(2.0 * rmax / dx) + 1

Pdown = np.zeros([nt+1, nxmap, nxmap])
Pup = np.zeros([nt+1, nxmap, nxmap])
Pafter = np.zeros([nt+1, nxmap, nxmap])
for t in range(tlim[0], tlim[1]):
    dt = ((t-1) * daystep + 0.001) * 3600 * 24
    for i in range(nxmap):
        x = (xwell - rmax) + float(i) * dx
        for j in range(nxmap):
            y = (ywell - rmax) + float(j) * dx
            r = np.sqrt((x-xwell)**2 + (y-ywell)**2)
            s = D * r**2 / dt
            Pdown[t, i, j] = prm.pi + prm.p0 * lib.ei(s) / 1000 / 1000        # In MPa

            dt_up = Pup_days * 3600 * 24
            s = D * r**2 / dt_up
            Pup[t, i, j] = prm.pi + prm.p0 * lib.ei(s) / 1000 / 1000#  - Pdown[t, i, j]       # In MPa

            s = D * r**2 / dt
            Pafter[t, i, j] = prm.pi + Pup[t, i, j] - Pdown[t, i, j]       # In MPa



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
        plt.imshow(np.transpose(Pdown[ind]), origin='lower', clim=[prm.pi, 11])
        # plt.contour(Pdown[ind])
        plt.colorbar()
        fr = plt.gca()
        fr.axes.get_xaxis().set_visible(False)
        fr.axes.get_yaxis().set_visible(False)
        fr.text(0.5, 0.85, 'Day '+str(t), transform=fr.transAxes, fontsize=12, horizontalalignment='center')
        t += daystep
        ind += 1
        ip += 1
plt.suptitle('Pressure down - absolute')


plt.figure(2)
nx = int(np.sqrt(nt))
t = tlim[0]
ind = tlim[0]
ip = 1
for i in range(nx):
    for j in range(nx):
        if ip>1:
            plt.subplot(nx, nx, ip, sharex=ax, sharey=ax)
        else:
            # ax = plt.subplot(nx, nx, ip)
            plt.subplot(nx, nx, ip, sharex=ax, sharey=ax)
        plt.imshow(np.transpose(Pup[ind]), origin='lower')#, clim=[prm.pi, 11])
        plt.colorbar()
        fr = plt.gca()
        fr.axes.get_xaxis().set_visible(False)
        fr.axes.get_yaxis().set_visible(False)
        fr.text(0.5, 0.85, 'Day '+str(t), transform=fr.transAxes, fontsize=12, horizontalalignment='center')
        t += daystep
        ind += 1
        ip += 1
plt.suptitle('Pressure up - absolute')

plt.figure(3)
nx = int(np.sqrt(nt))
t = tlim[0]
ind = tlim[0]
ip = 1
for i in range(nx):
    for j in range(nx):
        if ip>1:
            plt.subplot(nx, nx, ip, sharex=ax, sharey=ax)
        else:
            # ax = plt.subplot(nx, nx, ip)
            plt.subplot(nx, nx, ip, sharex=ax, sharey=ax)
        plt.imshow(np.transpose(Pafter[ind]), origin='lower')#, clim=[prm.pi, 11])
        plt.colorbar()
        fr = plt.gca()
        fr.axes.get_xaxis().set_visible(False)
        fr.axes.get_yaxis().set_visible(False)
        fr.text(0.5, 0.85, 'Day '+str(t), transform=fr.transAxes, fontsize=12, horizontalalignment='center')
        t += daystep
        ind += 1
        ip += 1
plt.suptitle('Pressure down - subtracted Max Pressure Date')
plt.show()


# Plot a cut across the center
plt.figure(4)
nx = int(np.sqrt(nt))
t = tlim[0]
ind = tlim[0]
ip = 1
for i in range(nx):
    for j in range(nx):
        if ip>1:
            plt.subplot(nx, nx, ip, sharex=ax1, sharey=ax1)
        else:
            ax1 = plt.subplot(nx, nx, ip)
        plt.plot(Pdown[ind, :, nxmap/2], 'r-', label='Pdown')
        plt.plot(Pup[ind, :, nxmap/2], 'k-', label='Pup')
        plt.plot(Pafter[ind, :, nxmap/2], 'b-', label='P Post Shutin')
        fr = plt.gca()
        fr.text(0.5, 0.85, 'Day '+str(t), transform=fr.transAxes, fontsize=12, horizontalalignment='center')
        # plt.legend()
        plt.grid()
        t += daystep
        ind += 1
        ip += 1
plt.suptitle('Cut through well')
plt.show()


day0 = 1524             # Day when we shutin
ofile.write("%16s%16s\n"% ( Pup, Pdown) )
for it in range(nt):
    for j in range(nxmap):
        for k in range(nxmap):
            x = (xwell - rmax) + float(j) * dx
            y = (ywell - rmax) + float(k) * dx
            ofile.write("%16.2f%16.2f%16d%16.2f%16.2f\n" % (x, y, it+day0, Pup[i, j, k], Pdown[i, j, k], Pafter[i, j, k]))


ofile.close()



