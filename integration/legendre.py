#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def eval_poly(c, x):
    ''' evaluate the polynom with given coefficients [c0, c1, ... , cN]
        at position x'''
    # instead we could write: polyval(reversed(c), x)
    return reduce(lambda c1, c2: c1*x + c2, reversed(c))

def generate_legendre(N):
    ''' generate Legendre polynom coefficients for P_n
        for n = 0..N'''

    from fivepoint import fivepoint
    from numpy import array, eye, dot

    # this is a lower diagonal matrix used to
    # multiply the polynoms by x which is a shift
    # of the coefficients to the rights
    shift_op = eye(N, k=-1)

    p=[]
    norm_factor=[1.]*N

    for i in xrange(N):
        poly = [0.]*N
        poly[i] = 1.
        p.append(array(poly))

    # generate the Legendre polynoms, P_0, P_1 are the monoms 1, x and we need them to start for the recursive relation
    for k in xrange(2, N):
        B = 100
        # this is the recursive relation for Gram-Schmidt
        c0 = fivepoint(lambda x: x*eval_poly(p[k-1],x)*eval_poly(p[k-1],x), -1., 1., B) / fivepoint(lambda x: eval_poly(p[k-1],x)*eval_poly(p[k-1],x), -1., 1., B)
        c1 = fivepoint(lambda x:   eval_poly(p[k-1],x)*eval_poly(p[k-1],x), -1., 1., B) / fivepoint(lambda x: eval_poly(p[k-2],x)*eval_poly(p[k-2],x), -1., 1., B)
        p[k] = dot(shift_op,p[k-1])-c0*p[k-1] - c1*p[k-2]
        norm_factor[k] = eval_poly(p[k],1.)

    # normalize
    for k in xrange(2, N):
        p[k] /= norm_factor[k]

    return p

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="calculate the Legendre polynom coefficients by using Gram-Schmidt and a 5-point open-type Newton-Cotes integrator")
    parser.add_argument('N', metavar='N', type=int, nargs=1, help="the number of polynomes to generate")
    parser.add_argument('-p', '--plot', dest='plot', action='store_const', const=True, default=False, help="plot the polynomes")
    args = parser.parse_args()

    N = args.N[0]
    p = generate_legendre(N)

    def monom_string(p, i):
        if p[i] == 0.0:
            return ''

        x = '*x^{}'
        if i == 0:
            x = ''

        return '{}{}'.format(p[i], x.format(i))

    def reduce_poly_string(l, r):
        if len(r) > 0:
            if len(l) > 0:
                return '{} + {}'.format(l, r)
            return r
        return l

    for i in xrange(N):
        print "P_{} = {}".format(i, reduce(reduce_poly_string, map(lambda j: monom_string(p[i], j), xrange(N))))

    if args.plot:
        from matplotlib.pyplot import plot, show
        from numpy import arange

        x = arange(-1., 1., 0.01)

        for i in xrange(N):
            plot(x, [eval_poly(p[i], x_j) for x_j in x])
        show()

