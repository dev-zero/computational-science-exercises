#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from cyclotron import Cyclotron
from rcyclotron import RelativisticCyclotron

import matplotlib
matplotlib.use('TkAgg')

class App:
    def __init__(self, master):
        from Tkinter import Label, Entry, Canvas, Button
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
        from matplotlib.figure import Figure
    
        Label(master, text="Initial conditions:").grid(row=0, column=0, columnspan=2)
        Label(master, text="x").grid(row=1, column=0)
        Label(master, text="y").grid(row=2, column=0)
        Label(master, text="p_x").grid(row=3, column=0)
        Label(master, text="p_y").grid(row=4, column=0)
        Label(master, text="alpha").grid(row=5, column=0)
        Label(master, text="omega").grid(row=6, column=0)
        Label(master, text="steps").grid(row=7, column=0)
        Button(master, text="Plot", command=self.replot).grid(row=8, column=0, columnspan=2)

        self.x = Entry(master)
        self.y = Entry(master)
        self.px = Entry(master)
        self.py = Entry(master)
        self.alpha = Entry(master)
        self.omega = Entry(master)
        self.steps = Entry(master)

        self.x.grid(row=1, column=1)
        self.y.grid(row=2, column=1)
        self.px.grid(row=3, column=1)
        self.py.grid(row=4, column=1)
        self.alpha.grid(row=5, column=1)
        self.omega.grid(row=6, column=1)
        self.steps.grid(row=7, column=1)

        self.x.insert(0, 0.)
        self.y.insert(0, 0.)
        self.px.insert(0, 0.)
        self.py.insert(0, 1.)
        self.alpha.insert(0, 1.)
        self.omega.insert(0, 2.)
        self.steps.insert(0, 1000)

        self.cyclotron = Cyclotron()
        self.rcyclotron = RelativisticCyclotron()
        self.resetInitialConditions()

        self.figure = Figure(figsize=(6,5), dpi=100)
        self.a = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=8)

    def resetInitialConditions(self):
        self.cyclotron.setInitialConditions(
                float(self.x.get()),
                float(self.y.get()),
                float(self.px.get()),
                float(self.py.get()),
                float(self.alpha.get()),
                float(self.omega.get()))
        self.rcyclotron.setInitialConditions(
                float(self.x.get()),
                float(self.y.get()),
                float(self.px.get()),
                float(self.py.get()),
                float(self.alpha.get()),
                float(self.omega.get()))

    def replot(self):
        self.resetInitialConditions()
        xs = []
        ys = []
        rxs = []
        rys = []
        for i in xrange(int(self.steps.get())):
            x,y = self.cyclotron.getPosition()
            xs.append(x)
            ys.append(y)
            x,y = self.rcyclotron.getPosition()
            rxs.append(x)
            rys.append(y)
            self.cyclotron.evolve(0.005)
            self.rcyclotron.evolve(0.005)

        self.a.clear()
        self.a.plot(xs, ys, rxs, rys)
        self.canvas.draw()

from Tkinter import Tk
window = Tk()
window.title("Cyclotron")
app=App(window)
window.mainloop()

