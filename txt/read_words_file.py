#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''
import re
import sys
from utf_print import utf_print

def print_words(fspec):
    with open(fspec, 'r', encoding="utf8") as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    utf_print(word)
            utf_print(words)

if __name__ == '__main__':
    fspec = sys.argv[1] if len(sys.argv) > 1 else 'text.txt'
    print_words(fspec)
