

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        # for i_a, v_a in enumerate(nums):
        #     dif = target - v_a
        #     for i_b, v_b in enumerate(nums[i_a + 1:]):
        #         if v_b == dif:
        #             return i_a, i_b + i_a + 1

        # size = len(nums)
        # for j in range(size):
        #     dif = target - nums[j]
        #     for k in range(j+1, size):
        #         if nums[k] == dif:
        #             return j,k

        dct = {}
        for idx, val in enumerate(nums):
            if val in dct:
                return dct[val], idx
            dct[target - val] = idx
            print "dct: ", dct
        return None

    def testIt(self):
        lst = [3,2,4]
        ans = self.twoSum(lst, 6)
        print("{} => {}".format(lst, ans))
        lst = [2,7,11,15]
        ans = self.twoSum(lst, 9)
        print("{} => {}".format(lst, ans))



if __name__ == '__main__':
    sln = Solution()
    sln.testIt()
