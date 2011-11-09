#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from scipy.integrate import ode
from numpy import array, linspace, append
import vtk
import random

def lorenz(t, c, sigma, r, b):
    return array([sigma*(c[1]-c[0]), c[0]*(r - c[2])-c[1], c[0]*c[1] - b*c[2]])

c0 = array([0., 1., 0.])
params = (10., 28., 8./3.)
t = linspace(0., 100., 5000)

o = ode(lorenz)

points = vtk.vtkPoints()
points.InsertPoint(0, c0)
lines = vtk.vtkCellArray()
lines.InsertNextCell(1) # number of points
lines.InsertCellPoint(0)

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
#renWin.SetSize(500, 500)
renWin.SetFullScreen(1)

iren.Initialize()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
renWin.Render()

o.set_initial_value(c0, 0.).set_f_params(params[0], params[1], params[2])
i = 1

def update(obj, event):
    global i

    if o.successful() and o.t < 100.:
        o.integrate(o.t+0.02)
        points.InsertPoint(i, o.y)
        points.Modified()

        lines.InsertNextCell(2)
        lines.InsertCellPoint(i-1)
        lines.InsertCellPoint(i)
        lines.Modified()

        iren = obj
        ren.ResetCamera()
        iren.GetRenderWindow().Render()
    
        i += 1

iren.AddObserver('TimerEvent', update)
iren.CreateRepeatingTimer(1);

iren.Start()
