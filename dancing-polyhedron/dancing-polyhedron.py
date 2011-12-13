#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

import quaternions as quat
from culling import pointInsidePolygon
from numpy import array, pi, reshape, append, sqrt
from numpy.linalg import norm

import Tkinter as tk

# PARAMETERS
WIDTH=512
HEIGHT=512
POINT_RADIUS=4
POINT_COLOR='red'
OFFSET=array([HEIGHT//2, WIDTH//2])
CUBESIZE=15


window = tk.Tk()
window.title("Dancing Polyhedron")

canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
canvas.pack(fill="both", expand="yes")

cube = [
         1, 1,-1,
        -1, 1,-1,
        -1,-1,-1,
         1,-1,-1,
         1, 1, 1,
        -1, 1, 1,
        -1,-1, 1,
         1,-1, 1,
        ]
cube = reshape(cube, (8,-1))
cube *= 2*CUBESIZE

rotv = array([0,1,1])
qs   = quat.quatFromVectorAngle(rotv, 0.)
qe   = quat.quatFromVectorAngle(rotv, pi)

camera = array([0, 100, 0])

steps = 32 # number of steps per 180° rotation
distance = 200

# projection to the x-z plane
def project2D(xyz, camera, d):
    xyz = xyz - camera
    return append(xyz[0], xyz[2])*d/xyz[1]

counter = 0

def update():
    global counter
    i = counter % steps

    canvas.delete(tk.ALL)

    q = quat.slerp(qs, qe, i*1./steps)
    rotated_coords = map(lambda p: quat.rotateVectorByQuat(p, q), cube)
    projected_tkcoords = map(lambda pp: project2D(pp, camera, distance)*array([1, -1]) + OFFSET, rotated_coords)
    
    # this iterates through all non-repeating permutations of (k,l,m) and checks
    # for each triple whether the lines k-l and k-m in the cube is not a diagonal, in that case it
    # takes the points as points of a polygon where we want to check whether it hides the specified point
    def checkMidpoint(point):
        for k in xrange(len(rotated_coords)):
            for l in xrange(k+1, len(rotated_coords)):
                if norm(cube[l]-cube[k]) > 2*2*CUBESIZE:
                    continue
                for m in xrange(l+1, len(rotated_coords)):
                    if norm(cube[m]-cube[k]) > 2*2*CUBESIZE:
                        continue

                    poly = array([rotated_coords[k], rotated_coords[l], rotated_coords[m]])
                    if pointInsidePolygon(poly, point, camera):
                        return True
        return False

    # draw edges, 3 per iteration
    for j in xrange(4):

        color = ['black']*3

        # calculated the midpoints of the edges going to be drawn in this iteration
        midpoint = [0]*3
        midpoint[0] = .5*(rotated_coords[j]+rotated_coords[(j+1)%4])
        midpoint[1] = .5*(rotated_coords[j]+rotated_coords[j+4])
        midpoint[2] = .5*(rotated_coords[j+4]+rotated_coords[(j+1)%4+4])

# this is test which can be enabled to follow a specific edge
#        M = 2
        
#        if j == 1:
#            print "here"
#            m = project2D(midpoint[M], camera, distance)*array([1, -1]) + OFFSET
#            tkpoint = tuple(append(m-POINT_RADIUS, m+POINT_RADIUS).astype(int))
#            canvas.create_oval(tkpoint, fill=POINT_COLOR)
#
#            if checkMidpoint(midpoint[M]):
#                color[M] = 'grey'


        # for each edge check whether it is hidden, if it is, set its color to gray
        for k in xrange(3):
            if checkMidpoint(midpoint[k]):
                color[k] = 'grey'

        canvas.create_line(tuple(projected_tkcoords[j]), tuple(projected_tkcoords[(j+1)%4]), fill=color[0])
        canvas.create_line(tuple(projected_tkcoords[j]), tuple(projected_tkcoords[j+4]), fill=color[1])
        canvas.create_line(tuple(projected_tkcoords[j+4]), tuple(projected_tkcoords[(j+1)%4+4]), fill=color[2])

    # draw points
#    for pp2d in projected_tkcoords:
#        tkpoint = tuple(append(pp2d-POINT_RADIUS, pp2d+POINT_RADIUS).astype(int))
#        canvas.create_oval(tkpoint, fill=POINT_COLOR)

    counter += 1
    canvas.after(40, update)

update()
window.mainloop()
