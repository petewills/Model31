__author__ = 'peterwills'
""" Library for the transient well functionality"""
from scipy.special import expn as expn
import pylab as plt
import numpy as np
import fdparm as fdprm
import parm as prm
from scipy.integrate import ode as ode
from scipy.integrate import odeint as odeint
import sys as sys
import math as math

def linesolve():
    """
    Solve the radial diffusivity equation using the method of lines
    :return: Pressure grid in time and space
    """


    def rhs(y, t):
        """
        Defines a rhs, where lhs is simply the time derivative
        1/r { P' + r P""}
        Note that the arrays are padded by one element at either end
        :param y: a single time step of the radial pressure vector
        """
        #
        if t > fdprm.tprev:
            print 'rhs t', t
            fdprm.tprev = t


        nr = len(y)             # includes the extra fake boundary points
        y0 = y[1:nr-1]
        ym = y[0:nr-2]
        yp = y[2:nr]

        pp = (y0 - ym)/fdprm.dr[1:nr-1]
        ppp = (yp - 2.0*y0 + ym)/fdprm.dr[1:nr-1]**2

        pp1, ppp1 = np.zeros(nr), np.zeros(nr)
        for i in range(1, nr-1):
            pp1[i] = (y[i] - y[i-1])/fdprm.dr[i]
            ppp1[i] = (y[i-1] - 2.0 * y[i] + y[i+1]) / fdprm.dr[i]**2


        deriv = np.zeros(nr)
        deriv[1:nr-1] = (pp + fdprm.r[1:nr-1] * ppp) * prm.nu
        deriv /= fdprm.r
        deriv[nr-1] = 0.0        # Dirichlet at boundary. There is no change to initial value
        deriv[0] = deriv[1]      # Neuman at zero. [0] and [1] move lockstep having been set in y0

        predict = y[:4] + h0*deriv[:4]

        # print 'deriv: ', deriv[:4]/1000/1000
        # print 'r: ', fdprm.r[:4], fdprm.dr[:4]
        # print 'y: ', y[0:4]/1000/1000
        # print 'predict y: ', predict / 1000/1000
        # print 'ppp, pp: ', ppp[:4]/1000/1000, pp[:4]/1000/1000
        # print 'ppp1, pp1: ', ppp1[1:5]/1000/1000, pp1[1:5]/1000/1000
        # print

        # plt.subplot(122)
        # plt.plot(fdprm.r[0:10], deriv[0:10])
        plt.figure(11)
        # plt.subplot(121)
        plt.plot(fdprm.r[1:10], y[1:10], 'o')


        return deriv


    y0 = np.ones(len(fdprm.r)) * prm.pi
    y0[0] = y0[1] + prm.Qnorm / fdprm.r[0] * fdprm.dr[0]    # Boundary cond set at beginning. derives will preserve it.
    # print 'y0: ', y0[0:4]/1000000
    # i = ode(rhs)
    # i.set_integrator('vode', method='bde')
    # i.set_initial_value(r, y0)

    # Loop over times
    h0 = 0.001
    y, output = odeint(rhs, y0, fdprm.tvals, h0=h0, hmax=2000.0, mxstep=2000, full_output=True)
    #plt.plot(y)

    plt.figure(12)
    plt.title('PDE time evolution')
    plt.xlabel('Space')
    plt.ylabel('Function value')
    plt.imshow(y, aspect='auto')
    plt.grid()
    plt.colorbar()

    plt.figure(13)
    plt.title('PDE time evolution')
    plt.xlabel('Space')
    plt.ylabel('Function value')
    print np.shape(y)
    for (i, t) in enumerate(fdprm.tvals):
        plt.plot(fdprm.r, y[i])
    plt.grid()
    #print y
    plt.show()

    print output['hu']




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