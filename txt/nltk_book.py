#!/usr/bin/env python3
'''nltk_book.py'''

from collections import Counter
import nltk

def lexical_diversity(text):
    '''ratio of word count to unique word count'''
    return len(text) / len(set(text))

def freq(text, word):
    '''frequency of a single word'''
    return text.count(word) / len(text)

def frac(text, word_set):
    '''fraction of text comprised of words in word_set'''
    total = sum([text.count(word) for word in word_set])
    return total / len(text)

def counter(text):
    '''Counter of words'''
    return Counter(text)

def bigrams_counter(text, min_len):
    '''Counter of bigrams'''
    big_counter = Counter()
    for big in nltk.bigrams(text):
        if len(big[0]) > min_len and len(big[1]) > min_len:
            big_counter.update([big])
    return big_counter

def trigrams_counter(text, min_len):
    '''Counter of trigrams'''
    big_counter = Counter()
    for trig in nltk.trigrams(text):
        if len(trig[0]) > min_len and len(trig[1]) > min_len:
            big_counter.update([trig])
    return big_counter

def test_nltk_book():
    '''test module methods'''

if __name__ == '__main__':
    test_nltk_book()
