#!/usr/env python'''
'''
Input:
"MCMXCIV"
Output:
2194
Expected:
1994
'''
import argparse
import sys

def romanToIntA(self, s):
    """
    :type s: str
    :rtype: int
    bad first try
    """
    n = 0
    for c in s[::-1]:
        if c == 'I':
            if n < 3:
                n += 1
            else:
                n -= 1
        elif c == 'V':
            n += 5
        elif c == 'X':
            if n/10 == 5 or n/10 == 10:
                n -= 10
            else:
                n += 10
        elif c == 'L':
            n += 50
        elif c == 'C':
            if n/100 == 5 or n/10 == 10:
                n -= 100
            else:
                n += 100
        elif c == 'D':
            n += 500
        elif c == 'M':
            n += 1000
    return n


class Solution(object):

    def __init__(self):
        self.rondo = {
            'I' : 1,
            'V' : 5,
            'X' : 10,
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000,
        }

    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        z = len(s) - 1
        if z < 0:
            return 0
        n = self.rondo.get(s[z])
        while z > 0:
            z -= 1
            d = self.rondo.get(s[z])
            if d == 1 and s[z+1] != 'I':
                n -= 1
            elif d == 10 and s[z+1] == 'C' or s[z+1] == 'L':
                n -= 10
            elif d == 100 and s[z+1] == 'D' or s[z+1] == 'M':
                n -= 100
            else:
                n += d
            print("s.{} => d.{} => n.{}".format(s[z], d, n))
        return n

def main():
    '''drive tests of Roman number converters'''
    parser = argparse.ArgumentParser(description="convert Roman number strings to ints")
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    vinfo = sys.version_info
    v_major = vinfo[0]
    v_minor = vinfo[1]
    ver_str = "Python %d.%d" % (v_major, v_minor)
    print(ver_str)

    test_pairs = {
        "MCMXCIV": 1994,
    }

    soln = Solution()
    for roman in test_pairs:
        expect = test_pairs[roman]
        actual = soln.romanToInt(roman)
        print("Roman {} => {} =?= {}".format(roman, actual, expect))


if __name__ == '__main__':
    main()
