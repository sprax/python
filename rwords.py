#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''Class and script to solve simple substitution cipher from corpus and encoded text'''

import re
import sys
##from string import punctuation
from collections import defaultdict
from collections import Counter

class SubCipher:
    '''Solver to infer a simple substituion cipher based on a large
    corpus and small sample of encoded text.   Assumes English for
    boot-strapping off these four words: I, a, the, and.'''
    def __init__(self, cipher_file, corpus_file):
        self.cipher_file = cipher_file
        self.corpus_file = corpus_file
        self.cipher_short, self.cipher_words = count_short_and_lowered_long_words(cipher_file, 1)
        self.corpus_short, self.corpus_words = count_short_and_lowered_long_words(corpus_file, 1)
        self.forward_map = defaultdict(int)
        self.inverse_map = defaultdict(int)

    def assign(self, corp, ciph):
        self.forward_map[corp] = ciph
        self.inverse_map[ciph] = corp
        print('        ', corp, " -> ", ciph)

    def find_a_and_I(self):
        '''Try to find the word "I" as the most common capitalized
        single-letter word, and "a" as the most common lowercase
        single-letter word.  Assuming English, obviously.'''
        print("Looking for the words 'a' and 'I'")
        ciphai = self.cipher_short.most_common(2)
        corpai = self.corpus_short.most_common(2)
        print(ciphai, corpai)
        corpchars = (corpai[0][0], corpai[1][0])
        if corpchars == ('a', 'I') or corpchars == ('I', 'a'):
            if ciphai[0][0].islower():
                self.assign('a', ciphai[0][0])
                self.assign('i', ciphai[1][0])
            else:
                self.assign('a', ciphai[1][0])
                self.assign('i', ciphai[0][0])
        else:
            print("Unexpected most commont 1-letter words in corpus: ", corpchars)


def decipher_file(cipher_file, corpus_file):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.'''

    subs = SubCipher(cipher_file, corpus_file)

    print("corpus_counts:")
    for (word, count) in subs.corpus_words.most_common(10):
        print(word, count)

    subs.find_a_and_I()

def count_words(file):
    '''Returns a Counter that has counted all ASCII-only words found in a text file.'''
    ##rgx_split = re.compile(r'[\d\s{}]+'.format(re.escape(punctuation)))
    rgx_match = re.compile(r"[A-Za-z]+")
    counter = Counter()
    with open(file, 'r') as text:
        for line in text:
            ##words = re.split(rgx_split, line.rstrip())
            words = re.findall(rgx_match, line.rstrip())
            words = [x.lower() if len(x) > 1 else x for x in words]
            ##print(words)
            counter.update(words)
    return counter

def count_short_and_lowered_long_words(file, max_short_len):
    '''Returns two Counters containing all the ASCII-only words found in a text file.
       The first counter counts only words up to length max_short_len, as-is.
       The second counter contains all the longer words, but lowercased.'''
    rgx_match = re.compile(r"[A-Za-z]+")
    short_counter = Counter()
    other_counter = Counter()
    with open(file, 'r') as text:
        for line in text:
            short = []
            other = []
            words = re.findall(rgx_match, line.rstrip())
            for word in words:
                if len(word) <= max_short_len:
                    short.append(word)
                else:
                    other.append(word.lower())
            short_counter.update(short)
            other_counter.update(other)
    return short_counter, other_counter

def main():
    '''Get file names for cipher and corpus texts and call decipher_file.'''

    # simple, inflexible arg parsing:
    argc = len(sys.argv)
    if argc > 2:
        print(sys.argv[0])
        print(__doc__)

    # Get the paths to the files (relative or absolute)
    cipher_file = sys.argv[1] if argc > 1 else r'cipher.txt'
    corpus_file = sys.argv[2] if argc > 2 else r'corpus.txt'

    decipher_file(cipher_file, corpus_file)


if __name__ == '__main__':
    main()
