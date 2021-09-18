#!/usr/bin/env python3
# @file: print_file.py
# @auth: sprax
# @date: 2016-07-27 01:31:55 Wed 27 Jul

# Sprax Lines       2016.07.25      Written with Python 3.5
'''print not necessarily ASCII text file to terminal'''

import sys


def read_file_lines(file):
    ''' read text file line by line '''
    lines = []
    with open(file, 'r') as text:
        for line in text:
            lines.append(line.rstrip())
            my_print(line)
    return lines


def print_lines(lines):
    ''' print items in a list on separate lines '''
    for line in lines:
        my_print(line)


def my_print(line):
    ''' print encoded string '''
    print(line.encode("utf-8"))


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    ''' print with encoding '''
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        def f(obj): return str(obj).encode(
            enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
