
#!/usr/bin/env python3
'''
find or create disjoint intervals
'''
from __future__ import print_function

import argparse
# import pdb
# from pdb import set_trace
import random
from collections import namedtuple

Interval = namedtuple("Interval", "beg end")


'''
input: list of Intervals
output: sub-list of input that doesn't overlap
'''

hobos = [
	[ 0 ], 			 # expected Parkour answer: NONE
	[ 0 ],			 # expected Ahopper answer: NONE
	[ 1,  2, 3 ], 	 # expected Parkour answer: 3, only one way
	[ 2,  2, 2 ],	 # expected Ahopper answer: 2 (first move 1, not 2)
	[ 1,  2, 2, 1 ], # expected Parkour answer: 3 (2 ways, via index 2 or 3)
	[ 2,  2, 1, 1 ], # expected Ahopper answer: 3 (2 ways, via index 1 or 2)
	[ 1,  9, 6 ],				# P 3
	[ 3,  1, 1 ],				# H 1
	[ 1,  6, 4, 5, 3 ],			# P 5
	[ 2,  2, 0, 1, 2 ],			# H 1
	[ 1, 11, 4, 4, 3 ],			# P 4
	[ 4,  0, 1, 2, 0 ],			# H 2
	[ 0,  2, 1, 2, 1, 3, 2, 5, 1, ],			# expected answer: 5
	[ 4,  1, 1, 4, 0, 2, 1, 1, 1, ],			# expected answer: 3
	[ 0,  1, 0, 3, 8, 2, 1, 7, 3, 4, 8, 5, 0, 4, 7, 7, 3, 8, 10, 5, 8, ],
	[ 3,  2, 4, 2, 2, 1, 0, 3, 2, 6, 3, 3, 9, 1, 7, 1, 8, 3,  1, 3, 0, ],
]

def park(ho, bo):
    '''
    counts Parkour moves
    '''
    sz = len(ho)
    assert sz == len(bo)
    mv, eg = [], []
    for j in range(sz):
    return mv[-1]


def merged_disjoint_pairs(intervals):
    '''
    returns list of disjoint interval pairs as 2-element lists,
    wherein overlapping input intervals are merged (no tuples).
    '''
    begasc = sorted(intervals, key=lambda x: x[0])  # sort by beginning (first list val)
    result = [list(begasc[0])]                      # clone first pair-list
    index = 0
    for elt in begasc[1:]:
        if elt[0] > result[index][1]:
            result.append(list(elt))                # clone
            index += 1
        elif result[index][1] < elt[1]:
            result[index][1] = elt[1]
            # index stays the same
    return result


def test_func_1(func_1, inputs, expect, verbose):
    '''
    tests whether func_1(inputs) == expect, and returns:
    0 if equal (result == expect),
    1 if not.
    '''
    result = func_1(inputs)
    passed = result == expect
    if verbose > passed:
        print("%s %s:" % (func_1.__name__, "PASS" if passed else "FAIL"))
        print("inputs: %s" % inputs)
        print("expect: %s" % expect)
        print("result: %s" % result)
    return not passed


def unit_test(args):
    ''' test disjoint interval functions '''
    verbose = args.verbose
    inlist_1 = [[0, 1], [.5, 1.5], [2, 2.3], [2.1, 2.2], [2.3, 2.4], [2.5, 2.667]]
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
        intervals = [Interval(x[0], x[1]) for x in inlist_1]
        expecteds = [Interval(y[0], y[1]) for y in outlst_1]
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
