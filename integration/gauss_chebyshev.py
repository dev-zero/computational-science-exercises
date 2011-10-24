#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def gauss_chebyshev(f, M):
    from numpy import cos, pi
    from math import fsum
    return (pi/float(M))*fsum(map(lambda k: f(cos((float(k) + 0.5)*pi/float(M))), xrange(M)))

def func_prod(lhs, rhs, N):
    return gauss_chebyshev(lambda x: lhs(x)*rhs(x), N)
