#!/usr/bin/env python3
import argparse
import itertools
import random
DEFAULT_SEED = 12345

PAIR_SUMS = [
    2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7,
    7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12]

def dice_pair_sum():
    ''' Sums of two random dice throws:
    2   1   11
    3   2   12, 21
    4   3   13, 31, 22
    5   4   14, 23, 32, 41
    6   5   15, 24, 33, 42, 51
    7   6   16, 25, 34, 43, 52, 61
    8   5   26, 35, 44, 53, 62
    9   4   36, 45, 54, 63
    10  3   46, 55, 64
    11  2   56, 65
    12  1   66
    -- --
       36
    '''
    rdx = random.randint(0, 35)
    return PAIR_SUMS[rdx]


def dice_pair_sum_gen():
    ''' generator on dice_pair_sum '''
    while True:
        yield dice_pair_sum()


def main():
    ''' driver for dice_pair_sum_gen'''
    default_file = '../words.txt'
    parser = argparse.ArgumentParser(description=dice_pair_sum_gen.__doc__)
    parser.add_argument('count', type=int, nargs='?', const=16, default=10,
                        help='Count of randomly sampled dice pair sums (const: 16, default: 10)')
    parser.add_argument('-islice', action='store_true',
                        help='use itertools.islice instead of list comprehension')
    parser.add_argument('-seed', type=int, nargs='?', const=1, default=12345,
                        help='seed for random (const: 1,  default: 12345)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    print("args.count:", args.count)

    if args.seed:
        random.seed(args.seed)                   # repeatability

    if args.islice:
        if args.verbose > 0:
            print("Using itertools.islice:")
        sums = list(itertools.islice(dice_pair_sum_gen(), 0, args.count, 1))
    else:
        if args.verbose > 0:
            print("Using list comprehension:")
        sums = [next(dice_pair_sum_gen()) for _ in range(args.count)]
    print("Sums:", sums)


if __name__ == '__main__':
    main()
