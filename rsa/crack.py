#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def word(n):
    s = ""
    while n > 0:
        c = chr(n % 32 + 96)
        if c < 'a' or c > 'z':
            c = ' '
        s += c
        n /= 32
    return s

def calculate_r(b, N):
    r = 1
    while pow(b, r, N) != 1:
        r += 1
    return r

def calculate_dprime(c, r):
    m = 1
    while (1+m*r) % c != 0:
        m += 1

    return (1+m*r) // c

def decode(b, d, N):
    return pow(b, d, N)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="decrypt a RSA-encrypted integer/word by brute-force")
    parser.add_argument('-N', dest='N', type=int, required=True, help="the product of the primes N=pq (part of the public key)")
    parser.add_argument('-c', dest='c', type=int, required=True, help="c as given in cd=1+s(p-1)(q-1) (part of the public key)")
    parser.add_argument('numbers', metavar='b', type=int, nargs='+', help="the numbers to crack with the specified public key")

    args = parser.parse_args()

    #N = 1024384027
    #c = 910510237
    #b = 100156265

    from time import time

    for b in args.numbers:
        print("cracking b: {} using N: {}, c: {}".format(b, args.N, args.c))

        start = time()
        r = calculate_r(b, args.N)
        r_time = time()-start
        print("calculated r: {} (in {} seconds)".format(r, r_time))

        start = time()
        dprime = calculate_dprime(args.c, r)
        dprime_time = time()-start
        print("calculated d': {} (in {} seconds)".format(dprime, dprime_time))

        a = pow(b, dprime, args.N)
        print "a: {}/'{}' (in {} seconds total)".format(a, word(a), r_time + dprime_time)
