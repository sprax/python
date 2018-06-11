#!/usr/bin/env python2
'''Python 2 counter closure'''

from __future__ import print_function

def init_counter(count=0):
    '''(re)set counter that increments whenever called (closure)'''
    _count_dict = { 'count' : count }       # put the enclosed value in a dict
    def _increment_counter():               # to avoid rebinding (for Python 2)
        '''inner incrementer function'''
        _count_dict['count'] += 1
        return _count_dict['count']
    return _increment_counter


def main():
    '''test driver for init_counter'''
    counter = init_counter(6)
    print("counter() =>",     counter())
    print("counter() => %d" % counter())
    print("Re-initializing counter...")
    counter = init_counter(0)
    print("counter() =>",     counter())
    print("counter() => %d" % counter())


if __name__ == '__main__':
    main()
