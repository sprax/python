
#!/usr/bin/env python3
'''
log-uniform random numbers (numbers uniform in the distribution of their logarithms)
'''
import argparse
import math
# import pdb
# from pdb import set_trace
import random

def random_log_uniform(lo_exp, hi_exp, base=10, offset=0):
    '''
    returns random number from log uniform distribution for interval:
    [base**lo_exp, base**hi_exp] + offset
    '''
    exponent = random.uniform(lo_exp, hi_exp)
    raw_rand = math.pow(base, exponent)
    return raw_rand + offset


def test_1_10_100(count):
    ''' test
    '''
    range_all = [random_log_uniform(0, 2) for x in range(count)]
    range_1_10 = [x for x in range_all if x < 10]
    count_1_10 = len(range_1_10)
    range_10_100 = [x for x in range_all if x >= 10]
    count_10_100 = len(range_10_100)
    print("\n%d log-uniform samples partitioned into [1, 10) and [10, 100):" % count)
    print("count in [1, 10): %d" % count_1_10)
    print("count in [10, 100): %d" % count_10_100)
    return count_1_10, count_10_100


def test_1_10_100_1000(count):
    ''' test
    '''
    range_all = [random_log_uniform(0, 3) for x in range(count)]
    range_1_10 = [x for x in range_all if x < 10]
    count_1_10 = len(range_1_10)
    range_10_100 = [x for x in range_all if x >= 10 and x < 100]
    count_10_100 = len(range_10_100)
    range_100_1000 = [x for x in range_all if x >= 100]
    count_100_1000 = len(range_100_1000)
    print("\n%d log-uniform samples partitioned into [1, 10), [10, 100), and [100, 1000):" % count)
    print("count in [1, 10): %d" % count_1_10)
    print("count in [10, 100): %d" % count_10_100)
    print("count in [100, 1000): %d]" % count_100_1000)
    return count_1_10, count_10_100


def unit_test(args):
    ''' unit test '''
    test_1_10_100(args.count)
    test_1_10_100_1000(args.count)
    print()


def main():
    '''driver for unit_test'''
    default_count = 10000
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('count', type=int, nargs='?', default=default_count,
                        help='Sample count (default: %d)' % default_count)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()
    unit_test(args)

if __name__ == '__main__':
    main()
