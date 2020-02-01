#!/usr/bin/env python3
''' add two numbers represented as linked lists
'''
import pdb
from pdb import set_trace

class Solution:
    '''
    1 <= job_cost.length <= 300
    0 <= job_cost[i] <= 1000
    1 <= d <= 10
    '''

    def min_cost(self, job_cost, days) -> int:
        ''' non-recursive driver '''
        num_jobs = len(job_cost)
        if num_jobs < days:
            return -1
        return self.min_cost_rec(0, job_cost, days)


    def min_cost_rec(self, offset, job_cost, days) -> int:
        ''' recursive helper '''
        assert(days > 0)
        num_jobs = len(job_cost) - offset
        assert(num_jobs >= days)

        if num_jobs == days:
            # set_trace()
            return sum(job_cost[offset:])

        if days == 1:
            return max(job_cost[offset:])

        max_hard = job_cost[offset]
        end = len(job_cost) - days + 1
        min_hard = 2**32
        for j in range(offset, end):
            hard = job_cost[j]
            if (max_hard < hard):
                max_hard = hard
            # set_trace()
            min_rest = self.min_cost_rec(j + 1, job_cost, days - 1)
            min_both = max_hard + min_rest
            if (min_hard > min_both):
                min_hard = min_both

        return min_hard

def test_one(expect, func, args):
    actual = func(*args)
    print("{}({}) => {} =?= {} expected"
        .format(func.__name__, args, actual, expect))
    return actual != expect


def main():
    ''' test driver '''
    sol = Solution()
    num_wrong = 0

    job_cost = [11]
    num_wrong += test_one(11, sol.min_cost, (job_cost, 1))
    job_cost = [22, 33]
    num_wrong += test_one(55, sol.min_cost, (job_cost, 2))
    job_cost = [22, 33, 44]
    num_wrong += test_one(66, sol.min_cost, (job_cost, 2))

    job_cost = [44, 33, 22]
    num_wrong += test_one(66, sol.min_cost, (job_cost, 2))

    job_cost = [11, 22, 35, 40]
    num_wrong += test_one(51, sol.min_cost, (job_cost, 2))
    num_wrong += test_one(73, sol.min_cost, (job_cost, 3))

    job_cost = [40, 35, 22, 11]
    num_wrong += test_one(51, sol.min_cost, (job_cost, 2))
    num_wrong += test_one(73, sol.min_cost, (job_cost, 3))

    job_cost = [57, 45, 33, 22, 10]
    num_wrong += test_one(57, sol.min_cost, (job_cost, 1))
    num_wrong += test_one(67, sol.min_cost, (job_cost, 2))
    num_wrong += test_one(89, sol.min_cost, (job_cost, 3))
    num_wrong += test_one(122, sol.min_cost, (job_cost, 4))

    job_cost = [1, 2]
    num_wrong += test_one(3, sol.min_cost, (job_cost, 2))

    job_cost = [1, 2, 3, 4]
    num_wrong += test_one(-1, sol.min_cost, (job_cost, 5))
    num_wrong += test_one(10, sol.min_cost, (job_cost, 4))

    print("num_wrong: %d" % num_wrong)

if __name__ == '__main__':
    main()
