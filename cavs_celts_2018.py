''' Cavaliers vs. Celtics 2018 ECF'''

from __future__ import print_function
from pprint import pprint

CAVS_CELTS_ECF_2018 = [
    (83, 108),
    (94, 107),
    (116, 86),
    (111, 102),
    (83, 96),
    (109, 99),
    (87, 79)
]

def avg_diffs():
    '''totals, diffs, averages'''
    cavs_pts = [x[0] for x in CAVS_CELTS_ECF_2018]
    celt_pts = [x[1] for x in CAVS_CELTS_ECF_2018]
    cavs_sum = sum(cavs_pts)
    celt_sum = sum(celt_pts)
    pprint(CAVS_CELTS_ECF_2018)
    print("Cavs total:", cavs_sum)
    print("Celt total:", celt_sum)
    print("Average: Cavs/Celts: ", float(cavs_sum)/celt_sum)
    cavs_wins = [x[0] - x[1] for x in CAVS_CELTS_ECF_2018 if x[0] > x[1]]
    celt_wins = [x[1] - x[0] for x in CAVS_CELTS_ECF_2018 if x[1] > x[0]]
    print("Cavs wins: ", cavs_wins, " avg: ", float(sum(cavs_wins))/len(cavs_wins))
    print("Celt wins: ", celt_wins, " avg: ", float(sum(celt_wins))/len(celt_wins))

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
    avg_diffs()

if __name__ == '__main__':
    main()
