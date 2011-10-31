#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

class Cyclotron:
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
        ''' p_x' = p_y - x - alpha*cos(omega*t)'''
        return self.py - self.x - self.alpha*cos(self.omega*self.t)

    def pydot(self):
        ''' p_y' = - p_x - y '''
        return -self.px - self.y

    def xdot(self):
        ''' x' = p_x + y'''
        return self.px + self.y

    def ydot(self):
        ''' y' = p_y - x '''
        return self.py - self.x

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
