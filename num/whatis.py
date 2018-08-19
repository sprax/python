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
import pdb
from pdb import set_trace

def find_x_y(max_y=25, verbose=1):
    ''' Solve for x & y:
        sqrt(x + y) + sqrt(x) = y
    '''
    for y in range(max_y):
        for x in range(max_y * max_y // 2):
            if abs(math.sqrt(x + y) + math.sqrt(y) - y) < 0.00001:
                print("sqrt(%d + %d) + sqrt(%d) == %d" % (x, y, x, y))



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


if __name__ == '__main__':
    if True:
        find_x_y()
    elif False:
        unittest.main()
    elif True:
        # Depends on runTest being defined (or bypassed ?)
        TBS = TestFinder()
        set_trace()
        TBS.init_data()
        print("\n\t  Direct call:")
        TBS.test_find_equal(interpolation_search_equals)
        # unittest.main()     # NOTE: This must be last, because basically it calls exit.
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFinder)
        unittest.TextTestRunner(verbosity=3).run(suite)
