
import pdb
from pdb import set_trace

class Solution(object):
    def countNegatives(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        rows = len(grid)
        if not rows:
            return 0
        nnn_count = 0
        cols = len(grid[0])
        tot_count = rows * cols
        # set_trace()
        for row in grid:
            nnn = 0
            for col in range(cols):
                if row[col] >= 0:
                    nnn += 1
                else:
                    cols = nnn
                    break
            nnn_count += nnn
        return tot_count - nnn_count

def main():
    ''' test Solution '''
    sol = Solution()
    grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]
    cnnn = sol.countNegatives(grid)
    print("countNegatives({}) => {}".format(grid, cnnn))

if __name__ == '__main__':
    main()
