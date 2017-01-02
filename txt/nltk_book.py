#!/usr/bin/env python3
'''nltk_book.py'''

import re
import random
import string
from collections import Counter
import nltk
from xdv import xdv

NLTK_VERBOSITY = 1

def set_nltk_verbosity(verbosity):
    '''Set the modul-global variable NLTK_VERBOSITY'''
    global NLTK_VERBOSITY
    print("Setting NLTK_VERBOSITY = {}".format(verbosity))
    NLTK_VERBOSITY = verbosity


def lexical_diversity(text):
    '''ratio of word count to unique word count'''
    return len(text) / len(set(text))

def text_vocab(text):
    '''set of lower-case words in text'''
    return set(w.lower() for w in text if w.isalpha())

def odd_words(text):
    '''originally: unusual_words'''
    all_vocab = text_vocab(text)
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    odd_vocab = all_vocab - english_vocab
    return sorted(odd_vocab)

def lexical_oddity(text):
    '''fraction of text's vocab not in NLTK's standard English vocab'''
    all_vocab = text_vocab(text)
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    odd_vocab = all_vocab - english_vocab
    return len(odd_vocab) / len(all_vocab)

def freq(text, word):
    '''frequency of a single word'''
    return text.count(word) / len(text)

def frac(text, word_set):
    '''fraction of text comprised of words in word_set'''
    total = sum([text.count(word) for word in word_set])
    return total / len(text)

def text_counter(text):
    '''Counter of words'''
    return Counter(text)

def bigrams_counter(text, min_len):
    '''Counter of bigrams'''
    counter = Counter()
    for big in nltk.bigrams(text):
        if len(big[0]) < min_len or len(big[1]) < min_len:
            continue
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

def filter_string_punct(tokenized):
    '''Filter out all tokens that are substrings of string.punctuation.'''
    for token in tokenized:
        if token not in string.punctuation:
            yield token

SENTENCE_PUNCTUATION = '!"\'()*+,./:;<>?[\\]^_`{|}~'

def filter_sentence_punct(tokenized):
    '''Filter out tokens that are substrings of string.punctualtion'''
    for token in tokenized:
        if token not in SENTENCE_PUNCTUATION:
            yield token

NLTK_PUNCTUATION_PATTERN = re.compile("[{}]".format(string.punctuation))

def filter_words_with_punct(tokenized):
    '''Filter out all tokens containing any punctuation.'''
    for token in tokenized:
        if not re.match(NLTK_PUNCTUATION_PATTERN, token):
            yield token

def join_tokenized(tokens):
    '''Join tokens into a sentence; partial inverse of word_tokenize.'''
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation
        and i not in ["n't"]
        else i for i in tokens]).strip()

def generate_cfd_max(cfdist, word, length=15):
    '''Generate sequence of up to length words,
    maximizing bigram frequency, duplicate words OK.'''
    words = [word]
    for _ in range(length):
        word = cfdist[word].max()
        words.append(word)
    return join_tokenized(words)

def generate_cfd_max_uniq(cfdist, word, length=15):
    '''Generate sequence of N words, maximizing bigram frequency except in the
    case of duplicates, where N <= length.'''
    words = [word]
    for _ in range(length):
        freqs = cfdist[word]
        for word in sorted(freqs.keys(), key=freqs.get, reverse=True):
            xdv(NLTK_VERBOSITY, "Try:", freqs[word], word)
            if word not in words:
                words.append(word)
                break
    return join_tokenized(words)

#Some fun ones using this function on bigrams from Moby Dick:
# The voyages now show white whale shakes down certain mathematical symmetry
# The Narwhale has ever new made what prodigious black foam that interval
#     passed round upon inquiry remains white steeds
#
def generate_cfd_rand_uniq(cfdist, word, length=15):
    '''generate random sequence of N unique words, where N <= length'''
    result = [word]
    for _ in range(length):
        freqs = cfdist[word]
        words = list(freqs.keys())
        count = len(words)
        ilist = list(range(count))
        while count > 0:
            index = random.randrange(count)
            word = words[index]
            xdv(NLTK_VERBOSITY, "Try:", freqs[word], word)
            if word not in result:
                result.append(word)
                break
            else:
                count -= 1
                ilist[index] = ilist[count]
        if count == 0:
            break
    return join_tokenized(result)

#Some fun ones using this function on bigrams from Moby Dick:
# The yards long voyage was dimly parted the capsized hull rolls upwards and nobler
#     thing still lingers
# The English whalers sometimes most elegant language cannot withstand them matters more recondite
#     and napping
# The subterranean laugh exclaimed Stubb was over tender than hitherto identified
#     with rippling straight path made incarnate
# The schooner moored alongside ere stepping upon immortals.
def generate_cfd_prob_uniq(cfdist, word, length=15):
    '''Generate next word randomly in proportion to CFD probability,
       and if it is already in the output, take the next most probable
       word that is not already in the output.'''
    result = [word]
    for _ in range(length):
        freqs = cfdist[word]
        if not freqs:
            xdv(NLTK_VERBOSITY, "Inner pre break.")
            break
        words = sorted(freqs.keys(), key=freqs.get, reverse=True)
        count = len(words)
        rlist = []
        total = 0
        for word in words:
            total += freqs[word]
            rlist.append(total)
        rdx = random.randrange(total)
        for index, total in enumerate(rlist):
            if rdx < total:
                for wdx in range(index, count):
                    word = words[wdx]
                    if word in result:
                        xdv(NLTK_VERBOSITY, "Dupe:", freqs[word], word)
                    else:
                        xdv(NLTK_VERBOSITY, "Uniq:", freqs[word], word)
                        result.append(word)
                        break
                break
        else:
            xdv(NLTK_VERBOSITY, "Else break outer.")
            break
    return join_tokenized(result)

def test_nltk_book(text=nltk.book.text1):
    '''test module methods'''
    trig_counter = trigrams_counter(text, 2, 10)
    print(trig_counter.most_common(10))

if __name__ == '__main__':
    test_nltk_book()
