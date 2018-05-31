#!/usr/bin/python
'''flattens nested lists/tuples into a generator'''
from __future__ import print_function

from collections import deque

def flatten(lst):
    '''Flattens nested lists or tuples in-order (but fails on strings)'''
    for item in lst:
        try:
            for i in flatten(item):
                yield i
        except TypeError:
            yield item


def flatten_bf(lst):
    '''Flattens nested lists or tuples "breadth-first" '''
    queue = deque(lst)
    while queue:
        lst = queue.popleft()
        try:
            first = lst[0]
            queue.append(first)
            last = lst[1:]
            if last:
                queue.append(last)
        except (IndexError, TypeError):
            # if lst:
            yield lst


'''
Claim 1: depth-first would be the same as in-order?
Try this for in order:
1, 2, 4, 5, 3, 6, 7, 8, 9

Claim 2: The simple flatten above gives pre-order
'''

def main():
    '''test flatten'''
    nlist = [1, 2, [3, [[4, 5], 6]], 7, [8, 9]]
    flist = list(flatten(nlist))
    total = sum(flist)
    print("  gen flatten(", nlist, ") => ", flist)
    print("  sum(flatten(", nlist, ") => ", total)
    blist = list(flatten_bf(nlist))
    print(" q flatten_bf(", nlist, ") => ", blist)

if __name__ == '__main__':
    main()
