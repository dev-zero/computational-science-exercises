#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from fractions import Fraction

coefficients = [ Fraction(335,96), Fraction(125,144), Fraction(1375,576)]

def fivepoint(f, a, b, B = 1):
    ''' 5-point open-type Newton-Cotes integration with non-equidistant
        points of support at [-5, -4, -2, 0, 2, 4, 5] where the boundary
        points -5, 5 are ignored because of the open type '''
        
    def phi(t):
        ''' the interval transformation -5..5 -> a..b '''
        return a + 0.1*(float(t)+5.)*(b-a)

    if B > 1:
        return sum(map(lambda i: fivepoint(f, a+i*(b-a)/float(B), a+(i+1)*(b-a)/float(B)), xrange(B)))

    return sum(map(lambda x: coefficients[abs(x)//2]*f(phi(float(x))), [-4, -2, 0, 2, 4]))*(b-a)*0.1

def func_prod(lhs, rhs, weightf=lambda x: 1., B=100, i=(-1.,1.)):
    from fivepoint import fivepoint
    return fivepoint(lambda x: lhs(x)*rhs(x)*weightf(x), i[0], i[1], B)

def gaussian_error_function_part_normalized(t):
    ''' this is the gaussian error function function part
        normalized to the range 0..1 (instead of -inf..inf)
        using the chainrule for the transformation t -> 1/(1-t) - 1 '''
    from math import exp
    return exp(-(1./(1.-t) -1.)*(1./(1.-t) -1.))/((1-t)*(1-t))

if __name__ == '__main__':
    from numpy import pi, sqrt
    print "int(exp(-x^2)) from -inf..inf =", 2.*fivepoint(gaussian_error_function_part_normalized, 0., 1., 100)
    print "sqrt(pi) =", sqrt(pi)
