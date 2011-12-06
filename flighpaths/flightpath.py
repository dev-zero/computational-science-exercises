#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

import Tkinter as tk
from PIL import Image, ImageTk

from numpy import sqrt, pi, sin, cos, array, cross, dot, arccos, append, arctan2, arcsin, linspace
from numpy.linalg import norm
from hammer_aitov import cartesian2spherical, spherical2cartesian
import quaternions as quat

WIDTH=1024
HEIGHT=512
POINT_RADIUS=4
POINT_COLOR='red'

window = tk.Tk()
window.title("Flightpaths")

canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
canvas.pack(fill="both", expand="yes")

image = Image.open("Hammer-Aitov_Projection.jpg")
projection = ImageTk.PhotoImage(image)

canvas.create_image((WIDTH//2,HEIGHT//2), image=projection)

start  = None
end    = (0,0)
points = []

def map2cartesian(xy):
    # scaling Tk coordinates to X=[-2*sqrt(2)..2*sqrt(2), Y=[-sqrt(2)..sqrt(2)]
    x, y = (2*sqrt(2)*(xy[0]-WIDTH/2)/(WIDTH/2), sqrt(2)*(-xy[1]+HEIGHT/2)/(HEIGHT/2))
    theta, phi = cartesian2spherical(x, y)
    xyz = array((cos(theta)*cos(phi), cos(theta)*sin(phi), sin(theta)))
    return xyz

def cartesian2map(xyz):
    theta = arcsin(xyz[2])
    phi   = arctan2(xyz[1], xyz[0])
    x, y = spherical2cartesian(theta, phi)
    return (int((WIDTH/2)*x/(2*sqrt(2)))+WIDTH//2, -int((HEIGHT/2)*y/sqrt(2)) + HEIGHT//2)

def clicked(event):
    global start, end, points
    if end != None:
        start = (event.x,event.y)
        end   = None
        for p in points:
            canvas.delete(p)
        points = []
    else:
        end = (event.x, event.y)

        s = map2cartesian(start)
        e = map2cartesian(end)

        for t in linspace(0, 1, 10):
            x, y = cartesian2map(quat.slerp(quat.quatFromVector(s), quat.quatFromVector(e), t)[1:4])
            points.append(canvas.create_oval(x-POINT_RADIUS, y-POINT_RADIUS, x+POINT_RADIUS, y+POINT_RADIUS, fill=POINT_COLOR))

canvas.bind("<Button-1>", clicked)
window.mainloop()

