#!/usr/bin/env python3
# Sprax Lines       2016.12.26      Written with Python 3.5
"""LHRWCC: Linear Homogenous Recurrence With Constant Coefficients.
   Class and unit tests.
   """

import os
import unittest

def os_walk():
    # Set the directory you want to start from
    rootDir = '.'
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname)

# class LinHomoRecWithConstCoeffs:
#     """LHRWCC: Linear Homogenous Recurrence With Constant Coefficients"""
#
#     def __init__(self, coeffs, inits):
#         '''Constructor'''
#         self.order = len(coeffs)
#         assert len(inits) == self.order
#         self.inits = inits
#         self.coeffs = coeffs
#         self.length = self.order
#
#     def a_n_recurse(self, idx):
#         '''Deprecated: recursively computes Nth term in the LHRWCC sequence'''
#         if idx < self.order:
#             return self.inits[idx]
#         tot = 0
#         for k in range(self.order):
#             tot += self.coeffs[k] * self.a_n_recurse(idx - k - 1)
#         return tot
#
#     def a_n_list(self, length):
#         '''Return a memo-ized list of numbers in the LHRWCC sequence'''
#         if self.length >= length:
#             return self.inits[:length]
#         if self.order == 2:
#             return self.a_n_ord2_list(length)
#         if self.order == 3:
#             return self.a_n_ord3_list(length)
#         while self.length < length:
#             tot = 0
#             for k in range(self.order):
#                 tot += self.coeffs[k] * self.inits[-(k + 1)]
#             self.inits.append(tot)
#             self.length += 1
#         assert len(self.inits) == length
#         return self.inits
#
#     def a_n_ord2_list(self, length):
#         '''Simplified list computation for order 2'''
#         start_len = len(self.inits)
#         am1, am2 = self.inits[-1], self.inits[-2]
#         cm1, cm2 = self.coeffs[0], self.coeffs[1]
#         while start_len < length:
#             am2, am1 = am1, cm2*am2 + cm1*am1
#             self.inits.append(am1)
#             start_len += 1
#         return self.inits
#
#     def a_n_ord3_list(self, length):
#         '''Simplified list computation for order 2'''
#         start_len = len(self.inits)
#         am1, am2, am3 = self.inits[-1], self.inits[-2], self.inits[-3]
#         cm1, cm2, cm3 = self.coeffs[0], self.coeffs[1], self.coeffs[2]
#         while start_len < length:
#             am3, am2, am1 = am2, am1, cm3*am3 + cm2*am2 + cm1*am1
#             self.inits.append(am1)
#             start_len += 1
#         return self.inits
#
# def try_reference_rec(ref_coef, ref_init, ref_list, ref_length):
#     '''Test against a known reference recurrence'''
#     length = ref_length
#     print("try_reference_rec", length)
#     test_rec = LinHomoRecWithConstCoeffs(ref_coef, ref_init)
#     print("test_rec.order: {}".format(test_rec.order))
#     save_list = []
#     for j in range(length):
#         a_j = test_rec.a_n_recurse(j)
#         r_j = ref_list[j]
#         print("test_rec.a_n_recurse({}) => {} =?= {}".format(j, a_j, r_j))
#         assert a_j == r_j
#         save_list.append(a_j)
#     test_list = test_rec.a_n_list(length)
#     print(test_list)
#     assert test_list == save_list
#
# #####################################################
# class TestLinHomoRecWithConstCoef(unittest.TestCase):
#     '''unit tests'''
#
#     # def __init__(self):
#     #     self.className = "TestLinHomoRecWithConstCoef(unittest.TestCase)"
#
#     def setUp(self):
#         print(str(LinHomoRecWithConstCoeffs.__doc__))
#         print(str(self.id()), '\n')
#
#     def test_fibonacci(self):
#         '''Test against fibonacci sequence'''
#         length = 30
#         print("test_fibonaccis", length)
#         ref_list = [y for y in fibonaccis.fib_generate(length+1)][1:]
#         try_reference_rec([1, 1], [1, 1], ref_list, length)
#
#     def test_lucas(self):
#         '''Test against Lucas number sequence'''
#         length = 30
#         print("test_lucas", length)
#         ref_list = lucas_list.lucas_list(length+1)
#         try_reference_rec([1, 1], [1, 3], ref_list, length)
#
#     def test_3_7(self):
#         '''Test against coef[3, 7] and init[1, 2] number sequence'''
#         length = 6
#         print("test_3_7", length)
#         ref_list = [1, 2, 13, 53, 250, 1121]
#         try_reference_rec([3, 7], [1, 2], ref_list, length)
#
#     def test_2_3_5(self):
#         '''Test against coef[2, 3, 5] and init[1, 2, 3] number sequence'''
#         length = 7
#         print("test_2_3_5", length)
#         ref_list = [1, 2, 3, 17, 53, 172, 588]
#         try_reference_rec([2, 3, 5], [1, 2, 3], ref_list, length)
#

if __name__ == '__main__':
    # unittest.main()
    os_walk()
