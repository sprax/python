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
'''
from __future__ import division
import math
import pdb
import sys
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import numpy as np

import sim_nltk

# Parameters to the algorithm. Currently set to values that was reported
# in the paper to produce "best" results.
ALPHA = 0.2
BETA = 0.45
ETA = 0.4
PHI = 0.2
DELTA = 0.8

BROWN_FREQS = dict()
N = 0

######################### word similarity ##########################

def get_best_synset_pair(word_1, word_2, word_tag_1=None, word_tag_2=None):
    """
    Choose the pair with highest path similarity among all pairs.
    Mimics pattern-seeking behavior of humans.
    """
    max_sim = -1.0
    synsets_1 = wn.synsets(word_1, word_tag_1)
    if synsets_1 is None:
        # print("synset(%s) is None" % word_1)
        return None, None

    synsets_2 = wn.synsets(word_2, word_tag_2)
    if synsets_2 is None:
        # print("synset(%s) is None" % word_2)
        return None, None

    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None

    fixme_count = 0

    max_sim = -1.0
    best_pair = None, None
    for synset_1 in synsets_1:
        for synset_2 in synsets_2:
            sim = wn.path_similarity(synset_1, synset_2)
            if sim is None:
                if fixme_count == 0:
                    # print("path_similarity from (%s, %s) is None (fixme_count %d)" % (word_1, word_2, fixme_count))
                    return None, None
            elif sim > max_sim:
                max_sim = sim
                best_pair = synset_1, synset_2
            fixme_count += 1
    return best_pair

def length_dist(synset_1, synset_2):
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
    return math.exp(-ALPHA * l_dist)

def hierarchy_dist(synset_1, synset_2):
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
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) /
            (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))

def word_similarity(word_1, word_2, word_tag_1=None, word_tag_2=None):
    '''synset distance between two words'''
    synset_pair = get_best_synset_pair(word_1, word_2, word_tag_1, word_tag_2)
    return (length_dist(synset_pair[0], synset_pair[1]) *
            hierarchy_dist(synset_pair[0], synset_pair[1]))


######################### sentence similarity ##########################

def most_similar_word(word, sent_word_set):
    """
    Find the word in the joint word set that is most similar to the word
    passed in. We use the algorithm above to compute word similarity between
    the word and each word in the joint word set, and return the most similar
    word and the actual similarity value.
    """
    max_sim = -1.0
    sim_word = ""
    for sent_word in sent_word_set:
        sim = word_similarity(word, sent_word)
        if sim > max_sim:
            max_sim = sim
            sim_word = sent_word
    return sim_word, max_sim


NON_SIM_WORDS = { 'a', 'the', 'in', 'on', 'to' }

def most_similar_pos_word(sent_word_dct, union_word, union_wtag=None):
    """
    Find the word in the joint word set that is most similar to the word
    passed in. We use the algorithm above to compute word similarity between
    the word and each word in the joint word set, and return the most similar
    word and the actual similarity value.
    """
    max_sim = -1.0
    sim_word = ""
    if union_word not in NON_SIM_WORDS:
        for sent_word in sent_word_dct:
            sim = word_similarity(union_word, sent_word, word_tag_1=union_wtag,
                                  word_tag_2=sent_word_dct[sent_word][1])
            if sim > max_sim:
                max_sim = sim
                sim_word = sent_word
    return sim_word, max_sim







def info_content(lookup_word):
    """
    Uses the Brown corpus available in NLTK to calculate a Laplace
    smoothed frequency distribution of words, then uses this information
    to compute the information content of the lookup_word.
    """
    global N
    if N == 0:
        # poor man's lazy evaluation
        for sent in brown.sents():
            for word in sent:
                word = word.lower()
                if not word in BROWN_FREQS:
                    BROWN_FREQS[word] = 0
                BROWN_FREQS[word] = BROWN_FREQS[word] + 1
                N = N + 1
    lookup_word = lookup_word.lower()
    count = 0 if not lookup_word in BROWN_FREQS else BROWN_FREQS[lookup_word]
    return 1.0 - (math.log(count + 1) / math.log(N + 1))

######################### semantic similarity ##########################

def semantic_vector(sent_set, joint_word_set, use_content_norm=False):
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
    for joint_word in joint_word_set:
        if joint_word in sent_set:
            # if word in union exists in the sentence, s(i) = 1 (unnormalized)
            sem_vec[i] = 1.0
            if use_content_norm:
                sem_vec[i] = sem_vec[i] * math.pow(info_content(joint_word), 2)
        else:
            # find the most similar word in the joint set and set the sim value
            sim_word, max_sim = most_similar_word(joint_word, sent_set)
            sem_vec[i] = PHI if max_sim > PHI else 0.0
            if use_content_norm:
                sem_vec[i] = sem_vec[i] * info_content(joint_word) * info_content(sim_word)
        i = i + 1
    return sem_vec

######################### word order similarity ##########################

def semantic_and_word_order_vectors(first_word, sent_word_dct, joint_word_set, use_content_norm=False):
    """
    Computes the word order vector for a sentence. The sentence is passed
    in as a collection of words. The size of the word order vector is the
    same as the size of the joint word set. The elements of the word order
    vector are the position mapping (from the windex dictionary) of the
    word in the joint set if the word exists in the sentence. If the word
    does not exist in the sentence, then the value of the element is the
    position of the most similar word in the sentence as long as the similarity
    is above the threshold ETA.
    """
    vec_len = len(joint_word_set)
    sem_vec = np.zeros(vec_len)
    ord_vec = np.zeros(vec_len)
    for idx, joint_word in enumerate(joint_word_set):
        try:    # TODO: shouldn't try/except KeyError be faster than checking 'in'??
            # word in joint_word_set found in sentence, just populate the index
            ord_vec[idx] = sent_word_dct[joint_word]
            sem_vec[idx] = 1.0
            if use_content_norm:
                info_cont = info_content(joint_word)
                sem_vec[idx] *= math.pow(info_content(joint_word), 2)
        except KeyError:
            # word not in joint_word_set, find most similar word and populate
            # word_vector with the thresholded similarity
            sim_word, max_sim = most_similar_word(joint_word, sent_word_dct.keys())
            ord_vec[idx] = sent_word_dct[sim_word] if max_sim > ETA else 0
            sem_vec[idx] = max_sim if max_sim > PHI else 0.0
            if use_content_norm:
                sem_vec[idx] = sem_vec[idx] * info_content(joint_word) * info_content(sim_word)
    return sem_vec, ord_vec

def pos_tag_sem_ord_word_vectors(first_word, sent_word_dct, joint_wordpos_set, use_content_norm=False):
    """
    Computes the word order vector for a sentence. The sentence is passed
    in as a collection of words. The size of the word order vector is the
    same as the size of the joint word set. The elements of the word order
    vector are the position mapping (from the windex dictionary) of the
    word in the joint set if the word exists in the sentence. If the word
    does not exist in the sentence, then the value of the element is the
    position of the most similar word in the sentence as long as the similarity
    is above the threshold ETA.
    """
    vec_len = len(joint_wordpos_set)
    sem_vec = np.zeros(vec_len)
    ord_vec = np.zeros(vec_len)
    for idx, joint_wordpos in enumerate(joint_wordpos_set):
        joint_word = joint_wordpos[0]
        joint_wtag = joint_wordpos[1]
        try:
            ord_vec[idx] = sent_word_dct[joint_word][0]
            sem_vec[idx] = 1.0
            if use_content_norm:
                info_cont = info_content(joint_word)
                sem_vec[idx] *= math.pow(info_content(joint_word), 2)
        except KeyError:
            # word not in joint_wordpos_set, find most similar word and populate
            # word_vector with the thresholded similarity
            # pdb.set_trace()
            sim_word, max_sim = most_similar_pos_word(sent_word_dct, joint_word, joint_wtag)
            ord_vec[idx] = sent_word_dct[sim_word][0] if max_sim > ETA else 0
            sem_vec[idx] = max_sim if max_sim > PHI else 0.0
            if use_content_norm:
                sem_vec[idx] = sem_vec[idx] * info_content(joint_word) * info_content(sim_word)
    return sem_vec, ord_vec

######################### vector cosine similarities ##########################

def semantic_similarity(sentence_1, sentence_2, use_content_norm=False):
    """
    Computes the semantic similarity between two sentences as the cosine
    similarity between the semantic vectors computed for each sentence.
    """
    word_set_1 = set(nltk.word_tokenize(sentence_1))
    word_set_2 = set(nltk.word_tokenize(sentence_2))
    joint_word_set = word_set_1.union(word_set_2)
    vec_1 = semantic_vector(word_set_1, joint_word_set, use_content_norm)
    vec_2 = semantic_vector(word_set_2, joint_word_set, use_content_norm)
    return np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))

def word_order_vector(sent_word_dct, joint_word_set):
    """
    Computes the word order vector for a sentence. The sentence is passed
    in as a collection of words. The size of the word order vector is the
    same as the size of the joint word set. The elements of the word order
    vector are the position mapping (from the windex dictionary) of the
    word in the joint set if the word exists in the sentence. If the word
    does not exist in the sentence, then the value of the element is the
    position of the most similar word in the sentence as long as the similarity
    is above the threshold ETA.
    """
    ord_vec = np.zeros(len(joint_word_set))
    for idx, joint_word in enumerate(joint_word_set):
        try:    # TODO: shouldn't try/except KeyError be faster than checking 'in'??
            # word in joint_word_set found in sentence, just populate the index
            ord_vec[idx] = sent_word_dct[joint_word]
        except KeyError:
            # word not in joint_word_set, find most similar word and populate
            # word_vector with the thresholded similarity
            sim_word, max_sim = most_similar_word(joint_word, sent_word_dct.keys())
            if max_sim > ETA:
                ord_vec[idx] = sent_word_dct[sim_word]
            else:
                ord_vec[idx] = 0
    return ord_vec

def word_order_similarity(sentence_1, sentence_2):
    """
    Computes the word-order similarity between two sentences as the normalized
    difference of word order between the two sentences.
    """
    # NOTE: These dicts record only the *last* occurence of each word
    word_lst_1 = nltk.word_tokenize(sentence_1)
    word_dct_1 = {word: idx for idx, word in enumerate(word_lst_1)}
    word_lst_2 = nltk.word_tokenize(sentence_2)
    word_dct_2 = {word: idx for idx, word in enumerate(word_lst_2)}

    # TODO: Don't neet to make this a list -- the enumerate order is constant.
    joint_word_set = set(word_dct_1.keys()).union(word_dct_2.keys())
    wov_1 = word_order_vector(word_dct_1, joint_word_set)
    wov_2 = word_order_vector(word_dct_2, joint_word_set)
    return 1.0 - (np.linalg.norm(wov_1 - wov_2) / np.linalg.norm(wov_1 + wov_2))

######################### overall similarity ##########################

NLTK_POS_TAG_TO_WORDNET_KEY = { 'A': 'a', 'N': 'n', 'R': 'r', 'V': 'v', 'S': 's'}

def pos_wnk(tag):
    try:
        return NLTK_POS_TAG_TO_WORDNET_KEY[tag[0]]
    except KeyError:
        return None

def sentence_similarity(sentence_1, sentence_2, use_content_norm=False, delta=DELTA):
    """
    Calculate the semantic similarity between two sentences. The last
    parameter is True or False depending on whether information content
    normalization is desired or not.
    """
    # NOTE: These dicts record only the *last* occurence of each word
    word_lst_1 = nltk.word_tokenize(sentence_1)
    first_wd_1 = word_lst_1[0]
    pos_tags_1 = nltk.pos_tag(word_lst_1)
    word_dct_1 = {wordpos[0]: (idx, pos_wnk(wordpos[1])) for idx, wordpos in enumerate(pos_tags_1)}
    word_set_1 = set(word_dct_1.keys())

    word_lst_2 = nltk.word_tokenize(sentence_2)
    first_wd_2 = word_lst_2[0]
    pos_tags_2 = nltk.pos_tag(word_lst_2)
    word_dct_2 = {wordpos[0]: (idx, pos_wnk(wordpos[1])) for idx, wordpos in enumerate(pos_tags_2)}
    word_set_2 = set(word_dct_2.keys())

    # pdb.set_trace()
    joint_word_set = word_set_1.union(word_set_2)
    joint_wordpos_set = { (word, word_dct_2[word][1] if word in word_dct_2 else word_dct_1[word][1]) for word in joint_word_set}

    semvec_1, ordvec_1 = pos_tag_sem_ord_word_vectors(first_wd_1, word_dct_1, joint_wordpos_set, use_content_norm)
    semvec_2, ordvec_2 = pos_tag_sem_ord_word_vectors(first_wd_2, word_dct_2, joint_wordpos_set, use_content_norm)
    semantic_sim = np.dot(semvec_1, semvec_2.T) / (np.linalg.norm(semvec_1) * np.linalg.norm(semvec_2))
    word_ord_sim = 1.0 - (np.linalg.norm(ordvec_1 - ordvec_2) / np.linalg.norm(ordvec_1 + ordvec_2))
    return delta * semantic_sim + (1.0 - delta) * word_ord_sim


def sentence_similarity_slow(sentence_1, sentence_2, use_content_norm=False, delta=DELTA):
    """
    Calculate the semantic similarity between two sentences. The last
    parameter is True or False depending on whether information content
    normalization is desired or not.
    """
    semantic_sim = semantic_similarity(sentence_1, sentence_2, use_content_norm)
    word_ord_sim = word_order_similarity(sentence_1, sentence_2)
    return delta * semantic_sim + (1.0 - delta) * word_ord_sim

######################### main / test ##########################

def smoke_test():
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
    print("W-Sim \t Paper \t word_1 \t word_2")
    print("----- \t ----- \t ------ \t ------")
    for word_pair in word_pairs:
        print(" %.2f \t %.2f \t %s %s %s" % (word_similarity(word_pair[0], word_pair[1]), word_pair[2],
                                             word_pair[0], ' '*(14 - len(word_pair[0])), word_pair[1]))

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
        print("%.3f\t %.3f\t %.3f\t %s %s %s" % (sentence_similarity(sent_pair[0], sent_pair[1], False),
                                                 sentence_similarity(sent_pair[0], sent_pair[1], True),
                                                 sent_pair[2], sent_pair[0], ' '*(spacing - len(sent_pair[0])),
                                                 sent_pair[1]))

def sim_weighted_qas(qst_1, ans_1, qst_2, ans_2, q_weight=0.5):
    '''dot-product (projection) similarity combining similarities of questions and, if available, answers'''
    assert q_weight > 0.0 and q_weight <= 1.0
    # print("SIM_WEIGHTED_QAS(", qst_1, ans_1, qst_2, ans_2, q_weight, sim_func, ")")
    q_sim = sentence_similarity(qst_1, qst_2)
    if q_weight < 1.0:
        if ans_1 and ans_2:
            try:
                a_sim = sentence_similarity(ans_1, ans_2)
                return (q_sim - a_sim) * q_weight + a_sim
            except ValueError as vex:
                print("Error on answers (%s|%s): %s" % (ans_1, ans_2, vex))
                raise vex
    return q_sim

def similarity_dict(train_quats, trial_quat, q_weight=1.0, min_sim_val=0):
    '''
    Returns a dict mapping train_quats' indexes to their similarity with this_text,
        provide their similarity value >= min_sim_val
        similarity_func:    function returning the similariy between two texts (as in sentences)
        min_sim_val:        similarity threshold
    '''
    sim_dict = {}
    for idx, train_quat in enumerate(train_quats):
        if train_quat is trial_quat:
            continue
        try:
            sim = sim_weighted_qas(train_quat.question, train_quat.answer,
                                   trial_quat.question, trial_quat.answer, q_weight=q_weight)
            # sim = unit_clip_verbose(sim)
            sim = sim_nltk.prob_clip_verbose(sim, where="(%d x %d)" % (train_quat.id, trial_quat.id), verbose=False)
            if  sim >= min_sim_val:
                sim_dict[idx] = sim
        except ValueError as ex:
            print("Continuing past error at idx: {}  ({})  ({})".format(idx, ex, train_quats[idx]))
            raise ex
    return  sim_dict


def find_nearest_quats(train_quats, trial_quat, q_weight=1.0, max_count=5, min_sim_val=0):
    '''
    Find the N most similar texts to this_text and return a list of (index, similarity) pairs in
    descending order of similarity.
        train_quats:        The training sentences or question-answer-tuples or whatever is to be compared.
        trial_quat:         The trial object to be compared with the training objects; must have at least a .question attribute.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
        max_count           maximum size of returned dict
    '''
    assert q_weight >= 0.0
    sim_dict = similarity_dict(train_quats, trial_quat, q_weight=q_weight, min_sim_val=min_sim_val)
    return sim_nltk.nlargest_items_by_value(sim_dict, max_count)


###############################################################################
if __name__ == '__main__':
    smoke_test()
