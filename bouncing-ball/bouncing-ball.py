#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from Tkinter import Tk, Canvas, ALL

ht = wd = 300
rad = 10
x = y = 150
vx = 5
vy = 2

window = Tk()
canv = Canvas(window, height = ht, width = wd)
canv.pack()

def update_ball():
    global x, y, vx, vy
    canv.delete(ALL)
    d = canv.create_oval(x-rad, y-rad,x+rad, y+rad, fill = "blue")

    if (x+rad > wd) or (x-rad < 0):
        vx = -vx
    if (y+rad > ht) or (y-rad < 0):
        vy = -vy

    x += vx
    y += vy

    canv.after(4, update_ball)

update_ball()
window.mainloop()

