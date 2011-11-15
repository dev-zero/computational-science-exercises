#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from schroedinger import Schroedinger1D

try:
    import gobject
    import matplotlib
    matplotlib.use('GTKAgg')
except:
    from sys import exit
    print("This app works only with GTK+ installed and matplotlib built with GTK+ support.")
    exit(1)

from pylab import plot, show, figure
from numpy import abs, real, imag, vectorize

# initialize the two simulations
s1 = Schroedinger1D(256, L=20)
s2 = Schroedinger1D(256, L=20)

# models the double well potential
def doubleWellPotential(x):
    sigma = 0.04
    pos = 2.

    if (x < pos) or (x > pos+sigma):
        return 0.
    return 10.

# use the double well potential in the second plot
s2.setPotential(vectorize(doubleWellPotential))

fig = figure()
ax = fig.add_subplot(211)
ax.set_title("Press 'space' to start/stop the simulation")
ax.set_ylim(-1.2, 1.2)

s1_l_amp,  = plot(s1.x(), abs(s1.f()), color='black')
s1_l_real, = plot(s1.x(), s1.f().real, color='red')
s1_l_imag, = plot(s1.x(), s1.f().imag, color='blue')
s1_l_pot   = plot(s1.x(), s1.V(), color='green')

ax = fig.add_subplot(212)
ax.set_ylim(-1.2, 1.2)

s2_l_amp,  = plot(s2.x(), abs(s2.f()), color='black')
s2_l_real, = plot(s2.x(), s2.f().real, color='red')
s2_l_imag, = plot(s2.x(), s2.f().imag, color='blue')
s2_l_pot   = plot(s2.x(), s2.V(), color='green')

runSimulation = False
i = 0

def update():
    global i
    i += 1
    s1.evolve(0.02)
    s2.evolve(0.02)
    s1_l_amp.set_ydata(abs(s1.f()))
    s1_l_real.set_ydata(real(s1.f()))
    s1_l_imag.set_ydata(imag(s1.f()))
    s2_l_amp.set_ydata(abs(s2.f()))
    s2_l_real.set_ydata(real(s2.f()))
    s2_l_imag.set_ydata(imag(s2.f()))
    fig.canvas.draw_idle()
    if not runSimulation:
        print "stopped simulation after {} iterations".format(i)
    return runSimulation # return False terminates this gobject-callback

def onpress(event):
    global runSimulation
    if event.key==' ':
        if runSimulation:
            print "stopping simulation"
            runSimulation = False
        else:
            print "starting simulation"
            runSimulation = True
            gobject.idle_add(update) # readding the gobject-callback function

fig.canvas.mpl_connect('key_press_event', onpress)
show()

