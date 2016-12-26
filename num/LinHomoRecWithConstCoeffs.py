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
        '''constructor'''
        assert len(coeffs) == len(inits)
        self.order = len(coeffs)
        self.coeffs = coeffs
        self.inits = inits

    def a_n_recurse(self, idx):
        '''recursively computes Nth term in the SHRWCC sequence'''
        if idx < self.order:
            return self.inits[idx]
        tot = 0
        for k in range(self.order):
            tot += self.coeffs[k] * self.a_n_recurse(idx - k - 1)
        return tot



class TestLinHomoRecWithConstCoef(unittest.TestCase):
    '''unit tests'''

    def setUp(self):
        self.fib_array = [y for y in fibonaccis.fib_generate(32)]
        print(str(LinHomoRecWithConstCoeffs.__doc__))
        print(str(self.id()), '\n')

    def test_fibs(self):
        '''Test against fibonaccis'''
        print("test_fibs")
        fibs = LinHomoRecWithConstCoeffs([1, 1], [1, 1])
        print("fibs.order: {}".format(fibs.order))
        for j in range(30):
            a_j = fibs.a_n_recurse(j)
            f_j = self.fib_array[j+1]
            print("fibs.a_n_recurse({}) => {} =?= {}".format(j, a_j, f_j))
            assert a_j == f_j

if __name__ == '__main__':
    unittest.main()
