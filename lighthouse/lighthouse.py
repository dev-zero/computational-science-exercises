#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from random import SystemRandom
from numpy import pi, arange, tan, arctan, exp, log, real, imag, prod

r = SystemRandom()

def randomX(a, b, s):
    xs = []
    while s > 0:
        x = a + b*tan(r.random()*2.*pi)
        if abs(x) > 1:
            continue
        else:
            s -= 1
            xs.append(x)
    return xs

def P(x, ab):
    def p(x, a, b):
        den = ((a**2 - 2*a*x + b**2 + x**2)*(arctan((1.-a)/b) + arctan((1.+a)/b)))
        if den == 0.:
            return 0.
        return b/den
    return prod(map(lambda x_i: p(x_i, ab.real, ab.imag), x))

def metropolisWalk(x, ab, s):
    p = P(x, ab)

    i = 0
    while True:
        d = r.random()*exp(r.random()*pi*2j)
        new_p = P(x, ab+d)
        if r.random() < (new_p/p):
            ab += d
            p = new_p
        i += 1

        # break if we have at least s steps and the current solution was 100% acceptable
        if (i > s) and new_p/p >= 1.:
            break

    return ab

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="generate random coordinates for the lighthouse problem and find the original a,b parameters by using the Metropolis(-Hastings) algorithm")
    parser.add_argument('-a', dest='a', metavar='x', action='store', type=float, default=-0.5, help="x-coordinate of the lighthouse (default: %(default)s)")
    parser.add_argument('-b', dest='b', metavar='y', action='store', type=float, default=0.7, help="y-coordinate of the lighthouse (default: %(default)s)")
    parser.add_argument('-s', '--samples', metavar='N', dest='samples', action='store', type=int, default=100, help="the number of measurement samples to generate (default: %(default)s)")
    parser.add_argument('-m', '--minsteps', metavar='N', dest='minsteps', action='store', type=int, default=100, help="the minimal number of steps in each of the random-walks in the Metropolis algorithm (default: %(default)s)")
    parser.add_argument('-w', '--walks', metavar='N', dest='walks', action='store', type=int, default=100, help="the number of random walks in the Metropolis algorithm (default: %(default)s)")
    args = parser.parse_args()

    # generate random x
    x = randomX(args.a, args.b, args.samples)

    ab_s = map(lambda ab: metropolisWalk(x, ab, args.minsteps), [1j]*args.walks)

    from matplotlib.pyplot import hist, show, figure

    figure = figure()
    subp = figure.add_subplot(311)
    subp.hist(x, histtype='step', bins=40)
    subp.set_xlabel("simulated measurements")
    subp = figure.add_subplot(312)
    subp.hist(real(ab_s), histtype='step', bins=40)
    subp.axvline(x=args.a, color='g', linewidth=2)
    subp.set_xlabel("recovered x-coordinate of the lighthouse")
    subp = figure.add_subplot(313) 
    subp.hist(imag(ab_s), histtype='step', bins=40)
    subp.axvline(x=args.b, color='g', linewidth=2)
    subp.set_xlabel("recovered y-coordinate of the lighthouse")

    show()

