#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import sqrt

def friedman_func(y, a, omega):
    return [-1/sqrt(omega/a + (1-omega)*a**2), y[0]/a]

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="integrate and plot the Friedman equations")
    parser.add_argument('-o', '--omega', dest='omega', action='store', type=float, default=1., help="the omega parameter")
    parser.add_argument('-t', '--time', dest='time', action='store', type=float, default=1., help="initial time")
    parser.add_argument('-r', '--radius', dest='radius', action='store', type=float, default=1., help="initial radius")
    args = parser.parse_args()
    

    from scipy import arange
    from scipy.integrate import odeint
    from matplotlib.pyplot import plot, show, figure

    a = arange(0.1, 1.0, 0.001)
    y = odeint(friedman_func, [args.time, args.radius], a, (args.omega,))

    figure = figure()
    subp = figure.add_subplot(2,1,1)
    subp.plot(a, y[:,0])
    subp = figure.add_subplot(2,1,2)
    subp.plot(a, y[:,1])
    show()

