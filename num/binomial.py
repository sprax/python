#!/user//bin/python
# Python 2.7
'''Binomial coefficients, or N choose R, for Python 2'''

import operator as op

def ncr(num, rem):
    ''' binomial coefficient, or, n take r '''
    if num < rem:
        return 0
    rem = min(rem, num-rem)
    if rem == 0:
        return 1
    numer = reduce(op.mul, xrange(num, num-rem, -1))
    denom = reduce(op.mul, xrange(1, rem+1))
    return numer//denom

print("ncr(3, 2) => ", ncr(4, 2))
print("ncr(4, 2) => ", ncr(4, 2))
print("ncr(5, 3) => ", ncr(5, 3))
print("ncr(6, 5) => ", ncr(6, 5))
print("ncr(5, 6) => ", ncr(5, 6))
