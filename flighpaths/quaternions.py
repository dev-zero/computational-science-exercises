#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import dot, array, cross, append, cos, sin, arccos
from numpy.linalg import norm

def quatFromVectorAngle(v, phi):
    w = v/norm(v)
    return append(cos(.5*phi), sin(.5*phi)*w)

def product(x, y):
    return append(x[0]*y[0]-dot(x[1:4], y[1:4]), x[0]*y[1:4]+y[0]*x[1:4]-cross(x[1:4], y[1:4]))

def conj(x):
    return append(x[0], -x[1:])

def inverse(x):
    return conj(x)/norm(x)

def rotateVectorByQuat(v, q):
    return product(q, product(append(0, v), inverse(q)))[1:]

def quatFromVector(v):
    return append(0, v)

def slerp(q0, q1, t):
    theta = arccos(dot(q0, q1))
    return (q0*sin(theta*(1.-t)) + q1*sin(theta*t))/sin(theta)


if __name__ == '__main__':
    import unittest
    from numpy import array_equal, pi, allclose, copy
    from numpy.linalg import norm
    from random import random, randint

    class TestQuaternions(unittest.TestCase):
        def test_quaternion(self):
            q0 = array([1, 0, 0, 0])
            q1 = array([0, 1, 0, 0])
            self.assertFalse(array_equal(q0, q1))

        def test_product(self):
            q0 = array([1, 0, 0, 0])
            q1 = array([0, 1, 0, 0])
            self.assertTrue(array_equal(product(q0, q1), q1))

        def test_conj(self):
            q0 = array([1, 0, 0, 0])
            self.assertTrue(array_equal(conj(q0), q0))

        def test_inverse(self):
            q0 = array([1, 0, 0, 0])
            self.assertTrue(array_equal(inverse(q0), q0))

        def test_quatFromVectorAngle(self):
            # 0-rotation around arbitary axis should be 0
            self.assertTrue(array_equal(quatFromVectorAngle(array([random(), random(), random()]), 0.), array([1,0,0,0])))
            # rotation of pi around x-axis
            self.assertTrue(allclose(quatFromVectorAngle(array([1,0,0]), pi), array([0,1,0,0])))
        def test_quatFromVectorAngleVectorIsModifiedBug(self):
            v = array([randint(-100,100), randint(-100,100), randint(-100,100)])
            w = copy(v) # need an explicit copy here, otherwise it is a reference
            phi = random()
            q = quatFromVectorAngle(v, phi)
            self.assertTrue(array_equal(v, w))

        def test_quatFromVector(self):
            self.assertTrue(array_equal(quatFromVector(array([1,2,3])), array([0,1,2,3])))

        def test_slerp(self):
            s = array([0,1,0,0])
            e = array([0,0,1,0])
            self.assertTrue(array_equal(slerp(s, e, 0), array([0,1,0,0])))
            self.assertTrue(array_equal(slerp(s, e, 1), array([0,0,1,0])))
        def test_rotateVectorByQuat(self):
            v = array([randint(-100, 100), randint(-100, 100), randint(-100, 100)])
            self.assertTrue(array_equal(rotateVectorByQuat(v, array([1,0,0,0])), v)) # 1-quaternion shouldn't touch a random vector
            self.assertTrue(array_equal(rotateVectorByQuat(v, array([0,1,0,0])), array([v[0], -v[1], -v[2]]))) # rotation by pi around x-axis
            self.assertTrue(array_equal(rotateVectorByQuat(v, array([0,0,1,0])), array([-v[0], v[1], -v[2]]))) # rotation by pi around y-axis

            q = quatFromVectorAngle(array([random(), random(), random()]), 2.*pi*random()) # random rotation
            self.assertTrue(allclose(norm(rotateVectorByQuat(v, q)), norm(v))) # ... should leave the norm of the vector unchanged

    unittest.main()
