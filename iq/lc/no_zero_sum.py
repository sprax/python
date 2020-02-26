
import pdb
from pdb import set_trace

class Solution(object):
    def get_no_zero_integers(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        rp = n // 2
        rq = n - rp
        dp, dq = rp, rq
        ten_p = 1
        while dp > 0:
            if dp % 10 == 0:
                print("dp %5d:  rp -= ten_p: %5d -= %5d,  rq += ten_p: %5d += %5d:\t [%d, %d]"
                      % (dp, rp, ten_p, rq, ten_p, rp, rq))
                rp -= ten_p
                rq += ten_p
            if dq % 10 == 0:
                print("dq %5d:  rp -= ten_p: %5d -= %5d,  rq += ten_p: %5d += %5d:\t [%d, %d]"
                      % (dq, rp, ten_p, rq, ten_p, rp, rq))
                rp -= ten_p
                rq += ten_p
            dq = dq // 10
            dp = dp // 10
            ten_p *= 10
        return [rp, rq]

    def getNoZeroIntegers(self, n):
        """
        return list [p, q] where p + q == n and no 0 appears in the decimal forms of p or q.
        :type n: int
        :rtype: List[int]
        """
        res_l = n // 2
        res_r = n - res_l
        qot_l = res_l
        qot_r = res_r
        ten_p = 1
        set_trace()
        while qot_l > 0:
            qot_l, rem_l = divmod(qot_l, 10)
            qot_r, rem_r = divmod(qot_r, 10)
            if rem_l == 0:
                if rem_r == 1:
                    res_l -= ten_p
                else:
                    res_l += ten_p
            elif rem_r == 0:
                if rem_l == 1:
                    res_l += ten_p
                else:
                    res_l -= ten_p
            res_r = n - res_l
            ten_p *= 10
            qot_l = res_l // ten_p
            qot_r = res_r // ten_p

        return [res_l, res_r]


def main():
    ''' test Solution '''
    sol = Solution()
    beg = 2218
    end = beg + 2
    for i, x in enumerate(range(beg, end)):
        r = sol.getNoZeroIntegers(x)
        print("%5d: %5d => %s" % (i, x, r))


if __name__ == '__main__':
    main()
