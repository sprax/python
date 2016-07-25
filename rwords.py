#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
""" Print cleaned-up space-separated 'words' from text file."""

import re
import sys
from string import punctuation

def decipher_file(cipher_file, corpus_file):
    ##rgx_split = re.compile(r'[\d\s{}]+'.format(re.escape(punctuation)))
    rgx_match = re.compile(r"[A-Za-z]+")
    with open(cipher_file, 'r') as f:
        for line in f:
            ##words = re.split(rgx_split, line.rstrip())
            words = re.findall(rgx_match, line.rstrip())
            for word in words:
                if len(word) > 0:
                    print(word)
            print(words)

def main():
    """ Get file names for cipher and corpus texts and call decipher_file."""

    # simple, inflexible arg parsing:
    numArgs = len(sys.argv)
    if numArgs > 2:
        print(sys.argv[0])
        print(rwords.__doc__)

    # Get the paths to the files (relative or absolute)
    cipher_file = sys.argv[1] if len(sys.argv) > 1 else r'cipher.txt'
    corpus_file = sys.argv[2] if len(sys.argv) > 2 else r'corpus.txt'

    decipher_file(cipher_file, corpus_file)


if __name__ == '__main__':
    main()
