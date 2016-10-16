#!/usr/bin/python
'''Python 2.7 script to calculate the area of "water"
that would be trapped by a histogram.'''

import sys

def histarea(histogram, length):
    '''Calculates the area of "fluid" that would be trapped in poured onto
    a histogram from above.'''

    area, height = 0, 0
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


def test_one(histogram):
    '''Test histarea on one array'''
    length = len(histogram)
    area = histarea(histogram, length)
    print("Area from histogram:", histogram, "=>", area)
    print()

def test_histarea():
    '''Test driver for histarea'''
    print(sys.argv[0], ": test_histarea")	# program_name
    test_one([10, 5, 10, 15, 10, 20])
    test_one([-1, 2, 32, -4, 4, 44, 2, 38, 0])

if __name__ == '__main__':
    test_histarea()
