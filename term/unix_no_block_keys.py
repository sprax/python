
#!/usr/bin/env python3
'''
non-blocking terminal input, linux.
'''
from __future__ import print_function
# import pdb
# from pdb import set_trace
import time
import argparse
import os
import sys
import atexit
import termios

# global
OLD_SETTINGS = None

def init_anykey():
    ''' init '''
    global OLD_SETTINGS
    OLD_SETTINGS = termios.tcgetattr(sys.stdin)
    new_settings = termios.tcgetattr(sys.stdin)
    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
    new_settings[6][termios.VMIN] = 0  # cc
    new_settings[6][termios.VTIME] = 0 # cc
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

@atexit.register
def term_anykey():
    ''' reset terminal settings at exit '''
    # global OLD_SETTINGS
    if OLD_SETTINGS:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, OLD_SETTINGS)

def any_keys():
    ''' get key(s) for one loop iteration '''
    chr_lst = []
    char = os.read(sys.stdin.fileno(), 1)
    while char:
        chr_lst.append(ord(char[0]))
        char = os.read(sys.stdin.fileno(), 1)
        return chr_lst

def term_input():
    ''' main loop function; calls any_keys() '''
    init_anykey()
    flt_seconds = 1.0
    while True:
        keys = any_keys()
        if keys:
            print("KEYS: ({})".format([(key, chr(key)) for key in keys]))
            if keys[0] == ord('q'):
                print("quitting!")
                break
            else:
                time.sleep(0.1)
        flt_seconds *= 1.1
        int_seconds = int(flt_seconds)
        print("Sleeping for %d (int(%f)) seconds..." % (int_seconds, flt_seconds))
        time.sleep(int_seconds)

def unit_test(args):
    '''
    unit test with args:'''
    print(unit_test.__doc__, args, "\n\thit 'q' to quit...")
    term_input()
    print()

###############################################################################
def main():
    '''driver for unit_test'''
    default_count = 10000
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('count', type=int, nargs='?', default=default_count,
                        help='Sample count (default: %d)' % default_count)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (const=2, default: 1)')
    args = parser.parse_args()
    unit_test(args)

if __name__ == '__main__':
    main()
