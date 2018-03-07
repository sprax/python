#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
import pdb
from pdb import set_trace

def has_one_repeated(string):
    '''returns True IFF string contains exactly one repeated character.'''
    return True if len(string) - 1 == len(set(string)) else False

def num_repeat_1_subs_slow(string, sublen):
    '''returns the number of substrings of string, of length sublen,
    that contain exactly one repeated character.
    '''
    num = 0
    for k in range(len(string) - sublen):
        num += has_one_repeated(string[k:k + sublen])
    return num


def test_func_args(func_args, args, expect, verbose):
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
    verbose = args.verbose
    samples = [
        [["abcd", 4], 0],
        [["abab", 2], 0],
        [["abac", 3], 1],
    ]
    num_wrong = 0
    for sample in samples:
        num_wrong += test_func_args(num_repeat_1_subs_slow, *sample, verbose)
    print("unit_test for has_one_repeated:  num_tests:", len(samples),
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
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()
    if  args.a and args.b:
        print("has_one_repeated(%s, %s) ? " % (args.a, args.b), end='')
        print(has_one_repeated(args.a, args.b))
    else:
        unit_test(args)


if __name__ == '__main__':
    main()
