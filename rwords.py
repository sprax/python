#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
""" Print cleaned-up space-separated 'words' from text file."""

import re
import sys
##from string import punctuation
##from collections import defaultdict
from collections import Counter

def decipher_file(cipher_file, corpus_file):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.'''

    cipher_counts = count_words(cipher_file)
    corpus_counts = count_words(corpus_file)


def count_words(file):
    '''Returns a Counter that has counted all ASCII-only words found in a text file.'''
    ##rgx_split = re.compile(r'[\d\s{}]+'.format(re.escape(punctuation)))
    rgx_match = re.compile(r"[A-Za-z]+")
    counter = Counter()
    with open(file, 'r') as text:
        for line in text:
            ##words = re.split(rgx_split, line.rstrip())
            words = re.findall(rgx_match, line.rstrip())
            print(words)
            words = [x.lower() if len(x) > 1 else x for x in words]
            for word in words:
                wordlen = len(word)
                if wordlen > 0:
                    print(word, counter[word])
                else:
                    print('Zero-lenght word!')
            print(words)
            counter.update(words)
    return counter

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
