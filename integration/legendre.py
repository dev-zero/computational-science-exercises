#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from fivepoint import fivepoint
from numpy import array, eye, dot, polyval, arange
from fractions import Fraction

def eval_poly(c, x):
    ''' evaluate the polynom with given coefficients [c0, c1, ... , cN]
        at position x'''
    # instead we could write: polyval(reversed(c), x)
    return reduce(lambda c1, c2: c1*x + c2, reversed(c))

N=10
shift_op = eye(N, k=-1)

p=[]
norm_factor=[1.]*N

for i in xrange(N):
    poly = [0.]*N
    poly[i] = 1.
    p.append(array(poly))

# generate the Legendre polynoms
for k in xrange(2,N):
    B = 100
    # this is the recursive relation for Gram-Schmidt
    c0 = fivepoint(lambda x: x*eval_poly(p[k-1],x)*eval_poly(p[k-1],x), -1., 1., B) / fivepoint(lambda x: eval_poly(p[k-1],x)*eval_poly(p[k-1],x), -1., 1., B)
    c1 = fivepoint(lambda x: eval_poly(p[k-1],x)*eval_poly(p[k-1],x), -1., 1., B) / fivepoint(lambda x: eval_poly(p[k-2],x)*eval_poly(p[k-2],x), -1., 1., B)
    p[k] = dot(shift_op,p[k-1])-c0*p[k-1] - c1*p[k-2]
    norm_factor[k] = eval_poly(p[k],1.)

from matplotlib.pyplot import plot, show

x = arange(-1., 1., 0.01)

for i in xrange(N):
    plot(x, [eval_poly(p[i] / norm_factor[i], x_j) for x_j in x])

show()

