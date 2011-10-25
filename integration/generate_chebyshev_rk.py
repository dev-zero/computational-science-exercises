#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def calculate_chebyshev(x, N):
    ''' calculate Chebyshev values for P_N '''

    from numpy import cos, sin, pi, array
    from rk import rk4th

    y = [0.]*len(x)
    z = [0.]*len(x)
    n = float(N)

    y[0] = cos(n*pi*0.5)
    z[0] = n*sin(n*pi*0.5)

    f_1 = lambda x, y: y[1]
    f_2 = lambda x, y: (x*y[1] - y[0]*n**2)/(1-x**2)

    for i in xrange(1, len(x)):
        h = x[i]-x[i-1]

        y[i] = y[i-1] + rk4th(f_1, x[i-1], array([y[i-1], z[i-1]]), h)
        z[i] = z[i-1] + rk4th(f_2, x[i-1], array([y[i-1], z[i-1]]), h)

    return y

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="calculate and plot the Chebyshev polynom values by using a Runge-Kutta 4th-order integrator")
    parser.add_argument('N', metavar='N', type=int, nargs=1, help="the number of polynomes to generate")
    parser.add_argument('-s', '--step', dest='step', type=float, default=0.001, help="The step size for the integrator (default: 0.001)")
    args = parser.parse_args()

    N = args.N[0]

    from matplotlib.pyplot import plot, show
    from numpy import arange

    x = arange(0., 1., args.step)

    for i in xrange(N):
        plot(x, calculate_chebyshev(x, i))
    show()

