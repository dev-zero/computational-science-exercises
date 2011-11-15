#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import zeros, exp, concatenate, arange, pi, abs, sqrt, array
from scipy import fft, ifft

def harmonicPotential(x):
    return 0.5*x**2

def wavePacket(x, k_0):
    return exp(-0.5*x**2 + 1j*k_0*x)

class Schroedinger1D:
    ''' This class encapsulates the 1D schroedinger equation solver '''
    def __init__(self, N=256, L=10):
        self._N = N
        self._L = L
        self._F = zeros(N)

        self._dx = 2.*L/N
        self._dk = 2.*pi / (N*self._dx)

        self._x = (arange(N) - N/2) * self._dx
        # this is the grid in momentum space. Instead of realigning self._F after fft and before momentumEvolve, resp again
        # after momentumEvolve and before ifft I simply transform the grid itself (see example (6.7) in the lecture notes)
        k = (arange(N) - N/2)
        self._k = concatenate((k[self._N//2:], k[0:self._N//2])) * self._dk

        # a simple wave-package moving constantly to the right and starting at x=0
        self.setInitial(lambda x: wavePacket(x, 2.))

        # use the harmonic potential as default potential
        self._V = harmonicPotential

    def evolve(self, dt = 0.001):
        ''' one iteration-step '''

        def spatialEvolve(f, x):
            return f*exp(-0.5 * self._V(x) * dt * 1j)
        def momentumEvolve(F, k):
            return F*exp(-0.5 * k*k * dt * 1j)

        self._f = map(spatialEvolve, self._f, self._x)
        self._F = fft(self._f)
        self._F = map(momentumEvolve, self._F, self._k)
        self._f = ifft(self._F)
        self._f = map(spatialEvolve, self._f, self._x)

    def f(self):
        return self._f

    def F(self):
        return self._F

    def x(self):
        return self._x

    def V(self):
        return self._V(self._x)

    def setPotential(self, V):
        ''' set the potential (as a function of an array of x-values)'''
        self._V = V

    def setInitial(self, f):
        ''' set the initial conditions (as a function of x of an array of x-values)'''
        self._f = f(self._x)

if __name__ == '__main__':
    from matplotlib.pyplot import plot, show

    s = Schroedinger1D(128)
    plot(s.x(), abs(s.f()))

    for i in xrange(100):
        s.evolve()

    plot(s.x(), abs(s.f()))
    show()
