__author__ = 'peterwills'

import pylab as plt
import matplotlib as mp
import sys

import Model31lib as M
import layer as L
import stack as S
import vintage as V
import parameters as prm
import models as mod

v = mod.first( nx=20, nz=10)
v.qc(prop='vp')
sys.exit()


#
# N = 10
# dg = 0.9 / float(N)
# delz = 23.0 / float(N)
# l = [L.Layer(prm.blueskyBIT, prm.BIT, prm.GAS, sg=0.0, dz=5.0)]
# for i in range(N-1):
#     l.append(L.Layer(prm.blueskyBIT, prm.BIT, prm.GAS, sg=float(i+1)*dg, dz=delz))
#
# s = S.Stack(l[0], dx=20.0)
# for lay in l[1:]:
#     s.append(lay)
# s.display()
# s.qc()
# sys.exit()


# Irreducible bitumen in sandstone and mix the fluids necessary
bcut = 0.2
mixGAS = M.fmix('mixGAS', [GAS, BIT], [1.0-bcut, bcut])
print mixGAS
print H2O
mixH2O = M.fmix('mixH2O', [H2O, BIT], [1.0 - bcut, bcut])
print mixH2O


blueskyH2O = M.gassman('blH2O', blueskyBIT, BIT, mixH2O, color='b')
blueskyGAS = M.gassman('blGAS', blueskyBIT, BIT, mixGAS, color='g')

# Test the gas substitution
M.testgas(GAS, H2O, blueskyH2O)

# Get synthetic TV pairs
# From the data: Calibration points area in polygons
InjTS = (0.35*(44000-22300) + 0.78*(22300-4451) + 1.1*(4451-2995) + 1.35*(2995-242) + 1.6*242)/44000
# InjTS = (0.78*(22300-4451) + 1.1*(4451-2995) + 1.35*(2995-242) + 1.6*(242))/40000
print 'InjTS: ', InjTS

# Or use 1 number
# InjTS = [[0.35, 44515], [0.78,22298],[1.1,4451],[1.35,2995],[1.6,242]]
# InjTS = 0.35
InjVol = 39100 * 1.25 - 22270*0.95      # Allow 25% thermal expansion injector and 5% producer
InjData = {'TS': InjTS,  'Vol': InjVol}  # injection minus production
ProdData = {'TS': [0.7], 'Vol': [23430/0.95]}   # we see a bigger volume at surface for 100C
M.createTVpair(prm.TVpath, blueskyH2O, GAS, H2O, Sg=[0.0, 0.6], A=23000, t='blowdown', data=ProdData, col='r')
M.createTVpair(prm.TVpath, blueskyH2O, GAS, H2O, Sg=[0.0, 0.80], A=44000, t='Injection', data=InjData, col='b')
plt.show()
sys.exit()

virgin = M.reservoir([[wilrich, 2], [blueskyBIT, 28.0], [debolt, 2.0]], prm.DIGI)
# Blowdown before seis movie
BDBEF = M.reservoir([[wilrich, 2], [blueskyGAS, 12.0], [blueskyBIT, 16.0], [debolt, 2.0]], prm.DIGI)
# Blowdown after seis movie
BDAFT = M.reservoir([[wilrich, 2], [blueskyGAS, 24.0], [blueskyBIT, 4.0], [debolt, 2.0]], prm.DIGI)
# Top flood
HSDUPPER = M.reservoir([[wilrich, 2], [blueskyH2O, 18.0], [blueskyGAS, 8.0], [blueskyBIT, 2.0],
                        [debolt, 2.0]], prm.DIGI)
# Base flood
HSDLOWER = M.reservoir([[wilrich, 2], [blueskyH2O, 26.0], [blueskyBIT, 2.0], [debolt, 2.0]], prm.DIGI)
reservoirs = [virgin, BDBEF, BDAFT, HSDUPPER, HSDLOWER]

# Positive NDRMS means baseline is bigger that monitor. This is hardening.
# Positive timeshift means baseline time is bigger than monitor time...means a speedup
rmstop, rmsbase, timeshift, ndrmstop, ndrmsbase = [], [], [], [], []
rmstop_base = virgin['rmstop']
rmsbase_base = virgin['rmsbase']
tt_base = virgin['tt']

for r in reservoirs:
    rmstop.append(r['rmstop'])
    rmsbase.append(r['rmsbase'])
    ndrmstop.append(2.0*(rmstop_base - r['rmstop'])/(rmstop_base + r['rmstop']))
    ndrmsbase.append(2.0*(rmsbase_base - r['rmsbase'])/(rmsbase_base + r['rmsbase']))
    timeshift.append(prm.DIGI*(tt_base - r['tt']))
labels = ['virgin', 'BD BEF SM', 'BD AFT SM', 'HSD UPPER', 'HSD LOWER']

# RMSPlot
# plt.figure(1)
# ax0 = plt.subplot(1,1,1)
# ax0_t = ax0.twinx()
# x = range(len(rmstop))
# ax0.plot(x, rmstop, 'ko-', label='RMS Top Reservoir')
# ax0.plot(x, rmsbase, 'ro-', label='RMS Base Reservoir')
# ax0_t.plot(x, timeshift, 'go-', label='Time in Reservoir')
# plt.xticks(x, labels, rotation='vertical')
# ax0.plot(0, 0, 'g-', label = 'Time in Reservoir')
# ax0.legend(loc='left')
# plt.title('RMS with fluid cut:' + str(bcut))

# NDSRMSPlot
plt.figure(2)
ax1 = plt.subplot(1, 1, 1)
ax1_t = ax1.twinx()
x = range(len(rmstop))
ax1.plot(x, ndrmstop, 'ko-', label='NDRMS Top Reservoir')
ax1.plot(x, ndrmsbase, 'ro-', label='NDRMS Base Reservoir')
ax1_t.plot(x, timeshift, 'go-', label='Time in Reservoir')
plt.xticks(x, labels, rotation='vertical')
ax1.plot(0, 0, 'g-', label='Time in Reservoir')
ax1.grid()
plt.title('NDRMS')
ax1.legend(loc='upper left')

# Trace plots
xlim = 0.08
y0 = int(100/prm.DIGI)
y1 = int(250/prm.DIGI)
y = range(y0, y1)
fig = plt.figure(3)
ax = plt.subplot(251)
plt.plot(virgin['trace'][y0:y1], y, 'r-')
plt.plot([-xlim, xlim], virgin['basegate'][0], 'b-')
plt.plot([-xlim, xlim], virgin['basegate'][1], 'b-')
plt.plot([-xlim, xlim], virgin['topgate'][0], 'g-')
plt.plot([-xlim, xlim], virgin['topgate'][1], 'g-')
ax.set_ylim(ax.get_ylim()[::-1])
plt.ylabel('time(ms)')
plt.title('virgin', fontsize=12)
plt.xticks(rotation=30, fontsize=8)
plt.xlim([-xlim, xlim])
plt.grid()

plt.subplot(252, sharex=ax, sharey=ax)
plt.plot(BDBEF['trace'][y0:y1], y, 'r-')
plt.plot([-xlim, xlim], BDBEF['basegate'][0], 'b-')
plt.plot([-xlim, xlim], BDBEF['basegate'][1], 'b-')
plt.plot([-xlim, xlim], BDBEF['topgate'][0], 'g-')
plt.plot([-xlim, xlim], BDBEF['topgate'][1], 'g-')
plt.title('BD Bef SM', fontsize=12)
plt.xticks(rotation=30, fontsize=8)
plt.xlim([-xlim, xlim])
plt.grid()

plt.subplot(253, sharex=ax, sharey=ax)
plt.plot(BDAFT['trace'][y0:y1], y, 'r-')
plt.plot([-xlim, xlim], BDAFT['basegate'][0], 'b-')
plt.plot([-xlim, xlim], BDAFT['basegate'][1], 'b-')
plt.plot([-xlim, xlim], BDAFT['topgate'][0], 'g-')
plt.plot([-xlim, xlim], BDAFT['topgate'][1], 'g-')
plt.title('BD Aft SM', fontsize=12)
plt.xticks(rotation=30, fontsize=8)
plt.xlim([-xlim, xlim])
plt.grid()

plt.subplot(254, sharex=ax, sharey=ax)
plt.plot(HSDUPPER['trace'][y0:y1], y, 'r-')
plt.plot([-xlim, xlim], HSDUPPER['basegate'][0], 'b-')
plt.plot([-xlim, xlim], HSDUPPER['basegate'][1], 'b-')
plt.plot([-xlim, xlim], HSDUPPER['topgate'][0], 'g-')
plt.plot([-xlim, xlim], HSDUPPER['topgate'][1], 'g-')
plt.title('HSD_UPPER', fontsize=12)
plt.xticks(rotation=30, fontsize=8)
plt.xlim([-xlim, xlim])
plt.grid()

plt.subplot(255, sharex=ax, sharey=ax)
plt.plot(HSDLOWER['trace'][y0:y1], y, 'r-')
plt.plot([-xlim, xlim], HSDLOWER['basegate'][0], 'b-')
plt.plot([-xlim, xlim], HSDLOWER['basegate'][1], 'b-')
plt.plot([-xlim, xlim], HSDLOWER['topgate'][0], 'g-')
plt.plot([-xlim, xlim], HSDLOWER['topgate'][1], 'g-')
plt.title('HSD_LOWER', fontsize=12)
plt.xticks(rotation=30, fontsize=8)
plt.xlim([-xlim, xlim])
plt.grid()

pltnum = 6
left = (1.0 - bcut) * 20
right = bcut * 20
for (k, r) in enumerate(reservoirs):
    lower = r['totthick']
    ax9 = fig.add_subplot(2, 5, pltnum)
    for (i, layer) in enumerate(r['thick']):
        lower -= layer
        rect = mp.patches.Rectangle((0, lower), left, layer, color=r['color'][i], ec='y')
        ax9.add_patch(rect)
    rect = mp.patches.Rectangle((left, 0), right, r['totthick'], color='k', ec='y')  # bitumen irreducible
    ax9.add_patch(rect)
    plt.xlim([0, 20])
    lim = r['totthick']
    plt.ylim([0, lim])
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    pltnum += 1


plt.show()

sys.exit()
