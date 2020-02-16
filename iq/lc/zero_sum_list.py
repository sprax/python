'''
Write an algorithm to determine if a number is "happy".

A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.

Example:

Input: 19
Output: true
Explanation:
12 + 92 = 82
82 + 22 = 68
62 + 82 = 100
12 + 02 + 02 = 1
'''
class Solution:
    def sumZero(self, n: int):
        if n % 2:
            return self.sumHelper((n - 1) // 2 + 1, [0])
        return self.sumHelper(n//2 + 1, [])

    def sumHelper(self, h: int, r):
        for x in range(1, h):
            r.append(x)
            r.append(-x)
        return r


def main():
    ''' test Solution '''
    sol = Solution()
    for i, x in enumerate(range(99)):
        r = sol.sumZero(x)
        print("%2d: %s" % (i, r))


if __name__ == '__main__':
    main()
