#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from sys import float_info

def arctan(x):
    k = 0
    while True:
        yield pow(-1, k) * pow(1./x, 2.*k+1) / (2.*k+1.)
        k += 1

arctan_1_5   = arctan(5.)
arctan_1_239 = arctan(239.)

l = next(arctan_1_5)
r = next(arctan_1_239)

pi_1_4 = 4.*l - r

while True:
    if abs(l) < float_info.min or abs(r) < float_info.min:
        break

    if abs(l) > abs(r):
        l = next(arctan_1_5)
        pi_1_4 += 4.*l
    else:
        r = next(arctan_1_239)
        pi_1_4 -= r

print("pi={:.52f}".format(4.*pi_1_4))
