__author__ = 'peterwills'
import Model31lib as M


class Layer:
    """A single layer in one spatial position at one time. Two phases max, always returns rock unit"""

    def __init__(self, unit, fluid, gas, sg=0.0, dz=10.0):
        self.baseunit = unit
        mixgas = M.fmix('mixgas', [gas, fluid], [sg, 1.0-sg])
        color = (sg, 0, 1 - sg)
        if self.baseunit['phi'] > 0.1:
            self.unit = M.gassman('blGAS', unit, fluid, mixgas, color=color)
        else:
            self.unit = unit
        self.unit['dz'] = dz


    def display(self):
        print "unit:", self.baseunit
        print "new unit:", self.unit