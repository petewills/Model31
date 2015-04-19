__author__ = 'peterwills'
import Model31lib as M


class Layer:
    """A single layer in one spatial position at one time. Two phases max, always returns rock unit"""

    def __init__(self, unit, fluid, gas, sg=0.0, dz=10.0):
        self.baseunit = unit
        mixgas = M.fmix('mixgas', [gas, fluid], [sg, 1.0-sg])
        self.sg = sg
        if self.baseunit['phi'] > 0.1:
            label = 'blGAS_' + str(sg)
            self.unit = M.gassman(label, unit, fluid, mixgas)
        else:
            self.unit = unit
        self.unit['dz'] = dz

    def get_color(self, prop):

        if prop == 'sg':
            return((self.sg, 0, 1 - self.sg))
        elif prop == 'vp':
            lim = [2500, 3400]
            v = self.unit[prop]
            norm = ((v - lim[0]) / (lim[1] - lim[0]))
            norm = max(0.0, norm); norm = min(1.0, norm)
            return((1.0 -norm, 0, norm))
        elif prop == 'rho':
            lim = [1800, 2500]
            v = self.unit[prop]
            norm = ((v - lim[0]) / (lim[1] - lim[0]))
            norm = max(0.0, norm); norm = min(1.0, norm)
            return((1.0 -norm, 0, norm))
        else:
            color = (0, 0, 1)


    def display(self):
        print "unit:", self.baseunit
        print "new unit:", self.unit