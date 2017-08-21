#!/usr/bin/env python3
# Depends on: nltk.download('punkt')

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    '''remove punctuation, lowercase, stem'''
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def smoke_test():
    sent_1 = 'a little bird'
    sent_2 = 'a little bird chirps'
    sent_3 = 'a big dog barks a lot'
    print("cosine_sim(%s, %s) == %f" % (sent_1, sent_1, cosine_sim(sent_1, sent_1)))
    print("cosine_sim(%s, %s) == %f" % (sent_1, sent_2, cosine_sim(sent_1, sent_2)))
    print("cosine_sim(%s, %s) == %f" % (sent_1, sent_3, cosine_sim(sent_1, sent_3)))

def nearest_other(similarity_func, this_text, other_texts, max_sim_val):
    '''
    Find the text in other_texts most similar to this_text.
    Returns the index of the found text.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
        max_sim_val:        the initial value of max, or the maximum similariy found so far.
    '''
    max_sim_idx = -99
    for idx, other_text in enumerate(other_texts):
        sim = similarity_func(this_text, other_text)
        if  max_sim_val < sim:
            max_sim_val = sim
            max_sim_idx = idx
    return  max_sim_idx, max_sim_val

def nearest_others(texts, similarity_func=cosine_sim):
    '''
    For each text in texts, find the index of the most similar other text.
    Returns the list of indexes.  The mapping is not necessarily 1-1, that is,
    two texts may share a most similar other text.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
    '''
    nearests = len(texts)*[None]
    for idx, txt in enumerate(texts):
        max_idx_0, max_sim_0 = nearest_other(similarity_func, txt, texts[:idx], -1)
        max_idx_1, max_sim_1 = nearest_other(similarity_func, txt, texts[idx+1:], max_sim_0)
        nearests[idx] = 1 + idx + max_idx_1 if max_sim_1 > max_sim_0 else max_idx_0
    return nearests

def show_nearest_neighbors(texts, nearest_indexes=None, similarity_func=cosine_sim, verbose=True):
    if nearest_indexes is None:
        nearest_indexes = nearest_others(texts)
    for idx, txt in enumerate(texts):
        nearest_idx = nearest_indexes[idx]
        nearest_txt = texts[nearest_idx]
        print("  %3d.  T  %s\n  %3d.  O  %s\n" % (idx, txt, nearest_idx, nearest_txt))
