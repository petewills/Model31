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

    def qc(self):
        """
        plot the vintage
        :return:
        """
        fig = plt.figure(1)
        ax = fig.add_subplot(1, 1, 1)
        minx = 0.0
        for s in self.vintage:
            s.qc_bare(ax, minx)
            minx += s.dx
        plt.ylim([0, s.thick])
        plt.xlim([0, minx])
        plt.show()

        print 'Vintage at date: ', self.day
        fig = plt.figure(1)
        lower = 0  # lower limit in Z
        ax = fig.add_subplot(1, 1, 1)
        for layer in self.stack:
            rect = mp.patches.Rectangle((0, lower), 20, layer.unit['dz'], color=layer.unit['color'], ec='y')
            ax.add_patch(rect)
            print 'lower:', lower, layer.unit['dz']
            lower += layer.unit['dz']
            # plt.xlim([0, 20])
            # lim = r['totthick']
            plt.ylim([0, self.thick])
            # frame1 = plt.gca()
            # frame1.axes.get_xaxis().set_ticks([])
        plt.show()