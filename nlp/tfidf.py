#!/usr/bin/env python3
'''
Compute TFIDF matrix on a list of vectorized documents
Sprax Lines       2018.01      Python 3.5
'''
from typing import List
import unittest
import numpy as np


def tfidf_np(mat):
    ''' Input: numpy array where rows are term-frequency vectors representing documents.
        Output: numpy array of TF-IDF vectors representing compared documents
        (same dimensions as input).
    '''
    result = mat.copy()
    # ndocs, ntoks = mat.shape
    doxfreq = np.sum(mat > 0, axis=0)
    doxfreq[doxfreq == 0] = 1
    result /= doxfreq
    return result


def tfidf_doc_list(doc_list : List[List[float]]):
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


class TestTfidf(unittest.TestCase):
    '''tests the toy TFIDF functions above'''

    def setUp(self):
        ''' create minimal instances for testing '''
        self.show = 1
        self.inputs = np.array([
            [1.0, 2.0, 3.0, 4.0, 3.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 3.0, 2.0, 6.0, 6.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 6.0, 6.0, 0.0, 3.0, 2.0, 0.0, 0.0],
            [0.0, 2.0, 9.0, 6.0, 6.0, 6.0, 0.0, 2.0, 0.0]])
        self.expect = np.array([
            [1.0, 1.0, 0.75, 1.0, 1.0, 0.0, 0.0, 0.5, 0.0],
            [0.0, 0.0, 0.75, 0.5, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.50, 1.5, 0.0, 1.0, 2.0, 0.0, 0.0],
            [0.0, 1.0, 2.25, 1.5, 2.0, 2.0, 0.0, 1.0, 0.0]])


    def test_tfidf_doc_list_1(self, ntokens=5):
        '''test that tfidf_doc_list gives the correct output for "diagonal==index" matrix input'''
        doc_list = []
        for idx in range(ntokens):
            lst = [0] * ntokens
            lst[idx] = idx
            doc_list.append(lst)
        if self.show:
            print(doc_list)

        expect = doc_list.copy()
        result = tfidf_doc_list(doc_list)
        self.assertEqual(result, expect)


    def test_tfidf_np_1(self):
        '''test that tfidf_np gives the expected output for self.inputs'''
        if self.show:
            print(self.inputs)
            print(self.expect)
        result = tfidf_np(self.inputs)
        self.assertTrue(np.array_equal(result, self.expect))


    def test_tfidf_same(self):
        '''test that tfidf_doc_list and tfidf_np give the same output for self.inputs'''
        result_np = tfidf_np(self.inputs)
        result_dl = tfidf_doc_list(self.inputs)
        self.assertTrue(np.array_equal(result_np, result_dl))


if __name__ == '__main__':
    unittest.main()
