#!/usr/bin/env python3
# Depends on: nltk.download('punkt')
'''Text similarity (between sentences or phrases) using NLTK'''

import heapq
import string
import time
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import text_fio

STEMMER = nltk.stem.porter.PorterStemmer()
TRANS_NO_PUNCT = str.maketrans('', '', string.punctuation)

def stem_tokens(tokens, stemmer=STEMMER):
    '''list of stems, one per input tokens'''
    return [stemmer.stem(item) for item in tokens]

def normalize(text, translation=TRANS_NO_PUNCT):
    '''remove punctuation, lowercase, stem'''
    return stem_tokens(nltk.word_tokenize(text.translate(TRANS_NO_PUNCT).lower()))

VECTORIZER = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def ident(obj):
    '''identify function: just returns its argument'''
    return obj

def first(obj):
    '''first: returns the first item from an indexible, or failing that, just the object'''
    try:
        return obj.__getitem__(0)
    except:
        return obj

def second(obj):
    '''second: returns second item from an indexible, or failing that, just the object'''
    try:
        return obj.__getitem__(1)
    except:
        return obj

def third(obj):
    '''second: returns second item from an indexible, or failing that, just the object'''
    try:
        return obj.__getitem__(2)
    except:
        return obj

def cosine_sim_txt(txt_obj_1, txt_obj_2, get_text=ident, vectorizer=VECTORIZER):
    '''dot-product (projection) similarity'''
    tfidf = vectorizer.fit_transform([get_text(txt_obj_1), get_text(txt_obj_2)])
    return ((tfidf * tfidf.T).A)[0, 1]

def cosine_sim_qas(qas_obj_1, qas_obj_2, get_question=second, get_answer=third, q_weight=0.5, vectorizer=VECTORIZER):
    '''dot-product (projection) similarity combining similarities of questions and, if available, answers'''
    assert 0.0 < q_weight and q_weight <= 1.0
    if q_weight >= 1.0:
        return cosine_sim_txt(qas_obj_1, qas_obj_2, get_question, vectorizer)
    # print("DBG CSQ:  Q(%s)  A(%s)" % (get_question(qas_obj_2), get_answer(qas_obj_2)))
    tfidf = vectorizer.fit_transform([get_question(qas_obj_1), get_question(qas_obj_2)])
    q_sim = ((tfidf * tfidf.T).A)[0, 1]
    if q_weight < 1.0:
        ans_1 = get_answer(qas_obj_1)
        ans_2 = get_answer(qas_obj_2)
        if ans_1 and ans_2:
            try:
                tfidf = vectorizer.fit_transform([ans_1, ans_2])
                a_sim = ((tfidf * tfidf.T).A)[0, 1]
                return (q_sim - a_sim) * q_weight - a_sim
            except ValueError as vex:
                print("Error on answers (%s|%s): %s" % (ans_1, ans_2, vex))
    return q_sim


def cosine_sim_qas_2(qas_obj_1, qas_obj_2, get_question=second, get_answer=third, q_weight=0.5, vectorizer=VECTORIZER):
    '''dot-product (projection) similarity combining similarities of questions and, if available, answers'''
    assert 0.0 < q_weight and q_weight <= 1.0
    if q_weight >= 1.0:
        print("Degenerate q_weight: ", q_weight)
        return cosine_sim_txt(qas_obj_1, qas_obj_2, get_question, vectorizer)
    # print("DBG CSQ:  Q(%s)  A(%s)" % (get_question(qas_obj_2), get_answer(qas_obj_2)))
    qst_1 = get_question(qas_obj_1)
    qst_2 = get_question(qas_obj_2)
    ans_1 = get_answer(qas_obj_1)
    ans_2 = get_answer(qas_obj_2)
    try:
        tfidf = vectorizer.fit_transform([qst_1, qst_2, ans_1, ans_2])
        q_sim = ((tfidf * tfidf.T).A)[0, 1]
        a_sim = ((tfidf * tfidf.T).A)[2, 3]
        return (q_sim - a_sim) * q_weight - a_sim
    except ValueError as vex:
        print("Error, probably on answers (%s|%s): %s" % (ans_1, ans_2, vex))
    return 0.0


def smoke_test():
    '''Tests that basic sentence similarity functionality works, or at least does not blow-up'''
    sent_1 = 'a little bird'
    sent_2 = 'a little bird chirps'
    sent_3 = 'a big dog barks a lot'
    print("cosine_sim_txt(%s, %s) == %f" % (sent_1, sent_1, cosine_sim_txt(sent_1, sent_1)))
    print("cosine_sim_txt(%s, %s) == %f" % (sent_1, sent_2, cosine_sim_txt(sent_1, sent_2)))
    print("cosine_sim_txt(%s, %s) == %f" % (sent_1, sent_3, cosine_sim_txt(sent_1, sent_3)))

def nearest_known(similarity_func, saved_texts, threshold, input_text):
    idx, sim = nearest_other_idx(similarity_func, saved_texts, input_text, threshold)
    if idx < 0:
        print("No saved text found more similar than %f" % threshold)
    else:
        print("Nearest at %f (%d) %s" % (sim, idx, saved_texts[idx]))

def nearest_other_idx(similarity_func, other_texts, this_text, max_sim_val):
    '''
    Find the text in other_texts most similar to this_text and return its index.
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

def list_nearest_other_idx(texts, similarity_func=cosine_sim_txt):
    '''
    For each text in texts, find the index of the most similar other text.
    Returns the list of indexes.  The mapping is not necessarily 1-1, that is,
    two texts may share a most similar other text.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
    '''
    nearests = len(texts)*[None]
    for idx, txt in enumerate(texts):
        max_idx_0, max_sim_0 = nearest_other_idx(similarity_func, texts[:idx], txt, -1)
        max_idx_1, max_sim_1 = nearest_other_idx(similarity_func, texts[idx+1:], txt, max_sim_0)
        nearests[idx] = 1 + idx + max_idx_1 if max_sim_1 > max_sim_0 else max_idx_0
    return nearests

def show_nearest_neighbors(texts, nearest_indexes=None, similarity_func=cosine_sim_txt, verbose=True):
    if nearest_indexes is None:
        nearest_indexes = list_nearest_other_idx(texts)
    for idx, txt in enumerate(texts):
        nearest_idx = nearest_indexes[idx]
        nearest_txt = texts[nearest_idx]
        print("  %3d.  T  %s\n  %3d.  O  %s\n" % (idx, txt, nearest_idx, nearest_txt))

###############################################################################
def similarity_dict(similarity_func, all_texts, this_text, excludes=None, min_sim_val=0.0):
    '''
    Returns a dict mapping all_texts' indexes to their similarity with this_text,
        provide their similarity value >= min_sim_val
        similarity_func:    function returning the similariy between two texts (as in sentences)
        min_sim_val:        similarity threshold
    '''
    if excludes == None:
        excludes = []
    sim_dict = {}
    for idx, a_text in enumerate(all_texts):
        if idx in excludes:
            continue
        sim = similarity_func(this_text, a_text)
        if  sim > min_sim_val:
            sim_dict[idx] = sim
    return  sim_dict

def nlargest_items_by_value(dict_with_comparable_values, count=10):
    '''Returns a list of the maximally valued N items (key, value)-tuples) in descending order by value.'''
    return heapq.nlargest(count, dict_with_comparable_values.items(), key=lambda item: item[1])

def nlargest_keys_by_value(dict_with_comparable_values, count=10):
    '''Returns a list of the keys to the greatest values, in descending order by value.'''
    return heapq.nlargest(count, dict_with_comparable_values, key=dict_with_comparable_values.get)

def nlargest_values(dict_with_comparable_values, count=10):
    '''Returns a list of the greatest values in descending order.  Duplicates permitted.'''
    return heapq.nlargest(count, dict_with_comparable_values.values())

def most_similar_items_list(similarity_func, all_texts, this_text, excludes=None, max_count=5, min_sim_val=0.0):
    '''
    Find the N most similar texts to this_text and return a list of (index, similarity) pairs in
    descending order of similarity.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
        max_count           maximum size of returned dict
        max_sim_val:        the initial value of max, or the maximum similariy found so far.
    '''
    sim_dict = similarity_dict(similarity_func, all_texts, this_text, excludes, min_sim_val)
    return nlargest_items_by_value(sim_dict, max_count)

def list_most_sim_texts_list(texts, similarity_func=cosine_sim_txt, exclude_self=True, max_count=5, min_sim_val=0.0):
    '''
    For each text in texts, find a list of indexes of the most similar texts.
    Returns list of lists of items as in: [[(index, similariy), ...], ...]
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
    '''
    if exclude_self:
        nearests = len(texts)*[None]
        for idx, txt in enumerate(texts):
            # print("DBG LMSTL: ", txt)
            nearests[idx] = most_similar_items_list(similarity_func, texts, txt, [idx], max_count, min_sim_val)
        return nearests
    return [most_similar_items_list(similarity_func, texts, txt, None, max_count, min_sim_val) for txt in texts]

def list_most_sim_texts_list_verbose(texts, similarity_func=cosine_sim_txt,
        exclude_self=True, max_count=5, min_sim_val=0.2):
    beg_time = time.time()
    most_sim_texts_list = list_most_sim_texts_list(texts, similarity_func, exclude_self, max_count, min_sim_val)
    seconds = time.time() - beg_time
    print("list_most_sim_texts_list(size=%d, count=%d) took %.1f seconds" % (len(texts), max_count, seconds))
    return most_sim_texts_list

def list_most_sim_qas_list_verbose(qas, similarity_func=cosine_sim_qas_2,
        exclude_self=True, max_count=5, min_sim_val=0.2, q_weight=0.6667):
    beg_time = time.time()
    most_sim_texts_list = list_most_sim_texts_list(qas, similarity_func, exclude_self, max_count, min_sim_val)
    seconds = time.time() - beg_time
    print("list_most_sim_qas_list(size=%d, count=%d) took %.1f seconds" % (len(qas), max_count, seconds))
    return most_sim_texts_list

def show_most_sim_texts_list(texts, most_sim_lists=None, similarity_func=cosine_sim_txt):
    if most_sim_lists is None:
        most_sim_lists = list_most_sim_qas_list_verbose(texts)     # use defaults
    for idx, txt in enumerate(texts):
        most_sim_list = most_sim_lists[idx]
        print("  %3d.  %s" % (idx, txt))
        for oix, sim in most_sim_list:
            print("        %3d   %.5f   %s" % (oix, sim, texts[oix]))
        print()
    return most_sim_lists

def save_most_sim_lists_tsv(texts, qas, path, most_sim_lists=None, exclude_self=True, max_count=7,
    min_sim_val = 0.0):
    if most_sim_lists is None:
        most_sim_lists = list_most_sim_texts_list(texts, exclude_self=exclude_self,
            max_count=max_count, min_sim_val=min_sim_val)
    with open(path, "w") as out:
        for idx, txt in enumerate(texts):
            most_sim_list = most_sim_lists[idx]
            assert txt == qas[idx][0]
            print(idx, txt, qas[idx][1], qas[idx][2], sep="\t", file=out)
            for oix, sim in most_sim_list:
                print("\t%d\t%.5f\t%s\t%s\t%s" % (oix, sim, texts[oix], qas[oix][1], str(qas[oix][2])), file=out)
            print(file=out)
    return most_sim_lists


def save_most_sim_qa_lists_tsv(qas, path, most_sim_lists=None, exclude_self=True, max_count=7,
    min_sim_val = 0.2, q_weight=0.8):
    if most_sim_lists is None:
        most_sim_lists = list_most_sim_qas_list_verbose(qas, exclude_self=exclude_self,
            max_count=max_count, min_sim_val=min_sim_val, q_weight=q_weight)
        assert len(most_sim_lists) > 0
    out = text_fio.open_out_file(path)
    for idx, lst in enumerate(qas):
        most_sim_list = most_sim_lists[idx]
        print(idx, lst[1], lst[2], lst[3], sep="\t", file=out)
        for oix, sim in most_sim_list:
            print("\t%3d\t%.5f\t%s\t%s\t%s\t" % (oix, sim, qas[oix][1], qas[oix][2], qas[oix][3]), file=out)
        print(file=out)
    if path != '-':
        close(out)
    return most_sim_lists
