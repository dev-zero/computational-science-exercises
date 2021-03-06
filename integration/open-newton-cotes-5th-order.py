#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import zeros
from scipy.linalg import solve
from fractions import Fraction

A = zeros((3,3))
b = zeros(3)

for p in [0, 2, 4]:
    for x in [-4, -2, 0, 2, 4]:
        A[p//2][abs(x)//2] += pow(x, p)*(p+1)
    b[p//2] = 2*pow(5, p+1)

x = solve(A,b)

print "coefficients:", x
print "coefficients (converted to fractions):", [str(Fraction(x_i).limit_denominator(1000000)) for x_i in x]
print "coefficients calculated by hand: [ 335/96, 125/144, 1375/576 ]"

