#!/usr/bin/env python3
'''
There are some chips, and the i-th chip is at position chips[i].

You can perform any of the two following types of moves any number of times (possibly zero) on any chip:

Move the i-th chip by 2 units to the left or to the right with a cost of 0.
Move the i-th chip by 1 unit to the left or to the right with a cost of 1.
There can be two or more chips at the same position initially.

Return the minimum cost needed to move all the chips to the same position (any position).



Example 1:

Input: chips = [1,2,3]
Output: 1
Explanation: Second chip will be moved to positon 3 with cost 1. First chip will be moved to position 3 with cost 0. Total cost is 1.
Example 2:

Input: chips = [2,2,2,3,3]
Output: 2
Explanation: Both fourth and fifth chip will be moved to position two with cost 1. Total minimum cost will be 2.
'''
import pdb
from pdb import set_trace
from typing import List
from collections import defaultdict

class Solution:
    '''
    Idea: no chip costs more than 1, because once it is on even/odd index, moving it by 2 is free.
    To put all the chips at one odd index, the cost is the number of chips that start even.
    To put all the chips at one even index, the cost is the number of chips that start odd.
    So the min cost is whichever is less: even or odd chips.
    skips:
    row 0 => (N - 1)*2 because N - 1 to get to bottom and N - 1 again to get back to top.
    row 1 => N - 2 to go down + N - 2 to go back up, but then 1 + 1 for the next, so 2*r,
             and repeat; so (N - 1 - r)*2 down-up, and 2*r up-down, which alternaates as:
             skip = (N - 1)*2 - r*2, skip = r*2 = (N - 1)*2 - (N - 1)*2 - r*2 = (N - 1)*2 - skip,
    row 2 => N - 3 down + N - 3 up = (N - r)*2 down-up, then again r*2 up-down
    row N => (N - 1)*2
    '''
    def convert(self, s: str, numRows: int) -> str:
        strlen = len(s)
        halfsz = numRows // 2
        result = ['_'] * strlen
        outidx = 0
        downup = (numRows - 1)*2
        for row in range(numRows):
            srcidx = row

            if row > halfsz:
                offset = numRows - 1 - row
                stride = offset * 2
            else:
                offset = row
                stride = downup - offset*2

            if offset:
                while srcidx < strlen:
                    result[outidx] = s[srcidx]
                    outidx += 1
                    srcidx += stride
                    stride = downup - stride    # the stride alternates: downup, downup, ...
            else:
                while srcidx < strlen:
                    result[outidx] = s[srcidx]
                    outidx += 1
                    srcidx += downup    # stride == downup
        return ''.join(result)


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
