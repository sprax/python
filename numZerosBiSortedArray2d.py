#!/usr/bin/python
'''Python 2.7 script to count the number of zeros in a bi-sorted 2d array.'''

import operator

def countZeros(array, length):
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

