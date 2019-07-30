#!/usr/bin/env python3
r'''
Given a word of length N, and n six-sided dice with a character in each side,
find out if this word is constructible by the set of given dice

RECURSIVE:
    A)  Natural order is just the word itself as a sequence:
        1.  Rollable(Word, Dice):
            for C in Word:
                for D in Dice:
                    if C in D:
                        if Dice\D is empty (or Tail := Word\C is empty):
                            return True
                        else:
                            if Rollable(Word\C, Dice\D):
                                return True
            return False
        2. O(N!), where N = 6 * len(word)
    B) Re-ordered recursion: IFF dice-letter distribution is known, look for rarest letter first
        1. Priority queue, most constrained first, to fail fast or succeed faster.
    C) Memoized recursion: If distribution is not known in advance, find it in a pre-pass,
       or add to it lazily as you go.  Banditry?
    D) Tail recursion?  The algoirithm in A.1. is not, as written.  Could these be made so?
DYNAMIC:
    A)  Make a hash table of all possible words from the dice and check if word is in hash
        1.  All possible strings would be wrong -- O(N!) for all permutations, or actually O(6^N)
        2.  Using a trie'd dictionary would be more like O(N^2 log N)

'''
from __future__ import print_function

import argparse
# import pdb
# from pdb import set_trace
# import random
# import re

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

###############################################################################

def can_roll_word_tail(head, tail, dice, verbose):
    ''' recursive head/tail word dice checker.  Is it tail-recursive? '''
    for die in dice:
        if head in die:
            if tail:
                # rest = dice.copy()    # needs Python 3
                rest = dice
                rest.remove(die)
                if verbose > 2:
                    print("Found head %s, look for tail %s in the rest: %s" % (head, tail, rest))
                if can_roll_word_tail(tail[0], tail[1:], rest, verbose):
                    return True
            else:
                if verbose > 1:
                    print("Found head %s and the tail is empty." % head)
                return True # The head was found and the tail is empty.
    return False


def dice_in_word_order_error(word, dice, verbose):
    ''' Returns 0 if dice list is already in word order, else an error measure '''
    if verbose > 0:
        print("test: word(%s)" % word)
        print("test: dice({})".format(dice))
    error = 0
    for letter, die in zip(word, dice):
        # set_trace()
        error += letter not in die
    return error

def can_roll_word(word, dice, verbose):
    ''' True IFF word can be made from give dice '''
    return can_roll_word_tail(word[0], word[1:], dice, verbose)

#
# def test_can_roll_word(word, dice, expect, verbose):
#     ''' True IFF can_roll_word result == expect '''
#     pass

def unit_test(args):
    ''' test Chrice (character-dice) stuff '''
    verbose = args.verbose
    word = 'fool'
    # dice = Chrix.from_chars('a','b','c','d','e','f')
    dice = [
        Chrix('a b c d e f'),
        Chrix('lololo'),
        Chrix('olives'),
        Chrix('jklmno'),
        ]

    num_wrong = 0
    # word_dice = [(word, dice)]
    expect = 1
    actual = can_roll_word(word, dice, verbose)
    num_wrong += (actual != expect)

    print("unit_test for can_roll_word:  num_tests:", 1,
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
