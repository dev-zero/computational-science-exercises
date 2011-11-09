#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from scipy.integrate import ode
from numpy import array, linspace, append
from mayavi import mlab

def lorenz(t, c, sigma, r, b):
    return array([sigma*(c[1]-c[0]), c[0]*(r - c[2])-c[1], c[0]*c[1] - b*c[2]])

c0 = array([0., 1., 0.])
params = (10., 28., 8./3.)
t = linspace(0., 100., 5000)

o = ode(lorenz)
values = array([c0])
s = mlab.plot3d(values[:,0], values[:,1], values[:,2], color=(1,1,1))
ms = s.mlab_source

@mlab.animate(delay=10, ui=False)
def generateLorenz():
    global values, ms

    f = mlab.gcf()
    mlab.view(distance=200)

    while True:
        values = array([c0])
        o.set_initial_value(c0, 0.).set_f_params(params[0], params[1], params[2])
        ms.reset(color=(0.5,0.5,0.5))
        i = 0
        print "generating a new one"
        while o.successful() and o.t < 100.:
            o.integrate(o.t+0.02)
            values = append(values, [o.y], axis=0)
            if i % 10 == 0:
                ms.reset(x=values[:,0], y=values[:,1], z=values[:,2])
                yield
            i += 1

g = generateLorenz()
mlab.show()
