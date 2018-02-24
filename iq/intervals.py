
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
    returns list of disjoint intervals,
    wherein overlapping input intervals are merged
    '''
    sorts = sorted(intervals, key=lambda x: x.beg)
    result = [Interval(*sorts[0])]
    index = 0
    for elt in sorts[1:]:
        if elt.beg > result[index].end:
            result.append(Interval(*elt))
            index += 1
        elif elt.end > result[index].end:
            result[index] = Interval(result[index].beg, elt.end)
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
    inputs_1 = [Interval(0, 1), Interval(.5, 1.5), Interval(2, 2.3), Interval(2.1, 2.2), Interval(2.5, 2.667)]
    expect_1 = [Interval(0, 1.5), Interval(2, 2.3), Interval(2.5, 2.667)]
    inputs_2 = list(inputs_1)   # copy
    random.shuffle(inputs_2)    # shuffle in place
    samples = [
        [inputs_1, expect_1],
        [inputs_2, expect_1],
    ]
    num_wrong = 0
    for sample in samples:
        num_wrong += test_func_1(merged_disjoint_intervals, sample[0], sample[1], verbose)

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
