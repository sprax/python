#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
from collections import deque
import struct
# import pdb
# from pdb import set_trace



# python 2.7:
def unpack_scoop_file(path="test_scoop.bin"):
    with open(path, mode='rb') as file: # b for binary
        bd = file.read()
        struct.unpack(">QI4d28dQ8d", bd[:340])         # > for big-endian

# (17397326213550882569L, 1234, 1.11, 2.22, 3.33, 4.44, 1.1, 1.2, 1.3, 1.8, 1.1, 2.2, 3.3, 2.1, 2.2, 2.3, 2.8, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.8, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.8, 4.1, 4.2, 4.3,
# 5124235558349908854, 7.567946863e-315, 0.11, 0.22, 0.33, 0.999, 0.888, 0.777, 0.666)```


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    pass


def main():
    '''driver for unit_test'''
    const_a = "abcdefgh"
    const_b = "abc_efgh"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', type=str, nargs='?', const=const_a,
                        help="str_a to test against str_b (const: %s)" % const_a)
    parser.add_argument('-b', type=str, nargs='?', const=const_b,
                        help="str_b to test against str_a (const: %s)" % const_b)
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    unit_test(args)


if __name__ == '__main__':
    main()
