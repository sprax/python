#!/user//bin/python
# Python 2.7
'''Binomial coefficients, or N choose R'''

import operator as op

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

print("ncr(4, 2) => ", ncr(4,2))
