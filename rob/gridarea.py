#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
from collections import deque
# import pdb
# from pdb import set_trace


def reachable_area(grid, r_init, c_init):
    '''
    returns the area of the explorable grid by summing the areas of
    contiguous grid tiles as indexed by two integers, starting at the tile
    indexed by (r_init, c_init), with adjacecy = 4.
    The contiguous area need not be convex.
    '''
    area = grid.contains(r_init, c_init)
    if area <= 0:
        return 0
    queue = deque()
    added = set()
    queue.append((r_init, c_init))
    added.add((r_init, c_init))
    while queue:
        row, col = queue.popleft()
        col += 1
        if (row, col) not in added:
            added.add((row, col))
            inc = grid.contains(row, col)
            if inc > 0:
                area += inc
                queue.append((row, col))
        col -= 1
        row -= 1
        if (row, col) not in added:
            added.add((row, col))
            inc = grid.contains(row, col)
            if inc > 0:
                area += inc
                queue.append((row, col))
        col -= 1
        row += 1
        if (row, col) not in added:
            added.add((row, col))
            inc = grid.contains(row, col)
            if inc > 0:
                area += inc
                queue.append((row, col))
        col += 1
        row += 1
        if (row, col) not in added:
            added.add((row, col))
            inc = grid.contains(row, col)
            if inc > 0:
                area += inc
                queue.append((row, col))
    return area


def rect_1_3_4(row, col):
    '''returns 1 IFF (row, col) is in the 3x4 rectangle in quadrant 1,
    that is, IFF 0 <= col < 4 and 0 <= row < 3
    0, 3 __ __ __ __ 4, 3
        |           |
        |           |
        |__ __ __ __|
    0, 0             4, 0
    '''
    if row < 0 or row > 2:
        return 0
    if col < 0 or col > 3:
        return 0
    return 1


def pmp_1_5_14_contains():
    '''Closure: this outer function returns a "contains" function
    for this shape in quadrant 1, without putting the boolean matrix
    representing it into the outer namespace.

    0, 7 .         __                   __         . 14, 7
                __|  |__             __|  |__
             __|   __   |__ __ __ __|   __   |__
          __|   __|  |__    __ __    __|  |__   |__
         |__   |__    __|  |__ __|  |__    __|   __|  Area: 42
            |__   |__|   __ __ __ __   |__|   __|
               |__    __|           |__    __|
         .        |__|                 |__|        .
    0, 0                                             14, 0
    '''
    bool_mat = [
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    ]
    def contains(row, col):
        '''returns bool_mat[row][col] if (row, col) is inside the bounding rectangle.'''
        if row < 0 or row > 6:
            return 0
        if col < 0 or col > 13:
            return 0
        # set_trace()
        # print("(%d, %d) -> " % (row, col), end='')
        # print(bool_mat[row][col])
        return bool_mat[row][col]
    # return the enclosed function:
    return contains


class BoundedGrid:
    '''Contiguous 2D grid specified by a containment function:
    contains(x, y) > 0 IFF the grid contains tile indexed by (x, y).
    The returned value may be regarded as the contained area of the tile.'''

    def __init__(self, contains, name=None):
        self.contains = contains
        self.name = name if name else contains.__name__

    def __repr__(self):
        '''reproducing expression'''
        return "%s(%s)" % (type(self).__name__, self.name)

    def __str__(self):
        '''informal toString'''
        return self.contains.__name__



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

def test_func_args(verbose, func, args, expect):
    '''
    tests the result of func applied to the *arguments against expect.
    Returns the number of wrong answers, that is,
    0 if result == expect,
    1 if not.
    '''
    result = func(*args)
    passed = result == expect
    if verbose > passed:
        print("%s(%s, %s) == %s, expected %s:  %s"
              % (func.__name__, args[0].__repr__(), args[1:], result, expect, "PASS" if passed else "FAIL"))
    return not passed

def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    num_wrong = 0
    grid = BoundedGrid(rect_1_3_4)
    num_wrong += test_func_args(args.verbose, reachable_area, (grid, 1, 1), 12)

    grid = BoundedGrid(pmp_1_5_14_contains(), pmp_1_5_14_contains.__name__)
    num_wrong += test_func_args(args.verbose, reachable_area, (grid, 1, 2), 42)

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
