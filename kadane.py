# kadane.py from the interwebs
'''Kadane algorithm for finding the maximum sum of a contiguous subarray'''

from __future__ import print_function

def max_contiguous_sum(array):
    '''function to find the maximum sum of a contiguous subarray'''
    max_so_far = max_ending_here = 0
    for elt in array:
        max_ending_here = max(0, max_ending_here + elt)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

def main():
    '''test max_contiguous_sum (Kadane algorithm)'''
    arr = [1, 2, -4, 1, 3, 4, 1, -2, 2, -1, 2, -1]
    mcs = max_contiguous_sum(arr)
    print(arr, " ==> ", mcs, "(expecting 10)")

if __name__ == '__main__':
    main()
