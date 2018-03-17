#!/usr/bin/env python2
"""
computes null space for matrix in Wikipedia example:
https://en.wikipedia.org/wiki/Kernel_(linear_algebra)
https://stackoverflow.com/questions/5889142/python-numpy-scipy-finding-the-null-space-of-a-matrix
"""
import scipy
import numpy as np
from scipy import linalg, matrix

def null(A, eps=1e-12):
    u, s, vh = scipy.linalg.svd(A)
    padding = max(0,np.shape(A)[1]-np.shape(s)[0])
    null_mask = np.concatenate(((s <= eps), np.ones((padding,),dtype=bool)),axis=0)
    null_space = scipy.compress(null_mask, vh, axis=0)
    return scipy.transpose(null_space)


def show_null(A):
    print "A:", A
    print "null(A):", null(A)
    print "A * null(A):", A * null(A)

A = matrix([
    [2,  3, 5],
    [-4, 2, 3]
])
show_null(A)

# [[ 0.         -0.70710678]
#  [ 0.          0.        ]
#  [ 0.          0.70710678]
#  [ 1.          0.        ]]

# null(A):
# [[  4.44089210e-16]
# [  6.66133815e-16]]

A = matrix([[1,0,1,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]])
show_null(A)
# print A * null(A)
# [[ 0.  0.]
#  [ 0.  0.]
#  [ 0.  0.]
#  [ 0.  0.]]
