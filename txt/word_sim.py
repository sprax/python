#!/usr/bin/env python3
# -*- encoding: <utf-8> -*-
# Sprax Lines from sujitpal@github      2017.08.31      Ported to Python 3.5
'''
word_sim.py - Semantic similarity of words, using NLTK tools.

FIXME: word_similarity is way too dependent on the particulars of Wordnet Synsets.
Those particulars need to be wrapped and filtered.  For instance, WN gives 0.0
as the similarity of "the" to any other word, including "this", "a", and "one",
whereas "a" has the same maximum similarity to any other single-letter word.
Words that don't get POS tags starting with 'a', 'n', 'r', or 'v' are ignored,
so the article "the" gets nothing, but "a" can be tagged as a noun, etc.
'''
from __future__ import division
import functools
import math
import pdb
import sys
import time
from collections import namedtuple
import inflection
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import numpy as np

import sim_nltk
import text_regex


class Warnt(namedtuple("Warnt", "tok pos wnt cap")):
    ''' Minimal class for WARNT: Word And Refined NLTK Tags.
        tok = token, pos = NLTK POS, wnt = WordNet Synset key, cap = capitalized.
    '''
    __slots__ = ()
    def __str__(self):
        return "%s  %s  %s  %s" % (self.tok, self.pos, self.wnt, self.cap)

NTags = namedtuple("NTags", "idx pos wnt")
NTags.__doc__ = "NLTK tags tuple.  Not for general use."


def plural_en(noun):
    '''
    Return the plural form of the argument string, assuming that it is an English
    noun.  Some results come from lookup tables, but most come from rules, and
    thus may be wrong, especially for loaner words, OOVs, etc.
    BUGS: inflection's rules sometimes go awry, e.g. (safe <-> saves)
    '''
    if noun.lower()[-3:] == 'afe':
        return noun + 's'
    return inflection.pluralize(noun)


def is_one_noun_plural_of_other_en(noun_a, noun_b):
    '''Returns True if one of the argument strings is the possessive form of
    the other one in English; otherwise False.  Could be made more efficient.'''
    len_a = len(noun_a)
    len_b = len(noun_b)
    if len_a < len_b:
        return plural_en(noun_a) == noun_b
    else:
        return noun_a == plural_en(noun_b)


def possessive_en(noun):
    '''Returns possessive form of the argument string, assuming it is an English noun.'''
    if noun.endswith('s'):
        return noun + "'"
    else:
        return noun + "'s"

def is_one_noun_possessive_of_other_en(noun_a, noun_b):
    '''Returns True if one of the argument strings is the possessive form of
    the other one in English; otherwise False.  Could be made more efficient.'''
    len_a = len(noun_a)
    len_b = len(noun_b)
    if len_a < len_b:
        return possessive_en(noun_a) == noun_b
    elif len_a > len_b:
        return noun_a == possessive_en(noun_b)
    return False

NLTK_POS_TAG_TO_WORDNET_KEY = {'J': 'a', 'N': 'n', 'R': 'r', 'V': 'v', 'S': 's'}

def pos_wnk(tag):
    '''translate NLTK token POS to Wordnet Synset key'''
    try:
        return NLTK_POS_TAG_TO_WORDNET_KEY[tag[0]]
    except KeyError:
        return None

######################### word similarity ##########################

class WordSimilarity:
    '''Word similarity using NLTK WordNet Synsets.'''

    def __init__(self, verbose=False):
        '''Initialize internals'''
        self.verbose = verbose
        self._synsets_fetches = 0
        self._synsets_fetched = 0
        self._ignore_synsets_words = {'a', 'the', 'in', 'on', 'to'}
        self._alpha = 0.2
        self._beta = 0.45
        self._sim_plural_proper_noun = 0.667   # TODO: rationalize this value?
        self._sim_possessive_proper_noun = 0.95   # TODO: rationalize this value?


    def print_stats(self):
        '''Show statistics since init.'''
        print("Synsets fetched/fetches:  %d / %d  =  %.3f" % (self._synsets_fetched, self._synsets_fetches,
                                                              self._synsets_fetched / self._synsets_fetches))

    def get_best_synset_pair(self, src_word, try_word, src_tag=None, try_tag=None):
        """
        Choose the pair with highest path similarity among all pairs.
        Mimics pattern-seeking behavior of humans.
        """
        max_sim = -1.0

        synsets_1 = wn.synsets(src_word, src_tag)
        self._synsets_fetches += 1
        if synsets_1 is None or len(synsets_1) == 0:
            # print("synset(%s) is None" % src_word)
            return None, None

        self._synsets_fetched += len(synsets_1)

        self._synsets_fetches += 1
        synsets_2 = wn.synsets(try_word, try_tag)
        if synsets_2 is None or len(synsets_2) == 0:
            # print("synset(%s) is None" % try_word)
            return None, None

        self._synsets_fetched += len(synsets_2)

        fixme_count = 0

        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
                sim = wn.path_similarity(synset_1, synset_2)
                if sim is None:
                    if fixme_count == 0:
                        # FIXME: when does this short-circut happen?
                        # print("path_similarity from (%s, %s) is None (fixme_count %d)" % (
                        #       src_word, try_word, fixme_count))
                        return None, None
                elif sim > max_sim:
                    max_sim = sim
                    best_pair = synset_1, synset_2
                fixme_count += 1
        return best_pair

    def length_dist(self, synset_1, synset_2):
        """
        Return a measure of the length of the shortest path in the semantic
        ontology (Wordnet in our case as well as the paper's) between two
        synsets.
        """
        l_dist = float("inf")
        if synset_1 is None or synset_2 is None:
            return 0.0
        if synset_1 == synset_2:
            # if synset_1 and synset_2 are the same synset return 0
            l_dist = 0.0
        else:
            wset_1 = set([str(x.name()) for x in synset_1.lemmas()])
            wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
            if len(wset_1.intersection(wset_2)) > 0:
                # if synset_1 != synset_2 but there is word overlap, return 1.0
                l_dist = 1.0
            else:
                # just compute the shortest path between the two
                l_dist = synset_1.shortest_path_distance(synset_2)
                if l_dist is None:
                    l_dist = 0.0
        # normalize path length to the range [0,1]
        return math.exp(-self._alpha * l_dist)

    def hierarchy_dist(self, synset_1, synset_2):
        """
        Return a measure of depth in the ontology to model the fact that
        nodes closer to the root are broader and have less semantic similarity
        than nodes further away from the root.
        """
        h_dist = sys.maxsize
        if synset_1 is None or synset_2 is None:
            return h_dist
        if synset_1 == synset_2:
            # return the depth of one of synset_1 or synset_2
            h_dist = max([x[1] for x in synset_1.hypernym_distances()])
        else:
            # find the max depth of least common subsumer
            hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
            hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
            lcs_candidates = set(hypernyms_1.keys()).intersection(
                set(hypernyms_2.keys()))
            if len(lcs_candidates) > 0:
                lcs_dists = []
                for lcs_candidate in lcs_candidates:
                    lcs_d1 = 0
                    if lcs_candidate in hypernyms_1:
                        lcs_d1 = hypernyms_1[lcs_candidate]
                    lcs_d2 = 0
                    if lcs_candidate in hypernyms_2:
                        lcs_d2 = hypernyms_2[lcs_candidate]
                    lcs_dists.append(max([lcs_d1, lcs_d2]))
                h_dist = max(lcs_dists)
            else:
                h_dist = 0
        exp_pos_beta_h = math.exp(self._beta * h_dist)
        exp_neg_beta_h = math.exp(-self._beta * h_dist)
        return (exp_pos_beta_h - exp_neg_beta_h)/(exp_pos_beta_h + exp_neg_beta_h)

    def word_similarity(self, src_word, try_word, src_tag=None, try_tag=None):
        '''Nominally, this is a synset-based similarity between two words, with
        some important caveats:
        *  This "similarity" is NOT symmetric:   sim(A, B) != sim(B, A).
        *  This "similarity" is NOT reflexive:   sim(A, A) != 1.0.  Often it just less than 1.
        *  Thus it does not yield a well-defined distance metric in 1 - similarity.
           While it approximates a metric, it violates the triangle rule in small ways.
        *  Out-of-vocabulary words (OOVs) always get a result of 0, even when compared to
        themselves.  Some examples: sim(yes, yes) is .999, sim(yes, not) is 0.0, but
        sim(yes, no) is .074, and sim(yes, duh) is 0.0 but so is sim(duh, duh).
        *  The arguments are named src_word and try_word to suggest that the first
        word is more important and less variable.  It's the known or fixed word,
        whereas the try_word is variable, one of many in a search set of, say, possible
        synonyms.  Maybe it's from an intersection, rather than a union.
        '''
        synset_pair = self.get_best_synset_pair(src_word, try_word, src_tag, try_tag)
        return (self.length_dist(synset_pair[0], synset_pair[1]) *
                self.hierarchy_dist(synset_pair[0], synset_pair[1]))


    def most_similar_word(self, sent_word_set, src_word):
        """
        Find the word in the sentence word set that is most similar to the source word
        (from the joint word set). We use the algorithm above to compute word similarity
        between the word and each word in the joint word set, and return the most similar
        word and the actual similarity value.
        """
        max_sim = 0.0 # This was -1.0, which meant that the first word compared would become the max,
        # and it would remain the max if no other word were more similar, even if the similarity was 0.
        sim_word = ""
        for sent_word in sent_word_set:
            sim = self.word_similarity(src_word, sent_word)
            if sim > max_sim:
                max_sim = sim
                sim_word = sent_word
        return sim_word, max_sim

    def most_similar_word_pos(self, sent_word_dct, union_word, union_ntags, use_propers=True):
        """
        Find the word in the joint word set that is most similar to the word
        passed in. We use the algorithm above to compute word similarity between
        the word and each word in the joint word set, and return the most similar
        word and the actual similarity value.
        """
        # print("%d  %3s  %s  %s" % (len(union_wpos), union_wpos, union_wtag, union_word))
        union_wpos = union_ntags.pos
        union_wtag = union_ntags.wnt
        max_sim = 0.0
        sim_word = ""
        if union_wtag is not None and union_word not in self._ignore_synsets_words:
            for item in sent_word_dct.items():
                sent_wtag = item[1].wnt
                if sent_wtag == union_wtag:
                # or sent_wtag == 'a' and union_wtag == 'r'
                # or sent_wtag == 'r' and union_wtag == 'a':
                    sent_wpos = item[1].pos
                    sent_word = item[0]
                    # FIXME: index from 1
                    if use_propers and sent_wpos == 'NNP' and union_wpos == 'NNP':
                        # sent_word is likely to be a proper noun.  If we only
                        # allow exact matches on proper nouns, then here we should
                        # just continue, because we checked for equality upstream.
                        if is_one_noun_possessive_of_other_en(union_word, sent_word):
                            sim = self._sim_possessive_proper_noun
                        elif is_one_noun_plural_of_other_en(union_word, sent_word):
                            sim = self._sim_plural_proper_noun
                        else:
                            sim = 0.0
                    else:
                        sim = self.word_similarity(union_word, sent_word, union_wtag, sent_wtag)
                    if sim > max_sim:
                        max_sim = sim
                        sim_word = sent_word
        return sim_word, max_sim

#################################### tests  ####################################
def test_word_similarity(wordsim):
    '''The results of the algorithm are largely dependent on the results of
    the word similarities, so we should test that first...'''
    print("\n\t Word Similarity:")
    word_pairs = [
        ["asylum", "fruit", 0.21],
        ["autograph", "shore", 0.29],
        ["autograph", "signature", 0.55],
        ["automobile", "car", 0.64],
        ["bird", "woodland", 0.33],
        ["boy", "rooster", 0.53],
        ["boy", "lad", 0.66],
        ["boy", "sage", 0.51],
        ["cemetery", "graveyard", 0.73],
        ["coast", "forest", 0.36],
        ["coast", "shore", 0.76],
        ["cock", "rooster", 1.00],
        ["cord", "smile", 0.33],
        ["cord", "string", 0.68],
        ["cushion", "pillow", 0.66],
        ["forest", "graveyard", 0.55],
        ["forest", "woodland", 0.70],
        ["furnace", "stove", 0.72],
        ["glass", "tumbler", 0.65],
        ["grin", "smile", 0.49],
        ["gem", "jewel", 0.83],
        ["hill", "woodland", 0.59],
        ["hill", "mound", 0.74],
        ["implement", "tool", 0.75],
        ["journey", "voyage", 0.52],
        ["magician", "oracle", 0.44],
        ["magician", "wizard", 0.65],
        ["midday", "noon", 1.0],
        ["oracle", "sage", 0.43],
        ["serf", "slave", 0.39]
    ]
    print("W-Sim \t Paper \t src_word \t try_word")
    print("----- \t ----- \t -------- \t --------")
    sum = 0.0
    for word_pair in word_pairs:
        sim = wordsim.word_similarity(word_pair[0], word_pair[1])
        print(" %.2f \t %.2f \t %s %s %s" % (sim, word_pair[2], word_pair[0],
                                             ' '*(14 - len(word_pair[0])), word_pair[1]))
        sum += sim
    avg_sim = sum / len(word_pairs)
    wordsim.print_stats()
    print("test_word_similarity: sum/num %.3f/%d = %.3f" % (sum, len(word_pairs), avg_sim))
    return avg_sim

def smoke_test():
    '''test very basic functionality'''
    wordsim = WordSimilarity(verbose=True)
    avg_sim = test_word_similarity(wordsim)
    return avg_sim

###############################################################################
if __name__ == '__main__':
    smoke_test()
