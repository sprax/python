#!/usr/bin/env python3
'''
XDV  == eXchange (I/O) Depending on Verbosity.
Basic debugging out for Python 3.5+
'''

XDV_VERBOSITY = None
XDV_DEFAULT = 0

def set_xdv_verbosity(verbosity):
    '''Set the modul-global variable XDV_VERBOSITY'''
    global XDV_VERBOSITY
    if XDV_VERBOSITY != verbosity:
        print("Setting XDV_VERBOSITY = {}".format(verbosity))
        XDV_VERBOSITY = verbosity

def xdv(level, *args, **kwargs):
    '''Conditional output: eXpress Depending on Verbosity'''
    if XDV_VERBOSITY is None:
        print("WARNING: XDV_VERBOSITY was None (in {}); setting it to {}".format(__name__, XDV_DEFAULT))
        set_xdv_verbosity(0)
    if level <= XDV_VERBOSITY:
        print(*args, **kwargs)

def try_xdv():
    '''test xdv'''
    xdv(0, "0 -- hi from xdv", 1)
    xdv(1, "1 -- greetings from xdv")
    xdv(2, "2 -- howdy from xdv")
    xdv(3, "3 -- hello from xdv", "\n", "goodbye from xdv", sep='')
    xdv(4, "4 -- hey from xdv", "YO", "\n{}".format("goodbye from xdv"), sep='')

def test_xdv():
    try_xdv()
    set_xdv_verbosity(2)
    try_xdv()
    set_xdv_verbosity(4)
    try_xdv()

if __name__ == '__main__':
    test_xdv()
