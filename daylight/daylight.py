#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

SPY = 31556952 # seconds per year
EQN = 1300708800 # the time of the equinox [s] (Epoch)
I = 0.409105 # Earth's inclination [rad]

def angles2coords(l, s, I, d):
    from numpy import sin, cos, array, dot
    direction   = array([[cos(d), sin(d), 0], [-sin(d), cos(d),      0], [0,       0,      1]])
    inclination = array([[     1,      0, 0], [      0, cos(I), sin(I)], [0, -sin(I), cos(I)]])
    vector      = array([cos(l)*cos(s), cos(l)*sin(s), sin(l)])
    return dot(direction, dot(inclination, vector))

if __name__ == '__main__':
    from time import time
    from argparse import ArgumentParser
    parser = ArgumentParser(description="calculate and plot daylight maps")
    parser.add_argument('-s', '--gridsize', dest='gridsize', metavar='N', action='store', type=int, default=100, help="the grid size for both Langitude and Longitude (default: %(default)s)")
    parser.add_argument('time', nargs='?', default=int(time()), metavar='time', action='store', help="The time provided either as a timestamp (YYYYMMDDHHSS) or as a value in seconds since 1.1.1970 (Epoch).")
    args = parser.parse_args()

    t = 0
    if type(args.time) == int: # the default value was used
        t = args.time
    else:
        try:
            from dateutil import parser
            d = parser.parse(args.time)
        except ImportError:
            print "python-dateutils is not installed, interpreting {} as seconds (Epoch)".format(args.time)
        except ValueError:
            t = int(args.time)
        else:
            t = int(d.strftime('%s'))

    from numpy import pi, linspace, zeros, array, arange

    l = linspace(-0.5*pi, 0.5*pi, args.gridsize)
    s = linspace(-pi, pi, args.gridsize)

    t -= EQN
    d = t*2.*pi/SPY
    s = s + d + (t/(24*3600.))*2.*pi

    x = zeros( (args.gridsize, args.gridsize) )
    for i in xrange(args.gridsize):
        for j in xrange(args.gridsize):
            x[i,j] = angles2coords(l[i], s[j], I, d)[0]

    from matplotlib.pyplot import contour, show, plot, annotate, xlabel, ylabel
    contour(linspace(-180, 180, args.gridsize), linspace(-90, 90, args.gridsize), x, arange(.0, 1.0, .1))
    xlabel("Longitude")
    ylabel("Latitude")
    xy = (8.799, 47.445)
    plot(xy[0], xy[1], 'o')
    annotate("Rikon im Toesstal", xy)
    show()
