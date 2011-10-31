#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

class RelativisticCyclotron:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.px = 0.
        self.py = 1.
        self.omega = 0.
        self.alpha = 0.
        self.t = 0.

    def setInitialConditions(self, x, y, px, py, alpha, omega):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.alpha = alpha
        self.omega = omega
        self.t = 0.

    def pxdot(self):
        from numpy import cos
        return (self.py - self.x)*self.commonFactor() - self.alpha*cos(self.omega*self.t)

    def pydot(self):
        return (-self.px - self.y)*self.commonFactor()

    def xdot(self):
        return (self.px + self.y)*self.commonFactor()

    def ydot(self):
        return (self.py - self.x)*self.commonFactor()

    def commonFactor(self):
        return pow(1 + (self.px + self.y)**2 + (self.py - self.x)**2, -0.5)

    def evolve(self, dt):
        ''' leapfrog integrator '''
        self.px += self.pxdot()*0.5*dt
        self.py += self.pydot()*0.5*dt

        self.x += self.xdot()*dt
        self.y += self.ydot()*dt
        self.t += dt

        self.px += self.pxdot()*0.5*dt
        self.py += self.pydot()*0.5*dt

    def getPosition(self):
        return (self.x, self.y)
