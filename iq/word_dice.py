
#!/usr/bin/env python3
'''
Given a word of length n, and n six-sided dice with a character in each side,
find out if this word is constructible by the set of given dice
'''
from __future__ import print_function

import argparse
# import pdb
# from pdb import set_trace
import random

from collections import namedtuple


class Chrix(namedtuple("Chrix", "c1 c2 c3 c4 c5 c6")):
    '''Minimal class for 6-sided character die, based on namedtuple.'''
    __slots__ = ()

    def __str__(self):
        return "%s  %s  %s  %s  %s  %s" % (self.c1, self.c2, self.c3, self.c4, self.c5, self.c6)


def unit_test(args):
    ''' test Chrice (character-dice) stuff '''
    verbose = args.verbose
    inlist_1 = [['a'], [.5, 1.5]]
    outlst_1 = [[0, 1.5], [2, 2.4], [2.5, 2.667]]
    inlist_2 = list(inlist_1)   # copy
    random.shuffle(inlist_2)    # shuffle in place
    samples = [
        [inlist_1, outlst_1],
        [inlist_2, outlst_1],
    ]

    num_wrong = 0
    for sample in samples:
        num_wrong += test_func_1(merged_disjoint_pairs, sample[0], sample[1], verbose)
        intervals = [Chrice(x[0], x[1]) for x in inlist_1]
        expecteds = [Chrice(y[0], y[1]) for y in outlst_1]
        num_wrong += test_func_1(merged_disjoint_intervals, intervals, expecteds, verbose)

    print("unit_test for has_one_repeated:  num_tests:", len(samples),
          " num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")


def main():
    '''driver for unit_test'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()

    unit_test(args)


if __name__ == '__main__':
    main()
