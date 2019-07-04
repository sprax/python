#!/usr/bin/env python3
r'''
Given a word of length N, and n six-sided dice with a character in each side,
find out if this word is constructible by the set of given dice

RECURSE:
    for C in Word:
        for D in Dice:
            if C in D:
                if Dice\D is empty (or Word\C is empty):
                    return True
                else:
                    return RECURSE
DYNAMIC:
ORDERED RECURSION:
'''
from __future__ import print_function

import argparse
# import pdb
# from pdb import set_trace
import random
import re

from collections import namedtuple


class Chrix(namedtuple("Chrix", "c1 c2 c3 c4 c5 c6")):
    '''Minimal class for 6-sided character die, based on namedtuple.'''
    __slots__ = ()

    def __str__(self):
        return "%s %s %s %s %s %s" % (self.c1, self.c2, self.c3, self.c4, self.c5, self.c6)

    def __new__(cls, str_6):
        '''create namedtuple class from raw tuple by parsing (splitting) a string'''
        try:
            return super(Chrix, cls).__new__(cls, *str_6.split()) # fastest whitespace parser
        except Exception:
            return super(Chrix, cls).__new__(cls, *list(str_6)) # assume no whitespace, Python 2 or 3

    @classmethod
    def from_chars(cls, c_1, c_2, c_3, c_4, c_5, c_6):
        '''create a Chrix object from 6 separate arguments'''
        return super(Chrix, cls).__new__(cls, c_1, c_2, c_3, c_4, c_5, c_6)



def can_roll_word(word, dice, verbose):
    ''' True IFF word can be made from give dice '''
    if verbose > 0:
        print("test: word(%s)" % word)
        print("test: dice({})".format(dice))
    return 0

def test_can_roll_word(word, dice, expect, verbose):
    ''' True IFF can_roll_word result == expect '''
    pass

def unit_test(args):
    ''' test Chrice (character-dice) stuff '''
    verbose = args.verbose
    word = 'fool'
    # dice = Chrix.from_chars('a','b','c','d','e','f')
    dice = [
        Chrix('a b c d e f'),
        Chrix('lololo'),
        Chrix('xyzabc'),
        Chrix('jklmno'),
        ]

    num_wrong = 0
    word_dice = [(word, dice)]
    expect = 0
    actual = can_roll_word(word, dice, verbose)
    num_wrong += (actual != expect)

    print("unit_test for has_one_repeated:  num_tests:", 1,
          " num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")


def main():
    '''driver for unit_test'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()

    unit_test(args)


if __name__ == '__main__':
    main()
