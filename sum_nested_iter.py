#!/usr/bin/python3
'''Sum up all values in a list or tuple of nested lists and tuples.
Usage (to run unit tests): python sum_nested_iter.py
'''

import collections

def is_iterable(vit):
    '''Is vit an iterable?  Or just a scalar value?
    Returns True for lists, tuples, and strings, False for numeric types.
    '''
    return isinstance(vit, collections.Iterable)

def is_indexible(vit):
    '''Not so idiomatic way of testing if vit is indexible.
    Returns True if vit is a list, False if vit is a tuple or string.
    '''
    return type(vit) is type([])


def sum_nested_iter_rec(vitlist, tot):
    '''Sum up all values in a list of nested lists.'''
    for vit in vitlist:
        if is_iterable(vit):
            tot = sum_nested_iter_rec(vit, tot)
        else:
            tot = tot + vit
    return tot

def sum_nested_index_rec(vitlist, tot):
    '''Sum up all values in a list of nested lists.'''
    for vit in vitlist:
        if is_indexible(vit):
            tot = sum_nested_index_rec(vit, tot)
        else:
            tot = tot + vit
    return tot


def test_sum_nested_iter():
    '''Test sum_nested_iter_rec'''
    print("Nested lists:")
    lst = [1, [2, 3], [4, [5, 6], 7], [[8, 9]]]
    print(lst)
    tot = sum_nested_iter_rec(lst, 0)
    print("iter sum:  ", tot)
    tot = sum_nested_index_rec(lst, 0)
    print("index sum: ", tot)
    print()
    print("Tuple of nested lists and tuples:")
    tpl = (1, [2, 3], (4, (5, 6), 7), [(8, 9)])
    print(tpl)
    tot = sum_nested_iter_rec(tpl, 0)
    print("iter sum:  ", tot)
    tot = sum_nested_index_rec(lst, 0)
    print("index sum: ", tot)


if __name__ == '__main__':
    test_sum_nested_iter()
