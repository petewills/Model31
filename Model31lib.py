__author__ = 'peterwills'
import math as math
import numpy as np
import scipy
import scipy.fftpack
import pylab as plt
import sys as sys
import matplotlib as mp

def get_rms( series, t, gate):
    """get the rms of a gated series with triangle window"""

    tmid = int(t)
    t0 = tmid - int(gate/2)
    t1 = tmid + int(gate/2)

    wgt = 0.0
    sum = 0.0
    for i in range(t0, t1):
        sum = sum + series[i] * series[i] * wgt
        wgt = 1.0 - float(abs(tmid-i)) / (gate/2)
        wgt = 1.0
    rms = np.sqrt(sum/(t1-t0))

    return rms



def compose_series(N, strat, tt, DIGI):
    """Given the strat, compose a seismic trace"""
    series = np.zeros(N)
    for (i, unit) in enumerate(strat):
        if i > 0:
            dt, a = get_refl(strat[i-1], strat[i])
            series = add_refl(series, a/DIGI, tt)
            if i < len(strat) - 1:  # First and last layers have no reservoir
                tt = tt + int(dt/DIGI)
    return series, tt

def add_refl( series, a, t):
    """Add a reflection to the series"""

    tl = int(math.floor(t))    # Small digi allows just to set one sample
    series[tl] -= a
    return series

def get_refl( ru, rl):
    """amplitude and time increment"""
    a = (ru['vp']*ru['rho'] - rl['vp']*rl['rho']) / (ru['vp']*ru['rho'] + rl['vp']*rl['rho'])
    dt = 2.0 * rl['dz']  / rl['vp'] * 1000.0

    return dt, a





def gassman(name, rock, f1, f2, color='y'):
    """Gassman on a given rock unit
    f1, f2 are before and after fluids """

    vp, vs, rho, Kg, phi = rock['vp'], rock['vs'], rock['rho'], rock['Kg'], rock['phi']
    vp_f1, rho_f1 = f1['vp'], f1['rho']
    vp_f2, rho_f2 = f2['vp'], f2['rho']
    K1 = rho*(vp*vp - 4/3*vs*vs)
    Kf_1 = rho_f1 * vp_f1 * vp_f1
    Kf_2 = rho_f2 * vp_f2 * vp_f2

    tmp = K1/(Kg-K1) - Kf_1/(Kg - Kf_1)/ phi + Kf_2/(Kg - Kf_2)/ phi
    K2 = Kg * tmp / (1 + tmp)

    rho_2 = rho + phi * ( rho_f2 - rho_f1 )
    mu2 = rho_2 * vs * vs

    vp_2 = np.sqrt((K2 + 4/3 * mu2)/rho_2)

    newrock = rock.copy()
    newrock['vp'] = vp_2
    newrock['rho'] = rho_2
    newrock['name'] = name
    newrock['color'] = color

    return newrock

def amp( ru, rl):
    a = (ru['vp']*ru['rho'] - rl['vp']*rl['rho']) / (ru['vp']*ru['rho'] + rl['vp']*rl['rho'])
    return a


def bp( ser, spect, DIGI, phase=0 ):
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

        if phase==90:
            re = np.real(fser[i])
            im = np.imag(fser[i])
            fser[i] = complex(im, re)

    s = np.abs(fser)
    # plt.figure(100)
    # plt.plot(freqs, s)
    # plt.show()
    newser = scipy.real(np.fft.ifft(fser))

    return newser

def reservoir(units, DIGI):
    """Build one vintage of reservoir"""

    gate = 20.0
    N = int(1000 / DIGI)
    spectrum = [20, 40, 110, 140]
    for i in range(4):
        spectrum[i] = int(spectrum[i])


    tt0 = 180.0 / DIGI   # Basic "zero" for the time section
    arg = []
    for unit in units:
        unit[0]['dz'] = unit[1]
        arg.append(unit[0])

    trace, tt = compose_series(N, arg, tt0, DIGI)
    trace = bp( trace, spectrum, DIGI, phase=0)

    rmstop = get_rms(trace, tt0, gate)
    rmsbase = get_rms(trace, tt, gate)

    # Gates fot plotting
    g1 = int((tt-gate/2.0/DIGI))
    g2 = int((tt+gate/2.0/DIGI))
    basegate = [[g1, g1], [g2, g2]]
    g1 = int((tt0-gate/2.0/DIGI))
    g2 = int((tt0+gate/2.0/DIGI))
    topgate = [[g1, g1], [g2, g2]]

    # Model for plotting
    thick = []
    col = []
    totthick = 0.0
    for unit in units:
        thick.append(float(unit[1]))
        col.append(unit[0]['color'])
        totthick += float(unit[1])

    res = {'trace':trace, 'tt':tt, 'rmstop':rmstop, 'rmsbase':rmsbase, 'basegate': basegate, 'topgate': topgate,
           'thick': thick, 'totthick': totthick, 'color': col}
    return res

def testgas(GAS, fluid, rock):
    """
    Plot the gas curve for test purposes
    """

    ds = 0.002
    ns = int(1.0 / ds) + 1

    cs = 0.0
    x, y, yr = [], [], []
    for i in range(ns):
        mix = fmix( 'fluid mix', [GAS, fluid], [cs, 1.0 - cs], patchy='NO')
        mixRock = gassman('mixrock', rock, fluid, mix )
        y.append( mix['vp'])
        yr.append( mixRock['vp'] )
        x.append(cs)
        cs = cs + ds

    plt.figure(100)
    plt.plot( x, y, 'ro-', label = 'fluid mix')
    plt.plot( x, yr, 'bo-', label = 'mixrock')
    plt.title( "Fluid Gas substitution into " + fluid['name'])
    plt.xlabel('Gas Saturation')
    plt.ylabel('Fluid P Wave Velocity')
    plt.grid()
    plt.legend()

def fmix( name, components, fractions, patchy = 'NO'):
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
def createTVpair(TVpath, rock, gas, fluid, Sg=[0.0,0.8], A=10000, t='', data=[], col='r'):
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
    delz = 1.0      # in meters
    NZ = 15
    phi = rock['phi']      # Porosity

    V = []; T = []; Z=[]
    currz = 0.0
    for i in range(NZ):
        V.append(currz * phi * (Sg[1]-Sg[0]) * A)
        TT0 = TT(rock, Sg[0], gas, fluid)
        TT1 = TT(rock, Sg[1], gas, fluid)
        print TT0, TT1, TT1-TT0
        T.append(currz * (TT1 - TT0))
        Z.append(currz)
        currz = currz + 1
    plt.figure(30)
    ax = plt.subplot(111)
    plt.plot(V, T, col+'-o', label=t + ': A = '+ str(A) + '  Sg = ' + str(Sg[0]) + '-' + str(Sg[1]))
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

    mix = fmix( 'fluid mix', [gas, fluid], [Sg, 1.0 - Sg], patchy='NO')
    mixRock = gassman('mixRock', rock, fluid, mix, color='y')

    T = 2000 * 1.0 / mixRock['vp']
    return T



# Use TV pairs to analyse the time shifts, following Tim
def TVpair(TVpath):

    f = open(TVpath)
    for line in f.readline():
        print line


    f.close()