__author__ = 'peterwills'
import Model31lib as M
import pylab as plt
import matplotlib as mp
import numpy as np
import Model31lib as L
import parameters as prm
import sys

class Stack:

    def __init__(self, layer,  dx=10.0):
        """
        A stack of layers at one spatial location and one time
        :param layer: first (deepest) unit in stack:
        :param X: Location on a traverse
        :return:
        """
        self.stack = [layer]
        self.N = 1
        self.dx = dx
        self.thick = layer.unit['dz']

    def append(self, layer):
        """
        Append a layer on top of the stack
        :param layer: the layer to append
        :return: nothing
        """
        self.stack.append(layer)
        self.thick += layer.unit['dz']
        self.N += 1

    def display(self):
        for unit in self.stack:
            print "unit:", unit

    def qc_bare(self, ax_prop, ax_tr, xmin, prop, wigcol, ingain):
        """
        Plot the stack
        :param ax_prop, ax_tr: the plot axes
        :param xmin: start distance along traverse
        :param prop: What property do we plot?
        :param wigcol: color of wiggle plot
        :param gain: gain for wiggle. 0.0 means autogain
        :return:
        """
        lower = 0.0
        for layer in self.stack:
            rect = mp.patches.Rectangle((xmin, lower), self.dx, layer.unit['dz'], color=layer.get_color(prop), ec='y')
            ax_prop.add_patch(rect)
            lower += layer.unit['dz']
        self.attributes(prm.DIGI, prm.LTRACE)
        xtr, ztr = self.limittr(lower, ingain)        # always use ingain
        ax_tr.plot(xtr + xmin + self.dx/2, ztr, wigcol)

    def limittr(self, zmax, ingain):
        """
        Limit the trace samples to the same range as the z of plots
        Gain is derived in 2 ways:
            - just use the input gain unless it is zero
            - if it is zero, derive from max in the trace
        : param zmax: upper limit of Z in the plot
        :return:
        """

        # for T/D, we need over and underburden as first and last reflections hung there
        over = self.stack[0].unit['vp']
        under = self.stack[-1].unit['vp']
        ntr = len(self.trace)
        s0 = (int(self.TT0) - 2.0 * prm.BURDEN / over * 1000.0) / prm.DIGI
        s1 = (int(self.ttbase) + 2.0 * prm.BURDEN / under * 1000.0) / prm.DIGI
        xtr = self.trace[s0:s1]
        ntr = len(xtr)
        ztot = zmax
        digz = ztot / float(ntr)
        ztr = np.arange(0.0, ztot, digz)

        # just use input gain plus harmonize  with x along vintage
        xtr = xtr * ingain * self.dx/2.0

        if len(ztr) > len(xtr):
            ztr = ztr[:len(xtr)]
        elif len(ztr) < len(xtr):
            xtr = xtr[:len(ztr)]

        return xtr, ztr

    def compose_series(self, N, tt, DIGI):
        """
        Compose the single vintage attributes for a stack
        :param N: Number of layers
        :param tt: travel time at the top
        :param DIGI: seismic digitization
        :return:the time series and time at bottom
        """

        series = np.zeros(N)
        for (i, unit) in enumerate(self.stack):
            if i > 0:
                print unit.unit
                dt, a = L.get_refl(self.stack[i-1].unit, self.stack[i].unit)
                print 'compose dt:', dt, tt
                series = L.add_refl(series, a/DIGI, int(tt))
                if i < len(self.stack) - 1:  # First and last layers have no reservoir
                    tt += dt/DIGI

        return series, tt

    def attributes(self, DIGI, LTRACE):
        """
        Build the trace and attributes for a stack
        :param DIGI: digitization of seismic
        :param LTRACE: length of seismic trace in ms
        :return:
        """

        gate = 20.0
        N = int(LTRACE / DIGI)                # 1000 ms trace length hardwired
        spectrum = [20, 40, 110, 140]
        for i in range(4):
            spectrum[i] = int(spectrum[i])

        self.trace, self.ttbase = self.compose_series(N, prm.TT0, DIGI)
        self.trace = L.bp(self.trace, spectrum, DIGI, phase=0)

        self.rmstop = L.get_rms(self.trace, prm.TT0, gate)
        self.rmsbase = L.get_rms(self.trace, self.ttbase, gate)

        self.ttbase *= DIGI     # put the time in ms, physical units
        self.TT0 = prm.TT0 * prm.DIGI
        print 'attr: ', self.TT0, self.ttbase

        # Model for plotting
        thick = []
        col = []
        totthick = 0.0
        for l in self.stack:
            thick.append(l.unit['dz'])
            col.append(l.unit['color'])
            totthick += float(l.unit['dz'])

