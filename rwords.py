#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''Class and script to solve simple substitution cipher from corpus and encoded text'''

import heapq
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
        self.cipher_chars = count_chars_from_words(self.cipher_words)
        self.corpus_chars = count_chars_from_words(self.corpus_words)
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

        # Looking at these most common corpus words only as a sanity-check
        corpai = self.corpus_short.most_common(2)
        corpchars = (corpai[0][0], corpai[1][0])
        if corpchars != ('a', 'I') and corpchars != ('I', 'a'):
            print("Unexpected most common 1-letter words in corpus: ", corpai)

        ciphai = self.cipher_short.most_common(2)
        if ciphai[0][0].islower():
            self.assign('a', ciphai[0][0])
            self.assign('i', ciphai[1][0])
        else:
            self.assign('a', ciphai[1][0])
            self.assign('i', ciphai[0][0])

    def find_the_and_and(self):
        '''Try to find the two most common English words: "the" and "and".'''
        print("Looking for the words 'the' and 'the'")

        # Looking at these most common corpus words only as a sanity-check
        corps = self.corpus_words.most_common(2)
        words = (corps[0][0], corps[1][0])
        if words != ('the', 'and') and words != ('and', 'the'):
            print("Unexpected most common 3-letter words in corpus: ", corps)

        most_freq_ciphs = self.cipher_chars.most_common(2)
        probable_e = most_freq_ciphs[0][0]
        alternate_e = most_freq_ciphs[0][0]
        found_and = False
        found_the = False
        for item in self.cipher_words.most_common(10):
            ciph = item[0]
            if len(ciph) == 3:
                if not found_the and (ciph[2] == probable_e or ciph[2] == alternate_e):
                    found_the = True
                    self.assign('t', ciph[0])
                    self.assign('h', ciph[1])
                    self.assign('e', ciph[2])
                if not found_and and ciph[0] == self.forward_map['a']:
                    found_and = True
                    self.assign('n', ciph[1])
                    self.assign('d', ciph[2])

    def find_words_from_ciphers(self):
        '''Find common corpus words comprised mostly of known inverse
        cipher chars, and try filling in the missing letters.  Trials
        are evaluated by scoring how many decoded cipher words then 
        match corpus words.  The highest score wins.  (That is, the 
        decision is immediate, not defered to accumulate multiple
        scoring passes or backpropogating votes.'''

        corpus = self.corpus_words.most_common(4000)
        pq = [] # priority = [num_unknown(updated on pop), -count, length]
        for item in self.cipher_words.items():
            ciph = item[0]
            count = item[1]
            entry = [self.num_unknown(ciph), -count, len(ciph), ciph]
            heapq.heappush(pq, entry)

        sentinel = ''   # terminate loop when seen twice
        while pq:
            unknowns, neg_count, length, ciph = heapq.heappop(pq)
            if unknowns == 0:
                continue
            unknowns = self.num_unknown(ciph)   # update in case any of its chars were discovered
            if unknowns == 1:
                print('Trying to match: ', ciph, unknowns, -neg_count)
                for item in corpus:
                    if len(item[0]) == length:
                        word = item[0]
                        for idx in range(length):
                            inv = self.inverse_map[ciph[idx]]
                            if inv != 0 and word[idx] != inv:
                                break
                            else:
                                if self.forward_map[word[idx]] == 0:
                                    self.assign(word[idx], ciph[idx])
            elif unknowns > 1:
                if ciph == sentinel:
                    print('Breaking from queue at: ', ciph, unknowns, -neg_count)
                    break
                elif not sentinel:
                    # Set the sentinel and give each item still in the queue
                    # a chance to update its unknowns.  Some may change to 1
                    # and get matched.  Quit when the sentinel comes back to
                    # the front.
                    sentinel = ciph
                    print('Replacing at end of queue: ', ciph, unknowns, -neg_count)
                    heapq.heappush(pq, [1000, 0, length, ciph])
            else:
                print ('Discarding: ', ciph, unknowns, -neg_count)

    def num_unknown(self, ciph):
        '''returns the number of unknown cipher characters in the string ciph'''
        return sum(map(lambda x: self.inverse_map[x] == 0, ciph))

def decipher_file(cipher_file, corpus_file):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.'''

    subs = SubCipher(cipher_file, corpus_file)

    print("corpus_words:")
    for (word, count) in subs.corpus_words.most_common(10):
        print(word, count)

    subs.find_a_and_I()
    subs.find_the_and_and()
    subs.find_words_from_ciphers()

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

def count_chars_from_words(word_counter):
    '''Count chars from all words times their counts'''
    char_counter = Counter()
    for item in word_counter.items():
        for _ in range(item[1]):
            char_counter.update(item[0])
    ##for c in char_counter.keys():
    ##    print(c, ' : ', char_counter[c])
    return char_counter

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
