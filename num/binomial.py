#!/user//bin/python
# Python 2.7
'''Binomial coefficients, or N choose R, for Python 2'''
from __future__ import print_function
import operator as op

def ncr(num, rem):
    ''' binomial coefficient, or, n take r '''
    if num < rem or num < 1:
        return 0
    rem = min(rem, num - rem)
    if rem == 0:
        return 1
    numer = reduce(op.mul, xrange(num, num-rem, -1))
    denom = reduce(op.mul, xrange(1, rem+1))
    return numer//denom

def show_ncr(num, rem):
    '''call ncr & print result'''
    print("ncr(%d, %d) => %d" % (num, rem, ncr(num, rem)))


def test_ncr():
    '''try ncr'''
    show_ncr(0, 0)
    show_ncr(-1, -1)
    show_ncr(1, 1)
    show_ncr(1, 2)
    show_ncr(2, 2)
    show_ncr(3, 1)
    show_ncr(3, 2)
    show_ncr(3, 3)
    show_ncr(4, 3)
    show_ncr(5, 3)
    show_ncr(6, 3)
    show_ncr(5, 6)

if __name__ == '__main__':
    test_ncr()
