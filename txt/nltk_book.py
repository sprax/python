#!/usr/bin/env python3
'''nltk_book.py'''

from collections import Counter

def lexical_diversity(text):
    '''ratio of word count to unique word count'''
    return len(text) / len(set(text))

def counter(text)
    return Counter(text)

def freq(text, word):
    return text.count(word) / len(text)

def frac(text, word_set):
    total = sum([text.count(word) for word in word_set])
    return total / len(text)


def test_nltk_book():
    '''test module methods'''

if __name__ == '__main__':
    test_nltk_book()
