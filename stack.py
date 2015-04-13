__author__ = 'peterwills'
import Model31lib as M
import pylab as plt
import matplotlib as mp
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
            rect = mp.patches.Rectangle((xmin, lower), self.dx, layer.unit['dz'], color=layer.unit['color'], ec='y')
            ax.add_patch(rect)
            lower += layer.unit['dz']


