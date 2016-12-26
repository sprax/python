#!/usr/bin/env python3
# Sprax Lines       2016.12.26      Written with Python 3.5
"""LHRWCC: Linear Homogenous Recurrence With Constant Coefficients.
   Class and unit tests.
   """

import unittest
import fibonaccis

class LinHomoRecWithConstCoeffs:
    """LHRWCC: Linear Homogenous Recurrence With Constant Coefficients"""

    def __init__(self, coeffs, inits):
        '''Constructor'''
        self.order = len(coeffs)
        assert len(inits) == self.order
        self.inits = inits
        self.coeffs = coeffs
        self.length = self.order 

    def a_n_recurse(self, idx):
        '''Deprecated: recursively computes Nth term in the SHRWCC sequence'''
        if idx < self.order:
            return self.inits[idx]
        tot = 0
        for k in range(self.order):
            tot += self.coeffs[k] * self.a_n_recurse(idx - k - 1)
        return tot

    def a_n_list(self, length):
        '''Return a memo-ized list of numbers in the SHRWCC sequence'''
        if self.length >= length:
            return self.inits[:length]
        while self.length < length:
            tot = 0
            for k in range(self.order):
                tot += self.coeffs[k] * self.inits[-(k + 1)]
            self.inits.append(tot)
            self.length += 1
        assert len(self.inits) == length
        return self.inits

class TestLinHomoRecWithConstCoef(unittest.TestCase):
    '''unit tests'''

    def setUp(self):
        self.fib_array = [y for y in fibonaccis.fib_generate(32)]
        print(str(LinHomoRecWithConstCoeffs.__doc__))
        print(str(self.id()), '\n')

    def test_fibs(self):
        '''Test against fibonaccis'''
        length = 30
        print("test_fibs", length)
        fibs = LinHomoRecWithConstCoeffs([1, 1], [1, 1])
        print("fibs.order: {}".format(fibs.order))
        save_list = []
        for j in range(length):
            a_j = fibs.a_n_recurse(j)
            f_j = self.fib_array[j+1]
            print("fibs.a_n_recurse({}) => {} =?= {}".format(j, a_j, f_j))
            assert a_j == f_j
            save_list.append(a_j)
        test_list = fibs.a_n_list(length)
        print(test_list)
        assert test_list == save_list

if __name__ == '__main__':
    unittest.main()
