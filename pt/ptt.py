#!/usr/bin/env python3
'''
pytorch tutorial stuff
'''

from __future__ import print_function
import argparse
# import pdb
# from pdb import set_trace
import torch


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    x = torch.Tensor(5, 3)
    print(x)

    num_wrong = 0
    print("unit_test:  num_tests:", 1,
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
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()


    unit_test(args)


if __name__ == '__main__':
    main()
