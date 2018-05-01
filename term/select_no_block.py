
#!/usr/bin/env python
'''
Use select in a loop to get input without blocking or busy-waiting.  Pythhon 2 or 3.
'''
from __future__ import print_function
# import pdb
# from pdb import set_trace
import argparse
import sys
import select
import tty
import termios
import time





def got_selected():
    ''' select can check for input of one or more characters '''
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def get_input_loop():
    ''' run a loop to get input without blocking or busy-waiting '''
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        i = 0
        while 1:
            print(i)
            i += 1
            if got_selected():
                char = sys.stdin.read(1)
                if char == '\x1b':         # x1b is ESC
                    break
                return char
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def term_input():
    ''' main loop function; calls any_keys() '''
    seconds = 1
    while True:
        keys = get_input_loop()
        if keys:
            print("KEY: ({})".format(keys))
            if keys == 'q':
                print("quitting!")
                break
            else:
                time.sleep(0.1)
        seconds += 1
        print("Sleeping for %d seconds..." % seconds)
        time.sleep(seconds)

def unit_test(args):
    ''' unit test: hit "q" to quit. '''
    print(unit_test.__doc__, "\nWith args:", args)
    term_input()
    print()


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
