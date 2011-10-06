#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
# This draws a resizeable triangle and allows one to draw points
# which are being colored in red if they are outside the triangle, green otherwise.
#
# In contrary to the suggested solution this does not clear the objects when resizing
# the triangle but rechecks whether they are inside the triangle after draggine the triangle.
# Avoiding that a point is being drawn when the triangle is dragged is realized by
# drawing the point when releasing the mouse button and only if the mouse was not moved in-between

from numpy import array, dot, arange
from Tkinter import Tk, Canvas, ALL, _flatten

triangle = [ [100, 100], [180,100], [100,40] ] # the triangle coordinates
selected_corner = None # the selected corner of the triangle
point_radius = 4
point_color = 'green' # the color of the point to be painted, having this shared between clicked and released avoids a second is_inside check
point_draw = False # this gives a little state machine, avoiding that a point is being drawn when we actually want to drag the triangle
points = [] # all the points being drawn to recheck them for being inside the triangle when resizing

def is_inside(point, triangle):
    ''' Tests whether a point is contained in a triangle
        specified by an array of points.
        The point and the points in the triangle must have
        a vector semantic (for example array() from numpy)
        and a dot-product must be defined (for example dot() from numpy).
        Calculation is done by specifying a coordinate transformation and
        then reversing it. The new coordination system is defined by
        the AB and AC axis of the triangle and the point A as an offet.
        A point which is inside must then have coords > 0 and must be
        smaller than 1 in the 1-norm.

        Any point can be written as P = A + u(B-A) + v(C-A)
        which is equivalent to P-A = u(B-A) + v(C-A).
        Applying once the dot-product with B-A and once with C-A
        yields two equations which can then be solved for u,v
        '''
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
        points.append(canvas.create_oval(event.x-point_radius, event.y-point_radius, event.x+point_radius, event.y+point_radius, fill=point_color))

def dragged(event):
    global point_draw
    point_draw = False

    if selected_corner == None:
        return

    global triangle
    triangle[selected_corner] = [event.x, event.y]
    canvas.coords(triangle_item, _flatten(triangle))

    for p in points:
        color = 'red'
        oval_coords = canvas.coords(p)
        point = array([oval_coords[0]+point_radius, oval_coords[1]+point_radius])
        if is_inside(point, array(triangle)):
            color = 'green'
        canvas.itemconfig(p, fill=color)
    

canvas.bind("<Button-1>", clicked)
canvas.bind("<B1-Motion>", dragged)
canvas.bind("<ButtonRelease-1>", released)
window.mainloop()
