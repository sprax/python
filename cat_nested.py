#!/usr/bin/env python3
'''
@file: cat_nested.py
@auth: Sprax Lines
@date: 2016-07-11 00:20:14 Mon 11 Jul

Concatenate all strings in a list or tuple of nested lists and tuples
as found, left-to-right.  (Thus nested lists/tuples are handled depth-first.)
Non-string leaf-nodes are converted to strings.

Usage (to run unit tests): python cat_nested.py
'''

import collections
import string


def is_iterable(vit):
    '''Is vit an iterable?  Or just a scalar value?
    Returns True for lists, tuples, and strings, False for numeric types.'''
    return isinstance(vit, collections.Iterable)


def cat_nested_rec(its):
    '''Concatenate all the strings in a nested iterable recursively.'''
    ans = ''
    if isinstance(its, str):
        return its
    elif is_iterable(its):
        for val in its:
            ans += cat_nested_rec(val)
    else:
        return str(its)
    return ans


def cat_nested_dfs(its):
    '''
    Concatenate all the strings in a nested iterable via depth-first traversal.
    '''
    ans = ''
    stack = [its]
    while stack:
        top = stack.pop()
        if isinstance(top, str):
            ans = top + ans
        elif is_iterable(top):
            for val in top:
                stack.append(val)
        else:
            ans = str(top) + ans
    return ans


def test_cat_nested(function, data):
    '''
    Test cat_nested* functions on the given nested lists and/or tuples of
    strings
    '''
    print("Nested lists/tuples of strings:")
    print("data = ", data)
    ans = function(data)
    print("cat_nested_rec(data) =>", ans)
    print()
    return ans


def test_function(function):
    '''
    Test one cat_nested* function on nested lists and/or tuples of strings
    '''
    print("Testing function:", function.__qualname__)
    print()
    lts = ['abc', ['def', 'ghi'], ['jkl', [['mno'], 'pqr'], 'stu'], [['vwx', 'yz']]]
    ans = test_cat_nested(function, lts)
    assert ans == string.ascii_lowercase
    lts = ['abc', ('def', ['ghi']), ['jkl', [['mno'], (('pqr'))], 'stu'], [[('vwx'), 'yz']]]
    ans = test_cat_nested(function, lts)
    assert ans == string.ascii_lowercase
    lts = ['abc', (123, ['ghi']), [456, [['mno'], ((789))], 'stu'], [[('vwx'), 'yz']]]
    ans = test_cat_nested(function, lts)
    assert ans == 'abc123ghi456mno789stuvwxyz'


def unit_test():
    '''cat_nested unit test'''
    print("cat_nested unit_test:")
    print(__doc__)
    test_function(cat_nested_rec)
    test_function(cat_nested_dfs)


if __name__ == '__main__':
    unit_test()
