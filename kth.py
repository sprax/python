#!/usr/bin/env python3
'''doubly sorted 2D array, right?'''

import sys


def add_if_not_exists(possibles, newt):
    if newt not in possibles:
        possibles.append(newt)


def find_next(arr, possibles):
    ''' find next biggest '''
    min = 9999999
    selx = 0
    sely = 0
    for (x, y) in possibles:
        if(arr[x][y] < min):
            min = arr[x][y]
            selx = x
            sely = y
            possibles.remove((selx, sely))
        if selx+1 < len(arr):
            add_if_not_exists(possibles, (selx+1, sely))
        if sely+1 < len(arr):
            add_if_not_exists(possibles, (selx, sely+1))
    return (selx, sely)


def find_kth(arr, k):
    ''' return kth biggest '''
    possibles = [(0, 0)]
    for idx in range(0, k):
        print("idx:", idx)
        (x, y) = find_next(arr, possibles)
        print("nxt:", x, y)
        print("val:", arr[x][y])
    return arr[x][y]


if __name__ == '__main__':
    arr = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]]
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    find_kth(arr, k)
