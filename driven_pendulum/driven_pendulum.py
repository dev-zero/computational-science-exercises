#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import cos, sin, array

class DrivenPendulum:
    def setInitialConditions(self, q, t, vel, p, b, l, g):
        self.g = g
        self.b = b
        self.l = l
        self.alpha = g / l
        self.beta = b / l
        self.q = q
        self.Q = t
        self.p = p
        self.vel = vel
        self.P = 0

    def pdot(self):
        return self.alpha * sin(self.q) + self.beta * sin(self.q - self.vel*self.Q)
    def Pdot(self):
        return -self.beta * self.vel * sin(self.q - self.vel*self.Q)
    def qdot(self):
        return self.p
    def Qdot(self):
        return self.vel

    def evolve(self, dt):
        ''' leapfrog '''
        self.p += 0.5*dt*self.pdot()
        self.P += 0.5*dt*self.Pdot()

        self.q += self.qdot()*dt
        self.Q += self.Qdot()*dt

        self.p += 0.5*dt*self.pdot()
        self.P += 0.5*dt*self.Pdot()

    def getInnerPosition(self):
        return self.b * array([sin(self.Q), -cos(self.Q)])

    def getOuterPosition(self):
        return self.getInnerPosition() + self.l * array([sin(self.q), -cos(self.q)])

    def getPhaseSpacePoint(self):
        return (self.q, self.p)

    def hamiltonian(self):
        return 0.5*self.p**2 + self.P - self.alpha*cos(self.q) - self.beta*cos(self.q - self.Q)
