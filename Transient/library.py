__author__ = 'peterwills'
""" Library for the transient well functionality"""
from scipy.special import expn as expn
import pylab as plt
import numpy as np


def ei(x):
    """
    exponential integral used in transient analysis
    :param x: input arg
    :return: ei
    """

    ei = expn(1, x)
    return ei


def onewell(pi, p0, D, r, t):
    """
    Compute pressure at r from a well at origin
    :param r: distance from well
    :param D: diffusivity
    :param P0: Pressure multiplier
    :param pi: injector pressure
    :param tv: times to calculate
    :return:Pressures at origin
    """
    arg = D * r * r / t
    p = pi + p0 * ei(arg) / 1000000.0       # pressure in MPa

    return p

def onewell_times(x, y, D, p0, pi, tv, fault='NULL'):
    """
    Compute pressure at test point from well at origin
    :param x: x coordinate test point
    :param y: y coordinate of test point
    :param D: diffusivity
    :param P0: Pressure multiplier
    :param pi: injector pressure
    :param tv: times to calculate(seconds)
    :param fault: x coordinate of fault
    :return:Pressures at origin
    """

    n = len(tv)
    pv = np.zeros(n)
    for i in range(n):
        r = np.sqrt(x*x + y*y)
        t = tv[i]

        pv[i] = onewell(pi, p0, D, r, t)
        if fault[0] == 'FAULT':
            x1 = x - 2.0 * fault[1]
            r1 = np.sqrt(x1*x1 + y*y)
            pv[i] += onewell(0.0, p0, D, r1, t)
        elif fault[0] == 'CIRCLE':   # generate a bunch of wells to give circular reservoir limit.
            nc = fault[2]
            c = 2.0 * 3.14159 * (2.0 * fault[1])
            dth = 2.0 * 3.1415 / float(nc)
            th = 0.0
            for j in range(nc-1):
                xc = x - np.cos(th) * 2.0 * fault[1]
                yc = y - np.sin(th) * 2.0 * fault[1]
                rc = np.sqrt(xc*xc+yc*yc)
                pv[i] += onewell(0.0, p0, D, rc, t) / float(nc)
                #print x, xc, rc, pv[i], th
                th += dth

    #sys.exit()
    return pv

def onewell_xy(xv, yv, D, p0, pi, T):
    """
    Compute pressure at origin from a well at this position
    :param x: x coordinate f well vector in meters
    :param y: y coordinate of well vector
    :param D: diffusivity
    :param P0: Pressure multiplier
    :param pi: injector pressure
    :param T: time of calculation in seconds
    :return:Pressures at origin
    """

    n = len(xv)
    pv = np.zeros(n)
    for i in range(n):
        r = np.sqrt(xv[i]*xv[i] + yv[i]*yv[i])

        pv[i] = onewell(pi, p0, D, r, T)

    return pv



def testei(fig=1):
    """
    Test the exponential integral
    :return:
    """
    xv = np.arange(0.001,1.0, 0.001)
    yv = []
    av = []
    for (i, x) in enumerate(xv):
        yv.append(ei(x))
        av.append(-np.log(1.781*x))

    plt.figure(fig)
    plt.subplot(1,2,1)
    plt.loglog(xv, yv, 'r-', label='ei', basex=10)
    plt.loglog(xv, av, 'b-', label='log', basex=10)
    plt.grid(which='both')
    plt.minorticks_on()
    plt.ylim([0.1, 10.0])
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(xv, yv, 'r-', label='ei')
    plt.plot(xv, av, 'b-', label='log')
    plt.grid()
    plt.minorticks_on()
    # plt.ylim([0.1, 10.0])
    plt.xlim([0,.2])
    plt.legend()
    plt.suptitle('Test of exponential integral')
    plt.show()