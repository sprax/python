#!/usr/bin/env python3
'''Find primes by checking each number in a range for divisors.  Primes have no divisors but 1 and themselves.'''
import math

print(str(2) + ' is a prime number')
for n in range(3, 100):
    bound = 1 + math.ceil(math.sqrt(n))
    for x in range(2, bound):
        if n % x == 0:
            print(str(n) + ' equals ' + str(x) + ' * ' + str(n//x))
            break
    else:
        # loop fell through without finding a factor
        print(str(n) + ' is a prime number')
