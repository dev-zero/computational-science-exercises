#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def root(a, epsilon=0.00001):
    """ find the positive square root using newton's method """

    if type(a) != float or not a > 0.:
        raise TypeError("Invalid type: argument must be a positive floating point number")

    x = 1. # newton converges for every initial x != 0 for finding the square root
    while True:
        old_x = x
        x = 0.5 * (x + a/x)
        if (abs(old_x-x) < epsilon):
            break
    return x

def print_usage(name):
    print("usage: {} <number> [<number2> [<number3> ...]]".format(name))

def print_roots(numbers):
    for n in numbers:
        print("sqrt({}) = {}").format(n, root(float(n)))

if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) > 1:
        print_roots(argv[1:])
    else:
        print_usage(argv[0])
    exit(0)

# vim: set ts=4 sw=4 tw=0 :
