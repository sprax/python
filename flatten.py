#!/usr/bin/python
'''flattens nested lists/tuples into a generator'''
from __future__ import print_function

def flatten(lst):
    '''Flattens nested lists or tuples (but fails on strings)'''
    for item in lst:
        try:
            for i in flatten(item):
                yield i
        except TypeError:
            yield item


NLIST = [1, 2, [3, [[4, 5], 6]]
    , 7, [8, 9]]
FLIST = list(flatten(NLIST))
TOTAL = sum(FLIST)
print(" flatten(", NLIST, ") => ", FLIST)
print(" sum(flatten(", NLIST, ") => ", TOTAL)
