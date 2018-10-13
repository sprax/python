#!/usr/bin/python
'''Python 2.7 script to calculate the area of "water"
that would be trapped by a histogram.'''

from __future__ import print_function
import sys

def histarea_length(histogram, length):
    '''
    Calculates the max area of "fluid" that could be
    retained among the columns of a histogram if poured
    or rained onto it from above.  Assume no "walls" at
    the ends.  (If there were, you could just add up the
    area "under" the historgram and subtract it from the
    area of the whole rectangle.)
    '''

    area = 0
    if length > 2:
        max_from_left = []

	# Pass 1: Initialize from first entry; don't skip the last entry.
        max_height = histogram[0]
        max_from_left.append(max_height)
        for j in range(1, length):
            height = histogram[j]
            if  max_height < height:
                max_height = height
            max_from_left.append(max_height)

	# Pass 2: Initialize from last entry; do skip the first entry.
        max_from_right = histogram[length-1]
        for j in range(length-2, 0, -1):
            height = histogram[j]
            if  max_from_right < height:
                max_from_right = height
            lesser_max = min(max_from_left[j], max_from_right)
            area += lesser_max - height
    return area


def histarea_simple(histogram):
    '''
    Calculates the max area of "fluid" that could be
    retained among the columns of a histogram if poured
    or rained onto it from above.  Assume no "walls" at
    the ends.  (If there were, you could just add up the
    area "under" the historgram and subtract it from the
    area of the whole rectangle.)
    '''
    length = len(histogram)
    if length < 3:
        return 0

	# Pass 1: Initialize from first entry; don't skip the last entry.
    max_height = histogram[0]
    max_from_left = []
    for height in histogram:
        if  max_height < height:
            max_height = height
        max_from_left.append(max_height)

	# Pass 2: Initialize from last entry; do skip the first entry.
    area = 0
    max_right = histogram[length-1]
    for j in range(length-2, 0, -1):
        height = histogram[j]
        if  max_right < height:
            max_right = height
        max_left = max_from_left[j]
        if max_left < max_right:
            area += max_left - height
        else:
            area += max_right - height
    return area




def test_one(histogram):
    '''Test histarea on one array'''
    length = len(histogram)
    area_l = histarea_length(histogram, length)
    area_s = histarea_simple(histogram)
    print("Histogram & areas:", histogram, "=> length:", area_l, " simple:", area_s)
    print()

def test_histarea():
    '''Test driver for histarea'''
    print(sys.argv[0], ": test_histarea")	# program_name
    test_one([10, 5, 10, 15, 10, 20])
    test_one([-1, 2, 32, -4, 4, 44, 2, 38, 0])

if __name__ == '__main__':
    test_histarea()
