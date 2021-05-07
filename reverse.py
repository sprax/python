#!/usr/bin/env python3
'''reverse a string'''
@file: reverse.py
@auth: Sprax Lines
@date: 2016-06-07 16:33:12 Tue 07 Jun

import sys


def reverse_string_slice(string):
    '''reverse'''
    return string[::-1]


def reverse_string_join_it(string):
    '''reverse'''
    return "".join(reversed(string))


def main():
    '''test reverse_string'''
    string = sys.argv[1] if len(sys.argv) > 1 else 'Jesus Mary and Joseph'
    print(string, '==>', reverse_string_slice(string))
    print(string, '==>', reverse_string_join_it(string))


if __name__ == '__main__':
    main()
