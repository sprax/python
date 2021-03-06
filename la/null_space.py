#!/usr/bin/env python2
"""
computes null space for matrix in Wikipedia example:
https://en.wikipedia.org/wiki/Kernel_(linear_algebra)
https://stackoverflow.com/questions/5889142/python-numpy-scipy-finding-the-null-space-of-a-matrix
"""
import scipy
import numpy as np
from scipy import linalg, matrix

def null(mat, eps=1e-12):
    '''returns null space of matrix mat'''
    u, s, vh = scipy.linalg.svd(mat)   # , full_matrices=False)
    padding = max(0, np.shape(mat)[1]-np.shape(s)[0])
    null_mask = np.concatenate(((s <= eps), np.ones((padding, ), dtype=bool)), axis=0)
    null_space = scipy.compress(null_mask, vh, axis=0)
    return scipy.transpose(null_space)


def show_null(mat):
    '''Print matrix and its null space'''
    print "mat:", mat
    print "null(mat):", null(mat)
    print "mat * null(mat):", mat * null(mat)

def main():
    '''test null function'''
    mat = matrix([
        [2, 3, 5],
        [-4, 2, 3]
    ])
    show_null(mat)

    # [[ 0.         -0.70710678]
    #  [ 0.          0.        ]
    #  [ 0.          0.70710678]
    #  [ 1.          0.        ]]

    # null(mat):
    # [[  4.44089210e-16]
    # [  6.66133815e-16]]

    B = matrix([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    show_null(B)
    # print mat * null(mat)
    # [[ 0.  0.]
    #  [ 0.  0.]
    #  [ 0.  0.]
    #  [ 0.  0.]]


if __name__ == '__main__':
    main()

