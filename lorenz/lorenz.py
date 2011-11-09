#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from scipy.integrate import odeint
from numpy import array, linspace

def lorenz(c, t, sigma, r, b):
    return array([sigma*(c[1]-c[0]), c[0]*(r - c[2])-c[1], c[0]*c[1] - b*c[2]])

c0 = array([0., 1., 0.])
params = (10., 28., 8./3.)
t = linspace(0., 100., 5000)

values = odeint(lorenz, c0, t, args=params)

from mayavi.mlab import plot3d, show
l = plot3d(values[:,0], values[:,1], values[:,2], color=(1,1,1))
show()

