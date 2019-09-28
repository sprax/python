
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
def set_add(set, elt):
    ''' Add elt to set and return True IFF elt not already in set. '''
    if elt in set:
        return False
    set.add(elt)
    return True

def have_common_ancestor_ab(pairs, id_a, id_b):
    '''
    returns True if id_a and id_b have a common ancestor
    as found in parent-child pairs
    '''
    # anc_ddict = defaultdict(set) # for all ancestors of any
    # find all ancestors of id_a, id_b
    anc_set_a = set()
    anc_set_b = set()
    while True:
        anc_added = False
        for parent, child in pairs:
            print("PC", parent, child)
            if child == id_a or child in anc_set_a:
                anc_added = set_add(anc_set_a, parent)
            if child == id_b or child in anc_set_b:
                anc_added = set_add(anc_set_b, parent)
        if not anc_added:
            break
    print("anc_set_a:", anc_set_a)
    print("anc_set_b:", anc_set_b)
    return anc_set_a.intersection(anc_set_b)



def test_func_1(func_1, inputs, expect, verbose):
    '''
    tests whether func_1(inputs) == expect, and returns:
    0 if equal (result == expect),
    1 if not.
    '''
    result = func_1(*inputs)
    passed = result == expect
    if verbose > passed:
        print("%s %s:" % (func_1.__name__, "PASS" if passed else "FAIL"))
        print("inputs: %s" % inputs)
        print("expect: %s" % expect)
        print("result: %s" % result)
    return not passed


def unit_test(args):
    ''' test PCP Common Ancestor functions '''
    verbose = args.verbose
    num_wrong = 0
    pairs = [ParentChildPair(3, 1),
             ParentChildPair(7, 5),
             ParentChildPair(5, 3),
             ParentChildPair(23, 7),
             ParentChildPair(4, 2),
             ParentChildPair(8, 6),
             ParentChildPair(6, 4),
             ParentChildPair(23, 8),
            ]
    num_wrong += test_func_1(have_common_ancestor_ab, [pairs, 1, 2], {23}, 1)
    print("num_wrong:", num_wrong)
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
