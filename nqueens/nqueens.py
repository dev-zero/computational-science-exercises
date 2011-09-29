#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Tiziano Müller <tm@dev-zero.ch>
#
#
#
#

def nqueens_solutions(size):
    def is_valid(p):
        for i in xrange(1,size):
            for j in xrange(1,1+i):
                if p[i] == p[i-j]+j or p[i] == p[i-j]-j:
                    return False
        return True

    # another possibility for is_valid would be the following:
    # see http://code.activestate.com/recipes/576647-eight-queens-six-lines/
    # def is_valid(p):
    #     if (size == len(set(p[i]+i for i in cols))
    #              == len(set(p[i]-i for i in cols))):
    #         return True
    #     return False

    # backtracking is probably faster, but this is easier
    from itertools import permutations
    for p in permutations(range(size)):
        if is_valid(p):
            yield p

def unique_solutions(size):
    solutions = []

    def complex_board(p, r=0):
        return sorted([complex(2.*i+1. - size, 2.*p[i]+1. - size)*(complex(0,1)**r) for i in xrange(size)], key = lambda x: x.real)

    for s in nqueens_solutions(size):
        complex_solutions = [complex_board(p) for p in solutions]

        for r in xrange(0,4):
            board = complex_board(s, r)

            if board in complex_solutions:
                break

            # board is already sorted by real-part, therefore conjugation does not change order
            if [x.conjugate() for x in board] in complex_solutions:
                break

        else:
            solutions.append(s)

    return solutions

def print_solutions(size):
    count = 0
    for solution in nqueens_solutions(size):
        count += 1
        print solution
    print ("number of solutions: {}".format(count))

def print_unique_solutions(size):
    solutions = unique_solutions(size)

    for solution in solutions:
        print solution

    print ("number of unique solutions: {}".format(len(solutions)))

if __name__ == '__main__':
    from sys import argv, exit
    size = 8
    if len(argv) == 2:
        size = int(argv[1])
        if (size < 2):
            print ("The size must be >= 2")
            exit(1)
    print_unique_solutions(size)
    exit(0)

# vim: set ts=4 sw=4 tw=0 :
