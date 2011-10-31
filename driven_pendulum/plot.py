#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from driven_pendulum import DrivenPendulum
from numpy import pi
from numpy.random import randn
from matplotlib.pyplot import plot, show

pendulum = DrivenPendulum()

samples = 1
npoints = 100
gridsize = 10

#for p in randn(samples, 1):
#    print "calculating sample for p=", p
p = randn()
pendulum.setInitialConditions(0., 0., 1., p, 0.025, 1., 0.025)
x = [0.]*npoints
y = [0.]*npoints
for i in xrange(npoints):
    for j in xrange(gridsize):
        pendulum.evolve(2.*pi/gridsize)
    x[i], y[i] = pendulum.getPhaseSpacePoint()
plot(x, y)
show()
