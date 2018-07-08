# fibonaccis.py -- several ways of generating and printing the Fibonacci series
# TODO: memoize iterative methods

from __future__ import print_function
import argparse
import math
from math import log

def fib_recurse(num):
    if num <= 1:
          return num
    else:
        return fib_recurse(num-1) + fib_recurse(num-2)


memo = {0:0, 1:1}

def fib_memoize(num):
    if not num in memo:
        memo[num] = fib_memoize(num-1) + fib_memoize(num-2)
    return memo[num]


def fib_iterate(num):
    '''iteratively compute function: seq num to fib num'''
    a, b = 0, 1
    for _ in range(num):
        a, b = b, a + b
    return a

# Binet's formula (only good for num < 70)
PHI = (1 + 5**0.5) / 2

def fib_binet(num):
    '''Binet's Fibonacci formula'''
    return int(round((PHI**num - (1-PHI)**num) / 5**0.5))

def fib_binet_inverse(f):
    '''Binet's Fibonacci inverse formula: fibonacci number to sequence number'''
    if f < 2:
        return f
    return int(round(log(f * 5**0.5) / log(PHI)))

def mul(A, B):
    '''matrix multiply, expanded out?
    a  b     d   e        a*d + b*e   a*e + b*f
          X           =
    c  0     f   0        b*d + c*e   b*e + c*f
    '''
    a, b, c = A
    d, e, f = B
    return a*d + b*e, a*e + b*f, b*e + c*f

def power(A, num):
    '''Raise A to the nth power'''
    if num == 1:     return A
    if num & 1 == 0: return power(mul(A, A), num//2)
    else:          return mul(A, power(mul(A, A), (num-1)//2))

def fib_matrix(num):
    '''fibonacci's from matrix to the Nth power'''
    if num < 2:
        return num
    return power((1,1,0), num-1)[0]


def fib_generate(num, start=0):
    '''fibonacci generator'''
    a, b, idx = start, 1, 0
    while idx < num:
        yield a
        a, b = b, a + b
        idx = idx + 1


def fib_generate_recip(num):
    '''fibonacci_reciprocal_generator'''
    a, b, idx = 1, 2, 1
    while idx < num:
        yield 1.0/a
        a, b = b, a + b
        idx = idx+1

################################################################################
DEFAULT_START = 0
DEFAULT_COUNT = 20
DEFAULT_MAX_VAL = 55555

def main_fib():
    '''test fibs'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-all', action='store_true', help='test all methods')
    parser.add_argument('-start', type=int, nargs='?', default=DEFAULT_START,
                        help='first number in test domain (default: %d)' % DEFAULT_START)
    parser.add_argument('count', type=int, nargs='?', default=DEFAULT_COUNT,
                        help='how many numbers to generate (default: %d)' % DEFAULT_COUNT)
    parser.add_argument('maxval', type=int, nargs='?', default=DEFAULT_MAX_VAL,
                        help='stop if generated value > maxval (default: %d)' % DEFAULT_MAX_VAL)
    parser.add_argument('-test', action='store_true', help='test all outputs')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        vinfo = sys.version_info
        v_major = vinfo[0]
        v_minor = vinfo[1]
        ver_str = "Python%d.%d" % (v_major, v_minor)
        print(ver_str, sys.argv[0])
        print("args:", args)

    num = args.count + 1
    fib_generated = [y for y in fib_generate(num)]
    print('idx  memoize   matrix  iterate generate  recurse    binet')
    for idx in range(1, num):
        print(repr(idx).rjust(3),
              repr(fib_memoize(idx)).rjust(8),
              repr(fib_matrix(idx)).rjust(8),
              repr(fib_iterate(idx)).rjust(8),
              repr(fib_generated[idx]).rjust(8),
              repr(fib_recurse(idx)).rjust(8),
              repr(fib_binet(idx)).rjust(8),
             )
    print('sum: {0}'.format(sum(fib_generate(32))))
    print('sum of {1}s: {0}'.format(sum(fib_generate_recip(32)), 'reciprocal'))
    #old style
    print('The values of PI and E are approximately: %7.5f and %7.5f.' % (math.pi, math.e))
    print('The values of GM and Euler\'s are close to {1:.5f} and {0:.5f}.'
          .format(math.e, (1 + math.sqrt(5))/2))
    print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred', other='George'))

if __name__ == '__main__':
    main_fib()
