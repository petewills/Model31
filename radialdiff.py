__author__ = 'nlpwi4'

"""
Compute pressures using the radial diffusion equation, for input into ndi
Used to simulate pressure in 31-08
Creates an ascii version of an int file
"""

ofile = open("pressure.dat", "w")

# s = phi * mu * c * r^2 / (4 * k * t)
# P = q * mu / (4*pi*h) Ei*-s)

phi = 0.28          # Porosity
mu =
c =

xwell = 511258
ywell = 6246989

rmax = 250.0            # generate data out to this radius
dx = 10.0
nx = int(2.0 * rmax / dx) + 1

x = xwell - rmax
y = ywell -rmax
for i in range(nx):
    for j in range(nx):




ofile.close()



