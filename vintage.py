__author__ = 'peterwills'
import Model31lib as M
import pylab as plt
import matplotlib as mp

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

    def qc(self, prop='sg'):
        """
        plot the vintage
        :return:
        """
        fig = plt.figure(1)
        ax_tr = plt.subplot(1, 2, 2)
        ax_prop = plt.subplot(1, 2, 1, sharex=ax_tr, sharey=ax_tr)

        minx = 0.0
        for s in self.vintage:
            s.qc_bare(ax_prop, ax_tr, minx, prop)
            minx += s.dx
        ax_prop.set_ylim([0, s.thick])
        ax_prop.set_xlim([0, minx])
        ax_prop.set_title(self.get_title(prop))
        ax_tr.set_ylim([0, s.thick])
        ax_tr.set_xlim([0, minx])
        ax_tr.set_title('Seismic traces')
        plt.show()

    def get_title(self, prop):
        """
        Given the property, come up with a plot title
        :param prop: the property we plot
        :return: the title
        """
        print 'prop: ', prop
        if prop == 'sg':
            title = 'Gas Saturation'
        elif prop == 'vp':
            title = 'Compressional velocity'
        elif prop == 'rho':
            title = 'Density'
        else:
            title =''

        return title