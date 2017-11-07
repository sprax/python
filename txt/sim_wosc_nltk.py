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

FIXME: word_similarity is way too dependent on the particulars of Wordnet Synsets.
Those particulars need to be wrapped and filtered.  For instance, WN gives 0.0
as the similarity of "the" to any other word, including "this", "a", and "one",
whereas "a" has the same maximum similarity to any other single-letter word.
Words that don't get POS tags starting with 'a', 'n', 'r', or 'v' are ignored,
so the article "the" gets nothing, but "a" can be tagged as a noun, etc.
'''
from __future__ import division
# import functools
import math
import pdb
import sys
import time
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import numpy as np

import sim_nltk
import text_regex

def possessive_en(noun):
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

NLTK_POS_TAG_TO_WORDNET_KEY = {'A': 'a', 'N': 'n', 'R': 'r', 'V': 'v', 'S': 's'}

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
        return ((math.exp(self._beta * h_dist) - math.exp(-self._beta * h_dist)) /
                (math.exp(self._beta * h_dist) + math.exp(-self._beta * h_dist)))

    def word_similarity(self, src_word, try_word, src_tag=None, try_tag=None):
        '''Nominally, this is a synset-based similarity between two words, with
        some important caveats:
        *  This "similarity" is NOT symmetric:   sim(A, B) != sim(B, A).
        *  This "similarity" is NOT reflexive:   sim(A, A) != 1.0.  Often it just less than 1.
        *  Thus it does not yield a well-defined distance metric in 1 - similarity.
           While it approximates a metric, it violates the triangle rule in small ways.
        *  Out of vocabulary words always get a result of 0, even when compared to
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

    def most_similar_word_pos(self, sent_word_dct, union_word, union_wtag, use_propers=False):
        """
        Find the word in the joint word set that is most similar to the word
        passed in. We use the algorithm above to compute word similarity between
        the word and each word in the joint word set, and return the most similar
        word and the actual similarity value.
        """
        max_sim = 0.0
        sim_word = ""
        if union_wtag is not None and union_word not in self._ignore_synsets_words:
            for item in sent_word_dct.items():
                sent_wtag = item[1][1]
                if sent_wtag == union_wtag:
                # or sent_wtag == 'a' and union_wtag == 'r'
                # or sent_wtag == 'r' and union_wtag == 'a':
                    sent_word = item[0]
                    # FIXME: index from 1
                    # FIXME: Use NNP tag instead of guessing from capitalization and first word!
                    if use_propers and sent_wtag == 'n' and sent_word[0].isupper() and item[1][0] > 0:
                        # sent_word is likely to be a proper noun.  If we only
                        # allow exact matches on proper nouns, then here we should
                        # just continue, because we checked for equality upstream.
                        if is_one_noun_possessive_of_other_en(union_word, sent_word):
                            # pdb.set_trace()
                            sim = self._sim_possessive_proper_noun
                        else:
                            sim = 0.0
                    else:
                        sim = self.word_similarity(union_word, sent_word, union_wtag, sent_wtag)
                    if sim > max_sim:
                        max_sim = sim
                        sim_word = sent_word
        return sim_word, max_sim

############################# sentence similarity #############################

class SentSimilarity:
    '''Sentence similarity using NLTK WordNet Synsets and word order.'''

    def __init__(self, wordsim, use_propers=True, verbose=False):
        '''Initialize internals'''
        self.wordsim = wordsim
        self.verbose = verbose
        self._brown_freq_count = 0
        self._brown_freqs = dict()
        self._delta = 0.8
        self._min_word_sim_semantic = 0.2   # formerly known as PHI
        self._min_word_sim_order = 0.4      # formerly known as ETA
        self._use_propers = use_propers


    def info_content(self, lookup_word):
        """
        Uses the Brown corpus available in NLTK to calculate a Laplace
        smoothed frequency distribution of words, then uses this information
        to compute the information content of the lookup_word.
        TODO: Optimize -- call once.
        """
        if self._brown_freq_count == 0:
            beg_time = time.time()
            # poor man's lazy evaluation
            for sent in brown.sents():
                for word in sent:
                    word = word.lower()
                    if not word in self._brown_freqs:
                        self._brown_freqs[word] = 0
                    self._brown_freqs[word] = self._brown_freqs[word] + 1
                    self._brown_freq_count = self._brown_freq_count + 1
            print("self.info_content: Initializing Brown Freqs took %d seconds" % (time.time() - beg_time))
        lookup_word = lookup_word.lower()
        count = 0 if not lookup_word in self._brown_freqs else self._brown_freqs[lookup_word]
        return 1.0 - (math.log(count + 1) / math.log(self._brown_freq_count + 1))


    ######################### word order similarity ##########################

    def semantic_and_word_order_vectors(self, sent_word_dct, joint_word_set, use_content_norm=False):
        """
        Computes the word order vector for a sentence. The sentence is passed
        in as a collection of words. The size of the word order vector is the
        same as the size of the joint word set. The elements of the word order
        vector are the position mapping (from the windex dictionary) of the
        word in the joint set if the word exists in the sentence. If the word
        does not exist in the sentence, then the value of the element is the
        position of the most similar word in the sentence as long as the similarity
        is above the threshold self._min_word_sim_order.
        """
        vec_len = len(joint_word_set)
        sem_vec = np.zeros(vec_len)
        ord_vec = np.zeros(vec_len)
        for idx, joint_word in enumerate(joint_word_set):
            try:
                # word in joint_word_set found in sentence, just populate the index
                ord_vec[idx] = sent_word_dct[joint_word]
                sem_vec[idx] = 1.0
                if use_content_norm:
                    info_cont = self.info_content(joint_word)
                    sem_vec[idx] *= info_cont * info_cont
            except KeyError:
                # word not in joint_word_set, find most similar word and populate
                # word_vector with the thresholded similarity
                sim_word, max_sim = self.wordsim.most_similar_word(sent_word_dct.keys(), joint_word)
                ord_vec[idx] = sent_word_dct[sim_word] if max_sim > self._min_word_sim_order else 0
                sem_vec[idx] = max_sim if max_sim > self._min_word_sim_semantic else 0.0
                if use_content_norm:
                    sem_vec[idx] = sem_vec[idx] * self.info_content(joint_word) * self.info_content(sim_word)
        return sem_vec, ord_vec

    ######################### semantic similarity ##########################

    def semantic_vector(self, sent_word_set, joint_word_set, use_content_norm=False):
        """
        Computes the semantic vector of a sentence. The sentence is passed in as
        a collection of words. The size of the semantic vector is the same as the
        size of the joint word set. The elements are 1 if a word in the sentence
        already exists in the joint word set, or the similarity of the word to the
        most similar word in the joint word set if it doesn't. Both values are
        further normalized by the word's (and similar word's) information content
        if use_content_norm is True.
        """
        sem_vec = np.zeros(len(joint_word_set))
        i = 0
        # print("SV:", end=' ')
        for joint_word in joint_word_set:
            # print(joint_word, end=' ')
            if joint_word in sent_word_set:
                # if word in union exists in the sentence, s(i) = 1 (unnormalized)
                sem_vec[i] = 1.0
                if use_content_norm:
                    sem_vec[i] = sem_vec[i] * math.pow(self.info_content(joint_word), 2)
            else:
                # find the most similar word in the joint set and set the sim value
                sim_word, max_sim = self.wordsim.most_similar_word(sent_word_set, joint_word)
                sem_vec[i] = max_sim if max_sim > self._min_word_sim_semantic else 0.0
                if use_content_norm:
                    sem_vec[i] = sem_vec[i] * self.info_content(joint_word) * self.info_content(sim_word)
            i = i + 1
        # print()
        # print("SV:", sem_vec)
        return sem_vec

    def sem_and_wo_vectors_pos(self, sent_word_dct, joint_wordpos_dct, use_content_norm=False,
                               use_pos=False):
        """
        Computes the word order vector for a sentence. The sentence is passed
        in as a collection of words. The size of the word order vector is the
        same as the size of the joint word set. The elements of the word order
        vector are the position mapping (from the windex dictionary) of the
        word in the joint set if the word exists in the sentence. If the word
        does not exist in the sentence, then the value of the element is the
        position of the most similar word in the sentence as long as the similarity
        is above the threshold self._min_word_sim_order.
        """
        vec_len = len(joint_wordpos_dct)
        sem_vec = np.zeros(vec_len)
        ord_vec = np.zeros(vec_len)
        # print("PT:", end=' ')
        for idx, joint_word in enumerate(joint_wordpos_dct):
            # print(joint_word, end=' ')
            if joint_word in sent_word_dct.keys():
                sem_vec[idx] = 1.0
                ord_vec[idx] = sent_word_dct[joint_word][0] if use_pos else sent_word_dct[joint_word]
                if use_content_norm:
                    info_cont = self.info_content(joint_word)
                    sem_vec[idx] *= info_cont * info_cont
            else:
                # word not in joint_wordpos_set, find most similar word and populate
                # word_vector with the thresholded similarity
                if use_pos:
                    joint_wtag = joint_wordpos_dct[joint_word]
                    sim_word, max_sim = self.wordsim.most_similar_word_pos(sent_word_dct, joint_word,
                                                                           joint_wtag, self._use_propers)
                else:
                    sim_word, max_sim = self.wordsim.most_similar_word(sent_word_dct.keys(), joint_word)

                if max_sim > self._min_word_sim_order:
                    ord_vec[idx] = sent_word_dct[sim_word][0] if use_pos else sent_word_dct[sim_word]
                else:
                    ord_vec[idx] = 0

                sem_vec[idx] = max_sim if max_sim > self._min_word_sim_semantic else 0.0

                if use_content_norm:
                    sem_vec[idx] = sem_vec[idx] * self.info_content(joint_word) * self.info_content(sim_word)
        # print()
        # print("PT:", sem_vec)
        # print(ord_vec)
        # print()
        return sem_vec, ord_vec

######################### vector cosine similarities ##########################

    def semantic_similarity(self, sentence_1, sentence_2, use_content_norm=False):
        """
        Computes the semantic similarity between two sentences as the cosine
        similarity between the semantic vectors computed for each sentence.
        """
        word_set_1 = set(nltk.word_tokenize(sentence_1))
        word_set_2 = set(nltk.word_tokenize(sentence_2))
        joint_word_set = word_set_1.union(word_set_2)
        vec_1 = self.semantic_vector(word_set_1, joint_word_set, use_content_norm)
        vec_2 = self.semantic_vector(word_set_2, joint_word_set, use_content_norm)
        return np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))

    def word_order_vector(self, sent_word_dct, joint_word_set):
        """
        Computes the word order vector for a sentence. The sentence is passed
        in as a collection of words. The size of the word order vector is the
        same as the size of the joint word set. The elements of the word order
        vector are the position mapping (from the windex dictionary) of the
        word in the joint set if the word exists in the sentence. If the word
        does not exist in the sentence, then the value of the element is the
        position of the most similar word in the sentence as long as the similarity
        is above the threshold self._min_word_sim_order.
        """
        ord_vec = np.zeros(len(joint_word_set))
        for idx, joint_word in enumerate(joint_word_set):
            try:
                # word in joint_word_set found in sentence, just populate the index
                ord_vec[idx] = sent_word_dct[joint_word]
            except KeyError:
                # word not in joint_word_set, find most similar word and populate
                # word_vector with the thresholded similarity
                sim_word, max_sim = self.wordsim.most_similar_word(sent_word_dct.keys(), joint_word)
                if max_sim > self._min_word_sim_order:
                    ord_vec[idx] = sent_word_dct[sim_word]
                else:
                    # FIXME: Should index from 1 because 0 is a legit word index value
                    ord_vec[idx] = 0
        return ord_vec

    def word_order_similarity(self, sentence_1, sentence_2):
        """
        Computes the word-order similarity between two sentences as the normalized
        difference of word order between the two sentences.
        """
        # NOTE: These dicts record only the *last* occurence of each word
        sent_tok_1 = nltk.word_tokenize(sentence_1)
        sent_dct_1 = {word: idx for idx, word in enumerate(sent_tok_1)}
        sent_tok_2 = nltk.word_tokenize(sentence_2)
        sent_dct_2 = {word: idx for idx, word in enumerate(sent_tok_2)}

        # Don't neet to make this a list -- the enumerate order is constant (in cPython)
        joint_word_set = set(sent_dct_1.keys()).union(sent_dct_2.keys())
        wov_1 = self.word_order_vector(sent_dct_1, joint_word_set)
        wov_2 = self.word_order_vector(sent_dct_2, joint_word_set)
        return 1.0 - (np.linalg.norm(wov_1 - wov_2) / np.linalg.norm(wov_1 + wov_2))

    ######################### overall similarity ##############################

    def compute_similarity(self, semvec_1, semvec_2, ordvec_1, ordvec_2):
        '''compute and interpolate between semantic and word-order (structural) similarities.'''
        semantic_sim = np.dot(semvec_1, semvec_2.T) / (np.linalg.norm(semvec_1) * np.linalg.norm(semvec_2))
        word_ord_sim = 1.0 - (np.linalg.norm(ordvec_1 - ordvec_2) / np.linalg.norm(ordvec_1 + ordvec_2))
        # return delta * semantic_sim + (1.0 - delta) * word_ord_sim
        return self._delta * (semantic_sim - word_ord_sim) + word_ord_sim

    ###########################################################################

    def sentence_similarity_pos(self, sentence_1, sentence_2, use_content_norm=False,
                                use_pos=True, word_tokenizer=None):
        """
        Calculate the semantic similarity between two sentences.  The last
        parameter is True or False depending on whether information content
        normalization is desired or not.
        """
        if word_tokenizer is None:
            word_tokenizer = nltk.word_tokenize
        # NOTE: These dicts record only the *last* occurence of each word
        sent_tok_1 = word_tokenizer(sentence_1)
        # pdb.set_trace()
        pos_tags_1 = nltk.pos_tag(sent_tok_1)
        sent_dct_1 = {wordpos[0]: (idx, pos_wnk(wordpos[1])) for idx, wordpos in enumerate(pos_tags_1)}
        word_set_1 = set(sent_dct_1.keys())

        sent_tok_2 = word_tokenizer(sentence_2)
        pos_tags_2 = nltk.pos_tag(sent_tok_2)
        sent_dct_2 = {wordpos[0]: (idx, pos_wnk(wordpos[1])) for idx, wordpos in enumerate(pos_tags_2)}
        word_set_2 = set(sent_dct_2.keys())

        joint_word_set = word_set_1.union(word_set_2)
        # NOTE: Prioritizing sentence_2 for POS, because it's expected to be the trial sentence.
        joint_wordpos_dct = {word: sent_dct_2[word][1] if word in sent_dct_2 else sent_dct_1[word][1]
                             for word in joint_word_set}

        #print("\n======== SSP COMPARE:", sentence_1, sentence_2)
        # print("JWPD: ", wordpos_dct)
        semvec_1, ordvec_1 = self.sem_and_wo_vectors_pos(sent_dct_1, joint_wordpos_dct,
                                                         use_content_norm, use_pos)
        semvec_2, ordvec_2 = self.sem_and_wo_vectors_pos(sent_dct_2, joint_wordpos_dct,
                                                         use_content_norm, use_pos)
        return self.compute_similarity(semvec_1, semvec_2, ordvec_1, ordvec_2)


    def sentence_similarity(self, sentence_1, sentence_2, use_content_norm=False):
        """
        Calculate the semantic similarity between two sentences. The last
        parameter is True or False depending on whether information content
        normalization is desired or not.
        """
        # NOTE: These dicts record only the *last* occurence of each word
        sent_tok_1 = nltk.word_tokenize(sentence_1)
        sent_dct_1 = {tok: idx for idx, tok in enumerate(sent_tok_1)}
        word_set_1 = set(sent_dct_1.keys())

        sent_tok_2 = nltk.word_tokenize(sentence_2)
        sent_dct_2 = {tok: idx for idx, tok in enumerate(sent_tok_2)}
        word_set_2 = set(sent_dct_2.keys())

        joint_word_set = word_set_1.union(word_set_2)

        #print("\n======== SS COMPARE:", sentence_1, sentence_2)
        semvec_1, ordvec_1 = self.sem_and_wo_vectors_pos(sent_dct_1, joint_word_set, use_content_norm, False)
        semvec_2, ordvec_2 = self.sem_and_wo_vectors_pos(sent_dct_2, joint_word_set, use_content_norm, False)
        return self.compute_similarity(semvec_1, semvec_2, ordvec_1, ordvec_2)

    def sentence_similarity_slow(self, sentence_1, sentence_2, use_content_norm=False, delta=None):
        """
        Calculate the semantic similarity between two sentences. The last
        parameter is True or False depending on whether information content
        normalization is desired or not.
        """
        semantic_sim = self.semantic_similarity(sentence_1, sentence_2, use_content_norm)
        word_ord_sim = self.word_order_similarity(sentence_1, sentence_2)
        delta = delta if delta is not None else self._delta
        return delta * (semantic_sim - word_ord_sim) + word_ord_sim

######################### main / test ##########################

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
    for word_pair in word_pairs:
        print(" %.2f \t %.2f \t %s %s %s" % (wordsim.word_similarity(word_pair[0], word_pair[1]), word_pair[2],
                                             word_pair[0], ' '*(14 - len(word_pair[0])), word_pair[1]))

def test_sentence_similarity(sentsim):
    '''test semantic and word-order similarity of sentence pairs.'''
    print("\n\t Sentence Similarity:")
    sentence_pairs = [
        ["I like that bachelor.", "I like that unmarried man.", 0.561],
        ["John is very nice.", "Is John very nice?", 0.977],
        ["Red alcoholic drink.", "A bottle of wine.", 0.585],
        ["Red alcoholic drink.", "Fresh orange juice.", 0.611],
        ["Red alcoholic drink.", "An English dictionary.", 0.0],
        ["Red alcoholic drink.", "Fresh apple juice.", 0.420],
        ["A glass of cider.", "A full cup of apple juice.", 0.678],
        ["It is a dog.", "That must be your dog.", 0.739],
        ["It is a dog.", "It is a log.", 0.623],
        ["It is a dog.", "It is a pig.", 0.790],
        ["Dogs are animals.", "They are common pets.", 0.738],
        ["Canis familiaris are animals.", "Dogs are common pets.", 0.362],
        ["I have a pen.", "Where do you live?", 0.0],
        ["I have a pen.", "Where is ink?", 0.129],
        ["I have a hammer.", "Take some nails.", 0.508],
        ["I have a hammer.", "Take some apples.", 0.121]
    ]
    spacing = 32
    spaces = ' '*(spacing - len('sentence_1'))
    print("Sim-F \t Sim-T \t Paper \t sentence_1 %s Sentence_2" % spaces)
    print("----- \t ----- \t ----- \t ---------- %s ----------" % spaces)
    for sent_pair in sentence_pairs:
        ss_f = sentsim.sentence_similarity(sent_pair[0], sent_pair[1], False)
        ss_t = sentsim.sentence_similarity(sent_pair[0], sent_pair[1], True)
        print("%.3f\t %.3f\t %.3f\t %s %s %s" % (ss_f, ss_t, sent_pair[2], sent_pair[0],
                                                 ' '*(spacing - len(sent_pair[0])),
                                                 sent_pair[1]))

def smoke_test():
    '''test very basic functionality'''
    wordsim = WordSimilarity(verbose=True)
    sentsim = SentSimilarity(wordsim, verbose=True)
    test_word_similarity(wordsim)
    test_sentence_similarity(sentsim)

def moby(mquats, tok=False, pos=True, ntry=8):
    '''
Finding all similarity lists (train 40, trial 40, nears 6) took 4137.7 seconds
match_ttt(n_train=40, n_trial=40, count=6) took 4137.7 seconds; score 78.5422

         1946348335 function calls (1944927287 primitive calls) in 4137.690 seconds

   Ordered by: cumulative time
   List reduced from 181 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000 4137.690 4137.690 /Users/sprax/asdf/spryt/txt/sim_nltk.py:523(match_ttt)
        1    0.000    0.000 4137.686 4137.686 /Users/sprax/asdf/spryt/txt/sim_nltk.py:337(find_ranked_qa_lists)
        1    0.000    0.000 4137.686 4137.686 /Users/sprax/asdf/spryt/txt/sim_nltk.py:297(find_nearest_qas_lists)
       40    0.000    0.000 4137.686  103.442 /Users/sprax/asdf/spryt/txt/sim_nltk.py:283(find_nearest_quats)
       40    0.015    0.000 4137.683  103.442 /Users/sprax/asdf/spryt/txt/sim_nltk.py:247(similarity_dict)
     1600    0.004    0.000 4137.661    2.586 /Users/sprax/asdf/spryt/txt/sim_nltk.py:69(sim_weighted_qas)
     1600    0.017    0.000 4137.658    2.586 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:475(sentence_similarity)
    45200    0.294    0.000 4135.730    0.091 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:143(most_similar_word)
   409046    0.925    0.000 4135.436    0.010 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:134(word_similarity)
   409046    7.404    0.000 4104.408    0.010 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:38(get_best_synset_pair)
  8557466    4.848    0.000 3819.285    0.000 .../wordnet.py:1680(path_similarity)
  8557466   19.730    0.000 3814.436    0.000 .../nltk/corpus/reader/wordnet.py:772(path_similarity)
  8667920  207.487    0.000 3289.453    0.000 .../wordnet.py:702(shortest_path_distance)
 17311096  551.115    0.000 2856.207    0.000 .../wordnet.py:678(_shortest_hypernym_paths)
     1600    0.052    0.000 2491.709    1.557 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:400(word_order_similarity)
     3200    0.115    0.000 2490.852    0.778 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:374(word_order_vector)
     1600    0.042    0.000 1645.931    1.029 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:362(semantic_similarity)
     3200    0.075    0.000 1645.103    0.514 /Users/sprax/asdf/spryt/txt/sim_wosc_nltk.py:290(semantic_vector)
    '''
    out_path = "moby_ttt_pos.txt" if pos else "moby_ttt_slo.txt"
    wordsim = WordSimilarity()
    sentsim = SentSimilarity(wordsim)
    if pos:
        if tok:
            # NOTE: The notnonword tokenizer gives "Pequod's" instead of "Pequod" and "'s'".
            # TODO: Therefore the treatment of proper nouns needs to see "Pequod" and "Pequod's"
            # as variants of the same word.
            sim_func = functools.partial(sentsim.sentence_similarity_pos,
                                         word_tokenizer=text_regex.notnonword_tokens)
        else:
            sim_func = sentsim.sentence_similarity_pos
    else:
        sim_func = sentsim.sentence_similarity

    scr, msl, trn, trl = sim_nltk.moby_ttt(mquats, 200, ntry, outpath=out_path,
                                           find_qas=sim_nltk.find_nearest_quats,
                                           sim_func=sim_func)
    wordsim.print_stats()
    return (scr, msl, trn, trl)

###############################################################################
if __name__ == '__main__':
    smoke_test()
