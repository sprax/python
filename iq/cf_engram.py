#!/usr/env python'''
'''
Compare two documents(string array) based on n grams.
doc1 – Today is Sunday.
doc2 – Today is Saturday
if n = 2 then number of duplicates is 1 (Today is)
if n = 1 then number of duplicates is 2 (Today, is)
if n = 3 duplicates is 0
'''

def n_grams(num, doc):
    ''' return n-grams of doc (list of tokens) as a set of n-tuples '''
    n_tuples = set()
    for idx in range(len(doc) - num + 1):
        n_tuples.add(tuple(doc[idx:idx + num]))
    return n_tuples

def main(beg=0, end=1):
    ''' test driver '''
    doc_a = "Today is Sunday".split()
    doc_b = "Today is Saturday".split()
    n_gram_2_a = n_grams(2, doc_a)
    n_gram_2_b = n_grams(2, doc_b)
    print("n_grams(2, doc_b):", n_gram_2_b)
    print("n_grams(2, doc_a):", n_gram_2_a)
    print("intersect(n_gram_2_a, n_gram_2_b):", n_gram_2_a.intersection(n_gram_2_b))


if __name__ == '__main__':
    main()
