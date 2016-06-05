# fibonaccis.py -- several ways of generating and printing the Fibonacci series

import math

def fib_recurse(n):
    if n <= 1:
          return n
    else:
        return fib_recurse(n-1) + fib_recurse(n-2)


memo = {0:0, 1:1}

def fib_memoize(n):
    if not n in memo:
        memo[n] = fib_memoize(n-1) + fib_memoize(n-2)
    return memo[n]


def fib_iterate(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
    
# Binet's formula (only good for n < 70)
phi = (1 + 5**0.5) / 2

def fib_binet(n):
    return int(round((phi**n - (1-phi)**n) / 5**0.5))
    
# Binet inverse formula
from math import log

def fib_binet_inverse(f):
    if f < 2:
        return f
    return int(round(log(f * 5**0.5) / log(phi)))

# fibonacci_matrix
def mul(A, B):
    a, b, c = A
    d, e, f = B
    return a*d + b*e, a*e + b*f, b*e + c*f

def pow(A, n):
    if n == 1:     return A
    if n & 1 == 0: return pow(mul(A, A), n//2)
    else:          return mul(A, pow(mul(A, A), (n-1)//2))

def fib_matrix(n):
    if n < 2: return n
    return pow((1,1,0), n-1)[0]


# fibonacci_generator
def fib_generate(n):
    a, b, x = 0, 1, 0
    while x < n:
        yield a
        a, b = b, a + b
        x = x+1


# fibonacci_generator
def fib_generate_recip(n):
    a, b, x = 1, 2, 1
    while x < n:
        yield 1.0/a
        a, b = b, a + b
        x = x+1


def main_fib():
    n = 7
    fib_generated = [y for y in fib_generate(n) ]
    print('memoize  matrix  iterate generate  recurse    binet')
    for x in range(1, n):
        print(repr(fib_memoize(x)).rjust(7), 
              repr(fib_matrix(x)).rjust(7),
              repr(fib_iterate(x)).rjust(8),
              repr(fib_generated[x]).rjust(8),
              repr(fib_recurse(x)).rjust(8),
              repr(fib_binet(x)).rjust(8),
              )
              
    print('sum: {0}'.format(sum(fib_generate(32))));
    print('sum of {1}s: {0}'.format(sum(fib_generate_recip(32)), 'reciprocal'))
    #old style
    print('The values of PI and E are approximately: %7.5f and %7.5f.' % (math.pi, math.e))
    print('The values of GM and Euler\'s are close to {1:.5f} and {0:.5f}.'.format(math.e, (1 + math.sqrt(5))/2))
    print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred', other='George'))

if __name__ == '__main__':
    main_fib()

