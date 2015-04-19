__author__ = 'peterwills'
import Model31lib as M
import pylab as plt
import matplotlib as mp
import sys as sys
import parameters as prm
import Model31lib as L

class Vintage:

    def __init__(self, stack, day):
        """
        Represents one vintage traverse, with order left to right (x=0 to xtotal)
        :param stack: leftmost stack
        :param day: calendar in days beyond baseline
        :return:
        """

        self.vintage = [stack]
        self.N = 1
        self.day = day
        self.x = 0.0

    def append(self, stack):
        """
        Append a stack on right of the vintage
        :param stack: the stack to append
        :return: nothing
        """
        self.vintage.append(stack)
        self.N += 1

    def get_gain(self):
        """
        Find the suggested gain to make this vintage plotable
        We derive panel gan from full trace - should be ok as it is zero above/below
        :return:
        """
        # v = self.vintage
        # gain = 0.0
        # for s in v:
        #     lower = 0.0
        #     for layer in s.stack:
        #         lower += layer.unit['dz']
        #     s.attributes(prm.DIGI, prm.LTRACE)
        #     xtr, ztr, g = s.limittr(lower, 0.0)
        #     gain += g / len(v)

        print 'getting gains'
        v = self.vintage
        gain = 0.0
        for s in v:
            s.attributes(prm.DIGI, prm.LTRACE)
            xtr, g = L.autogain(s.trace, s.dx / 2.0)
            gain += g / len(v)

        return gain


    def qc4d(self, base):
        """
        plot diagnostics for 4D, given the baseline
        :param base: baseline vintage class instance
        :return:
        """

        # Find the gain suggested for base and monitor
        gain = (base.get_gain() + self.get_gain())/2.0

        print 'first base qc'
        base.qc(prop='vp', show='NO', wigcol='b', figno=1, gain=gain)
        print 'second base qc'
        base.qc(prop='vp', show='NO', wigcol='b', figno=2, gain=gain)
        print 'mon qc'
        self.qc(prop='vp', show='NO', wigcol='r',figno=2, gain=gain)

        sb = base.vintage
        sm = self.vintage

        if len(sb) != len(sm):
            print 'Error in 4D qc: different number of spatial points'
            sys.exit()

        ts, ndrmstop, ndrmsbase = [], [], []
        # timeshift
        for (i, s) in enumerate(sm):
            print 'vintage: ', sb[i].ttbase, s.ttbase, sb[i].ttbase - s.ttbase
            ts.append(sb[i].ttbase - s.ttbase)          # timeshift at base reservoir
            ndrmstop.append( 2.0 * (sb[i].rmstop - s.rmstop) / (sb[i].rmstop + s.rmstop))       # ndrms at top reservoir
            ndrmsbase.append( 2.0 * (sb[i].rmsbase - s.rmsbase) / (sb[i].rmsbase + s.rmsbase) ) # ndrms at top reservoir

        plt.figure(3)
        ax_att = plt.subplot(1,1,1)
        plt.figure(2)
        ax_att_t = ax_att.twinx()

        x = range(len(ndrmstop))
        ax_att.plot(x, ndrmstop, 'ko-', label='NDRMS Top Reservoir')
        ax_att.plot(x, ndrmsbase, 'ro-', label='NDRMS Base Reservoir')
        ax_att_t.plot(x, ts, 'go-', label='Time in Reservoir')
        ax_att.plot(0, 0, 'g-', label='Time in Reservoir')
        ax_att.grid()
        plt.title('Attributes')
        ax_att.set_ylabel('NDRMS')
        ax_att_t.set_ylabel('timeshift(ms)')
        ax_att.legend(loc='upper left')
        plt.show()

        sys.exit()

    def qc(self, prop='sg', show='NO', wigcol='r', figno=1, gain=0.0):
        """
        plot the vintage
        : param prop: property to plot eg vp or sg
        :param show: whether or not to do plot.show
        :param wigcol: color for the wiggles
        :param figno: figure number. repeating means an overlay, goot for comparing traces
        :param gain: gain fro raw panel. zero means use autogain
        :return:
        """
        plt.figure(figno)
        ax_tr = plt.subplot(1, 2, 2)
        ax_prop = plt.subplot(1, 2, 1, sharex=ax_tr, sharey=ax_tr)

        minx = 0.0
        for s in self.vintage:
            s.qc_bare(ax_prop, ax_tr, minx, prop, wigcol, gain)
            minx += s.dx
        ax_prop.set_ylim([0, s.thick])
        ax_prop.set_xlim([0, minx])
        ax_prop.set_title(self.get_title(prop))
        ax_tr.set_ylim([0, s.thick])
        ax_tr.set_xlim([0, minx])
        ax_tr.set_title('Seismic traces: (red=mon)  (blue=base)')
        if show=='YES':
            plt.show()

    def get_title(self, prop):
        """
        Given the property, come up with a plot title
        :param prop: the property we plot
        :return: the title
        """

        if prop == 'sg':
            title = 'Gas Saturation'
        elif prop == 'vp':
            title = 'Compressional velocity'
        elif prop == 'rho':
            title = 'Density'
        else:
            title = ''

        return title