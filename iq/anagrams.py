#!/usr/bin/env python3
'''tests for various string predicates'''

import argparse
from collections import Counter
# import pdb
# from pdb import set_trace


def is_anagram_in_text(string, text):
    '''true IFF an anagram of string appears in text'''
    total = len(string)
    found = 0
    anagram = Counter(string)
    matched = None
    idx = 0
    len_text = len(text)
    while idx < len_text:
        char = text[idx]
        anum = anagram.get(char)
        if anum:
            if  matched is None:
                matched = Counter(char)
                found = 1
                start = idx
            else:
                fnum = matched.get(char, 0)
                if fnum < anum:
                    matched.update(char)
                    found += 1
                    if found == total:
                        return True
                else:
                    # fnum > 0.  Go back to start and subtract counts until Ok,
                    while text[start] != char:
                        matched.subtract(text[start])
                        found -= 1
                        start += 1
                    start += 1
        else:
            found = 0
            matched = None
        idx += 1
    return False


def test_predicate(predicate, verbose, expect, string, text):
    '''
    tests the predicate function on one string.
    Returns the number of wrong answers, that is,
    0 if predicate matches expect,
    1 if it does not.
    '''
    result = predicate(string, text)
    passed = result == expect
    if verbose > passed:
        print("%s %s: expected %s:  %s  %s" % (predicate.__name__,
                                               "PASS" if passed else "FAIL",
                                               expect, string, text))
    return not passed


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    verbose = args.verbose
    samples = [
        [0, "oo", "volvo"],
        [1, "lo", "volvo"],
        [1, "xyz", "volvoyyxzx"],
        [1, "xyxz", "volxyzvxoyyxzx"],
        [0, "xyxzz", "volxyzvxoyyxzx"],
    ]
    num_wrong = 0
    for sample in samples:
        num_wrong += test_predicate(is_anagram_in_text, verbose, *sample)
    print("END anagrams.unit_test:  num_wrong: %d" % num_wrong)


def main():
    '''Extract questions from text?'''
    parser = argparse.ArgumentParser(description=unit_test.__doc__)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    unit_test(args)


if __name__ == '__main__':
    main()
