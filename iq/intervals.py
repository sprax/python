
#!/usr/bin/env python3
'''
find or create disjoint intervals
'''

import argparse
import pdb
from pdb import set_trace
import random
from collections import namedtuple

Interval = namedtuple("Interval", "beg end")


'''
input: list of Intervals
output: sub-list of input that doesn't overlap

input
0:  [      ]
1:      [        ]
2:          [  ]

output
  [        ] [    ]
'''

def merged_disjoint_intervals(intervals):
    '''
    returns list of disjoint Intervals,
    wherein overlapping input Intervals are merged
    '''
    begasc = sorted(intervals, key=lambda x: x.beg)     # sort on Interval.beg
    result = [Interval(*begasc[0])]                     # clone Interval
    index = 0
    for elt in begasc[1:]:
        if elt.beg > result[index].end:
            result.append(Interval(*elt))
            index += 1
        elif elt.end > result[index].end:
            result[index] = Interval(result[index].beg, elt.end)
            # index stays the same
    return result


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
    const_a = "abcdefgh"
    const_b = "abc_efgh"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()

    unit_test(args)


if __name__ == '__main__':
    main()
