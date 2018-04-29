
#!/usr/bin/env python3
'''
log-uniform random numbers (numbers uniform in the distribution of their logarithms)
'''
from __future__ import print_function
from datetime import datetime
import pdb;
from pdb import set_trace
import time
import argparse
import math
import os
import sys
import atexit
import termios


old_settings=None

def init_anykey():
   global old_settings
   old_settings = termios.tcgetattr(sys.stdin)
   new_settings = termios.tcgetattr(sys.stdin)
   new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
   new_settings[6][termios.VMIN] = 0  # cc
   new_settings[6][termios.VTIME] = 0 # cc
   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

@atexit.register
def term_anykey():
   # global old_settings
   if old_settings:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def any_keys():
   ch_set = []
   ch = os.read(sys.stdin.fileno(), 1)
   while ch != None and len(ch) > 0:
      ch_set.append( ord(ch[0]) )
      ch = os.read(sys.stdin.fileno(), 1)
   return ch_set;

def term_input():
    init_anykey()
    while True:
       keys = any_keys()
       if keys:
          print("KEYS: ({})".format([(key, chr(key)) for key in keys]))
          if keys[0] == ord('q'):
              print("quitting!")
              break;
       else:
          time.sleep(0.5)



def unit_test(args):
    ''' unit test: hit "q" to quit. '''
    print(unit_test.__doc__)
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
