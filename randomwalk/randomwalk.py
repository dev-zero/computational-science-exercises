#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def directionsGenerator(steps):
    ''' generate unity steps in random directions '''
    from random import SystemRandom
    from numpy import exp, pi
    s = SystemRandom()
    for i in xrange(steps):
        yield exp(s.random()*pi*2j)

def distanceProbability(r, N):
    ''' the distance probability distribution'''
    from numpy import exp
    return (2.*r/N) * exp(-r**2./N)

def endpointProbability(x, y, N):
    ''' the endpoint probability distribution '''
    from numpy import exp, pi
    return (1./(N*pi)) * exp(-(x**2 + y**2)/N)

def endpointProbabilitySingleCoord(x, N):
    ''' simply the endpoint probability distribution integrated
        over one coordinate from -inf to inf'''
    from numpy import exp, pi, sqrt
    return (1./(sqrt(N*pi))) * exp(-x**2/N)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="generate and plot random walks")
    parser.add_argument('-s', '--steps', dest='steps', metavar='N', action='store', type=int, default=50, help="number of steps in one random walk")
    parser.add_argument('-c', '--count', dest='count', metavar='N', action='store', type=int, default=10**4, help="number of random walks")
    parser.add_argument('-b', '--bins', dest='bins', metavar='N', action='store', type=int, default=100, help="number of bins in the histograms")
    args = parser.parse_args()

    # generate the random walks
    coords = [sum(directionsGenerator(args.steps)) for c in xrange(args.count)]

    from pylab import hist, plot, show, figure, xlabel, ylabel
    from numpy import abs, real, imag, sqrt, arange, vectorize

    fig = figure()

    # the absolute value (aqa 'distance')
    ax = fig.add_subplot(311)
    n, bins, patches = hist(abs(coords), args.bins, normed=True, histtype='step')
    r = arange(0, bins[-1], 0.1)
    plot(r, distanceProbability(r, args.steps))
    xlabel("distance")
    ylabel("probability")

    # the x-coordinate
    ax = fig.add_subplot(312)
    n, bins, patches = hist(real(coords), args.bins, normed=True, histtype='step')
    x = arange(bins[0], bins[-1], 0.1)
    plot(x, endpointProbabilitySingleCoord(x, args.steps))
    xlabel("x-coordinate")
    ylabel("probability")

    # the y-coordinate
    ax = fig.add_subplot(313)
    n, bins, patches = hist(imag(coords), args.bins, normed=True, histtype='step')
    y = arange(bins[0], bins[-1], 0.1)
    plot(y, endpointProbabilitySingleCoord(y, args.steps))
    xlabel("y-coordinate")
    ylabel("probability")

    show()
