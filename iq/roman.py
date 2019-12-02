#!/usr/env python'''
'''
Input:
"MCMXCIV"
Output:
2194
Expected:
1994
'''

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

    self.rondo = {
        'I' : 1,
        'V' : 5,
        'X' : 10,
        'L' : 50,
        'C' : 100,
        'D' : 500,
        'M' : 1000
    }

    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        z = len(s) - 1
        if z < 0:
            return 0
        n = rondo.get(s[z])
        return n
