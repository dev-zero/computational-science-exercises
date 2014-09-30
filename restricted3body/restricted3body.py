#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

class Restricted3Body:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.px = 0.
        self.py = 1.
        self.mu = 0.2

    def setInitialConditions(self, x, y, px, py, mu):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.mu = mu

    def pxdot(self):
        ''' p_x' = -dV/dx + p_y'''
        return -self.dVdx() + self.py

    def pydot(self):
        ''' p_y' = -dV/dy - p_x '''
        return -self.dVdy() - self.px

    def xdot(self):
        ''' x' = p_x + y'''
        return self.px + self.y

    def ydot(self):
        ''' y' = p_y - x '''
        return self.py - self.x

    def dVdx(self):
        return self.dV(self.x + self.mu, self.x - 1. + self.mu)

    def dVdy(self):
        return self.dV(self.y, self.y)

    def dV(self, V1, V2):
        return (1.-self.mu)*pow((self.x+self.mu)**2 + self.y**2, -1.5)*V1 + self.mu*pow((self.x-1.+self.mu)**2 + self.y**2, -1.5)*V2

    def evolve(self, dt):
        ''' leapfrog integrator '''
        self.px += self.pxdot()*0.5*dt
        self.py += self.pydot()*0.5*dt

        self.x += self.xdot()*dt
        self.y += self.ydot()*dt

        self.px += self.pxdot()*0.5*dt
        self.py += self.pydot()*0.5*dt

    def V(self):
        return -(1.-self.mu)*pow((self.x+self.mu)**2 + self.y**2, -0.5) - self.mu*pow((self.x-1.+self.mu)**2 + self.y**2, -0.5)
    def hamiltonian(self):
        return 0.5*self.px**2 + 0.5*self.py**2 + self.V() + self.y*self.px - self.x*self.py

    def getPosition(self):
        return (self.x, self.y)

import matplotlib
matplotlib.use('TkAgg')

class App:
    def __init__(self, master):
        try:
            from tkinter import Label, Entry, Canvas, Button
        except ImportError:
            from Tkinter import Label, Entry, Canvas, Button
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
        from matplotlib.figure import Figure
    
        Label(master, text="Initial conditions:").grid(row=0, column=0, columnspan=2)
        Label(master, text="x").grid(row=1, column=0)
        Label(master, text="y").grid(row=2, column=0)
        Label(master, text="p_x").grid(row=3, column=0)
        Label(master, text="p_y").grid(row=4, column=0)
        Label(master, text="mu").grid(row=5, column=0)
        Label(master, text="steps").grid(row=6, column=0)
        Button(master, text="Plot", command=self.replot).grid(row=7, column=0, columnspan=2)

        self.x = Entry(master)
        self.y = Entry(master)
        self.px = Entry(master)
        self.py = Entry(master)
        self.mu = Entry(master)
        self.steps = Entry(master)

        self.x.grid(row=1, column=1)
        self.y.grid(row=2, column=1)
        self.px.grid(row=3, column=1)
        self.py.grid(row=4, column=1)
        self.mu.grid(row=5, column=1)
        self.steps.grid(row=6, column=1)

        self.x.insert(0, 0.)
        self.y.insert(0, 0.)
        self.px.insert(0, 0.)
        self.py.insert(0, 1.)
        self.mu.insert(0, 0.2)
        self.steps.insert(0, 1000)

        self.r3b = Restricted3Body()
        self.resetInitialConditions()

        self.figure = Figure(figsize=(6,5), dpi=100)
        self.a = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=8)

    def resetInitialConditions(self):
        self.r3b.setInitialConditions(
                float(self.x.get()),
                float(self.y.get()),
                float(self.px.get()),
                float(self.py.get()),
                float(self.mu.get()))

    def replot(self):
        self.resetInitialConditions()
        xs = []
        ys = []
        for i in range(int(self.steps.get())):
            x,y = self.r3b.getPosition()
            xs.append(x)
            ys.append(y)
            self.r3b.evolve(0.005)

        self.a.clear()
        self.a.plot(xs, ys)
        self.canvas.draw()

try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk

window = Tk()
window.title("Restricted Three-Body Problem")
app=App(window)
window.mainloop()

