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
    def min_cost_to_move_chips(self, chip_counts: List[int]) -> int:
        '''
        Idea: no chip costs more than 1, because once it is on even/odd index, moving it by 2 is free.
        To put all the chips at one odd index, the cost is the number of chips that start even.
        To put all the chips at one even index, the cost is the number of chips that start odd.
        So the min cost is whichever is less: even or odd chips.
        '''
        is_even = True
        num_evn, num_odd = 0, 0
        for count in chip_counts:
            if is_even:
                num_evn += count
            else:
                num_odd += count
            is_even = not is_even
        return min(num_evn, num_odd)


    def minCostToMoveChips(self, chips: List[int]) -> int:
        '''
        chips gives the index of each chip.
        So we need to count even and odd indexed chips a different way.
        '''
        num_evn, num_odd = 0, 0
        for index in chips:
            if index % 2:
                num_odd += 1
            else:
                num_evn += 1
        return min(num_evn, num_odd)


def test_one(arr, start, expect):
    sol = Solution()
    actual = sol.canReach(arr, start)
    print("arr({}) & start {} => {} =?= {}".format(arr, start, actual, expect))
    return actual != expect

def main():
    ''' test driver '''
    num_wrong = 0
    arr = [4,2,3,0,3,1,2]
    beg = 5
    num_wrong += test_one(arr, beg, True)
    arr = [3,0,2,1,2]
    beg = 2
    num_wrong += test_one(arr, beg, False)
    print("num_wrong: %d" % num_wrong)


if __name__ == '__main__':
    main()
