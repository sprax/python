#!/usr/bin/env python3
'''
Given an array of non-negative integers arr, you are initially positioned
at start index of the array.
When you are at index i, you can jump to i + arr[i] or i - arr[i],
check if you can reach to any index with value 0.

Notice that you can not jump outside of the array at any time.

Example 1:

Input: arr = [4,2,3,0,3,1,2], start = 5
Output: true
Explanation:
All possible ways to reach at index 3 with value 0 are:
index 5 -> index 4 -> index 1 -> index 3
index 5 -> index 6 -> index 4 -> index 1 -> index 3
Example 2:

Input: arr = [4,2,3,0,3,1,2], start = 0
Output: true
Explanation:
One possible way to reach at index 3 with value 0 is:
index 0 -> index 4 -> index 1 -> index 3
Example 3:

Input: arr = [3,0,2,1,2], start = 2
Output: false
Explanation: There is no way to reach at index 1 with value 0.


Constraints:
1 <= arr.length <= 5 * 10^4
0 <= arr[i] < arr.length
0 <= start < arr.length
Accepted    11,598      Submissions 18,960
'''
import pdb
from pdb import set_trace
from typing import List
from collections import defaultdict

class Solution:

    def __init__(self):
        self.seen = defaultdict(int)

    def canReach(self, arr: List[int], start: int) -> bool:
        return self.can_reach_96_100(arr, start)

    def can_reach_96_100(self, arr: List[int], start: int) -> bool:
        '''
        Runtime: 232 ms, faster than 95.46% of Python3 online submissions for Jump Game III.
        Memory Usage: 19.3 MB, less than 100.00% of Python3 online submissions for Jump Game III.
        '''
        return self.can_reach_rec(arr, start)

    def can_reach_rec(self, arr: List[int], idx: int) -> bool:
        val = arr[idx]
        if val == 0:
            return True
        self.seen[idx] = val
        nxt = idx + val
        if nxt < len(arr) and not self.seen[nxt]:
            self.seen[nxt] = val
            if self.can_reach_rec(arr, nxt):
                return True
        nxt = idx - val
        if 0 <= nxt and not self.seen[nxt]:
            self.seen[nxt] = val
            if self.can_reach_rec(arr, nxt):
                return True
        return False

    def can_reach_33_100(self, arr: List[int], start: int) -> bool:
        end = len(arr)
        visited = set()
        queue = [start]
        while queue:
            idx = queue.pop()
            val = arr[idx]
            if val == 0:
                return True
            visited.add(idx)
            nxt = idx + val
            if nxt < end and nxt not in visited:
                queue.append(nxt)
            nxt = idx - val
            if nxt >= 0 and nxt not in visited:
                queue.append(nxt)
        return False

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
