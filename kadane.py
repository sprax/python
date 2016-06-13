# kadane.py from the interwebs
'''Kadane algorithm for finding the maximum sum of a contiguous subarray'''

def max_contiguous_sum(array):
    '''function to find the maximum sum of a contiguous subarray'''
    max_so_far = max_ending_here = 0
    for elt in array:
        max_ending_here = max(0, max_ending_here + elt)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

