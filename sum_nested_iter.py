#!/usr/bin/python3
'''Sum up all values in a list or tuple of nested lists and tuples.
Usage (to run unit tests): python sum_nested_iter.py
None of the methods here can handle (nested) iterables containing strings.
That case could be handled by explicitly testing for type str, or type Number,
or using some logic with len() and is_subscriptable (defined below),
but what would you actually want it to do?  Convert strings to numbers
and sum them, or convert numbers to strings and concatenate them, or what?'''

import collections
from collections import deque

def is_iterable(vit):
    '''Is vit an iterable?  Or just a scalar value?
    Returns True for lists, tuples, and strings, False for numeric types.'''
    return isinstance(vit, collections.Iterable)

def is_list(vit):
    '''Returns True if vit is a list, False if vit is a tuple or string.
    A less idiomatic way, warned against by pylint: return type(vit) is type([])'''
    return isinstance(vit, list)

def is_subscriptable(vit):
    '''Returns True if vit can be subscripted and is non-empty.
    Thus it returns True for a non-empty list, tuple, or string.'''
    try:
        vit[0]
        return True
    except (TypeError, IndexError):
        return False


def sum_nested_iter_rec(vitlist, tot):
    '''Sum all values in a list or typle of nested iterables.
    Relatively efficient, because it only makes one recursive call to itself
    per nested iterable, but its first argument must be a list, not a scalar.'''
    for vit in vitlist:
        if is_iterable(vit):
            tot = sum_nested_iter_rec(vit, tot)
        else:
            tot = tot + vit
    return tot

def sum_nested_rec(vit):
    ''' Sum all values in a scalar argument, list or typle of nested iterables.
    Expect this function to be less efficient than sum_nested_iter_rec, because it
    makes at least one recursive call for every leaf element.'''
    tot = 0
    if is_iterable(vit):
        for val in vit:
            tot = tot + sum_nested_rec(val)
    else:
            tot = tot + vit
    return tot

def sum_nested_list_rec(vitlist, tot):
    '''Sum all values in a list of nested lists.'''
    for vit in vitlist:
        if is_list(vit):
            tot = sum_nested_list_rec(vit, tot)
        else:
            tot = tot + vit
    return tot


def sum_nested_iter_stack(vit):
    '''Sum all values in a list or typle of nested iterables using a stack (depth-first,
    meaning that nested iterables are processed as found, before processing the reest of
    the current iterable).'''
    tot = 0
    stack = [vit]
    while stack:
        vit = stack.pop()
        if is_iterable(vit):
            for item in vit:
                stack.append(item)
        else:
            tot = tot + vit
    return tot


def sum_nested_iter_deque(vit):
    '''Sum all values in a list or typle of nested iterables using a queue (breadth-first,
    meaning that more deeply nested lists or tuples are processed later).'''
    tot = 0
    queue = deque([vit])
    while queue:
        vit = queue.popleft()
        if is_iterable(vit):
            for item in vit:
                queue.append(item)
        else:
            tot = tot + vit
    return tot


def test_sum_nested_iter():
    '''Test sum_nested_iter functions on nested lists and/or tuples'''
    print("Nested lists:")
    lst = [1, [2, 3], [4, [5, 6], 7], [[8, 9]]]
    print(lst)
    tot = sum_nested_iter_rec(lst, 0)
    print("reclist sum:", tot)
    tot = sum_nested_rec(lst)
    print("rec val sum:", tot)
    tot = sum_nested_list_rec(lst, 0)
    print("index sum:  ", tot)
    tot = sum_nested_iter_stack(lst)
    print("stack sum:  ", tot)
    tot = sum_nested_iter_deque(lst)
    print("deque sum:  ", tot)
    print()
    print("Tuple of nested lists and tuples:")
    tpl = (1, [2, 3], (4, (5, 6), 7), [(8, 9)])
    print(tpl)
    tot = sum_nested_iter_rec(tpl, 0)
    print("rec sum:    ", tot)
    try:
        tot = sum_nested_list_rec(tpl, 0)
    except TypeError as ex:
        print("sum_nested_list_rec got a TypeError exception (expected)")
        print("\t because is_list is False for tuples:\n\t ", ex)
    tot = sum_nested_iter_stack(tpl)
    print("stack sum:  ", tot)
    tot = sum_nested_iter_deque(lst)
    print("deque sum:  ", tot)

def test_sum_nested_iter_on_scalar():
    '''Test sum_nested_iter functions on scalar arguments'''
    num = 6
    print("Number:", num)
    try:
        tot = sum_nested_iter_rec(num, 0) 
    except TypeError as ex:
        print("sum_nested_iter_rec got a TypeError exception, because this")
        print("\t recursive function assumes an iterable argument, thus:\n\t ", ex)
    tot = sum_nested_iter_stack(num)
    print("stack sum, number argument and sum: ", num, tot)
    string = "string"

if __name__ == '__main__':
    test_sum_nested_iter()
    test_sum_nested_iter_on_scalar()
