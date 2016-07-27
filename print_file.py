#!/usr/bin/env python3
# Sprax Lines       2016.07.25      Written with Python 3.5
'''Class and script to solve simple substitution cipher from corpus and encoded text'''

import sys


def read_file_lines(file):
    lines = []
    with open(file, 'r') as text:
        for line in text:
            lines.append(line.rstrip())
            my_print(line)
    return lines

def print_lines(lines):
    for line in lines:
        my_print(line)



def my_print(line):
    print(line.encode("utf-8"))


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

