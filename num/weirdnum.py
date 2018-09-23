#!/user/local/bin/python3
# https://www.hackerrank.com/challenges/py-if-else?h_r=next-challenge&h_v=zen
'''Without using if-else (elif)'''
from __future__ import print_function
import sys

def main():
    '''main'''
    vinfo = sys.version_info
    v_major = vinfo[0]
    v_minor = vinfo[1]
    ver_str = "Python%d.%d" % (v_major, v_minor)
    print(ver_str, sys.argv[0])
    if v_major < 3:
        print("input function needs Python 3!   exit(1)")
        exit(1)

    num = int(input().strip())
    if num % 2 == 0:
        if num < 6 or num > 20:
            print('Not ', end='')
    print('Weird')

main()
