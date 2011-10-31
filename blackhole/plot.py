#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from blackhole import Blackhole

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
        Label(master, text="steps").grid(row=5, column=0)
        Button(master, text="Plot", command=self.replot).grid(row=6, column=0, columnspan=2)

        self.x = Entry(master)
        self.y = Entry(master)
        self.px = Entry(master)
        self.py = Entry(master)
        self.steps = Entry(master)

        self.x.grid(row=1, column=1)
        self.y.grid(row=2, column=1)
        self.px.grid(row=3, column=1)
        self.py.grid(row=4, column=1)
        self.steps.grid(row=5, column=1)

        self.x.insert(0, 25.)
        self.y.insert(0, 0.)
        self.px.insert(0, 0.)
        self.py.insert(0, 0.2)
        self.steps.insert(0, 1000)

        self.blackhole = Blackhole()
        self.resetInitialConditions()

        self.figure = Figure(figsize=(6,5), dpi=100)
        self.a = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=7)

    def resetInitialConditions(self):
        self.blackhole.setInitialConditions(
                float(self.x.get()),
                float(self.y.get()),
                float(self.px.get()),
                float(self.py.get()))

    def replot(self):
        self.resetInitialConditions()
        xs = []
        ys = []
        for i in xrange(int(self.steps.get())):
            x,y = self.blackhole.getPosition()
            xs.append(x)
            ys.append(y)
            self.blackhole.evolve(0.005)

        self.a.clear()
        self.a.plot(xs, ys)
        self.canvas.draw()

from Tkinter import Tk
window = Tk()
window.title("Blackhole")
app=App(window)
window.mainloop()

