#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plan:
    Words|phrases -> words >= [phonetic syllables reprs]
    Emojis >= [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import argparse
import random
import re
import string
from collections import defaultdict

import emoji
import emotuples

EXAMPLES = {
    "There isn't one empyrean ouroborous; everyone knows there've always been several." : 24,
    #  1   2  3  4   5  6 78   9 0 1  2   3 4* 5     6     7  8   9  0    1    2 3 4
    '"There aren\'t really any homogeneous cultures," you\'ll say, "they\'ve always shown rifts."' : 21,
    #   1   2        3   5 6 7  8 9 0 1 2   3  4        5      6      7      8  9     0    1
    '"Ain\'t all y\'all young\'uns under 17," she\'d said, "like 11- or 15-years old?!"' : 21,
    #  1     2      3    4     5   6  7  +3     1     2      3   +3  7  +2  0    1}
    "Didn't you know my X-15's XLR-99 engine burned 15,000 pounds (6,717 kg) of propellant in 87 seconds?" : 35,
    # 1  2   3    4   5 6 +2    +3 +2 4  5    6     +2  +2  1     +3  +8 +3  6    7 8  9   0  +3  4 5
}

def qw(ss):
    return ss.split()

VOWEL_GROUPS = qw('a ae ai ay e ea ei eu ey i ie iou o oa oi ou oy u')

###############################################################################
WORD_SEP_INTERIOR = r"',.-"
RE_WORD_TOKEN = re.compile(r"((?:\w+[{}]\w*)+\w|\w+)".format(WORD_SEP_INTERIOR))

def word_tokens(sentence):
    return RE_WORD_TOKEN.findall(sentence)

###############################################################################
WORD_SEP_EXTERIOR = r'!"#$%&()*+./:;<=>?@[\]^_`{|}~\x82\x83\x84\x85\x86\x87\x88\x89' \
                    r'\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99'

RE_WORD_SEP = re.compile(r"(?:\s+[{}]+\s*|\s*[{}]+\s+|[{}]*[\s{}]+|\s+)".format(
    WORD_SEP_INTERIOR, WORD_SEP_INTERIOR, WORD_SEP_INTERIOR, WORD_SEP_EXTERIOR))

def word_splits(sentence):
    splits = RE_WORD_SEP.split(sentence)
    return [ss for ss in splits if len(ss) > 0]

###############################################################################
REGEX_PUNCTUATION = re.compile("[{}]".format(string.punctuation))
REGEX_NON_ALPHA = re.compile(r'(?:\W|[0-9])+')

###############################################################################
def qw_list(ss):
    return re.split(r'\W+', ss.rstrip())

def qw_tuple(ss):
    return tuple(qw_list(ss))

def main():
    '''test english -> emoji translation'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input_file')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-no_articles', action='store_true',
                        help='replace articles (a, an, the) with nothing')
    parser.add_argument('-subtraction', action='store_true',
                        help='allow subtraction of letters or syllables')
    parser.add_argument('-number', dest='max_lines', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-truncate', dest='max_words', type=int, nargs='?',
                        const=8, default=0,
                        help='truncate sentences after MAX words (default: INT_MAX)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    # test_misc()
    # print('VOWEL_GROUPS:', VOWEL_GROUPS, '\n')

    for key, val in EXAMPLES.items():
        print("MANUAL", val, key)
        tokens = word_tokens(key)
        print("TOKENS", len(tokens), tokens)
        swords = word_splits(key)
        print("SPLITS", len(swords), swords)
        print()


if __name__ == '__main__':
    main()
