
#!/usr/bin/env python3
# Sprax Lines       2018.01      Python 3.5
'''Compute TFIDF matrix on a list of vectorized documents'''

import numpy as np


def tfidf_doc_list(doc_list):
    ''' Input: list of term-frequency vectors representing documents.
        Output: list of TF-IDF vectors representing compared documents
        (same dimensions as input).
    '''
    ntokens = len(doc_list[0])  # count of all unique tokens
    doxfreq = [0] * ntokens     # count
    for doc in doc_list:
        for idx, count in enumerate(doc):
            if count > 0:
                doxfreq[idx] += 1
    for doc in doc_list:
        for idx, count in enumerate(doc):
            if doxfreq[idx] > 0:
                doc[idx] /= doxfreq[idx]
    return doc_list


def tfidf_np(mat):
    ''' Input: numpy array where rows are term-frequency vectors representing documents.
        Output: numpy array of TF-IDF vectors representing compared documents
        (same dimensions as input).
    '''
    result = mat.copy()
    ndocs, ntoks = mat.shape
    doxfreq = np.sum(mat > 0, axis=0)
    doxfreq[doxfreq == 0] = 1
    result /= doxfreq
    return result


def test_tfidf_doc_list_1(ntokens=5, show=False):
    '''test that tfidf_doc_list gives the correct output for "diagonal==index" matrix input'''
    doc_list = []
    for idx in range(ntokens):
        lst = [0] * ntokens
        lst[idx] = idx
        doc_list.append(lst)
    if show:
        print(doc_list)

    expect = doc_list.copy()
    result = tfidf_doc_list(doc_list)
    assert result == expect


def test_tfidf_np_1(show=False):
    '''test that tfidf_np gives the correct output for "diagonal==index" matrix input'''
    inputs = np.array([
        [ 1.,  2.,  3.,  4.,  3.,  0.,  0.,  1.,  0.],
        [ 0.,  0.,  3.,  2.,  6.,  6.,  0.,  0.,  0.],
        [ 0.,  0.,  6.,  6.,  0.,  3.,  2.,  0.,  0.],
        [ 0.,  2.,  9.,  6.,  6.,  6.,  0.,  2.,  0.]])
    expect = np.array([
        [ 1.  ,  1.  ,  0.75,  1.  ,  1.  ,  0.  ,  0.  ,  0.5 ,  0.  ],
        [ 0.  ,  0.  ,  0.75,  0.5 ,  2.  ,  2.  ,  0.  ,  0.  ,  0.  ],
        [ 0.  ,  0.  ,  1.5 ,  1.5 ,  0.  ,  1.  ,  2.  ,  0.  ,  0.  ],
        [ 0.  ,  1.  ,  2.25,  1.5 ,  2.  ,  2.  ,  0.  ,  1.  ,  0.  ]])
    if show:
        print(inputs)
        print(expect)
    result = tfidf_np(inputs)
    assert np.array_equal(result, expect)


def tests(show=False):
    test_tfidf_doc_list_1(6, show=show)
    test_tfidf_np_1(show=False)



if __name__ == '__main__':
    tests(show=True)
