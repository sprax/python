#!/usr/bin/env python3
'''
word2vec similarity
TODO: understand accuracy, and some others in:
    ['_load_specials', '_save_specials', '_smart_save', 'accuracy', 'doesnt_match',
    'evaluate_word_pairs', 'get_embedding_layer', 'index2word', 'init_sims', 'load',
    'load_word2vec_format', 'log_accuracy', 'log_evaluate_word_pairs', 'most_similar',
    'most_similar_cosmul', 'n_similarity', 'save', 'save_word2vec_format',
    'similar_by_vector', 'similar_by_word', 'similarity', 'syn0', 'syn0norm',
    'vector_size', 'vocab', 'wmdistance', 'word_vec', 'wv']
'''
from __future__ import division
# import nltk
# import scipy
import inspect
import random
import re
import string
import time
import gensim
import numpy as np
# from gensim.models import Word2Vec
# from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine

def default_word2vec_model(verbose=True):
    '''Load pre-made word2vec word2vec'''
    # TODO: Use _save_specials and _load_specials?
    beg = time.time()
    word2vec = gensim.models.KeyedVectors.load_word2vec_format(
        'Text/GoogleNews-vectors-negative300.bin', binary=True)
    if verbose:
        print("Seconds to load_word2vec_format:", time.time() - beg)
        # Seconds to load_word2vec_format: 44.98383688926697
    return word2vec

def word2vec_vocab(word2vec, verbose=True):
    '''Initialize vocab as the set of keys from a word2vec word2vec'''
    beg = time.time()
    vocab = set([key for key in word2vec.vocab.keys()])
    if verbose:
        print("Seconds to initialize vocab word2vec:", time.time() - beg)
        # Seconds to initialize vocab word2vec: 1.3567819595336914
    return vocab

def default_stop_words():
    '''get the default stop words'''
    # TODO: exclude who, what, when, where, why, etc.
    return stopwords.words('english')

def vocab_words(vocab, tokens):
    '''filtered words: returns the list of in-vocabulary words from a list of tokens'''
    return [tok for tok in tokens if tok in vocab]

def raw_tokens(text):
    '''given a string, returns a list of tokens, not necessarily words'''
    # TODO: use tokenizer from emo project that saves contractions.
    # TODO: Replace "didn't" with "did not", etc.?  What does the word2vec do?
    busted = re.sub(r'[\d%s]' % string.punctuation, ' ', text)
    return word_tokenize(busted)

def word_tokens(vocab, text):
    '''return list of word tokens from string'''
    tokens = raw_tokens(text)
    return vocab_words(vocab, tokens)

def similarity(vec_a, vec_b):
    '''similarity as cosine (dot product)'''
    return cosine(vec_a, vec_b)

def distance(vec_a, vec_b):
    '''distance as 1.0 - dot_product'''
    return 1.0 - similarity(vec_a, vec_b)

def sum_sentence_similarity(word2vec, vocab, sent_1, sent_2):
    '''crude sentence-content similarity based on summing word vectors'''
    vsent_1 = sum([word2vec[tok] for tok in word_tokens(vocab, sent_1)])
    vsent_2 = sum([word2vec[tok] for tok in word_tokens(vocab, sent_2)])
    return similarity(vsent_1, vsent_2)

def sum_tokens(word2vec, tokens, verbose=False, stops=None):
    '''Vector sum of in-vocabulary word vectors from tokens.'''
    v_sum = None
    for token in tokens:
        try:
            v_tok = word2vec[token]
            v_sum = v_tok if v_sum is None else v_sum + v_tok
        except KeyError as ex:
            if verbose and token.lower() not in stops:
                print("KeyError in", inspect.currentframe().f_code.co_name, ':', ex)
    return v_sum

def sum_tokens_similarity(word2vec, tokens_1, tokens_2, verbose=False):
    '''
    Crude token-list content similarity based on summing word vectors.
    Only in-vocabulary tokens contribute; others are ignored.
    '''
    v_sum_1 = sum_tokens(word2vec, tokens_1, verbose)
    v_sum_2 = sum_tokens(word2vec, tokens_2, verbose)
    return cosine(v_sum_1, v_sum_2)

def compare_token_lists(word2vec, tokens_1, tokens_2, verbose=True):
    '''Show crude token-list content similarity based on summing word vectors.'''
    sim = sum_tokens_similarity(word2vec, tokens_1, tokens_2, verbose)
    dif = 1.0 - sim
    st1 = ' '.join(tokens_1)
    st2 = ' '.join(tokens_2)
    if verbose:
        print("Comparing (%s) & (%s) %s sim %.5f  dif %.5f" % (st1, st2, " "*(24 - len(st1 + st2)), sim, dif))
    return sim

def nearest_neighbors(word2vec, vocab, texts, verbose=False):
    '''For each text in texts, find the index of the most similar other text'''
    nearests = len(texts)*[None]
    stops_words = default_stop_words()
    for idx, txt in enumerate(texts):
        max_sim = 0.0
        max_idx = -99
        txt_tok = raw_tokens(txt)
        txt_sum = sum_tokens(word2vec, txt_tok, verbose, stops_words)
        for oix, oth in enumerate(texts[:idx] + texts[idx + 1:]):
            oth_tok = word_tokens(vocab, oth)
            oth_sum = sum_tokens(word2vec, oth_tok)
            sim = similarity(txt_sum, oth_sum)
            if max_sim < sim:
                max_sim = sim
                max_idx = oix
        nearests[idx] = max_idx if max_idx < idx else max_idx + 1
    return nearests

def show_nearest_neighbors(word2vec, vocab, texts, verbose=True):
    nearest_indexes = nearest_neighbors(word2vec, vocab, texts, verbose)
    for idx, txt in enumerate(texts):
        nearest_idx = nearest_indexes[idx]
        nearest_txt = texts[nearest_idx]
        print("  %3d.  T  %s\n  %3d.  O  %s\n" % (idx, txt, nearest_idx, nearest_txt))

def randomly(seq):
    lst = list(seq)
    random.shuffle(lst)
    return iter(lst)

def show_ascending_norms(word2vec, thresh=4.11):
    max_norm = thresh
    for key in randomly(word2vec.vocab.keys()):
        vec = word2vec[key]
        nrm = np.sqrt(vec.dot(vec))
        # nrm = np.linalg.norm(vec)
        if max_norm < nrm:
            max_norm = nrm
            print("  %.4f  %s" % (nrm, key))
        elif nrm > 6.0/7*max_norm:
            print("           %.4f  %s" % (nrm, key))
#################################### TESTS ####################################

def test_word_similarity(word2vec, aa='king', bb='queen', cc='man', dd='woman'):
    '''show similarity on a tetrad of (analogous) words'''
    print("test_word_similarity:", test_word_similarity.__doc__)
    sim_aa = word2vec.similarity(aa, aa)
    sim_bb = word2vec.similarity(bb, bb)
    absdif = abs(sim_aa - sim_bb)
    print("self similarities of %s and %s to themselves:\t%f and %f, dif %f" %
          (aa, bb, sim_aa, sim_bb, absdif))
    sim_ab = word2vec.similarity(aa, bb)
    sim_ba = word2vec.similarity(bb, aa)
    absdif = abs(sim_ab - sim_ba)
    print("symm similarities of %s to %s and %s to %s:\t%f and %f, dif %f" %
          (aa, bb, bb, aa, sim_ab, sim_ba, absdif))
    sim_ab = word2vec.similarity(aa, bb)
    sim_cd = word2vec.similarity(cc, dd)
    absdif = abs(sim_ab - sim_cd)
    print("opposite sims a:b:c:d %s to %s and %s to %s:\t%f and %f, dif %f" %
          (aa, bb, cc, dd, sim_ab, sim_cd, absdif))
    sim_ac = word2vec.similarity(aa, cc)
    sim_bd = word2vec.similarity(bb, dd)
    absdif = abs(sim_ac - sim_bd)
    print("analogous sims a:c:b:d %s to %s and %s to %s:\t%f and %f, dif %f" %
          (aa, cc, bb, dd, sim_ac, sim_bd, absdif))

def test_word_differences(word2vec, aa='king', bb='queen', cc='man', dd='woman'):
    '''show differences on a tetrad of (analogous) words'''
    vec_aa = word2vec[aa]
    vec_bb = word2vec[bb]
    vec_cc = word2vec[cc]
    vec_dd = word2vec[dd]

    dif_ab = vec_aa - vec_bb
    dif_cd = vec_cc - vec_dd
    sim_xx = cosine(dif_ab, dif_cd)
    print("similarity of vec(%s) - vec(%s) to vec(%s) - vec(%s): %f" % (aa, bb, cc, dd, sim_xx))

    dif_ac = vec_aa - vec_cc
    dif_bd = vec_bb - vec_dd
    sim_yy = cosine(dif_ac, dif_bd)
    print("similarity of vec(%s) - vec(%s) to vec(%s) - vec(%s): %f" % (aa, cc, bb, dd, sim_yy))

def test_word_analogies(word2vec, aa='king', bb='queen', cc='man', dd='woman'):
    '''show arithmetic combos on a tetrad of (analogous) words'''
    vec_aa = word2vec[aa]
    vec_bb = word2vec[bb]
    vec_cc = word2vec[cc]
    vec_dd = word2vec[dd]
    vec_acd = vec_aa - vec_cc + vec_dd
    vec_bdc = vec_bb - vec_dd + vec_cc
    sim_acdb = cosine(vec_acd, vec_bb)
    print("similarity of vec(%s) - vec(%s) + vec(%s) to vec(%s): %f" % (aa, cc, dd, bb, sim_acdb))
    sim_bdca = cosine(vec_bdc, vec_aa)
    print("similarity of vec(%s) - vec(%s) + vec(%s) to vec(%s): %f" % (bb, dd, cc, aa, sim_bdca))

def test_sentence_distance(word2vec, vocab, sent_1="This is a sentence.",
                           sent_2="This, IS, some, OTHER, Sentence!"):
    '''show simple sub-based sentence distance'''
    toks_1 = word_tokens(vocab, sent_1)
    toks_2 = word_tokens(vocab, sent_2)
    print("word_tokens({}) == {}".format(sent_1, toks_1))
    print("word_tokens({}) == {}".format(sent_2, toks_2))
    dist12 = sum_tokens_distance(word2vec, vocab, sent_1, sent_2)
    print("sum_tokens_distance => ", dist12)

def test_contractions(word2vec, verbose=True):
    t_do = ["do"]
    t_does = ["does"]
    t_did = ["did"]
    t_not = ["not"]
    t_do_not = t_do + t_not
    t_does_not = t_does + t_not
    t_did_not = t_did + t_not
    t_dont = ["don't"]
    t_doesnt = ["doesn't"]
    t_didnt = ["didn't"]
    compare_token_lists(word2vec, t_do, t_does, verbose=True)
    compare_token_lists(word2vec, t_do, t_did, verbose=True)
    compare_token_lists(word2vec, t_do, t_not, verbose=True)

    compare_token_lists(word2vec, t_do_not, t_not, verbose=True)
    compare_token_lists(word2vec, t_do_not, t_does_not, verbose=True)
    compare_token_lists(word2vec, t_do_not, t_did_not, verbose=True)

    compare_token_lists(word2vec, t_do_not, t_dont, verbose=True)
    compare_token_lists(word2vec, t_do_not, t_doesnt, verbose=True)
    compare_token_lists(word2vec, t_do_not, t_didnt, verbose=True)

    compare_token_lists(word2vec, t_does_not, t_dont, verbose=True)
    compare_token_lists(word2vec, t_does_not, t_doesnt, verbose=True)
    compare_token_lists(word2vec, t_does_not, t_didnt, verbose=True)

    compare_token_lists(word2vec, t_did_not, t_dont, verbose=True)
    compare_token_lists(word2vec, t_did_not, t_doesnt, verbose=True)
    compare_token_lists(word2vec, t_did_not, t_didnt, verbose=True)

    compare_token_lists(word2vec, t_dont, t_doesnt, verbose=True)
    compare_token_lists(word2vec, t_dont, t_didnt, verbose=True)
    compare_token_lists(word2vec, t_doesnt, t_didnt, verbose=True)

def smoke_test(word2vec, vocab):
    '''sanity checking'''
    test_word_similarity(word2vec)
    test_word_differences(word2vec)
    test_word_analogies(word2vec)
    test_sentence_distance(word2vec, vocab)
    test_contractions(word2vec, verbose=True)
