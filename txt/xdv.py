#!/usr/bin/env python3
'''
XDV  == eXchange (I/O) Depending on Verbosity.
Basic debugging output for Python 3.5+
'''

XDV_VERBOSITY = None
XDV_DEFAULT = 0

def printv(level, verbose, *args, **kwargs):
    '''
    prints args with kwargs if level < verbose.
    Lightweight conditional output.
    '''
    if level < verbose:
        print(*args, **kwargs)


def set_xdv_verbosity(verbosity):
    '''Set the module-global variable XDV_VERBOSITY'''
    global XDV_VERBOSITY
    if XDV_VERBOSITY != verbosity:
        print("Setting XDV_VERBOSITY = %d" % verbosity)
        XDV_VERBOSITY = verbosity

def get_xdv_verbosity():
    '''get the current verbosity'''
    if XDV_VERBOSITY is None:
        set_xdv_verbosity()
    return XDV_VERBOSITY

def xdv(level, *args, **kwargs):
    '''Conditional output: eXpress Depending on Verbosity'''
    try:
        if level <= XDV_VERBOSITY:
            print(*args, **kwargs)
    except TypeError:
        print("WARNING: XDV_VERBOSITY was None (in {}); setting it to {}"
              .format(__name__, XDV_DEFAULT))
        set_xdv_verbosity(XDV_DEFAULT)
        xdv(level, *args, **kwargs)

def xdvr(level, *args, **kwargs):
    '''Conditional output: eXpress Depending on Verbosity'''
    try:
        if level <= xdvr_verbosity():
            print(*args, **kwargs)
    except TypeError:
        print("WARNING: XDV_VERBOSITY was None (in {}); setting it to {}"
              .format(__name__, XDV_DEFAULT))
        def xdvr_verbosity():
            return xdvr
        xdv(level, *args, **kwargs)

def try_xdv():
    '''try xdv'''
    xdv(0, "0 -- hi from xdv", 0)
    xdv(1, "1 -- greetings from xdv")
    xdv(2, "2 -- howdy from xdv")
    xdv(3, "3 -- hello from xdv", "\n",
        "     -- bonus line, still in xdv(3 ...", sep='')
    xdv(4, "4 -- hey from xdv", " YO, 4 is as high as I go!",
        "\n{}".format("goodbye from xdv"), sep='')

def test_xdv():
    '''test xdv module methods'''
    try_xdv()
    set_xdv_verbosity(2)
    try_xdv()
    set_xdv_verbosity(4)
    try_xdv()

if __name__ == '__main__':
    test_xdv()
