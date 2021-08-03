#!/usr/bin/env python3
# @file: partial.py
# @auth: Sprax Lines
# @date: 2017-07-02 01:07:48 Sun 02 Jul

'''bind a function with some args'''


def partial(func, *args, **kwargs):
    '''
    return partially bound function func with args and kwargs already defined
    '''
    def wrapped(*args2, **kwargs2):
        return func(*args, *args2, **kwargs, **kwargs2)
    return wrapped
