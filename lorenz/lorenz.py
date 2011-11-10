#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from scipy.integrate import ode
from numpy import array
import vtk
import random

class Lorenz:
    ''' Formulate the problem, capsulate the ODE solver
        and provide access functions for points, initial conditions
        and parameters '''
    def __init__(self):
        # parameters
        self.sigma = 10.
        self.r = 28.
        self.b = 8./3.

        # initial condition
        self.c0 = [0., 1., 0.]

        # the ODE solver and iteration counter
        self.o = ode(self.diff)
        self.i = 0

        # initialize the solver
        self.setInitial(self.c0)
        self.setParams(self.sigma, self.r, self.b)

    def setParams(self, sigma, r, b):
        self.o.set_f_params(sigma, r, b)
        self.sigma = sigma
        self.r = r
        self.b = b
        self.setInitial(self.c0)

    def setInitial(self, c0, t = 0.):
        self.o.set_initial_value(c0, t)
        self.c0 = c0
        self.i = 0

    def diff(self, t, c, sigma, r, b):
        return array([sigma*(c[1]-c[0]), c[0]*(r - c[2])-c[1], c[0]*c[1] - b*c[2]])

    def eval(self, dt = 0.02, steps=1):
        self.i += 1
        for s in xrange(steps):
            self.o.integrate(self.o.t + dt)
            if not self.o.successful():
                return False
        return True

    def getValue(self):
        return self.o.y

    def getIteration(self):
        return self.i

def randomLorenzParameters():
    return (random.random()*20, random.random()*50, random.random()*10)

l = Lorenz()

points = vtk.vtkPoints()
lines = vtk.vtkCellArray()

track = vtk.vtkPolyData()
track.SetPoints(points)
track.SetLines(lines)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(track)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(random.random(), random.random(), random.random())

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(actor)

ren.SetBackground(0, 0, 0)
renWin.SetFullScreen(1)

iren.Initialize()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
renWin.Render()

def update(obj, event):
    if l.getIteration() < 1000 and l.getIteration() > 0:
        points.InsertPoint(l.getIteration(), l.getValue())
        points.Modified()

        lines.InsertNextCell(2)
        lines.InsertCellPoint(l.getIteration()-1)
        lines.InsertCellPoint(l.getIteration())
        lines.Modified()

    else:
        sigma, r, b = randomLorenzParameters()
        l.setParams(sigma, r, b)
        points.Reset()
        points.InsertPoint(l.getIteration(), l.getValue())
        points.Modified()
        lines.Reset()
        lines.InsertNextCell(1)
        lines.InsertCellPoint(0)
        lines.Modified()

    if not l.eval():
        import sys.exit
        exit(1)

    iren = obj
    ren.ResetCamera()
    iren.GetRenderWindow().Render()

iren.AddObserver('TimerEvent', update)
iren.CreateRepeatingTimer(1);
iren.Start()
