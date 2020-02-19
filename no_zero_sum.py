class Solution(object):
    def getNoZeroIntegers(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        rp = n // 2
        rq = n - rp
        dp, dq = rp, rq
        tt = 1
        while n > 0:
            if dq % 10 == 0 or dp % 10 == 0:
                rp -= tt
                rq += tt
            dq = dq // 10
            dp = dp // 10
            tt *= 10
            n = n // 10
