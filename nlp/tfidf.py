
#!/usr/bin/env python3
# Sprax Lines       2018.01      Python 3.5
'''Compute TFIDF matrix on a list of vectorized documents'''


def tfidf_doc_list(doc_list):
    ''' Input: list of term-frequency vectors representing documents.
        Output: list of TF-IDF vectors representing compared documents
        (same dimensions as input)
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


def test_tfidf_doc_list_1(ntokens=5, show=False):
    '''test that tfidf_doc_list gives the correct output for "idendity matrix" input'''
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


test_tfidf_doc_list_1(6, show=True)
