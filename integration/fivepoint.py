#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from fractions import Fraction
from math import exp

coefficients = [ Fraction('335/96'), Fraction('125/144'), Fraction('1375/576')]

def fivepoint(f, a, b, B = 1):
    def phi(t):
        return a + 0.1*(float(t)+5.)*(b-a)

    if B == 1:
        return sum(map(lambda x: coefficients[abs(x)//2]*f(phi(x)), [-4, -2, 0, 2, 4]))*(b-a)*0.1
    else:
        return sum([fivepoint(f, a+i*(b-a)/B, a+(i+1)*(b-a)/B) for i in range(B)])

def gaussian_error_function_part_normalized(t):
    ''' this is the gaussian error function function part
        normalized to the range 0..1 (instead of -inf..inf)'''
    return 2.*exp(-(1./(1.-t) -1.)*(1./(1.-t) -1.))/((1-t)*(1-t))
        
#print fivepoint(lambda x: cos(x), -3., 4., 200)

print fivepoint(gaussian_error_function_normalized, 0., 1., 10000)
