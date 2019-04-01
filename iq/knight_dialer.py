#!/usr/bin/env python3
''' How can a chess knight jump around on a 10-digit dialing pad?
    1   2   3
    4   5   6
    7   8   9
        0

    To construct the numbers dialed, you need a table:
    0   :   4,  6
    1   :   6,  8
    2   :   7,  9
    3   :   4,  8
    4   :   0,  3,  9
    5   :   None
    6   :   0,  1,  7
    7   :   2,  6
    8   :   1,  3
    9   :   2,  4

    But since every sequence produces a unique number, you don't need
    to define equivalence classes or track numbers already visited.
    So if you only want to know how many numbers R can be dialed by
    N knight moves, you need only table the numers of possibler moves:
    { 0 : 2, 1: 2, 2: 2, ...}

    In short, 5 => None, 4 and 6 => 3, and the other seven => 2.
    So all you need to know is that after any move but the first,
    7 of the resulting numbers each give 2 next choices, and
    2 of them each give 3 choices:

    N   R
    1   10  (land on any 1st number, even the dead-end 5)
    2   20  = 7 * 2   +     2 * 3
    3   46  = 7 * 2 * 2  +  2 * 3 * 3   = 28 + 18
    4  110  = 7 * 2**3   +  2 * 3**3    = 56 + 54
    5  274  = 7 * 2**4   +  2 * 3**4    = 56 * 2  +  54 * 3  = 112 + 162

    So the count-only knight-dialer function can be represented as:
    N --> { N = 1: 10
          , N > 1: 7 * 2**(N-1) + 2 * 3**(N-1) }

    You could memoize the 2 addends if you really want to optimize
    computing the value of this 2-term polynomial.
'''
import argparse
from itertools import islice
from random import randint, seed
DEFAULT_SEED = 12345

PAIR_SUMS = [
    2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7,
    7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12]


def dice_pair_sum():
    ''' Sum value from the one throw of a pair of dice '''
    rdx = randint(0, 35)
    return PAIR_SUMS[rdx]


def dice_pair_sum_gen():
    ''' generator on dice_pair_sum '''
    while True:
        yield dice_pair_sum()

def dice_pair():
    ''' returns random values for one throw of a pair of dice '''
    return (randint(1, 6), randint(1, 6))


def main():
    ''' driver for dice_pair_sum_gen'''
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
        seed(args.seed)                   # repeatability

    if args.islice:
        if args.verbose > 0:
            print("Using itertools.islice:")
        sums = list(islice(dice_pair_sum_gen(), 0, args.count, 1))
    else:
        if args.verbose > 0:
            print("Using list comprehension:")
        sums = [next(dice_pair_sum_gen()) for _ in range(args.count)]

    print("Sums:", sums)
    print("Pair:", dice_pair())


if __name__ == '__main__':
    main()
