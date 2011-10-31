#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from Tkinter import Tk, Canvas, ALL
from numpy import cos, sin, array, concatenate

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

    def getEnergy(self):
        return 0.5*self.p**2 + self.P - self.alpha*cos(self.q) - self.beta*cos(self.q - self.Q)

class App:
    def __init__(self, master, height, width):
        from Tkinter import Label, Entry, Canvas, Button
    
        Label(master, text="Initial conditions:").grid(row=0, column=0, columnspan=2)
        Label(master, text="q").grid(row=1, column=0)
        Label(master, text="p").grid(row=2, column=0)
        Label(master, text="t").grid(row=3, column=0)
        Label(master, text="v").grid(row=4, column=0)
        Label(master, text="b").grid(row=5, column=0)
        Label(master, text="l").grid(row=6, column=0)
        Label(master, text="g").grid(row=7, column=0)
        Button(master, text="Reset", command=self.resetInitialConditions).grid(row=8, column=0, columnspan=2)

        self.q = Entry(master)
        self.p = Entry(master)
        self.t = Entry(master)
        self.v = Entry(master)
        self.b = Entry(master)
        self.l = Entry(master)
        self.g = Entry(master)

        self.q.grid(row=1, column=1)
        self.p.grid(row=2, column=1)
        self.t.grid(row=3, column=1)
        self.v.grid(row=4, column=1)
        self.b.grid(row=5, column=1)
        self.l.grid(row=6, column=1)
        self.g.grid(row=7, column=1)

        self.canv = Canvas(master, height=height, width=width)
        self.canv.grid(row=0, column=2, rowspan=8)

        self.pendulum = DrivenPendulum()

        self.q.insert(0, 2.)
        self.p.insert(0, 0.)
        self.t.insert(0, 0.)
        self.v.insert(0, 2.)
        self.b.insert(0, 1.)
        self.l.insert(0, 1.5)
        self.g.insert(0, -10.)

        self.rad = 8
        self.scaleFactor = 50
        self.shiftPosition = array([width//2, height//2])

        self.axes = self.canv.create_line(tuple(self.shiftPosition) + tuple(self.shiftPosition) + tuple(self.shiftPosition))
        self.bob1 = self.canv.create_oval(self.getOvalCoords(self.shiftPosition), fill="blue")
        self.bob2 = self.canv.create_oval(self.getOvalCoords(self.shiftPosition), fill="red")

        self.resetInitialConditions()
        self.updatePendulum()

    def getOvalCoords(self, position):
        return (position[0]-self.rad, position[1]-self.rad, position[0]+self.rad, position[1]+self.rad)

    def updatePendulum(self):

        pos1 = (self.scaleFactor*self.pendulum.getInnerPosition()*array([1, -1])).astype(int) + self.shiftPosition
        pos2 = (self.scaleFactor*self.pendulum.getOuterPosition()*array([1, -1])).astype(int) + self.shiftPosition

        self.canv.coords(self.axes, tuple(self.shiftPosition) + tuple(pos1) + tuple(pos2))
        self.canv.coords(self.bob1, self.getOvalCoords(pos1))
        self.canv.coords(self.bob2, self.getOvalCoords(pos2))

        self.pendulum.evolve(0.05)
        self.canv.after(20, self.updatePendulum)

    def resetInitialConditions(self):
        self.pendulum.setInitialConditions(
                float(self.q.get()),
                float(self.t.get()),
                float(self.v.get()),
                float(self.p.get()),
                float(self.b.get()),
                float(self.l.get()),
                float(self.g.get()),
                )


window = Tk()
window.title("Driven Pendulum Simulation")
ht = wd = 400
app = App(window, ht, wd)

#app.updatePendulum()
window.mainloop()
