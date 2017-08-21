#!/usr/bin/env python3
# Depends on: nltk.download('punkt')

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def smoke_test():
    sent_1 = 'a little bird'
    sent_2 = 'a little bird chirps'
    sent_3 = 'a big dog barks'
    print("cosine_sim(%s, %s) == %f" % (sent1, sent1, cosine_sim(sent_1, sent_1)))
    print("cosine_sim(%s, %s) == %f" % (sent1, sent2, cosine_sim(sent_1, sent_2)))
    print("cosine_sim(%s, %s) == %f" % (sent1, sent3, cosine_sim(sent_1, sent_3)))


def nearest_other(sim_func, vocab, this_text, other_texts, starting_max):
    '''
    Find the text in other_texts most similar to this_text.
    Returns the index of the found text.
    sim_func:   function returning the similariy between two texts (as in sentences)
    vocab:      the set of all known words
    starting_max:   the initial value of max, or the maximum similariy found so far.
    '''
    max_oth = None
    this_tok = raw_tokens(this_text)
    this_sum = sum_tokens(model, this_tok)
    for idx, other in enumerate(other_texts):
        other_tok = word_tokens(vocab, other)
        other_sum = sum_tokens(model, other_tok)
        sim = similarity(this_sum, other_sum)
        if max_sim < sim:
            max_sim = sim
            max_idx = idx
    return max_idx, max_sim

def nearest_others(sim_func, vocab, texts):
    '''
    For each text in texts, find the index of the most similar other text.
    Returns the list of indexes.  The mapping is not necessarily 1-1, that is,
    two texts may share a most similar other text.
    sim_func:   function returning the similariy between two texts (as in sentences)
    vocab:      the set of all known words
    '''
    nearests = len(texts)*[None]
    for idx, txt in enumerate(texts):
        sim_idx_0, max_sim_0 = nearest_other(model, vocab, txt, texts[:idx], -1)
        sim_idx_1, max_sim_1 = nearest_other(model, vocab, txt, texts[idx+1:], max_sim_0)
        nearests[idx] = sim_idx_1 if max_sim_1 > max_sim_0 else max_idx_0
    return nearests
