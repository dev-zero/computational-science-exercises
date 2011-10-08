#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def generate_primes(N):
    ''' returns an array with primes up to size N'''
    # ideas for optimization:
    # - preset even numbers with False
    #   and set the loop-increment for i to 2
    # - or store the value of 2n+1 at position n
    #   (which would also half the storage requirement)

    numbers = [True]*(N+1)
    numbers[0] = numbers[1] = False
    
    i = 2
    while i**2 <= N:
        if numbers[i]:
            for k in xrange(i**2, N+1, i):
                numbers[k] = False
        i += 1

    return [n for n,v in enumerate(numbers) if v]

def generate_primes2(N):
    ''' returns a generator of up to size N'''
    multiples = []

    yield 2
    n = 3
    while n < N:
        if n not in multiples:
            multiples += range(n**2, N+1, n)
            yield n
        n += 2

def print_primes(N):
    ''' print all primes between 1..N '''
    for n in generate_primes(N):
        print ("{} is prime".format(n))

def plot_primes(N):
    ''' print all primes between 1..N and plot P_k vs k*ln(P_k) '''
    from math import log
    from pylab import plot, show, xlabel, ylabel
    x = []
    y = []
    for n in generate_primes(N):
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
