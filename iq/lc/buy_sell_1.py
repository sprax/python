#!/usr/bin/env python3
'''
121. Best Time to Buy and Sell Stock
Easy

Say you have an array for which the ith element is the price of a given stock on day i.

If you were only permitted to complete at most one transaction (i.e., buy one and sell one share of the stock), design an algorithm to find the maximum profit.

Note that you cannot sell a stock before you buy one.

Example 1:

Input: [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
             Not 7-1 = 6, as selling price needs to be larger than buying price.
Example 2:

Input: [7,6,4,3,1]
Output: 0
Explanation: In this case, no transaction is done, i.e. max profit = 0.
Accepted
726,234
Submissions
1,470,169
'''

class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        hi, lo, mx, max_diff = -float('inf'), float('inf'), 0, 0
        for pr in prices:
            if lo > pr:
                lo = pr
                hi = pr
                df = hi - lo
                if max_diff < df:
                    max_diff = df
            elif hi < pr:
                hi = pr
                df = hi - lo
                if max_diff < df:
                    max_diff = df
        return max_diff


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
