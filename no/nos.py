#!/usr/bin/env python3
# Sprax Lines       2016.09.01      Written with Python 3.5
'''How many ways have writers written "No"?

Usage: python3 nos.py [adverb_file [corpus_file [verbosity]]]
Where: TBD
'''

import heapq
import itertools
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
        self.corpus_words = count_words(corpus_file)
        self.adverb_freqs = load_counted_word_file(adverb_file)
        self.corpus_adverbs = count_counted_words(self)
        self.verbose = verbose
        numfreq = 4

        print("print_paragraphs:")
        print_paragraphs(corpus_file)

        self.replies = find_quoted_replies(corpus_file)

        if self.verbose > 1:
            print("The", numfreq, "most common corpus words:")
            for word, count in self.corpus_words.most_common(numfreq):
                print('    {:>7d} {}'.format(count, word))

        print("All adverbs in the corpus:")
        for word, count in self.corpus_adverbs.items():
            print(word, count)

        print("The", numfreq, "most common corpus adverbs:")
        for word in sorted(self.corpus_adverbs.keys(), key=self.corpus_adverbs.get,
            reverse=True)[:numfreq]:
            count = self.corpus_adverbs[word]
            print('    {:>7d} {}'.format(count, word))

        print("The", numfreq, "most common reply phrases:")
        for phrase, count in self.replies.most_common(numfreq*10):
            print('    {:>7d} {}'.format(count, phrase))


    def find_no(self):
        '''Look for ways of sayning No'''

    def show_no(self):
        '''Show frequent ways of saying No'''



def paragraphs(fileobj, separator='\n'):
    """Iterate a fileobject by paragraph"""
    ## Makes no assumptions about the encoding used in the file
    lines = []
    for line in fileobj:
        if line == separator and lines:
            yield ' '.join(lines)
            lines = []
        else:
            lines.append(line)
    yield ' '.join(lines)

def paragraphs_re(fileobj, separator='\n'):
    """Iterate a fileobject by paragraph"""
    ## Makes no assumptions about the encoding used in the file
    lines = []
    for line in fileobj:
        if re.match(separator, line) and lines:
            yield ' '.join(lines)
            lines = []
        else:
            line = line.rstrip()
            if line:
               lines.append(line)
    yield ' '.join(lines)


def print_paragraphs(path):
    with open(path) as f:
        for idx, para in enumerate(paragraphs_re(f)):
            print("    Paragraph {}:".format(idx))
            print(para)
            print()

def count_counted_words(self):
    word_counts = {}
    for word in self.adverb_freqs.keys():
        count = self.corpus_words[word]
        if count > 0:
            word_counts[word] = count
    return word_counts

def load_counted_word_file(path):
    '''reads a text file of format <count word> into a dictionary'''
    word_counts = {}
    with open(path, 'r') as text:
        for line in text:
            count, word = line.split()
            word_counts[word] = count
            # print(count, word)
    return word_counts

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

def find_quoted_replies(path):
    '''Finds first 3 (or fewer) words starting quoted replies.  
       Returns a defaultdict mapping these phrases to their counts.
       Words longer than 1-letter are lowercased.'''
    rgx_quoted_B = re.compile(r'(["])(?:(?=(\\?))\2.)*?\1')
    rgx_quoted_A = re.compile(r'([^"]+)')
    rgx_quoted = re.compile(r'"([^"]*)"')
    rgx_word = re.compile(r"[A-Za-z]+")
    counter = Counter()
    idx = 0
    with open(path, 'r', encoding="utf8") as text:
        for para in paragraphs_re(text):
            quotes = re.findall(rgx_quoted, para)
            phrases = []
            for quote in quotes:
                print("quote {}: {}".format(idx, quote))
                idx += 1
                phrase = []
                words = re.findall(rgx_word, quote)
                for word in words[:3]:
                    if len(word) == 1:
                        phrase.append(word)
                    else:
                        phrase.append(word.lower())
                phrases.append(' '.join(phrase))
                counter.update(phrases)
    print(phrases)
    return counter

def count_chars_from_words(word_counter):
    '''Count chars from all words times their counts'''
    char_counter = Counter()
    for item in word_counter.items():
        for _ in range(item[1]):
            char_counter.update(item[0])
    return char_counter

def find_quoted_no_phrases(adverb_file, corpus_file, verbose):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.
    Uses the GetNo class.
    '''
    subs = GetNo(adverb_file, corpus_file, verbose)
    subs.find_no()

def main():
    '''Get file names for cipher and corpus texts and call
    find_quoted_no_phrases.'''

    # simple, inflexible arg parsing:
    argc = len(sys.argv)
    if argc > 4:
        print(sys.argv[0])
        print(__doc__)
        exit(0)

    # Get the paths to the files (relative or absolute)
    adverb_file = sys.argv[1] if argc > 1 else r'adverb.txt'
    corpus_file = sys.argv[2] if argc > 2 else r'corpus.txt'
    verbose = int(sys.argv[3]) if argc > 3 else 3

    find_quoted_no_phrases(adverb_file, corpus_file, verbose)


if __name__ == '__main__':
    main()
