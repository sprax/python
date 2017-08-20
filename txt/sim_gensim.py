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
import string
import re
import time
import gensim
# from gensim.models import Word2Vec
# from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine

def get_stop_words():
    '''get the default stop words'''
    return stopwords.words('english')

def init_word2vec_model(verbose=True):
    '''Initialize simple language processing'''
    beg = time.time()
    model = gensim.models.KeyedVectors.load_word2vec_format('Text/GoogleNews-vectors-negative300.bin', binary=True)
    if verbose:
        print("Time to load_word2vec_format:", time.time() - beg)
        # Seconds to load_word2vec_format: 44.98383688926697
    return model

def init_vocab(model, verbose=True):
    '''Initialize vocab from word2vec model'''
    beg = time.time()
    vocab = set([i for i in model.vocab.keys()])
    if verbose:
        print("Time to initialize vocab model:", time.time() - beg)
        # Seconds to initialize vocab model: 1.3567819595336914
    return vocab

def word_tokens(vocab, text):
    '''return list of word tokens form string'''
    txt = re.sub(r'[\d%s]' % string.punctuation, ' ', text)
    raw = word_tokenize(txt)
    tok = [i for i in raw if i in vocab]
    return tok

def sum_tokens_distance(model, vocab, sent_1, sent_2):
    '''simple sum-based distance'''
    vs1 = sum([model[i] for i in word_tokens(vocab, sent_1)])
    vs2 = sum([model[i] for i in word_tokens(vocab, sent_2)])
    return 1.0 - cosine(vs1, vs2)

def test_word_similarity(model, aa='king', bb='queen', cc='man', dd='woman'):
    '''show similarity on a tetrad of (analogous) words'''
    print("test_word_similarity:", test_word_similarity.__doc__)
    sim_aa = model.similarity(aa, aa)
    sim_bb = model.similarity(bb, bb)
    absdif = abs(sim_aa - sim_bb)
    print("self similarities of %s and %s to themselves:\t%f and %f, dif %f" %
          (aa, bb, sim_aa, sim_bb, absdif))
    sim_ab = model.similarity(aa, bb)
    sim_ba = model.similarity(bb, aa)
    absdif = abs(sim_ab - sim_ba)
    print("symm similarities of %s to %s and %s to %s:\t%f and %f, dif %f" %
          (aa, bb, bb, aa, sim_ab, sim_ba, absdif))
    sim_ab = model.similarity(aa, bb)
    sim_cd = model.similarity(cc, dd)
    absdif = abs(sim_ab - sim_cd)
    print("opposite sims a:b:c:d %s to %s and %s to %s:\t%f and %f, dif %f" %
          (aa, bb, cc, dd, sim_ab, sim_cd, absdif))
    sim_ac = model.similarity(aa, cc)
    sim_bd = model.similarity(bb, dd)
    absdif = abs(sim_ac - sim_bd)
    print("analogous sims a:c:b:d %s to %s and %s to %s:\t%f and %f, dif %f" %
          (aa, cc, bb, dd, sim_ac, sim_bd, absdif))

def test_word_differences(model, aa='king', bb='queen', cc='man', dd='woman'):
    '''show differences on a tetrad of (analogous) words'''
    vec_aa = model[aa]
    vec_bb = model[bb]
    vec_cc = model[cc]
    vec_dd = model[dd]

    dif_ab = vec_aa - vec_bb
    dif_cd = vec_cc - vec_dd
    sim_xx = cosine(dif_ab, dif_cd)
    print("similarity of vec(%s) - vec(%s) to vec(%s) - vec(%s): %f" % (aa, bb, cc, dd, sim_xx))

    dif_ac = vec_aa - vec_cc
    dif_bd = vec_bb - vec_dd
    sim_yy = cosine(dif_ac, dif_bd)
    print("similarity of vec(%s) - vec(%s) to vec(%s) - vec(%s): %f" % (aa, cc, bb, dd, sim_yy))

def test_word_analogies(model, aa='king', bb='queen', cc='man', dd='woman'):
    '''show arithmetic combos on a tetrad of (analogous) words'''
    vec_aa = model[aa]
    vec_bb = model[bb]
    vec_cc = model[cc]
    vec_dd = model[dd]
    vec_acd = vec_aa - vec_cc + vec_dd
    vec_bdc = vec_bb - vec_dd + vec_cc
    sim_acdb = cosine(vec_acd, vec_bb)
    print("similarity of vec(%s) - vec(%s) + vec(%s) to vec(%s): %f" % (aa, cc, dd, bb, sim_acdb))
    sim_bdca = cosine(vec_bdc, vec_aa)
    print("similarity of vec(%s) - vec(%s) + vec(%s) to vec(%s): %f" % (bb, dd, cc, aa, sim_bdca))

def test_sentence_distance(model, vocab, sent_1="This is a sentence.", sent_2="This, IS, some, OTHER, Sentence!"):
    '''show simple sub-based sentence distance'''
    toks_1 = word_tokens(vocab, sent_1)
    toks_2 = word_tokens(vocab, sent_2)
    print("word_tokens({}) == {}".format(sent_1, toks_1))
    print("word_tokens({}) == {}".format(sent_2, toks_2))
    dist12 = sum_tokens_distance(model, vocab, sent_1, sent_2)
    print("sum_tokens_distance => ", dist12)

def smoke_test(model, vocab):
    '''sanity checking'''
    test_word_similarity(model)
    test_word_differences(model)
    test_word_analogies(model)
    test_sentence_distance(model, vocab)
