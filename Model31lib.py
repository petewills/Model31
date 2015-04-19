__author__ = 'peterwills'
import math as math
import numpy as np
import scipy
import scipy.fftpack
import pylab as plt
import sys as sys
import matplotlib as mp



def setmodel():
    """
    Set up a 4D model with the full model hierarchy
    :return: the model
    """

    # Basic rock layers
    wilrich = {'name': 'wil', 'vp': 3000.0, 'vs': 1800.0, 'rho': 2400.0, 'phi': 0.05, 'dz': 0.0, 'color': 'm'}
    blueskyBIT = {'name': 'blBIT', 'vp': 2850.0, 'vs': 1700.0, 'rho': 2090.0, 'phi': 0.28,
              'kg': 36.0*1000.0*1000.0*1000.0, 'dz': 28.0, 'color': 'k'}
    debolt = {'name': 'deb', 'vp': 3200.0, 'vs': 1800.0, 'rho': 2400.0, 'phi': 0.05, 'dz': 0.0, 'color': 'm'}

    # Basic fluid layers
    H2O = {'name': 'H2O', 'vp': 1630.0, 'rho': 980.0}
    GAS = {'name': 'GAS', 'vp': 650.0, 'rho': 280.0}
    BIT = {'name': 'BIT', 'vp': 1350.0, 'rho': 940.0}


def autogain(trace, extragain):
    """
    Gained relative to maximum amplitude and multiplied by extra gain
    :param trace: the seismic trace
    :param extragain: extra gain to multiply by
    :return:
    """

    gain = 1.0 / np.max(np.absolute(trace))

    return trace * gain * extragain, gain


def get_rms( series, t, gate):
    """get the rms of a gated series with triangle window"""

    tmid = int(t)
    t0 = tmid - int(gate/2)
    t1 = tmid + int(gate/2)

    wgt = 0.0
    sum = 0.0
    for i in range(t0, t1):
        sum = sum + series[i] * series[i] * wgt
        # wgt = 1.0 - float(abs(tmid-i)) / (gate/2)
        wgt = 1.0
    rms = np.sqrt(sum/(t1-t0))

    return rms


# def compose_series(N, strat, tt, DIGI):
#     """Given the strat, compose a seismic trace"""
#     series = np.zeros(N)
#     for (i, unit) in enumerate(strat):
#         if i > 0:
#             dt, a = get_refl(strat[i-1], strat[i])
#             series = add_refl(series, a/DIGI, int(tt))
#             if i < len(strat) - 1:  # First and last layers have no reservoir
#                 tt = tt + dt/DIGI
#     return series, tt


def add_refl(series, a, t):
    """Add a reflection to the series"""

    tl = int(math.floor(t))    # Small digi allows just to set one sample
    series[tl] -= a
    return series


def get_refl(ru, rl):
    """amplitude and time increment"""
    a = (ru['vp']*ru['rho'] - rl['vp']*rl['rho']) / (ru['vp']*ru['rho'] + rl['vp']*rl['rho'])
    dt = 2.0 * rl['dz'] / rl['vp'] * 1000.0

    return dt, a


def gassman(name, rock, f1, f2, color='y'):
    """Gassman on a given rock unit
    f1, f2 are before and after fluids """

    vp, vs, rho, kg, phi = rock['vp'], rock['vs'], rock['rho'], rock['kg'], rock['phi']
    vp_f1, rho_f1 = f1['vp'], f1['rho']
    vp_f2, rho_f2 = f2['vp'], f2['rho']
    K1 = rho*(vp*vp - 4/3*vs*vs)
    Kf_1 = rho_f1 * vp_f1 * vp_f1
    Kf_2 = rho_f2 * vp_f2 * vp_f2

    tmp = K1/(kg - K1) - Kf_1/(kg - Kf_1) / phi + Kf_2/(kg - Kf_2) / phi
    K2 = kg * tmp / (1 + tmp)

    rho_2 = rho + phi * (rho_f2 - rho_f1)
    mu2 = rho_2 * vs * vs

    vp_2 = np.sqrt((K2 + 4/3 * mu2)/rho_2)

    newrock = rock.copy()
    newrock['vp'] = vp_2
    newrock['rho'] = rho_2
    newrock['name'] = name
    newrock['color'] = color

    return newrock


def amp(ru, rl):
    a = (ru['vp']*ru['rho'] - rl['vp']*rl['rho']) / (ru['vp']*ru['rho'] + rl['vp']*rl['rho'])
    return a


def bp(ser, spect, DIGI, phase=0):
    digi = DIGI/1000.0
    N = len(ser)
    fser = np.fft.fft(ser)

    freqs = np.fft.fftfreq(N, d=digi)

    spect1 = []
    for i in range(4):
        spect1.append(spect[i])

    for i in range(N):
        f = abs(freqs[i])
        if f < spect1[0]:
            fser[i] = fser[i] * 0.0
        elif f >= spect1[0] and f < spect1[1]:
            fser[i] = fser[i] * (f - spect1[0]) / (spect1[1] - spect1[0])
        elif f >= spect1[1] and f < spect1[2]:
            fser[i] = fser[i] * 1.0
        elif f >= spect1[2] and f < spect1[3]:
            fser[i] = fser[i] * (spect1[3] - f) / (spect1[3] - spect1[2])
        else:
            fser[i] = fser[i] * 0.0

        if phase == 90:
            re = np.real(fser[i])
            im = np.imag(fser[i])
            fser[i] = complex(im, re)

    # s = np.abs(fser)
    # plt.figure(100)
    # plt.plot(freqs, s)
    # plt.show()
    newser = scipy.real(np.fft.ifft(fser))

    return newser

def testgas(GAS, fluid, rock):
    """
    Plot the gas curve for test purposes
    """

    ds = 0.002
    ns = int(1.0 / ds) + 1

    cs = 0.0
    x, y, yr = [], [], []
    for i in range(ns):
        mix = fmix('fluid mix', [GAS, fluid], [cs, 1.0 - cs], patchy='NO')
        mixRock = gassman('mixrock', rock, fluid, mix)
        y.append(mix['vp'])
        yr.append(mixRock['vp'])
        x.append(cs)
        cs = cs + ds

    plt.figure(100)
    plt.plot(x, y, 'ro-', label='fluid mix')
    plt.plot(x, yr, 'bo-', label='mixrock')
    plt.title("Fluid Gas substitution into " + fluid['name'])
    plt.xlabel('Gas Saturation')
    plt.ylabel('Fluid P Wave Velocity')
    plt.grid()
    plt.legend()


def fmix(name, components, fractions, patchy='NO'):
    """Mix several fluids"""

    all = 0.0
    for fraction in fractions:
        all = all + fraction
    if all != 1.0:
        print 'Error in fluid mix:', all, fractions
        sys.exit()

    KI = 0.0
    K = 0.0
    rho = 0.0
    for (i, c) in enumerate(components):
        if patchy == 'NO':
            KI += fractions[i] / (c['rho'] * c['vp'] * c['vp'])
        else:
            K += fractions[i] * (c['rho'] * c['vp'] * c['vp'])
        rho += c['rho'] * fractions[i]
    if patchy == 'NO':
        K = 1.0 / KI

    mix = components[0].copy()
    mix['vp'] = np.sqrt(K/rho)
    mix['rho'] = rho
    mix['name'] = name

    return mix


# Create TV pairs synthetic to test the plotting
def createTVpair(TVpath, rock, gas, fluid, Sg=[0.0, 0.8], A=10000, t='', data=[], col='r'):
    """
    :param TVpath: where to store the pairs
    :param rock: reservoir rock
    :param gas: gaseous part
    :param fluid: fluid part
    :param Sg: gas saturation: before/after
    :param A: area of stimulation in m2
    :param t: label of process
    :return:
    """

    f = open(TVpath, 'w')
    NZ = 15
    phi = rock['phi']      # Porosity

    V = []; T = []; Z = []
    currz = 0.0
    for i in range(NZ):
        V.append(currz * phi * (Sg[1] - Sg[0]) * A)
        TT0 = TT(rock, Sg[0], gas, fluid)
        TT1 = TT(rock, Sg[1], gas, fluid)
        T.append(currz * (TT1 - TT0))
        Z.append(currz)
        currz = currz + 1
    plt.figure(30)
    plt.subplot(111)
    plt.plot(V, T, col+'-o', label=t + ': A = ' + str(A) + '  Sg = ' + str(Sg[0]) + '-' + str(Sg[1]))
    y = [data['TS']]
    x = [data['Vol']]
    plt.plot(x, y, col+'s', markersize=14, label=t + ' data')
    plt.xlabel('Volume(m3)')
    plt.ylabel('Timeshift(ms)')
    plt.title('Volume vs Timeshift. zmax = ' + str(NZ-1))
    plt.grid()
    plt.legend(loc='upper left')

    f.close()


# Calculate the 2 way travel time for one meter. units are ms/m
def TT(rock, Sg, gas, fluid):
    """
    :param rock: reservoir rock with zero gas
    :param Sg: Gas saturation
    :param gas: gas properties
    :param fluid: fluid fill properties with no gas
    :return: Timeshift
    """

    mix = fmix('fluid mix', [gas, fluid], [Sg, 1.0 - Sg], patchy='NO')
    mixRock = gassman('mixRock', rock, fluid, mix, color='y')

    T = 2000 * 1.0 / mixRock['vp']
    return T


# Use TV pairs to analyse the time shifts, following Tim
def TVpair(TVpath):

    f = open(TVpath)
    for line in f.readline():
        print line

    f.close()