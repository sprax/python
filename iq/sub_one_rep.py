#!/usr/bin/env python3
'''
find sub-lists with one repeated element
'''

import argparse
from collections import Counter
import pdb
from pdb import set_trace

def has_one_repeated(string):
    '''returns True IFF string contains exactly one repeated character.'''
    return True if len(string) - 1 == len(set(string)) else False

def num_repeat_1_subs_slow(string, sublen):
    '''returns the number of substrings of string, of length sublen,
    that contain exactly one repeated character.
    '''
    result = 0
    for k in range(len(string) + 1 - sublen):
        result += has_one_repeated(string[k:k + sublen])
    return result


def num_repeat_1_subs_counter(string, sublen):
    '''returns the number of substrings of string, of length sublen,
    that contain exactly one repeated character.
    '''
    totlen = len(string)
    if sublen > totlen:
        return 0

    # Initialize container representing the sliding window
    counter = Counter(string[0:sublen])
    sublen_m1 = sublen - 1
    result = 0

    for k in range(len(string) - sublen):
        if len(counter) == sublen_m1:
            result += 1
        char = string[k]
        if counter.get(char) == 1:
            counter.pop(char)
        else:
            counter.subtract(char)
        counter.update(string[k + sublen])

    # Check the last window position after the loop ends
    if len(counter) == sublen_m1:
        result += 1
    return result




def test_func_2(func_2, pair, expect, verbose):
    '''
    tests the result of func_2 applied to the pair of arguments against expect.
    Returns the number of wrong answers, that is,
    0 if result == expect,
    1 if not.
    '''
    result = func_2(*pair)
    passed = result == expect
    if verbose > passed:
        print("%s(%s, %d)  %s: expect: %s, result: %s"
              % (func_2.__name__, pair[0], pair[1], "PASS" if passed else "FAIL",
                 expect, result))
    return not passed


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    verbose = args.verbose
    samples = [
        [["abcd", 4], 0],
        [["abab", 2], 0],
        [["abac", 3], 1],
        [["abacadede", 3], 4],
    ]
    num_wrong = 0
    for sample in samples:
        num_wrong += test_func_2(num_repeat_1_subs_slow, *sample, verbose)
    for sample in samples:
        num_wrong += test_func_2(num_repeat_1_subs_counter, *sample, verbose)
    print("unit_test for has_one_repeated:  num_tests:", len(samples),
          " num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")


def main():
    '''driver for unit_test'''
    const_a = "abcdefgh"
    const_b = "abc_efgh"
    parser = argparse.ArgumentParser(description=has_one_repeated.__doc__)
    parser.add_argument('-a', type=str, nargs='?', const=const_a,
                        help="str_a to test against str_b (const: %s)" % const_a)
    parser.add_argument('-b', type=str, nargs='?', const=const_b,
                        help="str_b to test against str_a (const: %s)" % const_b)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    if  args.a and args.b:
        print("has_one_repeated(%s, %s) ? " % (args.a, args.b), end='')
        print(has_one_repeated(args.a))
    else:
        unit_test(args)


if __name__ == '__main__':
    main()
