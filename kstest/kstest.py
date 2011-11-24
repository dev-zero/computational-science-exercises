#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def randomWalk(N1, N2):
    from random import SystemRandom
    s = SystemRandom()
    positions = [0]
    n1 = 0
    n2 = 0
    # the steps are in units of 1/N1 * N1*N2, resp. 1/N2 * N1*N2 to make sure
    # we don't accumulate round-off errors in the summation
    while (n1 < N1 or n2 < N2):
        if s.random() >= 0.5:
            if n1 < N1:
                n1 += 1
                positions.append(positions[-1]+N2)
            # else:
            #     positions.append(positions[-1])
        else:
            if n2 < N2:
                n2 += 1
                positions.append(positions[-1]-N1)
            # else:
            #     positions.append(positions[-1])

    # returning to stepsize 1/N1, resp. 1/N2
    return [float(p)/(N1*N2) for p in positions]

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="generate random walks with maximal steps N1/N2, and plot the KS statistics for the maximal distance")
    parser.add_argument('-s', '--samples', dest='samples', metavar='N', action='store', type=int, default=1000, help="number of samples")
    parser.add_argument('-n', '--n1', dest='n1', metavar='N', action='store', type=int, default=24, help="total number of steps to the right")
    parser.add_argument('-m', '--n2', dest='n2', metavar='N', action='store', type=int, default=36, help="total number of steps to the left")
    parser.add_argument('-b', '--bins', dest='bins', metavar='N', action='store', type=int, default=100, help="number of bins in the histogram")
    args = parser.parse_args()

    distances = map(lambda r: max(abs(min(r)), max(r)), [randomWalk(args.n1, args.n2) for s in xrange(args.samples)])

    from matplotlib.pyplot import hist, show, xlabel
    hist(distances, cumulative=True, bins=args.bins, histtype='step', normed=True)
    xlabel('cumulative sum of the maximum distances giving the KS statistics of the two random walks')
    show()
