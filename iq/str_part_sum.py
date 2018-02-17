#!/usr/bin/env python3
'''
Partition a String of Digits (SoD) in such manner that, when converted to numbers,
the Kth substring is the sum of (K-1)'th and (K-2)'nd substring for K > 2.
If such partition is not possible, then return an empty list.
Examples:
1) given "1111223" then return [1, 11, 12, 23]
2) given "1111213" then return [11, 1, 12, 13]
3) given "11121114" then return []
'''
import argparse
import pdb
from pdb import set_trace

def printv(level, verbose, *args, **kwargs):
    '''print args with kwargs if level < verbose'''
    if level < verbose:
        print(*args, **kwargs)


def str_part_sum(sod, verbose=1):
    '''
    returns the first parsed number list found if the given string of digits (SOD)
    can be segmented such that, when converted to numbers, the i'th substring is
    the sum of (i-1)'th and (i-2)'nd substring throughout.
    Examples:
        "1111213"   ->  [11, 1, 12, 13]
        "11121114"  ->  []
    '''
    size = len(sod)
    for beg_2 in range(1, size):
        printv(3, verbose, "beg_2:", beg_2, "\t\t\t _____", sod[0:beg_2], sod[beg_2:])
        int_1 = int(sod[0:beg_2])
        for beg_3 in range(1 + beg_2, size):
            int_2 = int(sod[beg_2:beg_3])
            printv(2, verbose, "\tbeg_3:", beg_3, "\t\t _____", sod[0:beg_2], sod[beg_2:beg_3], sod[beg_3:])
            num_list = str_part_sum_rec(sod[beg_3:], size - beg_3, [int_1, int_2], max(beg_2, beg_3), verbose)
            if num_list:
                return num_list
    return []


def str_part_sum_rec(sod, size, num_list, min_num_digits, verbose=1):
    '''continue'''
    assert len(num_list) > 1
    if size == 0:
        return num_list

    int_1 = num_list[-2]
    int_2 = num_list[-1]
    for end_3 in range(1, size + 1):
        int_3 = int(sod[0:end_3])
        is_sum = int_1 + int_2 == int_3
        printv(1, verbose, "\t\tend_3: %2d =>\t%2d + %2d %s= %3d" % (end_3, int_1, int_2, '=' if is_sum else '!', int_3))
        if is_sum:
            num_list.append(int_3)
            new_list = str_part_sum_rec(sod[end_3:], size - end_3, num_list, max(min_num_digits, end_3), verbose)
            if new_list:
                return new_list
    return []


def test_str_part_sum(sod, expect, verbose=1):
    '''test is_str_part_sum(sod)'''
    print("___________ is_str_part_sum(%s) ? Expect: %s" % (sod, expect))
    result = str_part_sum(sod, verbose)
    failed = result != expect
    print("___________ is_str_part_sum(%s)   Result: %s  --  %s\n" % (sod, result, "FAIL" if failed else "PASS"))
    return failed

def unit_test(verbose):
    '''test examples'''
    num_wrong = 0
    num_wrong += test_str_part_sum("11", [])
    num_wrong += test_str_part_sum("113", [])
    num_wrong += test_str_part_sum("1123", [1, 1, 2, 3])
    num_wrong += test_str_part_sum("11224", [])   # 1 + 1 == 2 and 2 + 2 == 4 but 1 + 2 != 2
    num_wrong += test_str_part_sum("12315", [12, 3, 15], verbose)
    num_wrong += test_str_part_sum("12324", [1, 23, 24], verbose)
    num_wrong += test_str_part_sum("1111213", [11, 1, 12, 13], verbose)
    num_wrong += test_str_part_sum("1111223", [1, 11, 12, 23], verbose)
    print("unit_test for str_part_sum: num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")

def main():
    '''Extract questions from text?'''
    const_sod = "123581321345589144"
    parser = argparse.ArgumentParser(description=str_part_sum.__doc__)
    parser.add_argument('-digits', type=str, nargs='?', const=const_sod,
                        help="string of digits to test, instead of running unit_test "
                        "(const: %s)" % const_sod)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    verbose = args.verbose

    if args.digits:
        nums = str_part_sum(args.digits, verbose)
        print("{} -> {}".format(args.digits, nums))
    else:
        unit_test(verbose)

if __name__ == '__main__':
    main()
