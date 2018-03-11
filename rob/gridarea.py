#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
from collections import deque
# import pdb
# from pdb import set_trace


def rect_1_3_4(xin, yin):
    '''returns 1 IFF (xin, yin) is in the 3x4 rectangle in quadrant 1,
    that is, IFF 0 <= xin < 4 and 0 <= yin < 3
    0, 3 __ __ __ __ 4, 3
        |           |
        |           |
        |__ __ __ __|
    0, 0             4, 0
    '''
    if xin < 0 or xin > 3:
        return 0
    if yin < 0 or yin > 2:
        return 0
    return 1


class BoundedGrid:
    '''Contiguous 2D grid specified by a containment function:
    contains(x, y) > 0 IFF the grid contains tile indexed by (x, y).
    The returned value may be regarded as the contained area of the tile.'''

    def __init__(self, contains):
        self.contains = contains



def reachable_area(grid, x_init, y_init):
    '''
    returns the area of the explorable grid by summing the areas of
    contiguous grid tiles as indexed by two integers, starting at the tile
    indexed by (x_init, y_init), with adjacecy = 4.
    The contiguous area need not be convex.
    '''
    area = grid.contains(x_init, y_init)
    if area <= 0:
        return 0
    queue = deque()
    added = set()
    queue.append((x_init, y_init))
    added.add((x_init, y_init))
    while queue:
        xin, yin = queue.popleft()
        xin += 1
        if (xin, yin) not in added:
            added.add((xin, yin))
            inc = grid.contains(xin, yin)
            if inc > 0:
                area += inc
                queue.append((xin, yin))
        xin -= 1
        yin -= 1
        if (xin, yin) not in added:
            added.add((xin, yin))
            inc = grid.contains(xin, yin)
            if inc > 0:
                area += inc
                queue.append((xin, yin))
        xin -= 1
        yin += 1
        if (xin, yin) not in added:
            added.add((xin, yin))
            inc = grid.contains(xin, yin)
            if inc > 0:
                area += inc
                queue.append((xin, yin))
        xin += 1
        yin += 1
        if (xin, yin) not in added:
            added.add((xin, yin))
            inc = grid.contains(xin, yin)
            if inc > 0:
                area += inc
                queue.append((xin, yin))
    return area

def test_predicate(verbose, predicate, subject, expect):
    '''
    tests if the predicate function, applied to subject, gives the expected answer.
    Returns the number of wrong answers, that is,
    0 if predicate(subject) == expect,
    1 otherwise.
    '''
    result = predicate(subject)
    passed = result == expect
    if verbose > passed:
        print("%s %s: expected %s for %s"
              % (predicate.__name__, "PASS" if passed else "FAIL", expect, subject))
    return not passed

def test_func_args(verbose, func_args, args, expect):
    '''
    tests the result of func_args applied to the *arguments against expect.
    Returns the number of wrong answers, that is,
    0 if result == expect,
    1 if not.
    '''
    result = func_args(*args)
    passed = result == expect
    if verbose > passed:
        print("%s %s: expected %s:  %s  %s" % (func_args.__name__,
                                               "PASS" if passed else "FAIL",
                                               expect, args[0], args[1]))
    return not passed

def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    num_wrong = 0
    grid = BoundedGrid(rect_1_3_4)
    area = reachable_area(grid, 1, 1)
    num_wrong += area != 12
    if args.verbose > 1:
        print("area %d =?= 12" % area)
    print("unit_test:  num_tests:",
          " num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")


def main():
    '''driver for unit_test'''
    const_a = "abcdefgh"
    const_b = "abc_efgh"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', type=str, nargs='?', const=const_a,
                        help="str_a to test against str_b (const: %s)" % const_a)
    parser.add_argument('-b', type=str, nargs='?', const=const_b,
                        help="str_b to test against str_a (const: %s)" % const_b)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()


    unit_test(args)


if __name__ == '__main__':
    main()
