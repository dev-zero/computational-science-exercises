#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def nroot(n, a):
    """ find the positive n-th root using newton's method """

    if type(a) != float or type(n) != int or a <= 0.:
        raise TypeError("Invalid type: argument must be a positive floating point number and the root an integer")

    from sys import float_info

    x = 1.
    while True:
        old_x = x
        x = ((n-1)*x + a/pow(x,n-1))/n
        # means that the difference is only representable subnormal and we are in the "regime" of gradual underflow:
        if (abs(old_x-x) < float_info.min):
            break
    return x


def print_usage(name):
    print("usage: {} <root> <number> [<number2> [<number3> ...]]".format(name))

def print_nroots(root, numbers):
    for n in numbers:
        print("sqrt({}) = {}").format(n, nroot(int(root), float(n)))

if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) > 2:
        print_nroots(argv[1], argv[2:])
    else:
        print_usage(argv[0])
    exit(0)

# vim: set ts=4 sw=4 tw=0 :
