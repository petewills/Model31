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
        print 'Stack at location: ', self.dx
        for unit in self.stack:
            print "unit:", unit

    def qc(self, prop='sg'):
        """
        standalone plot of the stack
        :return:
        """
        fig = plt.figure(1)
        ax_prop = plt.subplot(1, 2, 1)
        ax_tr = plt.subplot(1, 2, 2)
        self.qc_bare(ax_prop, ax_tr, 0.0, prop)
        plt.ylim([0, self.thick])
        plt.xlim([0, self.dx])
        plt.show()

    def qc_bare(self, ax_prop, ax_tr, xmin, prop):
        """
        Plot the stack
        :param ax_prop, ax_tr: the plot axes
        :param xmin: start distance along traverse
        :param prop: What property do we plot?
        :return:
        """
        # print 'Stack at location: ', xmin + self.dx / 2
        lower = 0.0
        for layer in self.stack:
            rect = mp.patches.Rectangle((xmin, lower), self.dx, layer.unit['dz'], color=layer.get_color(prop), ec='y')
            ax_prop.add_patch(rect)
            lower += layer.unit['dz']
        self.attributes(prm.DIGI, prm.LTRACE)
        ntr = len(self.trace)
        xtr = self.trace[:ntr/2]
        ntr = len(xtr)
        digz = lower / float(ntr)
        ztr = np.arange(0.0, lower, digz)
        xtr, ztr = self.limittr(lower)
        ax_tr.plot(xtr + xmin + self.dx/2, ztr)

    def limittr(self, zmax):
        """
        Limit the trace samples to the same range as the z of plots
        : param zmax: upper limit of Z in the plot
        :return:
        """
        ntr = len(self.trace)
        s0 = int(prm.TT0)
        s1 = int(self.ttbase)
        print s0, s1, ntr

        xtr = self.trace[s0:s1]
        ntr = len(xtr)
        digz = zmax / float(ntr)
        ztr = np.arange(0.0, zmax, digz)
        xtr = L.autogain(xtr, self.dx/2.0)

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
                dt, a = L.get_refl(self.stack[i-1].unit, self.stack[i].unit)
                print 'a dt is: ', a, dt, tt
                series = L.add_refl(series, a/DIGI, tt)
                if i < len(self.stack) - 1:  # First and last layers have no reservoir
                    tt = tt + int(dt/DIGI)

        return series, tt

    def attributes(self, DIGI, LTRACE):
        """
        Build the trace and attributes for a stack
        :param DIGI: digitization of seismic
        : param LTRACE: length of seismic trace in ms
        :return:
        """

        gate = 20.0
        N = int(LTRACE / DIGI)                # 1000 ms trace length hardwired
        spectrum = [20, 40, 110, 140]
        for i in range(4):
            spectrum[i] = int(spectrum[i])

        # arg = []
        # for layer in self.stack:
        #     layer.display()
        #     arg.append(unit[0])

        print 'set trace'
        self.trace, self.ttbase = self.compose_series(N, prm.TT0, DIGI)
        self.trace = L.bp(self.trace, spectrum, DIGI, phase=0)

        rmstop = L.get_rms(self.trace, prm.TT0, gate)
        rmsbase = L.get_rms(self.trace, self.ttbase, gate)

        # Gates fot plotting
        g1 = int((self.ttbase-gate/2.0/DIGI))
        g2 = int((self.ttbase+gate/2.0/DIGI))
        basegate = [[g1, g1], [g2, g2]]
        g1 = int((prm.TT0-gate/2.0/DIGI))
        g2 = int((prm.TT0+gate/2.0/DIGI))
        topgate = [[g1, g1], [g2, g2]]

        # Model for plotting
        thick = []
        col = []
        totthick = 0.0
        for l in self.stack:
            thick.append(l.unit['dz'])
            col.append(l.unit['color'])
            totthick += float(l.unit['dz'])

        res = {'trace': self.trace, 'tt': self.ttbase, 'rmstop': rmstop, 'rmsbase': rmsbase, 'basegate': basegate, 'topgate': topgate,
           'thick': thick, 'totthick': totthick, 'color': col}


