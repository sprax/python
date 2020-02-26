
import pdb
from pdb import set_trace


class Solution(object):
    def decompressRLElist(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        result = []
        j, size = 0, len(nums)
        while j < size:
            result +=  nums[j] * [nums[j+1]]
            j += 2
        return result

    def decompress_rle_list(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        g = [nums[j]*[nums[j+1]] for j in [k*2 for k in range(len(nums)//2)]]
        return [item for ss in g for item in ss]

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
