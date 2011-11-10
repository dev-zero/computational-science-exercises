#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import array

class Lorenz:
    ''' Formulate the problem, capsulate the ODE solver
        and provide access functions for points, initial conditions
        and parameters '''
    def __init__(self):
        from scipy.integrate import ode

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
    from random import random
    return (random()*20, random()*50, random()*10)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="draw Lorenz plots in screensaver style")
    parser.add_argument('-f', '--fullscreen', dest='fullscreen', action='store_const', const=True, default=False, help="go fullscreen")
    parser.add_argument('-s', '--steps', dest='steps', metavar='N', action='store', type=int, default=1000, help="do N simulation steps before generating a new set of parameters and restart drawing")

    args = parser.parse_args()

    # create the Lorenz object
    l = Lorenz()

    import vtk
    import random

    # define the points and lines arrays
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    # dataset which represents the line objects
    track = vtk.vtkPolyData()
    track.SetPoints(points)
    track.SetLines(lines)

    # map the line objects to graphic primitives
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(track)

    # represents the graphic primitives in the scene
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # create a rendered and a window
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    # create an interactor for the window
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(actor)
    ren.SetBackground(0, 0, 0)

    # make it fullscreen
    if args.fullscreen:
        renWin.SetFullScreen(1)
    else:
        renWin.SetSize(400, 400)
    
    # initialize the interactor and set the control style to trackball
    iren.Initialize()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    # start rendering
    renWin.Render()

    def update(obj, event):
        if l.getIteration() < args.steps and l.getIteration() > 0:
            # add the new point
            points.InsertPoint(l.getIteration(), l.getValue())
            points.Modified()
    
            # and update the lines accordingly
            lines.InsertNextCell(2)
            lines.InsertCellPoint(l.getIteration()-1)
            lines.InsertCellPoint(l.getIteration())
            lines.Modified()
    
        else:
            sigma, r, b = randomLorenzParameters()
            print "starting with new parameters (sigma, r, b) = ", sigma, r, b
            l.setParams(sigma, r, b)
    
            # reset the points array, does not free the space
            # and therefore makes sure we don't always allocate/free memory
            points.Reset()
            points.InsertPoint(l.getIteration(), l.getValue())
            points.Modified()

            # ... and do the ame for the lines
            lines.Reset()
            lines.InsertNextCell(1)
            lines.InsertCellPoint(0)
            lines.Modified()

            # let the actor paint in a new random color
            actor.GetProperty().SetColor(random.random(), random.random(), random.random())

        if not l.eval():
            import sys.exit
            exit(1)

        # resets the camera (only "zoom out") to include the complete line
        ren.ResetCamera()

        # and rotate the view a little (we could have used Yaw instead to rotate the scene instead of the camera)
        ren.GetActiveCamera().Azimuth(0.5)

        # the obj is the RenderWindowInteractor since the callback was registered for it
        # render again
        obj.GetRenderWindow().Render()

    iren.AddObserver('TimerEvent', update)
    iren.CreateRepeatingTimer(1);
    iren.Start()

