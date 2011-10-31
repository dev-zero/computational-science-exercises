#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

class Blackhole:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.px = 0.
        self.py = 1.

    def setInitialConditions(self, x, y, px, py):
        self.x = x
        self.y = y
        self.px = px
        self.py = py

    def r(self):
        return pow(self.x**2 + self.y**2, 0.5)

    def r3(self):
        return pow(self.x**2 + self.y**2, -1.5)

    def pcdot(self, a, b):
        return (-a*pow(1.-2./self.r(), -2) + (2*(self.x*self.px + self.y*self.py)*b - 3*a*(self.x*self.px + self.y*self.py)**2/self.r()**2))*self.r3()

    def pxdot(self):
        return self.pcdot(self.x, self.px)

    def pydot(self):
        return self.pcdot(self.y, self.py)

    def xdot(self):
        return self.px - 2.*(self.x*self.px + self.y*self.py)*self.x*self.r3()

    def ydot(self):
        return self.py - 2.*(self.x*self.px + self.y*self.py)*self.y*self.r3()

    def evolve(self, dt):
        ''' leapfrog integrator '''
        self.px += self.pxdot()*0.5*dt
        self.py += self.pydot()*0.5*dt

        self.x += self.xdot()*dt
        self.y += self.ydot()*dt

        self.px += self.pxdot()*0.5*dt
        self.py += self.pydot()*0.5*dt

    def getPosition(self):
        return (self.x, self.y)
