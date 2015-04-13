__author__ = 'nlpwi4'
import layer as L
import stack as S
import vintage as V
import parameters as prm

""" Models that have been constructed"""

def first(nx=5, nz=5):
    """
    First model tried, mainly for debugging
    :param nx, nz The model dimensions
    :return:
    """
    delliq = 10.0 / float(nx)
    delx = 1000 / float(nx)
    dg = 0.9 / float(nz)
    dz_burden = 5.0
    for ix in range(nx):
        liqlev = 5.0 + float(ix) * delliq
        rest = max(28.0 + 2.0 * dz_burden - liqlev, 0.0)
        delz = rest / float(nz-1)
        print ix, liqlev, rest, delz
        l = [L.Layer(prm.debolt, prm.BIT, prm.BIT, sg=0.0, dz=dz_burden)]       # Underburden
        l.append(L.Layer(prm.blueskyBIT, prm.BIT, prm.GAS, sg=0.0, dz=liqlev)) # liquid
        for iz in range(nz-1):
            l.append(L.Layer(prm.blueskyBIT, prm.BIT, prm.GAS, sg=float(iz + 1)*dg, dz=delz))
        l.append(L.Layer(prm.wilrich, prm.BIT, prm.BIT, sg=0.0, dz=dz_burden))  # Overburden

        s = S.Stack(l[0], dx=delx)
        for lay in l[1:]:
            s.append(lay)
        if (ix == 0):
            v = V.Vintage(s, 0)
        else:
            v.append(s)
    return v
