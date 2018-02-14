#!/usr/bin/env python3
import argparse



def is_palindrome(string):
    '''true iff palindrome'''
    half_len = len(string) // 2
    for j in range(half_len):
        if  string[j] != string[-j-1]:
            return False
    return True



def test_is_palindrome(expect, string, verbose=0):
    ''' tests is_palindrome and returns the number of wrong answers, that is,
    0 if is_palindrome matches expect, 1 if it does not. '''
    is_pal = is_palindrome(string)
    passed = is_pal == expect
    if verbose > passed:
        print("%s: %s palindrome: %s %s" % ("PASS" if passed else "FAIL",
                                            "Yes" if expect else "Not",
                                            " "*(24 - len(string)),
                                            " ".join(string)))
    return not passed


def unit_test(args):
    ''' test palindromes and others '''
    verbose = args.verbose
    num_wrong = 0
    num_wrong += test_is_palindrome(0, "volvo", verbose)
    num_wrong += test_is_palindrome(1, "volvovlov", verbose)
    num_wrong += test_is_palindrome(1, "XX", verbose)
    num_wrong += test_is_palindrome(0, "XOX", verbose)
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
