#!/usr/bin/env python3
'''tests for various palindromes'''

from __future__ import print_function
import argparse
# import pdb
# from pdb import set_trace


def next_palindromic_num(num):
    '''case-based generation of next (greater) palindromic integer'''
    assert 0 <= num
    if num < 9:
        return num + 1
    if num == 10:
        return 11
    if num < 22:
        return 22
    if num < 33:
        return 33
    raise NotImplementedError("Not Yet Implemented for value %d > 32" % num)

def gen_palindromic_nums(num):
    '''case-based generation of next (greater) palindromic integer'''
    raise NotImplementedError("Not Yet Implemented for num == %d" % num)

def init_counter(count=0):
    '''(re)set counter that increments whenever called (closure)'''
    _count_dict = { 'count' : count }       # put the enclosed value in a dict
    def _increment_counter():               # to avoid rebinding (for Python 2)
        '''inner incrementer function'''
        _count_dict['count'] += 1
        return _count_dict['count']
    return _increment_counter


NUM = 0
def gen_even():
    '''yield all even natural numbers'''
    global NUM
    while True:
        NUM += 2
        yield num


def is_palindrome_slice(string):
    '''true IFF palindrome'''
    half_len = len(string) // 2
    for lef, rig in zip(string[0:half_len+1], string[-1:half_len-1:-1]):
        if lef != rig:
            return False
    return True

def is_chunky_palindrome(string):
    '''
    true IFF palindrome in chunks, as in:
    volvo -> (vo)l(vo)
    oliverelivo -> (o)(liv)(e)(r)(e)(liv)(o)
    Greedy algorithm should succeed.
    '''
    half_len = len(string) // 2
    beg = 0
    while beg < half_len:
        end = -1 - beg
        if string[beg] != string[end]:
            end = None if end == -1 else end + 1
            for med in range(beg+2, half_len+1):
                if string[beg:med] == string[-med:end]:
                    beg = med
                    break
            else:
                return False
        else:
            beg += 1
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


def test_is_palindrome(is_palindrome, expect_string_pairs, verbose=0):
    ''' tests an is_palindrome function and returns the number of wrong answers'''
    num_wrong = 0
    for expect, string in expect_string_pairs:
        num_wrong += test_one_string(is_palindrome, expect, verbose, string)
    return num_wrong

def unit_test(args):
    ''' test different (kinds of) palindrome detectors '''
    verbose = args.verbose
    expect_string_pairs = [
        [0, "volvo"],
        [0, "oliverelivo"],
        [1, "volvovlov"],
        [0, "XO"],
        [1, "ZZ"],
        [1, "XOX"],
    ]
    num_wrong = 0
    num_wrong += test_is_palindrome(is_palindrome_range, expect_string_pairs, verbose)
    num_wrong += test_is_palindrome(is_palindrome_slice, expect_string_pairs, verbose)
    expect_string_pairs[1][0] = expect_string_pairs[0][0] = 1
    num_wrong += test_is_palindrome(is_chunky_palindrome, expect_string_pairs, verbose)
    print("END palindromes.unit_test:  num_wrong: %d" % num_wrong)


def main():
    '''Extract questions from text?'''
    parser = argparse.ArgumentParser(description=unit_test.__doc__)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    unit_test(args)

def even_fib_gen():
    a,b = 1,2
    while True:
        yield b
        a,b = a+2*b, 2*a+3*b

if __name__ == '__main__':
    even_fibs = even_fib_gen()
    print("even_fibs.next returns:", even_fibs.next())
    print("even_fibs.next returns:", even_fibs.next())
    print("even_fibs.next returns:", even_fibs.next())
    print("even_fibs.next returns:", even_fibs.next())
    print("even_fibs.next returns:", even_fibs.next())
