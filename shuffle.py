#!/usr/bin/env python3
# Sprax Lines       2016.07.25      Written with Python 3.5
'''print not necessarily ASCII text file to terminal'''

import sys

from random import randrange

def sattolo_cycle(items):
    '''efficient shuffle'''
    i = len(items)
    while i > 1:
        i = i - 1
        j = randrange(i)  # 0 <= j <= i-1
        items[j], items[i] = items[i], items[j]
    return

def main():
    '''test driver for shuffles'''
    size = int(sys.argv[1])
    ilist = list(range(size))
    sattolo_cycle(ilist)
    print(ilist)

if __name__ == '__main__':
    main()
