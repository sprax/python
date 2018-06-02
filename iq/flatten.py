#!/usr/bin/python
'''
Functions and tests for flattening nested lists/tuples into a generator.

Question 1: Would depth-first be the same as in-order?
Question 2: Does the simple flatten_df_rec give pre-order?
'''
from __future__ import print_function

from collections import deque

EASIER_LIST = [0, [3, 4], 1, [5, [7]], 2, [6]]
'''           [ ]
            /  |  \
           0   1   2
         / |   |   |
        3  4   5   6
               |
               7
'''

HARDER_LIST = [[2], 0, [3, [6, [[10, [12, [14, 15], 13], 11]]], [7, 8, 9]], 1, [4, 5]]
'''
              [ ]
            /  |   \
          [ ]  0    1
          /    |   / \
         2     3  4   5
              / \
             6  [ ]
            /  / | \
          [ ] 7  8  9
          / \
         10  11
        / \
      12   13
     /  \
    14  15
'''

def flatten_df_rec(lst):
    '''Flattens nested lists or tuples in-order
    (but fails on strings)'''
    for item in lst:
        try:
            for i in flatten_df_rec(item):
                yield i
        except TypeError:
            yield item


def flatten_bf_itr(lst, trace=False):
    '''
    Flattens nested lists or tuples in "breadth-first" or "level-order"
    '''
    queue = deque([lst])
    while queue:
        lst = queue.popleft()
        try:
            for elt in lst:
                try:
                    first = elt[0]
                    queue.append(elt)
                    if trace:
                        print("elt[0]={}\tQ<{}>)".format(first, queue))
                except (IndexError, TypeError):
                    if trace:
                        print("E={}\tq<{}>)".format(elt, queue))
                    yield elt
        except (IndexError, TypeError):
            if trace:
                print("X({})\tq<{}>)".format(lst, queue))
            yield lst

def alt_sum(flat_iter):
    '''
    alternately adds and subtracts elements in an iterable (as in a simple list
    or tuple), with verbosity.  Adds first element, subtracts second, and so on.
    '''
    asum, sign = 0, 1
    for elem in flat_iter:
        asum += sign * elem
        sign = -sign
    return asum

def test_flatten(flatten_func, nested_list, verbose):
    '''applies a function to flatten a possibly nested list, with verbosity'''
    result = flatten_func(nested_list)
    if verbose:
        listed = list(result)
        print("test_flatten({}, {}) => {}".format(flatten_func.__name__,
                                                  nested_list, listed))
        return listed
    return result

def test_pos_sum(pos_sum_func, flat_iter, verbose):
    ''' applies a function to sum a simple iterable (as in a list or tuple),
        with verbosity '''
    result = pos_sum_func(list(flat_iter))
    if verbose:
        print("test_pos_sum({}, {}) => {}".format(pos_sum_func.__name__,
                                                  flat_iter, result))
    return result

def test_alt_sum(alt_sum_func, flat_iter, verbose):
    ''' applies a function to alternately add and subtract elements in an iterable
    (as in a simple list or tuple), with verbosity '''
    result = alt_sum_func(list(flat_iter))
    if verbose:
        print("test_alt_sum({}, {}) => {}".format(test_alt_sum.__name__,
                                                  flat_iter, result))
    return result







def test_flatten_pos_alt_sums(flatten_func, nested_list, verbose):
    ''' Tests flattening and summing functions '''
    flat_iter = test_flatten(flatten_func, nested_list, verbose)
    pos_value = test_pos_sum(pos_sum, flat_iter, verbose)
    alt_value = test_alt_sum(alt_sum, flat_iter, verbose)
    if verbose:
        print("pos sum: %d,  alt sum: %d\n" % (pos_value, alt_value))
    return flat_iter, pos_value, alt_value

def test_flattens_and_sums(nested_list, verbose):
    ''' Tests flattening and summing functions '''
    df_flat, df_pos, df_alt = test_flatten_pos_alt_sums(flatten_df_rec, nested_list, verbose)
    bf_flat, bf_pos, bf_alt = test_flatten_pos_alt_sums(flatten_bf_itr, nested_list, verbose)
    intersection = [pair[0] for pair in zip(bf_flat, df_flat) if pair[0] == pair[1]]
    if verbose:
        print("intersection of breadth-first and depth-first flattened lists:", intersection)
    return intersection


def main():
    '''tests flatten and sum functions as applied to lists'''
    verbose = True
    flat, pos, alt = test_flattens_and_sums(EASIER_LIST, verbose)
    flat, pos, alt = test_flattens_and_sums(HARDER_LIST, verbose)


if __name__ == '__main__':
    main()
