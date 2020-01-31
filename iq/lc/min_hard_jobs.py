#!/usr/bin/env python3
''' add two numbers represented as linked lists
'''
import pdb
from pdb import set_trace

class Solution:
    def minDifficulty(self, jobDifficulty, days) -> int:

        jobs = len(jobDifficulty)
        # set_trace()
        if jobs < days:
            return -1
        min_hard = self.minDifficultyRec(0, jobDifficulty, days, jobs, -1)
        if min_hard >= 0:
            return min_hard
        return -1

    def minDifficultyRec(self, offset: int, jobDifficulty, days, jobs, best) -> int:
        if days < 1:
            return -1
        min_rest = 0
        num_jobs = len(jobDifficulty) - offset
        max_hard = jobDifficulty[offset]
        for j in range(offset + 1, num_jobs - days + 1):
            hard = jobDifficulty[j]
            if max_hard < hard:
                max_hard = hard
            min_rest = minDifficultyRec(j, jobDifficulty, days - 1, num_jobs - 1, best)
            min_hard = max_hard + min_rest
        return max_hard + min_rest

def test_one(expect, func, args):
    actual = func(*args)
    print("{}({}) => {} =?= {} expected"
        .format(func.__name__, args, actual, expect))
    return actual != expect


def main():
    ''' test driver '''
    sol = Solution()
    num_wrong = 0

    job_difficulty = [1, 2, 3, 4]
    num_wrong += test_one(-1, sol.minDifficulty, (job_difficulty, 5))
    num_wrong += test_one(10, sol.minDifficulty, (job_difficulty, 4))

    print("num_wrong: %d" % num_wrong)

if __name__ == '__main__':
    main()
