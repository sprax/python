#!/usr/bin/env python3
'''
Routines from the NLTK book.  NB: Many of these functions take a
parameter called "tokens", which is assumed to name an array of tokens.
The actual argument can be a text as imported from nltk.book, or an
arbitrary array of strings, numbers, objects, whatever.  Treating an
entire book or corpus as one flat array of tokens may yield dull results.
'''
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

def lexical_diversity(tokens):
    '''ratio of word count to unique word count'''
    return len(tokens) / len(set(tokens))

def text_vocab(tokens):
    '''set of lower-case words in tokens'''
    return set(w.lower() for w in tokens if w.isalpha())

def odd_words(tokens):
    '''originally: unusual_words'''
    all_vocab = text_vocab(tokens)
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    odd_vocab = all_vocab - english_vocab
    return sorted(odd_vocab)

def lexical_oddity(tokens):
    '''fraction of tokens vocab not in NLTK's standard English vocab'''
    all_vocab = text_vocab(tokens)
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    odd_vocab = all_vocab - english_vocab
    return len(odd_vocab) / len(all_vocab)

def freq(tokens, word):
    '''frequency of a single word'''
    return tokens.count(word) / len(tokens)

def frac(tokens, word_set):
    '''fraction of tokens comprised of words in word_set'''
    total = sum([tokens.count(word) for word in word_set])
    return total / len(tokens)

def content_fraction(tokens):
    '''What fraction of tokens are not stopwords?'''
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in tokens if w.lower() not in stopwords]
    return len(content) / len(tokens)

def text_from_tokens(tokens):
    '''Counter of words'''
    return Counter(tokens)

def bigrams_from_tokens(tokens, min_len):
    '''Counter of bigrams'''
    counter = Counter()
    for big in nltk.bigrams(tokens):
        if len(big[0]) < min_len or len(big[1]) < min_len:
            continue
        counter.update([big])
    return counter

def word_bigrams_from_sentences(sentences):
    '''Counter of bigrams found in an array of sentences.  For example:
    sentences = nltk.corpus.genesis.sents('english-kjv.txt')
    word_bigrams = word_bigrams_from_sentences(sentences)
    '''
    counter = Counter()
    for sent_tokens in sentences:
        for big in nltk.bigrams(sent_tokens):
            if re.match(NON_ALPHA_PATTERN, big[0]):
                continue
            if re.match(NON_ALPHA_PATTERN, big[1]):
                continue
            counter.update([big])
    return counter

def word_trigrams_from_sentences(sentences):
    '''Counter of trigrams found in an array of sentences using an FSM.
    For example:
    sentences = nltk.corpus.gutenberg.sents('melville-moby_dick.txt')
    word_trigrams = word_trigrams_from_sentences(sentences)
    '''
    counter = Counter()
    for sent_tokens in sentences:
        length = len(sent_tokens)
        idx = 2
        while idx < length:
            if re.match(NON_ALPHA_PATTERN, sent_tokens[idx - 2]):
                idx += 1
                continue
            if re.match(NON_ALPHA_PATTERN, sent_tokens[idx - 1]):
                idx += 2
                continue
            if re.match(NON_ALPHA_PATTERN, sent_tokens[idx]):
                idx += 3
                continue
            idx += 1
            counter.update([tuple(sent_tokens[idx-3:idx])])
            while idx < length:
                if re.match(NON_ALPHA_PATTERN, sent_tokens[idx]):
                    idx += 3
                    break
                else:
                    idx += 1
                    counter.update([tuple(sent_tokens[idx-3:idx])])
    return counter


def trigrams_from_tokens(tokens, min_len, min_sum_len):
    '''Counter of trigrams'''
    counter = Counter()
    for trig in nltk.trigrams(tokens):
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

def reject_string_punct(tokenized):
    '''Filter out all tokens that are substrings of string.punctuation.'''
    for token in tokenized:
        if token not in string.punctuation:
            yield token

SENTENCE_PUNCTUATION = '!"\'()*+,./:;<>?[\\]^_`{|}~'

def reject_sentence_punct(tokenized):
    '''Filter out tokens that are substrings of string.punctualtion'''
    for token in tokenized:
        if token not in SENTENCE_PUNCTUATION:
            yield token

NLTK_PUNCTUATION_PATTERN = re.compile("[{}]".format(string.punctuation))


def reject_words_with_punct(tokenized):
    '''Filter out all tokens containing any punctuation.'''
    for token in tokenized:
        if not re.search(NLTK_PUNCTUATION_PATTERN, token):
            yield token

NON_ALPHA_PATTERN = re.compile(r'(?:\W|[0-9])+')

def reject_non_alpha(tokenized):
    '''Retain only alphabetic strings (words, presumably), no non-word characters.'''
    for token in tokenized:
        if not re.search(NON_ALPHA_PATTERN, token):
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

def test_nltk_book(tokens=nltk.book.text1):
    '''test module methods'''
    trigs = trigrams_from_tokens(tokens, 2, 10)
    print(trigs.most_common(10))

if __name__ == '__main__':
    test_nltk_book()
