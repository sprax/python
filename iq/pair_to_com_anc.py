
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
from collections import defaultdict


ParentChildPair = namedtuple("ParentChildPair", "parent child")



'''
input: list of parent-child ID pairs, and two child IDs.
output: common ancestors: bool, first, or full set.

'''

def have_common_ancestor(pairs, id_a, id_b):
    '''
    returns True if id_a and id_b have a common ancestor
    as found in parent-child pairs
    '''
    # find all ancestors of id_a
    anc_set_a = set()
    anc_dct_a = defaultdict(list)
    for parent, child in pairs:
        print("PC", parent, child)
        if child == id_a:
            anc_set_a.add(parent)
    return False




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
    ''' test PCP CA functions '''
    verbose = args.verbose
    num_wrong = 0
    pairs = [ParentChildPair(1, 3),
             ParentChildPair(3, 5),
             ParentChildPair(5, 7),
             ParentChildPair(7, 23),
             ParentChildPair(2, 4),
             ParentChildPair(4, 6),
             ParentChildPair(6, 8),
             ParentChildPair(8, 23),
            ]
    have = have_common_ancestor(pairs, 1, 2)
    print("have:", have)
    return num_wrong


def main():
    '''driver for unit_test'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()

    unit_test(args)


if __name__ == '__main__':
    main()
