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
class Solution(object):

    def is_cyclic(self, n):
        """
        :type n: int
        :rtype: int
        """
        ss = str(n)
        sums = set()
        while True:
            x = 0
            for c in ss:
                d = int(c)
                x += d*d
            if x == 1:
                return 1
            if x in sums:
                # print("rep %d" % x, end='')
                return x
            sums.add(x)
            ss = str(x)


    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        return 1 == self.is_cyclic(n)

def main():
    ''' test Solution '''
    sol = Solution()
    for x in range(37):
        # print("isHappy({}) => {}".format(x, sol.isHappy(x)))
        sic = sol.is_cyclic(x)
        hap = 1 == sic
        print("is_cyclic({}) => {:3} (so happy == {})".format(x, sic, hap))

if __name__ == '__main__':
    main()
