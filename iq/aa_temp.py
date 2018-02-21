#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
# import pdb
# from pdb import set_trace


def _is_subs_dist_1_eq_len(s_a, s_b, start_dist):
    '''
    returns True IFF 1 == substitution-only distance between s_a and s_b,
    assuming len(s_a) == len(s_b), and given a starting distance of 0 or 1
    (due to alignment).
    '''
    dist = start_dist
    for a, b in zip(s_a, s_b):
        if a != b:
            dist += 1
            if dist > 1:
                return False
    return 1 == dist


def is_subs_dist_1(s_a, s_b):
    '''
    returns True IFF 1 == substitution-only distance between s_a and s_b,
    where any difference in length also adds to substitution count.
    '''
    len_a = len(s_a)
    len_b = len(s_b)
    dif_a_b = len_a - len_b
    if  dif_a_b == 0:
        return _is_subs_dist_1_eq_len(s_a, s_b, 0)
    if  dif_a_b == -1:
        dif_a_b = 1
        s_a, s_b = s_b, s_a         # swap
    if  dif_a_b == 1:              # s_a is one character longer than s_b
        if s_a[0] == s_b[0]:
            return _is_subs_dist_1_eq_len(s_a[0:-1], s_b, 1)
        if s_a[1] == s_b[0]:
            return _is_subs_dist_1_eq_len(s_a[1:], s_b, 1)
    return False


def test_predicate(predicate, verbose, expect, str_a, text):
    '''
    tests the predicate function on one str_a.
    Returns the number of wrong answers, that is,
    0 if predicate matches expect,
    1 if it does not.
    '''
    result = predicate(str_a, text)
    passed = result == expect
    if verbose > passed:
        print("%s %s: expected %s:  %s  %s" % (predicate.__name__,
                                               "PASS" if passed else "FAIL",
                                               expect, str_a, text))
    return not passed


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    verbose = args.verbose
    samples = [
        [0, "abc", "abc"],
        [1, "abc", "abcd"],
        [1, "abcd", "bcd"],
        [1, "pqrs", "pors"],
        [0, "pqrs", "pqsr"],
        [0, "pqrs", "pqst"],
        [0, "pqrs", "pqrstu"],
    ]
    num_wrong = 0
    for sample in samples:
        num_wrong += test_predicate(is_subs_dist_1, verbose, *sample)
    print("unit_test for is_subs_dist_1:  num_tests:", len(samples),
          " num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")


def main():
    '''driver for unit_test'''
    const_a = "abcdefgh"
    const_b = "abc_efgh"
    parser = argparse.ArgumentParser(description=is_subs_dist_1.__doc__)
    parser.add_argument('-a', type=str, nargs='?', const=const_a,
                        help="str_a to test against str_b (const: %s)" % const_a)
    parser.add_argument('-b', type=str, nargs='?', const=const_b,
                        help="str_b to test against str_a (const: %s)" % const_b)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    if  args.a and args.b:
        print("is_subs_dist_1(%s, %s) ? " % (args.a, args.b), end='')
        print(is_subs_dist_1(args.a, args.b))
    else:
        unit_test(args)


if __name__ == '__main__':
    main()
