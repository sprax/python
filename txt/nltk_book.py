#!/usr/bin/env python3
'''nltk_book.py'''

from collections import Counter
import nltk
from xdv import xdv, set_xdv_verbosity

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
    counter = Counter()
    for big in nltk.bigrams(text):
        if len(big[0]) > min_len and len(big[1]) > min_len:
            counter.update([big])
    return counter

def trigrams_counter(text, min_len, min_sum_len):
    '''Counter of trigrams'''
    counter = Counter()
    for trig in nltk.trigrams(text):
        len0 = len(trig[0])
        if len0 < min_len:
            continue
        len1 = len(trig[0])
        if len1 < min_len:
            continue
        len2 = len(trig[2])
        if len2 < min_len:
            continue
        if len0 + len1 + len2 < min_sum_len:
            continue
        counter.update([trig])
    return counter

def generate_cfd_max(cfdist, word, length=15):
    words = [word]
    for _ in range(length):
        word = cfdist[word].max()
        words.append(word)
    print(join_tokenized(words))

def generate_cfd_max_skip_dupes(cfdist, word, length=15):
    words = [word]
    for _ in range(length):
        word = cfdist[word].max()
        if word not in words:
            words.append(word)
    print(join_tokenized(words))

def generate_cfd_prob(cfdist, word, length=15):
    words = [word]
    for _ in range(length):
        freqs = cfdist[word]
        for word in sorted(freqs.keys(), key=freqs.get, reverse=True):
            xdv(1, "Try:", freqs[word], word)
            if word not in words:
                words.append(word)
                break
    print(join_tokenized(words))


def join_tokenized(tokens):
    '''Join tokens into a sentence; partial inverse of word_tokenize.'''
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation and i not in ["n't"]
        else i for i in tokens]).strip()


def test_nltk_book(text):
    '''test module methods'''
    trig_counter = trigrams_counter(text)

if __name__ == '__main__':
    test_nltk_book()
