#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def generate_primes(N):
    ''' returns an array with each position in the array
        defining the number and its value whether or not it's a prime '''
    numbers = [True]*(N+1)
    numbers[0] = numbers[1] = False
    
    i = 2
    while i**2 <= N:
        if numbers[i]:
            for k in xrange(i**2, N+1, i):
                numbers[k] = False
        i += 1

    return numbers

def print_primes(N):
    ''' print all primes between 1..N '''
    for n, v in enumerate(generate_primes(N)):
        if v:
            print ("{} is prime".format(n))

def plot_primes(N):
    ''' print all primes between 1..N and plot P_k vs k*ln(P_k) '''
    from math import log
    from pylab import plot, show, xlabel, ylabel
    x = []
    y = []
    for n, v in enumerate(generate_primes(N)):
        if v:
            print ("{} is prime".format(n))
            x.append(n)
            y.append((len(y)+1)*log(n))

    plot(x, y)
    xlabel("P_k")
    ylabel("k ln(P_k)")
    show()

def print_usage(progname):
    print ("usage: {} <boundary>".format(progname))

if __name__ == '__main__':
    from sys import argv, exit
    if (len(argv) != 2):
        print_usage(argv[0])
        exit(1)

    plot_primes(int(argv[1]))
    exit(0)
