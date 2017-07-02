#!/usr/bin/env python3
'''bind a function with some args'''

def partial(func, *args, **kwargs):
    '''return partially bound function func with args and kwargs already defined'''
    def wrapped(*args2, **kwargs2):
        return func(*args, *args2, **kwargs, **kwargs2)
    return wrapped
