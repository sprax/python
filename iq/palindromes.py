#!/usr/bin/env python3
import argparse



def is_palindrome_range(string):
    '''true IFF palindrome'''
    half_len = len(string) // 2
    for j in range(half_len):
        if  string[j] != string[-j-1]:
            return False
    return True


def is_palindrome_slice(string):
    '''true IFF palindrome'''
    half_len = len(string) // 2
    for lef, rig in zip(string[0:half_len], string[-1:half_len:-1]):
        if  lef != rig:
            return False
    return True

def is_span_palindrome(string):
    '''true IFF palindrome'''
    half_len = len(string) // 2
    for j in range(half_len):
        if  string[j] != string[-j-1]:
            return False
    return True



def test_one_string(is_palindrome, expect, verbose, string):
    '''
    tests the is_palindrome function on one string.
    Returns the number of wrong answers, that is,
    0 if is_palindrome matches expect,
    1 if it does not.
    '''
    is_pal = is_palindrome(string)
    passed = is_pal == expect
    if verbose > passed:
        print("%s %s: expected %s: %s %s" % (is_palindrome.__name__,
                                             "PASS" if passed else "FAIL",
                                             expect,
                                             " "*(24 - len(string)),
                                             " ".join(string)))
    return not passed


def test_is_palindrome(is_palindrome, verbose=0):
    ''' tests an is_palindrome function and returns the number of wrong answers'''
    num_wrong = 0
    num_wrong += test_one_string(is_palindrome, 0, verbose, "volvo")
    num_wrong += test_one_string(is_palindrome, 1, verbose, "volvovlov")
    num_wrong += test_one_string(is_palindrome, 1, verbose, "ZZ")
    num_wrong += test_one_string(is_palindrome, 1, verbose, "XOX")
    return num_wrong

def unit_test(args):
    ''' test palindromes and others '''
    verbose = args.verbose
    num_wrong = 0
    num_wrong += test_is_palindrome(is_palindrome_range, verbose)
    num_wrong += test_is_palindrome(is_palindrome_slice, verbose)
    print("END palindromes.unit_test:  num_wrong: %d" % num_wrong)


def main():
    '''Extract questions from text?'''
    parser = argparse.ArgumentParser(description="Validate balance and order of "
                                     "parentheses, braces, and brackets (), {}, []")
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    unit_test(args)


if __name__ == '__main__':
    main()
