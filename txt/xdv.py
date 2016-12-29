#!/usr/bin/env python3
'''Debugging output and tools.   Python 3.5+'''

XDV_VERBOSITY = 1

def xdv(verbosity, *args, **kwargs):
    '''Conditional output: eXpress Depending on Verbosity'''
    if verbosity > XDV_VERBOSITY:
        print(*args, **kwargs)

def set_xdv_threshold(level):
    '''Set the modul-global variable XDV_VERBOSITY'''
    global XDV_VERBOSITY
    XDV_VERBOSITY = level

def test_debug():
    '''test xdv'''
    xdv(1, "hi from xdv", 1)
    xdv(1,"greetings from xdv")
    xdv(2, "howdy from xdv")
    xdv(2, "hello from xdv", "\n", "goodbye from xdv", sep='')
    xdv(2, "hey from xdv", "YO", "\n{}".format("goodbye from xdv"), sep='')

if __name__ == '__main__':
    test_debug()
