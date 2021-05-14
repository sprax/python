#!/usr/bin/env python3
'''reverse a string'''
@file: shift.py
@auth: Sprax Lines
@date: 2016-06-07 16:33:12 Tue 07 Jun

import sys


def shift_string(string):
    '''shift ==> tisfh'''
    # return string[::-2] + string[1:-1:-2]
    return string[::-2] + string[0:-1][::-2]


if __name__ == '__main__':
    STRING = sys.argv[1] if len(sys.argv) > 1 else 'Jesus Mary and Joseph'
    print(STRING, '==>', shift_string(STRING))
