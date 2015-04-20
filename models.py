__author__ = 'nlpwi4'
import layer as L
import stack as S
import vintage as V
import parameters as prm

""" Models that have been constructed"""

def first(nx=5, nz=5, liqlev=5.0, delliq=0.0, dgtot=[0.0, 0.0]):
    """
    This model has gas saturation gradient rising above a liquid layer
    :param nx, nz The model dimensions
    :param liqlev: liquid level in the baseline
    :param delliq: governs how much the liquid level changes with x
    :param dgtot: gas change limits at bottom.top of gas column
    :return:
    """
    # delliq = 10.0 / float(nx)
    delx = 1000 / float(nx)
    dz_sand = 28.0
    dg = (dgtot[1] - dgtot[0]) / float(nz)
    for ix in range(nx):
        level = liqlev + float(ix) * delliq
        rest = max(dz_sand - level, 0.0)
        delz = rest / float(nz-1)
        l = [L.Layer(prm.debolt, prm.BIT, prm.BIT, sg=0.0, dz=prm.BURDEN)]       # Underburden
        l.append(L.Layer(prm.blueskyBIT, prm.BIT, prm.GAS, sg=0.0, dz=level)) # liquid
        for iz in range(nz-1):
            l.append(L.Layer(prm.blueskyBIT, prm.BIT, prm.GAS, sg=dgtot[0] + float(iz)*dg, dz=delz))
        l.append(L.Layer(prm.wilrich, prm.BIT, prm.BIT, sg=0.0, dz=prm.BURDEN))  # Overburden

        s = S.Stack(l[0], dx=delx)
        for lay in l[1:]:
            s.append(lay)
        if (ix == 0):
            v = V.Vintage(s, 0)
        else:
            v.append(s)
    return v
