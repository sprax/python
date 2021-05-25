#!/usr/bin/env python3
''' benchmark '''
@file: slow_regex.py
@auth: Sprax Lines
@date: 2017-07-31 12:09:44 Mon 31 Jul

from __future__ import print_function
import timeit
import re

REX = re.compile('(foo|bar|hello)')


def one(mystring):
    ''' tester '''
    any(s in mystring for s in ('foo', 'bar', 'hello'))


def two(mystring):
    ''' tester '''
    REX.search(mystring)


def main():
    ''' test function '''
    mystring = "hello"*1000
    print([timeit.timeit(k(mystring), number=10000) for k in (one, two)])
    mystring = "goodbye"*1000
    print([timeit.timeit(k(mystring), number=10000) for k in (one, two)])
    print(mystring)


if __name__ == '__main__':
    main()
