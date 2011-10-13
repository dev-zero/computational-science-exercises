#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
# Generates primes or pseudoprimes up to a given number.
#
# Usage: ./eratosthenes.py --help
# ... this should give enough information on how to run it

def generate_primes_array(N):
    ''' returns an array of booleans of size N
        where a True value at position i of the array
        marks the value i as prime '''
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

    return numbers

def generate_primes(N):
    ''' returns an array with primes up to size N'''
    return [n for n,v in enumerate(generate_primes_array(N)) if v]

def generate_primes2(N):
    ''' generator for primes up to N (different method than generate_primes)'''
    multiples = []

    yield 2
    n = 3
    while n < N:
        if n not in multiples:
            multiples += range(n**2, N+1, n)
            yield n
        n += 2

def generate_pseudoprimes(N):
    ''' generator for all pseudoprimes up to N '''
    from fractions import gcd
    numbers = generate_primes_array(N)
    for i in xrange(3,N,2):
        if not numbers[i]: # check only non-primes
            for j in xrange(3,i,2): # Carmichael numbers are not even
                # if i,j are not coprime, take the next j and if they are
                # they should not fail the Fermat primality test for being
                # a Carmicheal number
                if gcd(j, i) == 1 and pow(j, i-1, i) != 1:
                    break
            else:
                yield i

def print_pseudoprimes(N):
    ''' print all primes between 1..N using generate_primes'''
    for n in generate_pseudoprimes(N):
        print ("{} is pseudoprime".format(n))

def print_primes(N):
    ''' print all primes between 1..N '''
    for n in generate_primes(N):
        print ("{} is prime".format(n))

def print_primes2(N):
    ''' print all primes between 1..N using generate_primes2'''
    for n in generate_primes2(N):
        print ("{} is prime".format(n))

def plot_primes(N):
    ''' print all primes between 1..N and plot P_k vs k*ln(P_k) using generate_primes'''
    from math import log
    from pylab import plot, show, xlabel, ylabel
    x = []
    y = []
    for n in generate_primes(N):
        x.append(n)
        y.append((len(y)+1)*log(n))

    plot(x, y)
    xlabel("P_k")
    ylabel("k ln(P_k)")
    show()

if __name__ == '__main__':
    from sys import argv, exit
    from argparse import ArgumentParser
    parser = ArgumentParser(description="print or plot primes or pseudoprimes")
    parser.add_argument('-n', '--number', dest='n', type=int, required=True,
            help="the largest number to check for (pseudo-)primality")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--plot-primes", dest='function', action='store_const', const=plot_primes,
            help="plot primes (k-th prime vs k ln(P_k)")
    group.add_argument("--print-primes", dest='function', action='store_const', const=print_primes,
            help="print primes up to size N")
    group.add_argument("--print-primes2", dest='function', action='store_const', const=print_primes2,
            help="print primes up to size N (using a different method)")
    group.add_argument("--print-pseudoprimes", dest='function', action='store_const', const=print_pseudoprimes,
            help="print pseudoprimes (Carmichael numbers) up to size N")
    args = parser.parse_args()
    
    if args.function == None or args.n == None:
        parser.print_help()
        exit(2)

    args.function(args.n)

    exit(0)
