#!/usr/bin/python3
'''Sum up all values in a list or tuple of nested lists and tuples.
Usage (to run unit tests): python sum_nested_iter.py
'''

import collections

def is_iterable(vit):
    '''Is vit iterable?  Or just a value?'''
    return isinstance(vit, collections.Iterable)

def is_indexible(vit):
    '''More idiomatic than return type(vit) is ([])'''
    return isinstance(vit, [])

def sum_nested_iter_rec(listval, tot):
    '''Sum up all values in a list of nested lists.'''
    for vit in listval:
        if is_iterable(vit):
            tot = sum_nested_iter_rec(vit, tot)
        else:
            tot = tot + vit
    return tot

def test_sum_nested_iter():
    '''Test sum_nested_iter_rec'''
    print("Nested lists:")
    lst = [1, [2, 3], [4, [5, 6], 7], [[8, 9]]]
    print(lst)
    tot = sum_nested_iter_rec(lst, 0)
    print("sum: ", tot)
    print()
    print("Tuple of nested lists and tuples:")
    tpl = (1, [2, 3], [4, (5, 6), 7], [(8, 9)])
    print(tpl)
    tot = sum_nested_iter_rec(tpl, 0)
    print("sum: ", tot)


if __name__ == '__main__':
    test_sum_nested_iter()
