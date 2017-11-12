#!/usr/bin/env python3
# -*- encoding: <utf-8> -*-
# Sprax Lines from sujitpal@github      2017.08.31      Ported to Python 3.5
'''
sim_wosc_nltk.py - Semantic similarity of words, and word-order similarity of sentences
using NLTK tools. (word-order + semantic content = wosc)
Python/NLTK implementation of algorithm to detect similarity between
short sentences described in the paper - "Sentence Similarity based
on Semantic Nets and Corpus Statistics" by Li, et al.
Results achieved are NOT identical to that reported in the paper, but
this is very likely due to the differences in the way the algorithm was
described in the paper and how I implemented it.

See the paper above for parameters values reported to produce the "best" results
on their data sets.

FIXME: word order vectors should index words as 1-based, saving 0 as a sentinel
indicating that no match was found.  As it is now, with 0-based indexing,
first words and missing words both get mapped to the 0 index.  It is causing
errors, that is, wrong sentence similarity scores that break the rankings.
'''
# import pdb
from collections import namedtuple
import inflection
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown

NLTK_POS_TAG_TO_WORDNET_KEY = {'J': 'a', 'N': 'n', 'R': 'r', 'V': 'v', 'S': 's'}

def pos_wnk(tag):
    '''translate NLTK tok POS to Wordnet Synset key'''
    try:
        return NLTK_POS_TAG_TO_WORDNET_KEY[tag[0]]
    except KeyError:
        return None

def make(token, pos_tag, wordnet_key=None, capitalized=None):
    cap = token[0].isupper() if capitalized is None else capitalized
    tok = token.lower()
    pos = pos_tag
    wnk = pos_wnk(pos_tag) if wordnet_key is None else wordnet_key
    return Warnt(tok, pos, wnk, cap)



def make_tuple(token, pos_tag, wordnet_key=None, capitalized=None):
    cap = token[0].isupper() if capitalized is None else capitalized
    tok = token.lower()
    pos = pos_tag
    wnk = pos_wnk(pos_tag) if wordnet_key is None else wordnet_key
    return (tok, pos, wnk, cap)


class Warnt(namedtuple("Warnt", "token pos_tag wnk cap")):
    ''' Minimal class for WARNT: Word And Reduced NLP Tags.
        token: tok
        pos_tag: NLTK Part-of-Speech tag (Penn Treebank)
        wnk: WordNet Synset key (extended).  Original WN: { a, n, r, v, s }
        cap: capitalized -- the tok's initial character was uppercase in its original context.
    '''
    __slots__ = ()

    def __new__(cls, token, pos_tag, wordnet_key=None, capitalized=None):
        # cap = token[0].isupper() if capitalized is None else capitalized
        # tok = token.lower()
        # pos = pos_tag
        # wnk = pos_wnk(pos_tag) if wordnet_key is None else wordnet_key
        return super(Warnt, cls).__new__(cls, *make_tuple(token, pos_tag, wordnet_key, capitalized))

NTags = namedtuple("NTags", "idx pos_tag wnk")
NTags.__doc__ = "NLTK tags tuple.  Not for general use."


def smoke_test():
    '''Test Warnt, a word-tok and tags-tuple'''
    warnt1 = Warnt("fool", "NN", 'n', False)
    print("warnt1: ", warnt1)
    warnt2 = make("Jester", "NN", 'n')
    print("warnt2: ", warnt2)

###############################################################################
if __name__ == '__main__':
    smoke_test()
