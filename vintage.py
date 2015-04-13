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
        ax = fig.add_subplot(1, 1, 1)
        minx = 0.0
        for s in self.vintage:
            s.qc_bare(ax, minx, prop)
            minx += s.dx
        plt.ylim([0, s.thick])
        plt.xlim([0, minx])
        plt.show()