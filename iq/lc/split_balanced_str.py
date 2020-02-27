#!/usr/bin/env python3
'''
1221. Split a String in Balanced Strings
Easy

261

188

Add to List

Share
Balanced strings are those who have equal quantity of 'L' and 'R' characters.

Given a balanced string s split it in the maximum amount of balanced strings.

Return the maximum amount of splitted balanced strings.



Example 1:

Input: s = "RLRRLLRLRL"
Output: 4
Explanation: s can be split into "RL", "RRLL", "RL", "RL", each substring contains same number of 'L' and 'R'.
Example 2:

Input: s = "RLLLLRRRLR"
Output: 3
Explanation: s can be split into "RL", "LLLRRR", "LR", each substring contains same number of 'L' and 'R'.
Example 3:

Input: s = "LLLLRRRR"
Output: 1
Explanation: s can be split into "LLLLRRRR".
Example 4:

Input: s = "RLRRRLLRLL"
Output: 2
Explanation: s can be split into "RL", "RRRLLRLL", since each substring contains an equal number of 'L' a
'''
import pdb
from pdb import set_trace
from typing import List
from collections import defaultdict

class Solution:
    def balancedStringSplit(self, s: str) -> int:
        '''
        returns max number of LR-balanced substrings.
        '''
        nL, nR, result = 0, 0, 0
        for c in s:
            if c == 'L':
                nL += 1
            elif c == 'R':
                nR += 1
            if nL == nR:
                nL, nR, result = 0, 0, result + 1
        return result

def test_one(arr, start, expect):
    sol = Solution()
    actual = sol.convert(arr, start)
    print("convert({}, {}) => {} =?= {}".format(arr, start, actual, expect))
    return actual != expect


def main():
    ''' test driver '''
    num_wrong = 0
    in_str = "PAYPALISHIRING"
    num_rows = 4
    expect = "PINALSIGYAHRPI"
    num_wrong += test_one(in_str, num_rows, expect)
    num_rows = 3
    expect = "PAHNAPLSIIGYIR"
    num_wrong += test_one(in_str, num_rows, expect)
    print("num_wrong: %d" % num_wrong)


if __name__ == '__main__':
    main()
