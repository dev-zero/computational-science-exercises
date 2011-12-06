#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import sqrt, arcsin, arctan2, sin, cos, max

def cartesian2spherical(x, y):
    u = sqrt(1. - x**2/16. - y**2/4.)
    return (arcsin(u*y), 2.*arctan2(u*x, 4*u**2 - 2.))

def spherical2cartesian(theta, phi):
    denom = sqrt(1.+cos(theta)*cos(.5*phi))
    return (2.*sqrt(2)*cos(theta)*sin(.5*phi)/denom, sqrt(2)*sin(theta)/denom)

if __name__ == '__main__':
    import unittest
    from numpy import array, allclose, linspace

    class TestHammerAitov(unittest.TestCase):
        def test_cartesian2spherical(self):
            self.assertEqual(cartesian2spherical(0, 0), (0,0))

        def test_spherical2cartesian(self):
            self.assertEqual(spherical2cartesian(0, 0), (0,0))

        def test_transformation(self):
            for x in linspace(-2*sqrt(2)+0.0001, 2*sqrt(2)-0.0001):
                for y in linspace(-sqrt(2)+0.0001, sqrt(2)-0.0001):
                    theta, phi = cartesian2spherical(x, y)
                    xp, yp = spherical2cartesian(theta, phi)
                    self.assertTrue(allclose(array((x, y)), array((xp, yp))))

    unittest.main()
