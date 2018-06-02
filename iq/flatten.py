#!/usr/bin/python
'''flattens nested lists/tuples into a generator'''
from __future__ import print_function

from collections import deque

# NESTED_LIST = [0, 1, [3, [6, [[8, [11, 12], 10]], 7, [9]]], 2, [4, 5]]
NESTED_LIST = [9, [11, 12], 10]
'''
                  [ ]
                /  |   \
               0   1    2
                   |   / \
                   3  4   5
                  / \
                 6   7
                /     \
               []      9
              /  \
             8    10
            / \
          11   12
'''

def flatten(lst):
    '''Flattens nested lists or tuples in-order
    (but fails on strings)'''
    for item in lst:
        try:
            for i in flatten(item):
                yield i
        except TypeError:
            yield item


def flatten_bf(lst):
    '''
    Flattens nested lists or tuples in
    "breadth-first" or "level-order"
    '''
    queue = deque(lst)
    while queue:
        lst = queue.popleft()
        try:
            first = lst[0]
            queue.append(first)
            last = lst[1:]
            if last:
                queue.append(last)
            print("f({})  l[{}]  q<{}>".format(first, last, queue))
        except (IndexError, TypeError):
            # if lst:
            print("E({}    q<{}>)".format(lst, queue))
            yield lst


'''
Claim 1: depth-first would be the same as in-order?
Try this for in order:
1, 2, 4, 5, 3, 6, 7, 8, 9

Claim 2: The simple flatten above gives pre-order
'''

def main():
    '''test flatten'''
    nlist = NESTED_LIST
    flist = list(flatten(nlist))
    total = sum(flist)
    print("  gen flatten(", nlist, ") => ", flist)
    print("  sum(flatten(", nlist, ") => ", total)
    blist = list(flatten_bf(nlist))
    print(" q flatten_bf(", nlist, ") => ", blist)

if __name__ == '__main__':
    main()
