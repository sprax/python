#!/usr/bin/env python3
# @file: slice_by_index.py
# @auth: sprax
# @date: 2020-04-03 01:37:23 Fri 03 Apr

'''
https://stackoverflow.com/questions/9106065/python-list-slicing-with-arbitrary-indices
'''

from operator import itemgetter


def slice_by_index(lst, indexes):
    """Slice list by positional indexes.

    Adapted from https://stackoverflow.com/a/9108109/304209.

    Args:
        lst: list to slice.
        indexes: iterable of 0-based indexes of the list positions to return.

    Returns:
        a new list containing elements of lst on positions specified by
        indexes.

    >>> slice_by_index([], [])
    []
    >>> slice_by_index([], [0, 1])
    []
    >>> slice_by_index(['a', 'b', 'c'], [])
    []
    >>> slice_by_index(['a', 'b', 'c'], [0, 2])
    ['a', 'c']
    >>> slice_by_index(['a', 'b', 'c'], [0, 1])
    ['a', 'b']
    >>> slice_by_index(['a', 'b', 'c'], [1])
    ['b']
    """
    if not lst or not indexes:
        return []
    slice_ = itemgetter(*indexes)(lst)
    if len(indexes) == 1:
        return [slice_]
    return list(slice_)

