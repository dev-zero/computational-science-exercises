#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

from numpy import array, dot, arange
from Tkinter import Tk, Canvas, ALL, _flatten

triangle = [ [100, 100], [180,100], [100,40] ]
selected_corner = None
point_radius = 4
point_color = 'green'
point_draw = False

def is_inside(point, triangle):
    v = []
    v.append(triangle[2] - triangle[0])
    v.append(triangle[1] - triangle[0])
    v.append(point - triangle[0])

    dots = [None]*9
    for i in xrange(3):
        for j in xrange(i,3):
            dots[i*3+j] = dot(v[i],v[j])

    denom = dots[0]*dots[4] - dots[1]*dots[1]
    u = (dots[4]*dots[2] - dots[1]*dots[5]) / float(denom)
    v = (dots[0]*dots[5] - dots[1]*dots[2]) / float(denom)

    return (u > 0.) and (v > 0.) and (u+v < 1.)


window = Tk()
canvas = Canvas(window)
canvas.pack(fill="both", expand="yes")

triangle_item = canvas.create_polygon(triangle, fill='white', outline='black')

def moved(event):
    color = 'green'
    if is_inside(array([event.x, event.y]), [array(p) for p in triangle]):
        color = 'red'
    canvas.itemconfig(triangle_item, fill=color)

def clicked(event):
    global selected_corner, point_color, point_draw
    position = array([event.x, event.y])
    point_color = 'red'
    point_draw = True
    if is_inside(position, [array(p) for p in triangle]):
        point_color = 'green'
        distances = [dot(position-array(p), position-array(p)) for p in triangle]
        selected_corner = 0
        for i in xrange(1,3):
            if (distances[i] < distances[selected_corner]):
                selected_corner = i
    else:
        selected_corner = None

    print "selected_corner for movement:", selected_corner

def released(event):
    if point_draw:
        canvas.create_oval(event.x-point_radius, event.y-point_radius, event.x+point_radius, event.y+point_radius, fill=point_color)

def dragged(event):
    global point_draw
    point_draw = False

    if selected_corner == None:
        return

    global triangle
    triangle[selected_corner] = [event.x, event.y]
    canvas.coords(triangle_item, _flatten(triangle))
    

canvas.bind("<Button-1>", clicked)
canvas.bind("<B1-Motion>", dragged)
canvas.bind("<ButtonRelease-1>", released)
window.mainloop()
