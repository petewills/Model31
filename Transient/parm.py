__author__ = 'peterwills'


q = 500.0 / (3600.0 * 24.0)                                       # flow rate m3/sec
mu = 1.0 * 9.0 / 10000.0                                          # viscosity of water in Pa-s at 20C (assume cool water)
k = 0.1 * 9.869 / 1000.0 / 1000.0 / 1000.0 / 1000.0 / 10.0       # permeability in m2. equal to 1 D
mu_4k = mu / (4.0*k)

print 'mu_k: ', mu_4k/1000000
h = 10.0                                                          # reservoir thickness(m)
phi = 0.28                                                        # porosity
c = 1.0 * 0.5/1000.0 / 1000.0 / 1000.0                            # compressibility water(Pa-1)

D = phi * mu_4k * c                         # phi * mu * C / ( 4.8 * k )        units are s / m2
p0 = q * mu_4k / (3.1415 * h)               # Pressure multiplies exponential integral in Pa
pi = 12.0                                    # background reservoir pressure(MPa)

print p0, D
fault = 'YES'                               # uses mirror well to produce a N-S strike fault at well