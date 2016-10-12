#!/bin/python3
# https://www.hackerrank.com/challenges/py-if-else?h_r=next-challenge&h_v=zen
'''Without using if-else (elif)'''

N = int(input().strip())
if N % 2 == 0:
    if N < 6 or N > 20:
        print('Not ', end='')
print('Weird')
