#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def rk4th(f, x, y, h):
    f1 = f(x,         y)
    f2 = f(x + 0.5*h, y + 0.5*h*f1)
    f3 = f(x + 0.5*h, y + 0.5*h*f2)
    f4 = f(x +     h, y *     h*f3)
    return h*(f1 + 2.*f2 + 2.*f3 + f4)/6.

