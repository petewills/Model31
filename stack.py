__author__ = 'peterwills'
import Model31lib as M
import pylab as plt
import matplotlib as mp
import numpy as np
import Model31lib as L
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
        ax = fig.add_subplot(1, 1, 1)
        self.qc_bare(ax, 0.0, prop)
        plt.ylim([0, self.thick])
        plt.xlim([0, self.dx])
        plt.show()

    def qc_bare(self, ax, xmin, prop):
        """
        Plot the stack
        :param axis: the plot axis
        :param xmin: start distance along traverse
        :param prop: What property do we plot?
        :return:
        """
        # print 'Stack at location: ', xmin + self.dx / 2
        lower = 0.0
        for layer in self.stack:
            rect = mp.patches.Rectangle((xmin, lower), self.dx, layer.unit['dz'], color=layer.get_color(prop), ec='y')
            ax.add_patch(rect)
            lower += layer.unit['dz']
        self.attributes(0.1)

    def compose_series(self, N, tt, DIGI):
        """
        Compose the single vintage attributes for a stack
        :param N: Number of layers
        :param tt: travel time at the top
        :param DIGI: seismic digitization
        :return:
        """

        series = np.zeros(N)
        for (i, unit) in enumerate(self.stack):
            if i > 0:
                dt, a = L.get_refl(self.stack[i-1].unit, self.stack[i].unit)
                series = L.add_refl(series, a/DIGI, tt)
                if i < len(self.stack) - 1:  # First and last layers have no reservoir
                    tt = tt + int(dt/DIGI)

        return series, tt

    def attributes(self, DIGI):
        """
        Build the trace and attributes for a stack
        :param DIGI: digitization of seismic
        :return:
        """

        gate = 20.0
        N = int(1000 / DIGI)
        spectrum = [20, 40, 110, 140]
        for i in range(4):
            spectrum[i] = int(spectrum[i])

        tt0 = 180.0 / DIGI   # Basic "zero" for the time section
        # arg = []
        # for layer in self.stack:
        #     layer.display()
        #     arg.append(unit[0])

        trace, tt = self.compose_series(N, tt0, DIGI)
        trace = L.bp(trace, spectrum, DIGI, phase=0)

        rmstop = L.get_rms(trace, tt0, gate)
        rmsbase = L.get_rms(trace, tt, gate)

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
        for l in self.stack:
            thick.append(l.unit['dz'])
            col.append(l.unit['color'])
            totthick += float(l.unit['dz'])

        res = {'trace': trace, 'tt': tt, 'rmstop': rmstop, 'rmsbase': rmsbase, 'basegate': basegate, 'topgate': topgate,
           'thick': thick, 'totthick': totthick, 'color': col}


