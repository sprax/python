#!/usr/bin/env python3
''' tests for various palindromes using Python 3 generators
    Python 2.7 *can* run this version.
'''
from __future__ import print_function
import argparse
import math
import sys
# import pdb
# from pdb import set_trace

ONE_PLUS_EPS = 1.0 + sys.float_info.epsilon
DEFAULT_BEG = 0
DEFAULT_END = 41

def num_digits(num, base=10):
    '''returns number of digits in num as a decimal integer.
    Unless base != 10, in which case it returns the number of digits num
    would have in the specified base representation.
    NOTE: Without the ONE_PLUS_EPS factor, num_digits(1000 would return 3, not 4.
    '''
    return 1 + int(math.log(num * ONE_PLUS_EPS, base))


def next_palindromic_num(num):
    '''Given an integral num, compute the next palindromic number (strictly
    greater than num) using only arithmetic operations.
    TODO: better argument checking?
    '''
    num = int(num)  # Try to convert arg to int.  TODO: Raise on any non-integral arg?
    if num < 0:     # Negative numbers are not palindromes due to the "-"
        return 0
    if num < 9:
        return num + 1
    if num < 11:
        return 11
    num += 1
    # print("num %d incremented to %d" % (num-1, num))
    num_len = num_digits(num)
    lef_den = 10 ** (num_len - 1)
    rig_den = 1
    haf_len = num_len // 2
    evn_max = (num_len + 1) // 2 - 1
    for idx in range(haf_len):
        lef_dig = (num // lef_den) % 10
        rig_dig = (num // rig_den) % 10
        # print("\nidx %d,  num %d: lef_dig, rig_dig == (%d, %d)" % (idx, num, lef_dig, rig_dig))
        if  lef_dig > rig_dig:
            # print("simple: lef_dig %d > %d rig_dig" % (lef_dig, rig_dig))
            num += (lef_dig - rig_dig)*rig_den
        elif lef_dig < rig_dig:
            add_num = num + rig_den*10
            nxt_dec = (num / lef_den + 1) * lef_den # a.k.a. lef_dig + 1) * lef_den)
            # print("add_num == num + rig_den*10 = %d + %d*%d = %d" % (num, rig_den, 10, add_num))
            # print("        >? (%d / %d + 1) * %d = %d * %d = %d" % (num, lef_den, lef_den, num/lef_den + 1, lef_den, nxt_dec))
            if add_num > nxt_dec:
                # print("----- carry numbers -----  num %d -> %d > %d   " % (num, add_num, nxt_dec))
                num += rig_den*10 + rig_den*(1 + lef_dig - rig_dig)
            else:
                # print("---- no carry ----")
                num += rig_den*10 + rig_den*(lef_dig - rig_dig)
        lef_den /= 10
        rig_den *= 10
    return  num


def _sup_palindromic_num_str(num_str):
    '''
    returns the supremum palindrome of the num in num_str, that is,
    the least palindromic number greater than or equal to num.
    Thus it returns num IFF num_str is already a palindrome, and otherwise
    it returns the next great palindromic number.
    '''
    assert(isinstance(num_str, str))
    slen = len(num_str)
    hlen = slen // 2
    mlen = (slen + 1) // 2
    pref = num_str[:mlen]

    outa = []
    for idx, dig in enumerate(num_str):
        if  dig > num_str[slen - 1 - idx]:
            outa.append(dig)

    suff = ''.join(outa)[::-1]
    return int(pref + suff)

    # raise NotImplementedError("Not Yet Implemented for value %d > 32" % num)


def next_palindromic_num_cb(num):
    '''case-based generation of next (greater) palindromic integer'''
    assert 0 <= num
    if num < 9:
        return num + 1
    if num < 11:
        return 11
    if num < 22:
        return 22
    if num < 33:
        return 33
    if num < 99:
        return _sup_palindromic_num_str(str(num + 1))
    raise NotImplementedError("Not Yet Implemented for value %d > 98" % num)






def is_palindrome_slice(string):
    '''true IFF palindrome'''
    half_len = len(string) // 2
    for lef, rig in zip(string[0:half_len+1], string[-1:half_len-1:-1]):
        if lef != rig:
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


def test_is_palindrome(is_palindrome, expect_string_pairs, verbose=0):
    ''' tests an is_palindrome function and returns the number of wrong answers'''
    num_wrong = 0
    for expect, string in expect_string_pairs:
        num_wrong += test_one_string(is_palindrome, expect, verbose, string)
    return num_wrong

def unit_test():
    ''' tests '''


def main():
    '''palindromic numbers'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('beg', type=int, nargs='?', default=DEFAULT_BEG,
                        help='first number in test range (default: %d' % DEFAULT_BEG)
    parser.add_argument('end', type=int, nargs='?', default=DEFAULT_END,
                        help='last number in test range (default: %d' % DEFAULT_END)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    vinfo = sys.version_info
    v_major = vinfo[0]
    v_minor = vinfo[1]
    ver_str = "Python %d.%d" % (v_major, v_minor)
    print(ver_str)

    num = 0
    for idx in range(args.end):
        nxt = next_palindromic_num(num)
        print("%3d  next_palindromic_num(%4d) -> %4d" % (idx, num, nxt))
        # num += 1 + num/2 + 3 * (nxt - num) / 4
        num = nxt
    return

    even_fibs = even_fib_gen()
    print("Python %s: next(even_fibs) yields: %d" % (ver_str, next(even_fibs)))
    print("Python %s: next(even_fibs) yields: %d" % (ver_str, next(even_fibs)))
    # print("Python %s: next(even_fibs) yields: %d" % (ver_str, next(even_fibs)))
    # print("Python %s: next(even_fibs) yields: %d" % (ver_str, next(even_fibs)))
    # print("Python %s: next(even_fibs) yields: %d" % (ver_str, next(even_fibs)))
    # if v_major < 3:
    #     raise Exception("Call this script with Python 3")
    for idx, num in enumerate(even_fib_gen()):
        if idx > 12:
            break;
        print("for-loop:  %2d  %30d" % (idx, num))
    # unit_test(args)
    num = 51
    for _ in range(10):
        npn = next_palindromic_num_cb(num)
        print("next_palindromic_num_cb(%4d) == %4d\n" % (num, npn))
        num = npn



if __name__ == '__main__':
    main()
