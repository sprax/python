#!/usr/bin/env python3 
'''Find primes by checking each number in a range for divisors.  Primes have no divisors but 1 and themselves.'''

for n in range(2, 53):
    for x in range(2, n):
        if n % x == 0:
            print(str(n) + ' equals ' + str(x) + ' * ' + str(n/x))
            break
    else:
        # loop fell through without finding a factor
        print(str(n) + ' is a prime number')

