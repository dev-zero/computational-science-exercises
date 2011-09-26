#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def root(n, epsilon=0.0001):
    """ find the square root using newton's method """
    initial = 1. # TODO: better choice?
    x = initial
    while True:
        old_x = x
        x = 0.5 * (x + n/x)
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
