__author__ = 'peterwills'

HOME = '/Users/peterwills/PyCharmProjects/Model31'
TVpath = HOME + 'TVPair.dat'

# All physical numbers in ms. I use small digi for hanging waves on spikes
DIGI = 0.1


# Basic rock and fluid units
wilrich = {'name': 'wil', 'vp': 3000.0, 'vs': 1800.0, 'rho': 2400.0, 'phi': 0.05, 'dz': 0.0, 'color': 'm'}
blueskyBIT = {'name': 'blBIT', 'vp': 2850.0, 'vs': 1700.0, 'rho': 2090.0, 'phi': 0.28,
              'kg': 36.0*1000.0*1000.0*1000.0, 'dz': 28.0, 'color': 'k'}
debolt = {'name': 'deb', 'vp': 3200.0, 'vs': 1800.0, 'rho': 2400.0, 'phi': 0.05, 'dz': 0.0, 'color': 'm'}
H2O = {'name': 'H2O', 'vp': 1630.0, 'rho': 980.0}
GAS = {'name': 'GAS', 'vp': 650.0, 'rho': 280.0}
BIT = {'name': 'BIT', 'vp': 1350.0, 'rho': 940.0}