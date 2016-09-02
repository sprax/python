#!/usr/bin/env python3
# Sprax Lines       2016.09.01      Written with Python 3.5
'''How many ways have writers written "No"?

Usage: python3 nos.py [adverb_file [corpus_file [verbosity]]]
Where: TBD
'''

import heapq
import re
import sys
from collections import defaultdict
from collections import Counter

import utfprint

class GetNo:
    '''Counts ways of saying No'''
    def __init__(self, adverb_file, corpus_file, verbose):
        self.adverb_file = adverb_file
        self.corpus_file = corpus_file
        self.corpus_words = word_counts(corpus_file)
        self.dialogue = defaultdict(int)

        self.verbose = verbose
        if self.verbose > 1:
            print("The dozen most common corpus words and their counts:")
            for word, count in self.corpus_words.most_common(12):
                print("\t", word, "\t", count)

    def find_no(self):
        '''Look for ways of sayning No'''

    def show_no(self):
        '''Show frequent ways of saying No'''

def uprint(*objects, sep=' ', end='\n', outfile=sys.stdout):
    '''Prints non-ASCII Unicode (UTF-8) characters in a safe (but possibly
    ugly) way even in a Windows command terminal.  Unicode-enabled terminals
    such as on Mac or KDE have no problem, nor do most IDE's, but calling
    Python's built-in print to print such characters (e.g., an em-dash)
    from a Windows cmd or Powershell terminal causes errors such as:
    UnicodeEncodeError: 'charmap' codec can't encode characters in position 32-33:
    character maps to <undefined> '''
    enc = outfile.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=outfile)
    else:
        enc_dec = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(enc_dec, objects), sep=sep, end=end, file=outfile)

def char_range_inclusive(first, last, step=1):
    '''ranges from specified first to last character, inclusive, in
    any character set, depending only on ord()'''
    for char in range(ord(first), ord(last)+1, step):
        yield chr(char)


def read_file_lines(path):
    '''reads a text file into a list of lines'''
    lines = []
    with open(path, 'r') as text:
        for line in text:
            lines.append(line.rstrip())
    return lines

def count_words(path):
    '''Returns a Counter that has counted all ASCII-only words found in a text file.'''
    rgx_match = re.compile(r"[A-Za-z]+")
    counter = Counter()
    with open(path, 'r') as text:
        for line in text:
            words = re.findall(rgx_match, line.rstrip())
            words = [x.lower() if len(x) > 1 else x for x in words]
            counter.update(words)
    return counter

def word_counts_short_and_long(path, max_short_len):
    '''Returns two Counters containing all the ASCII-only words found in a text file.
       The first counter counts only words up to length max_short_len, as-is.
       The second counter contains all the longer words, but lowercased.'''
    rgx_match = re.compile(r"[A-Za-z]+")
    short_counter = Counter()
    other_counter = Counter()
    with open(path, 'r', encoding="utf8") as text:
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
    return char_counter

def find_no_simple_substition_cipher(adverb_file, corpus_file, verbose):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.
    Uses the GetNo class.
    '''
    subs = GetNo(adverb_file, corpus_file, verbose)
    subs.find_no()

def main():
    '''Get file names for cipher and corpus texts and call
    find_no_simple_substition_cipher.'''

    # simple, inflexible arg parsing:
    argc = len(sys.argv)
    if argc > 4:
        print(sys.argv[0])
        print(__doc__)
        exit(0)

    # Get the paths to the files (relative or absolute)
    adverb_file = sys.argv[1] if argc > 1 else r'cipher.txt.bak'
    corpus_file = sys.argv[2] if argc > 2 else r'corpus.txt.bak'
    verbose = int(sys.argv[3]) if argc > 3 else 1

    find_no_simple_substition_cipher(adverb_file, corpus_file, verbose)


if __name__ == '__main__':
    main()
