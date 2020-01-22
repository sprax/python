
class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        from collections import defaultdict
        dd = defaultdict(int)
        for c in s:
            dd[c] += 1
        for c in t:
            if not dd[c]:
                return False
            dd[c] -= 1
        sum = 0
        for c in dd:
            sum += dd[c]
        return sum == 0



def main():
    ''' driver for Solution '''
    sol = Solution()
    sss = "anagram"
    ttt = "magaran"
    isa = sol.isAnagram(sss, ttt)
    print("isAnagram({}, {}) => {}".format(sss, ttt, isa))


if __name__ == '__main__':
    main()
