__author__ = 'peterwills'
import Model31lib as M
import pylab as plt
import matplotlib as mp

class Stack:

    def __init__(self, layer, X):
        """
        A stack of layers at one spatial location and one time
        :param unit: first (deepest) unit in stack:
        :param X: Location on a traverse
        :return:
        """
        self.stack = [layer]
        self.N = 1
        self.X = X
        layer.display()
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
        print 'Stack at location: ', self.X
        for unit in self.stack:
            print "unit:", unit

    def qc(self):
        print 'Stack at location: ', self.X
        fig = plt.figure(1)
        lower = 0
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


