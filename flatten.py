#!/usr/bin/python
'''flattens nested lists/tuples into a generator'''

def flatten(lst):
    '''Flattens nested lists or tuples (but fails on strings)'''
    for item in lst:
        try:
            for i in flatten(item):
                yield i
        except TypeError:
            yield item


NLIST = [1, 3, [2, [4, [9]]], 5, 6, [7, 8]]
TOTAL = sum(flatten(NLIST))
print(" sum(flatten(", NLIST, ") => ", TOTAL)
