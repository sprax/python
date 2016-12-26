#!/usr/bin/env python3
# Sprax Lines       2016.12.26      Written with Python 3.5
"""LHRWCC: Linear Homogenous Recurrence With Constant Coefficients.
   Class and unit tests.
   """

import unittest
import fibonaccis
import lucas_list

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
        print(str(LinHomoRecWithConstCoeffs.__doc__))
        print(str(self.id()), '\n')

    def test_fibonacci(self):
        '''Test against fibonacci sequence'''
        length = 30
        print("test_fibonaccis", length)
        ref_list = [y for y in fibonaccis.fib_generate(length+1)][1:]
        self.try_reference_rec([1, 1], [1, 1], ref_list, length)

    def test_lucas(self):
        '''Test against Lucas number sequence'''
        length = 30
        print("test_lucas", length)
        ref_list = lucas_list.lucas_list(length+1)
        self.try_reference_rec([1, 1], [1, 3], ref_list, length)

    def try_reference_rec(self, ref_coef, ref_init, ref_list, ref_length):
        '''Test against a known reference recurrence'''
        length = ref_length
        print("test_reference_rec", length)
        test_rec = LinHomoRecWithConstCoeffs(ref_coef, ref_init)
        print("test_rec.order: {}".format(test_rec.order))
        save_list = []
        for j in range(length):
            a_j = test_rec.a_n_recurse(j)
            r_j = ref_list[j]
            print("test_rec.a_n_recurse({}) => {} =?= {}".format(j, a_j, r_j))
            assert a_j == r_j
            save_list.append(a_j)
        test_list = test_rec.a_n_list(length)
        print(test_list)
        assert test_list == save_list

if __name__ == '__main__':
    unittest.main()
