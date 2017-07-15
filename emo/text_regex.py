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

EXAMPLES = [
    # (text, words, syllables)
    ("There isn't one empyrean ouroborous; everyone knows there've always been several.", 11, 24),
    #  1   2  3  4   5  6 78   9 0 1  2   3 4* 5     6     7  8   9  0    1    2 3 4
    ('"There aren\'t really any homogeneous cultures," you\'ll say, "they\'ve always shown rifts."', 12, 21),
    #   1   2        3   5 6 7  8 9 0 1 2   3  4        5      6      7      8  9     0    1
    ('"Ain\'t all y\'all young\'uns under 17," she\'d said, "like 11- or 15-years old?!"', 13, 21),
    #  1     2      3    4     5   6  7  +3     1     2      3   +3  7  +2  0    1}
    ("Didn't you know my X-15's XLR-99 engine burned 15,000 pounds (6,717 kg) of propellant in 87 seconds?", 17, 35),
    # 1  2   3    4   5 6 +2    +3 +2 4  5    6     +2  +2  1     +3  +8 +3  6    7 8  9   0  +3  4 5
    (" _This Is _My_ Title_, you one-eyed jack-ass!!", 7, 11),
    #    1  2   3  4  5  6     7  8   9    0   1
]

# WORD_SEP_INTERIOR = r"',."
WORD_SEP_INTERIOR = r"-',."

###############################################################################
RE_WORD_TOKEN = re.compile(r"((?:\w+[{}]\w*)+\w|\w+)".format(WORD_SEP_INTERIOR))

def word_tokens(sentence):
    '''
    Returns tokens comprised of word chars (\w) embedding one or more single
    interior punctuation characters (',.-) ').  Because \w matches _, tokens
    are stripped of _ (underscores) at either end.
    '''
    words = RE_WORD_TOKEN.findall(sentence)
    return [word.strip('_') for word in words]

###############################################################################
RE_NOT_NON_WORD_TOKEN = re.compile(r"((?:[^\W_]+[{}][^\W_]*)+[^\W_]|[^\W_]+)".format(WORD_SEP_INTERIOR))

def notnonword_tokens(sentence):
    '''
    Returns tokens comprised of not non-word chars (\W and _) surrounding one or more
    individual interior punctuation characters (-',.) ').  Because \w matches _,
    \W does not match _, so we must add it to the characters that cannot begin, end, or
    be contained inside a word.
    '''
    return RE_NOT_NON_WORD_TOKEN.findall(sentence)
    # return [word.strip('_') for word in words]


def replace_non_non_words(rep_func, text_phrase):
    return RE_NOT_NON_WORD_TOKEN.sub(rep_func, text_phrase)

###############################################################################
WORD_SEP_EXTERIOR = r'!"#$%&()*+./:;<=>?@[\]^_`{|}~\x82\x83\x84\x85\x86\x87\x88\x89' \
                    r'\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99'

RE_WORD_SEP = re.compile(r"(?:\s+[{}]+\s*|\s*[{}]+\s+|[{}]*[\s{}]+|\s+)".format(
    WORD_SEP_INTERIOR, WORD_SEP_INTERIOR, WORD_SEP_INTERIOR, WORD_SEP_EXTERIOR))

def word_splits(sentence_body):
    splits = RE_WORD_SEP.split(sentence_body)
    return [ss for ss in splits if len(ss) > 0]

RE_SENTENCE_ENDS = re.compile(r"(\w.*)\b(?=\W*$)")

def sentence_body_and_end(sentence):
    '''return sentence parts as [beg, body, end] where beg and end may be 0-length'''
    return RE_SENTENCE_ENDS.split(sentence)

# The < is for <3, <=, <--, etc.
WORD_EXT_BEG = r'[<]'

# The . is for abbreviations; any sentence-ending punctuation should already be removed.
WORD_EXT_END = r'[_%.>]'

RE_WORD_EXT = re.compile(r"((?:{}?[\w]+[{}]*)[\w]+{}?|{}?\w{}?)".format(
    WORD_EXT_BEG, WORD_SEP_INTERIOR, WORD_EXT_END, WORD_EXT_BEG, WORD_EXT_END))

def replace_words_extended(rep_func, text_phrase):
    return RE_WORD_EXT.sub(rep_func, text_phrase)

###############################################################################
REGEX_PUNCTUATION = re.compile("[{}]".format(string.punctuation))
REGEX_NON_ALPHA = re.compile(r'(?:\W|[0-9])+')
###############################################################################

def main():
    '''test regex patterns for text: separate words'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input_file')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    # test_misc()

    print("NUM_TOKENS          WORD_TOKENS:")
    for sentence, words, syllables in EXAMPLES:
        print("MANUAL", words, sentence)
        tokens = word_tokens(sentence)
        print("TOKENS", len(tokens), tokens)
        swords = word_splits(sentence)
        print("SPLITS", len(swords), swords)
        nuwrds = notnonword_tokens(sentence)
        print("NOTUNS", len(nuwrds), nuwrds)
        print()

if __name__ == '__main__':
    main()
