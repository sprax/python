#!/usr/bin/env python3
'''
@file: findxy.py
@auth: sprax
@date: 2018-08-19 00:38:43 Sun 19 Aug

Solve for x:
    sqrt(x + 15) + sqrt(x) = 15
    x = 49
'''
from __future__ import print_function
import math
import unittest
import sys
# import argparse
# import pdb
# from pdb import set_trace


def find_x_y(max_y=25, verbose=1):
    ''' Solve for x & y:
        sqrt(x + y) + sqrt(x) = y
    '''
    for y in range(max_y):
        for x in range(max_y * max_y):
            if abs(math.sqrt(x + y) + math.sqrt(x) - y) < 0.00001:
                # set_trace()
                print("sqrt(%d + %d) + sqrt(%d) == %d" % (x, y, x, y))
            elif verbose > 1:
                print("sqrt(%d + %d) + sqrt(%d) != %d" % (x, y, x, y))


class TestFinder(unittest.TestCase):
    '''Tests for class binary search functions'''

    def init_data(self):
        ''' init test data '''
        self.max_y = 50

    def runTest(self):
        '''why?'''
        pass

    def setUp(self):
        ''' init test data '''
        self.init_data()
        print(str(__doc__))

    # def test_find_some(self):
    #     ''' tests find_equal '''
    #     pass


def main():
    '''test driver'''
    argc = len(sys.argv)
    if argc < 2:
        find_x_y()
    elif argc < 3:
        unittest.main()
    elif argc < 4:
        print("argc == %d: Depends on runTest being defined (or bypassed ?"
              % argc)
        tester = TestFinder()
        # set_trace()
        tester.init_data()
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFinder)
        unittest.TextTestRunner(verbosity=3).run(suite)


if __name__ == '__main__':
    main()
