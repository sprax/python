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

DEFAULT_START = 1
DEFAULT_COUNT = 4
DEFAULT_MAX_VAL = 2222

ONE_PLUS_EPS = 1.0 + sys.float_info.epsilon

def num_digits_log(num, base=10):
    '''returns number of digits in num as a non-negative decimal integer.
    Unless base != 10, in which case it returns the number of digits num
    would have in the specified base representation.
    NOTE: Without the ONE_PLUS_EPS factor, num_digits_log(1000 would return 3, not 4.
    '''
    return 1 + int(math.log(num * ONE_PLUS_EPS, base))

def num_digits_str(num):
    '''returns number of digits in num, when interpreted as a non-negative
    int and converted to a string.'''
    num = int(num)
    if num < 0:
        raise ValueError("num < 0")
    return len(str(num))



def next_palindromic_num_math(num):
    '''Given an integral num, compute the next palindromic number (strictly
    greater than num) using only arithmetic operations (and math.log for num_len).
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
    num_len = num_digits_log(num)
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


def palinums_math_gen(verbose=1):
    '''
    Generator for the sequence of palindromic natural numbers starting at 1,
    using only arithmetic.
    ret_num = 0,
    inc =   1,  c =  9, ret_num += inc: 1 2 3 4 5 6 7 8 9
    inc =   2,  c =  1, ret_num += inc: 11
    inc =  11,  c =  9, ret_num += inc: 22 33 44 55 66 77 88 99
    inc =   2,  c =  1, ret_num += inc: 101
    inc =  10,  c =  9, ret_num += inc: 111, 121, 131, 141, 151, 161, 171, 181, 191
    inc =  11,  c =  1, ret_num += inc: 202
    inc =  10,  c =  9, ret_num += inc: 212, 222, 232, ... 292
    inc =  11,  c =  1, ret_num += inc: 303
    inc =  10,  c =  9, ret_num += inc: 313, 323, 333, ... 393
    inc =  11,  c =  1, ret_num += inc: 404
       . . .
    inc =  10,  c =  9, ret_num += inc: 919, 929, 939, ... 999
    inc =   2,  c =  1, ret_num += inc: 1001
    inc = 110,  c =  9, ret_num += inc: 1111, 1221, 1331, ... 1991
    inc =  11,  c =  1, ret_num += inc: 2002
       . . .
    inc =  10,  c =  9, ret_num += inc: 9119, 9229, ... 9999
    inc =   2,  c =  1, ret_num += inc: 10001
    inc = 100,  c =  9, ret_num += inc: 10101, 10201, ... 10901
    inc = 110,  c =  1, ret_num += inc: 11011
    inc = 100,  c =  9, ret_num += inc: 11111, 11211, ... 11911
    inc = 110,  c =  1, ret_num += inc: 12021
    inc = 100,  c =  9, ret_num += inc: 12121, 12221, ... 12921
       . . .
    inc = 100,  c =  9, ret_num += inc: 19191, 19291, ... 19991
    inc =  11,  c =  1, ret_num += inc: 20002
    [(1, 9), (2, 1), (11, 8), (2, 1), (10, 9), (11, 1), (10, 9), (11, 1)]

    10901 + 110 -> 11011 + 100 -> 11111
    90909 + 110 -> 91019 + 100 -> 91119
    9009009 + 1100 -> 9010109
    9099909 + 110 -> 9111119
    900090009 + 11000 -> 900101009
    901090109 + 11000 -> 901101109
    '''
    iii, ret_num, inc, c, num_dig = 1, 0, 1, 0, 1
    even, first = True, True
    max_num, c_max = 9, 9
    while True:
        iii += 1
        if verbose > 1:
            print("%4d %4d %4d   %d/%d  %4d" % (iii, ret_num, inc, c, c_max, num_dig), end="\t")
        ret_num += inc
        yield ret_num
        c += 1
        if  c == c_max:
            if verbose > 3:
                print("c == c_max: %d == %d" % (c, c_max), end="\t")
            if  ret_num == max_num:
                if verbose > 2:
                    print("ret_num == max_num, so max_num: %d -> %d" % (max_num, max_num*10 + 9), end="\t")
                max_num = max_num * 10 + 9  # 9 -> 99 -> 999 -> 9999 ...
                num_dig += 1
                inc = 2
            else:
                if even:
                    if num_dig > 3:
                        if verbose > 1:
                            print("num_dig %d, even %s, and num_dig // 2 is %d" % (num_dig, even, num_dig//2), end="\t")
                        inc = 11 * (10 ** (num_dig // 2 - 1))
                    else:
                        inc = 11
                else:
                    if num_dig > 2 and num_dig % 2 == 0:
                        inc = 11
                    else:
                        inc = 10 ** (num_dig // 2)
                if verbose > 2:
                    print("%d != %d, c_max %d, c: %d, even: %s, and num_dig: %d, so inc -> %d"
                          % (ret_num, max_num, c_max, c, even, num_dig, inc), end="\t")
                even = not even
            if  c_max == 9:
                c_max = 1
                c = 0
            else:
                c_max = 9
                c = 0
                if  first:
                    first = False
                    c = 1
        if verbose > 1:
            print()




def next_palindromic_num_hybrid(num):
    '''
    returns the supremum palindrome of num, that is,
    the least palindromic number greater than or equal to num.
    Thus it returns num IFF num is already a palindrome;
    otherwise, it returns the next great palindromic number.
    '''
    if num == 9:
        return 11
    numd = int(num) + 1
    nums = str(numd)
    slen = len(nums)
    hlen = slen // 2
    olen = slen - hlen
    outa = [c for c in nums]
    # print("BEGIN: ", outa)
    add_ten = False
    rig_idx = slen
    for idx, lef_dig in enumerate(nums[:hlen]):
        rig_idx -= 1
        rig_dig = nums[rig_idx]
        if add_ten:
            if  rig_dig == '9':
                rig_dig =  '0'
            else:
                rig_dig = chr(ord(rig_dig) + 1)
                add_ten = False
        if lef_dig > rig_dig:
            outa[rig_idx] = lef_dig
        elif lef_dig < rig_dig:
            add_ten = True
            outa[rig_idx] = lef_dig
        else:
            outa[rig_idx] = lef_dig

    idx = hlen
    # # print("nums:", nums)
    # print("MIDDLE:", outa)
    # # print("idx:", idx)
    # # print("nums[idx]:", nums[idx])
    if add_ten:
        if hlen == olen:    # even length
            idx -= 1
            # print("even BEFORE idx %d,  dig %s" % (idx, outa[idx]))
            while outa[idx] == '9':
                outa[idx] = '0'
                outa[slen - 1 - idx] = '0'
                idx -= 1
            # print("even  AFTER idx %d,  dig %s" % (idx, outa[idx]))
            dig = chr(ord(outa[idx]) + 1)
            outa[idx] = dig
            outa[slen - 1 - idx] = dig
        else:
            if nums[idx] == '9':
                outa[idx] = '0'
                idx -= 1
                while nums[idx] == '9':
                    outa[idx] = '0'
                    outa[slen - 1 - idx] = '0'
                    idx -= 1
                dig = chr(ord(outa[idx]) + 1)
                outa[idx] = dig
                outa[slen - 1 - idx] = dig
            else:
                outa[idx] = chr(ord(nums[idx]) + 1)
    else:
        outa[idx] = nums[idx]

    return int(''.join(outa))
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
        return next_palindromic_num_hybrid(str(num + 1))
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
        print("%s: expected %s(%s) to be %s %s %s" % ("PASS" if passed else "FAIL",
                                                      is_palindrome.__name__,
                                                      string,
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
    parser.add_argument('-all', action='store_true', help='test all methods')
    parser.add_argument('start', type=int, nargs='?', default=DEFAULT_START,
                        help='first number in test domain (default: %d)' % DEFAULT_START)
    parser.add_argument('count', type=int, nargs='?', default=DEFAULT_COUNT,
                        help='how many numbers to generate (default: %d)' % DEFAULT_COUNT)
    parser.add_argument('maxval', type=int, nargs='?', default=DEFAULT_MAX_VAL,
                        help='stop if generated value > maxval (default: %d)' % DEFAULT_MAX_VAL)
    parser.add_argument('-test', action='store_true', help='test all outputs')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        vinfo = sys.version_info
        v_major = vinfo[0]
        v_minor = vinfo[1]
        ver_str = "Python%d.%d" % (v_major, v_minor)
        print(ver_str, sys.argv[0])
        print("args:", args)

    if args.all:
        num = args.start
        for idx in range(args.count):
            npn = next_palindromic_num_math(num)
            print("%4d  next_palindromic_num_math %4d -> %4d" % (idx, num, npn))
            # num += 1 + num/2 + 3 * (npn - num) / 4
            if args.test:
                test_one_string(is_palindrome_slice, True, args.verbose, str(npn))
            num = npn
        num = args.start
        for idx in range(args.count):
            npn = next_palindromic_num_hybrid(num)
            print("%4d  next_palindromic_num_hybrid %4d => %4d" % (idx, num, npn))
            if args.test:
                assert num < npn
                test_one_string(is_palindrome_slice, True, args.verbose, str(npn))
            num = npn

    for idx, num in enumerate(palinums_math_gen(args.verbose), 1):
        if  args.verbose == 1:
            print("pmg: %4d  %10d" % (idx, num))
        if  args.test:
            if test_one_string(is_palindrome_slice, True, 1, str(num)):
                break
        if  idx > args.count:
            break
        if  num > args.maxval:
            break
    print()


if __name__ == '__main__':
    main()
