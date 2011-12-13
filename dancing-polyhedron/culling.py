#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import array
from numpy.linalg import solve

def pointInsidePolygon(polygon, point, camera):
    v0 = polygon[0]
    v1 = polygon[1]-polygon[0]
    v2 = polygon[2]-polygon[0]
    n = point - camera
    A = array([v1, v2, n]).transpose()
    try:
        a, b, c = solve(A, camera-v0)*array([1, 1, -1])
    except:
        return False

    # have to use something smaller than 1. due to floating point errors
    if a > 0 and a < .9999999 and b > 0 and b < .9999999 and c > 0 and c < .9999999:
        return True
    return False

if __name__ == '__main__':
    polygon = array([[1, -1, -1], [1, 1, -1], [1, 0, 1]])
    camera = array([0, 0, 0])
    print pointInsidePolygon(polygon, array([2, 0, 0]), camera)
    print pointInsidePolygon(polygon, array([2, 10, 0]), camera)
