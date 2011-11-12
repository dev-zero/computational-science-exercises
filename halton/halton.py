#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def intToHalton(i, b = 2):
    h = 0
    frac = 1./b
    while i > 0:
        d = i % b
        h += d*frac
        i = (i-d)//b
        frac /= b
    return h

def intSeqToHalton(i, b = 2):
    return map(lambda f: intToHalton(f, b), i)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="generate and plot Halton sequence")
    parser.add_argument('-s', '--start', dest='start', metavar='N', action='store', type=int, default=0, help="start from N when generating the sequence")
    parser.add_argument('-n', '--numbers', dest='numbers', metavar='N', action='store', type=int, default=512, help="generate N numbers")
    parser.add_argument('-x', '--xbase', dest='xbase', metavar='N', action='store', type=int, default=2, help="use N as base for the numbers on the x-axis")
    parser.add_argument('-y', '--ybase', dest='ybase', metavar='N', action='store', type=int, default=3, help="use N as base for the numbers on the y-axis")
    parser.add_argument('-r', '--random', dest='random', action='store_const', default=False, const=True, help="generate an equal number of random numbers (using /dev/urandom) and plot in a subplot")
    args = parser.parse_args()

    i = range(args.start, args.start+args.numbers)

    from matplotlib.pyplot import scatter, show, figure
    fig = figure()
    ax = fig.add_subplot(2 if args.random else 1, 1, 1)
    ax.set_title("Halton sequences for [{},{}) using bases {} and {}".format(args.start, args.start+args.numbers, args.xbase, args.ybase))
    scatter(intSeqToHalton(i, args.xbase), intSeqToHalton(i, args.ybase))

    if args.random:
        from random import SystemRandom
        s = SystemRandom()
        ax = fig.add_subplot(2, 1, 2)
        ax.set_title("{} random number pairs generated using /dev/urandom".format(args.numbers))
        scatter(map(lambda i: s.uniform(0.,1.), i), map(lambda i: s.uniform(0.,1.), i))

    show()
