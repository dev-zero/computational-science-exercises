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

from numpy import sqrt, arcsin, arccos, arctan2, sin, cos, pi

window = tk.Tk()
window.title("Flightpaths")

canvas = tk.Canvas(window, height=512, width=1024)
canvas.pack(fill="both", expand="yes")

image = Image.open("Hammer-Aitov_Projection.jpg")
projection = ImageTk.PhotoImage(image)

canvas.create_image((512,256), image=projection)

def cartesian2spherical_ha(x, y):
    u = sqrt(1. - x**2/16. - y**2/4.)
    return (arcsin(u*y), 2.*arctan2(u*x, 4*u**2 -2.))

def spherical2cartesian_ha(theta, phi):
    return (2.*sqrt(2)*sin(theta)*sin(.5*phi)/sqrt(1.+sin(theta)*cos(.5*phi)), 2.*cos(theta)/sqrt(1.+sin(theta)*cos(.5*phi)))

def moved(event):
    x = 2*sqrt(2)*(event.x-512)/1024.
    y =   sqrt(2)*(-event.y+256)/512.
    print x, y
    theta, phi = cartesian2spherical_ha(x, y)
    print 360*theta/pi, 360*phi/pi

canvas.bind("<Motion>", moved)
window.mainloop()

