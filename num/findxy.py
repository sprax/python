#!/usr/bin/env python
'''
Solve for x:
    sqrt(x + 15) + sqrt(x) = 15
    x = 49
'''
from __future__ import print_function
import math
import unittest
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
    if True:
        find_x_y()
    elif False:
        unittest.main()
    elif True:
        # Depends on runTest being defined (or bypassed ?)
        tester = TestFinder()
        # set_trace()
        tester.init_data()
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFinder)
        unittest.TextTestRunner(verbosity=3).run(suite)


if __name__ == '__main__':
    main()
