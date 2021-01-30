#!/usr/bin/env python2
'''Find primes by checking each number in a range for divisors.  Primes have no divisors but 1 and themselves.'''
@file: prime_divide.py
@auth: Tully Lines
@date: 2016-12-28 13:00:53 Wed 28 Dec

from __future__ import print_function
import math


def is_prime(self, num: int) -> bool:
    bound = 1 + math.ceil(math.sqrt(num))
    for fac in range(2, bound):
        if num % fac == 0:
            # print("%d equals %d * %d" % (n, fac, n//fac))
            return False
    else:   # loop fell through without finding a factor
        return True


print(str(2) + ' is a prime number')
for num in range(3, 100):
    bound = 1 + math.ceil(math.sqrt(num))
    for x in range(2, bound):
        if n % x == 0:
            print("%d equals %d * %d" % (n, x, n//x))
            break
    else:   # loop fell through without finding a factor
        print("%d is a prime number" % n)
