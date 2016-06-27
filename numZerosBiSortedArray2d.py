#!/usr/bin/python
'''Python 2.7 script to count the number of zeros in a bi-sorted 2d array.
Fast algorithm for NxN matrix: Use the fact that M[j,j] == 0 implies M[p,q] == 0
for any p <= j and q <= j.  Do a biniary search on the diagonal elements to
find min k s.t. M[k,k] == 1,  Add k*k to count of zeros.  Now do the same,
recursively, for the sub-matrices directly right of and below this k x k sub-matrix.
Terminate the recursion when the next sub-matrix has zero extent.
'''

import operator

def countZeros(array, length):
    '''naive counting, O(MN)'''
    return length - reduce(operator.add, array)

def test_countZeros():
    matrix = [
              [0, 0, 0, 0],
              [0, 0, 1, 1],
              [0, 0, 1, 1],
              [0, 1, 1, 1],
              [0, 1, 1, 1],
             ]
    rows = len(matrix)
    cols = len(matrix[0])
    print "rows: ", rows, " cols: ", cols
    result = sum([countZeros(matrix[i], cols) for i in range(rows)])
    print "test_countZeros: ",  result


if __name__ == '__main__':
    test_countZeros()

