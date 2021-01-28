#!/usr/bin/env python
''' Binary Search functions and a test class
    Find exact values or bounds in a numerical array.
'''
from __future__ import print_function
import unittest
# import argparse
import pdb
from pdb import set_trace
# from pprint import pprint
import fibonaccis

def find_equal(mono_l, target):
    """find_equal
    Numerical binary search
    Do a binary search for an index of a value in a sorted array mono_l,
    that is, return k s.t. value == mono_l[k].
    If the specified value is not in mono_l, return -1.

    @param mono_l   sorted array (indexible list)
    @param target   value to be searched for in mono_l
    @return         an index k s.t. v == mono_l[k], or -1 (invalid index)
    """
    jlo = 0
    jhi = len(mono_l) - 1
    while jlo <= jhi:
        jmd = (jhi + jlo) // 2
        # print("jlo, jmd, jhi: %2d %2d %2d : %d" % (jlo, jmd, jhi, mono_l[jmd]))
        if mono_l[jmd] > target:
            jhi = jmd - 1
        elif mono_l[jmd] < target:
            jlo = jmd + 1
        else:
            # print("exact: mono_l[%d] (%d) == (%d)" % (jmd, mono_l[jmd], target))
            return jmd
    return None # this line coult be omitted


def find_lower_bound(mono_l, target):
    """find_lower_bound
    Return an index for the largest element in mono_l (a monotonically
    increasing list of numbers) such that mono_l[index] <= the specified target.
    If there is no such element in mono_l, return -1
    """
    jlo, jmd, jhi = 0, 0, len(mono_l) - 1
    while jlo <= jhi:
        jmd = (jhi + jlo) >> 1
        if mono_l[jmd] > target:
            jhi = jmd - 1
        elif mono_l[jmd] < target:
            jlo = jmd + 1
        else:
            # assert mono_l[jmd] == target
            return jmd

    if mono_l[jmd] <= target:
        return jmd

    jmd = jmd - 1
    if jmd >= 0 and mono_l[jmd] <= target:
        return jmd
    return -1


def find_upper_bound(mono_l, target):
    """find_upper_bound
    Return index of smallest element v in mono_l s.t v >= specified value.
    If there is no such element in mono_l, return -1.
    """
    jlo, jmd, jhi = 0, 0, len(mono_l) - 1
    while jlo <= jhi:
        jmd = (jhi + jlo) >> 1
        if mono_l[jmd] > target:
            jhi = jmd - 1
        elif mono_l[jmd] < target:
            jlo = jmd + 1
        else:
            assert mono_l[jmd] == target
            return jmd

    if mono_l[jmd] >= target:
        return jmd

    jmd = jmd + 1
    if jmd < len(mono_l) and mono_l[jmd] >= target:
        return jmd
    return -1


def interpolation_search_equals(mono_l, target):
    """
    binary search for an index for the value v in a sorted array mono_l,
    that is, find k s.t. v == mono_l[k].  Obviously, v must be the value
    of an actual element in mono_l.

    @param mono_l     sorted array of int
    @param target   value to be search for in mono_l
    @return      an index k s.t. v == mono_l[k], or -1 (invalid index)
    """
    # Must do error checking before allowing interpolation
    if not mono_l:
        return None
    jlo = 0
    jhi = len(mono_l) - 1
    # print("interpolation_search_equals: mono_l has type:", type(mono_l).__name__)
    if target < mono_l[jlo] or target > mono_l[jhi]:
        return None

    jmd = 0
    while jlo <= jhi:
        if mono_l[jhi] == mono_l[jlo]:
            # value of mono_l is const in [jlo .. jhi];
            # either this value == v, or v is not in mono_l.
            if mono_l[jlo] == target:
                return jlo          # So return the smallest index found,
            break                   # or return NotFound.
        else:
            delta = (jhi - jlo) * (target - mono_l[jlo]) / (mono_l[jhi] - mono_l[jlo])
            if delta > 1.0 or delta < -1.0:
                jmd = jlo + int(delta)
            else:
                jmd = (jlo + jhi) >> 1

#        if 0.0 <= delta && delta <= 1.0
#          jmd = jlo + 1;
#        else if -1.0 <= delta && delta < 0.0
#          jmd = jlo - 1;
#        else
#          jmd = jlo + (int)delta;

        if mono_l[jmd] == target:
            return jmd
        if mono_l[jmd] > target:
            jhi = jmd - 1
        else:
            jlo = jmd + 1
    return None # explicit return could be omitted


def etc():
    """
    public static int test_binarySearch(int size)
    {
      int nRows = 2, nCols = 20;
      int minVal = 10, maxVal = 0;
      int maxInc = 9;
      long  seed = 1; # System.currentTimeMillis();
      int AA[][] = ArrayAlgo.makeRandomRowColSortedArray(nRows, nCols, minVal, maxInc, seed);
    #int SS[] = AA[0];
      int SS[] = { 10, 12, 14, 14, 14, 14, 14, 14, 15, 16, 17, 18, 36, 44, 55, 66};
      nCols   = SS.length;
      minVal  = SS[0];
      maxVal  = SS[nCols-1];
      int mmmVal = maxVal - 1;
      int medVal = Medians.medianOfSortedArray(SS);
      int midVal = (minVal + maxVal) >> 1;
      int modVal = Integer.MIN_VALUE;
      for int v : SS {
        if v >=  medVal {
          modVal = v;       # mode target: first v in mono_l s.t. v >= medVal
          break;
        }
      }
      for (int j = 0; j < SS.length; j++)
        System.out.format(" %2d", j);
      Sx.puts();
      Sx.putsArray(SS);
      Sx.puts("mode " + modVal + "  median " + medVal + "  middle " + midVal);

      int iF  = find_equal(SS, minVal);
      int iN  = find_equal(SS, modVal);
      int iD  = find_equal(SS, medVal);
      int iA  = find_equal(SS, midVal);
      int iM  = find_equal(SS, mmmVal);
      int iL  = find_equal(SS, maxVal);
      Sx.print("binary search:");
      System.out.format(" first mode median mid 2nd last  %2d  %2d  %2d  %2d  %2d  %2d\n", iF, iN, iD, iA, iM, iL);

      iF  = interpolationSearchEquals(SS, minVal);
      iN  = interpolationSearchEquals(SS, modVal);
      iD  = interpolationSearchEquals(SS, medVal);
      iA  = interpolationSearchEquals(SS, midVal);
      iM  = interpolationSearchEquals(SS, mmmVal);
      iL  = interpolationSearchEquals(SS, maxVal);
      Sx.print("interpolation:");
      System.out.format(" first mode median mid 2nd last  %2d  %2d  %2d  %2d  %2d  %2d\n", iF, iN, iD, iA, iM, iL);

      iF  = binarySearchLowerBound(SS, minVal);
      iN  = binarySearchLowerBound(SS, modVal);
      iD  = binarySearchLowerBound(SS, medVal);
      iA  = binarySearchLowerBound(SS, midVal);
      iM  = binarySearchLowerBound(SS, mmmVal);
      iL  = binarySearchLowerBound(SS, maxVal);
      Sx.print("lower bound:  ");
      System.out.format(" first mode median mid 2nd last  %2d  %2d  %2d  %2d  %2d  %2d\n", iF, iN, iD, iA, iM, iL);

      iF  = binarySearchUpperBound(SS, minVal);
      iN  = binarySearchUpperBound(SS, modVal);
      iD  = binarySearchUpperBound(SS, medVal);
      iA  = binarySearchUpperBound(SS, midVal);
      iM  = binarySearchUpperBound(SS, mmmVal);
      iL  = binarySearchUpperBound(SS, maxVal);
      Sx.print("upper bound:  ");
      System.out.format(" first mode median mid 2nd last  %2d  %2d  %2d  %2d  %2d  %2d\n", iF, iN, iD, iA, iM, iL);

      return 0;
    }
  """


class TestBinarySearch(unittest.TestCase):
    '''Tests for class binary search functions'''

    def init_data(self):
        ''' init test data '''
        self.mono_l = [y for y in fibonaccis.fib_generate(20)]
        self.test_vals = [-2, 0, 1, 2, 5, 8, 13, 20, 21, 22, 8888]
        self.expecteds = [x in self.mono_l for x in self.test_vals]

    def runTest(self):
        pass

    # NOTE: Already defined in base class, no need to extend.
    # def __init__(self):
    #     ''' init self '''
    #     self.init_data()

    def setUp(self):
        ''' init test data '''
        self.init_data()
        print(str(__doc__))
        print(str(self.id()), '\n')
        # print("mono_l is of type:", type(self.mono_l).__name__)
        print("fibs:", self.mono_l)
        print("vals:", self.test_vals)
        print("exps:", self.expecteds)

    def test_find_equal(self, find_equal_func=find_equal):
        ''' tests find_equal '''
        num_wrong = 0
        print(str(find_equal_func.__doc__))
        for target, exp in zip(self.test_vals, self.expecteds):
            result = find_equal_func(self.mono_l, target)
            if result is not None:
                num_wrong += not exp
                print("%d | exact value %3d found at index %d"
                      % (num_wrong, self.mono_l[result], result))
            else:
                num_wrong += exp
                print("%d | exact value %3d not found" % (num_wrong, target))
        print("num_wrong:", num_wrong)
        return num_wrong


    def test_find_lower_bound(self):
        '''tests find_lower_bound'''
        func = find_lower_bound
        print(str(func.__doc__))
        for target in self.test_vals:
            result = func(self.mono_l, target)
            if result >= 0:
                print(
                    "lower bound",
                    self.mono_l[result],
                    "found for",
                    target,
                    "at index",
                    result)
            else:
                print("lower bound for", target, "not found")
        print()

    def test_find_upper_bound(self):
        '''tests find_upper_bound'''
        func = find_upper_bound
        print(str(func.__doc__))
        print(self.mono_l)
        for target in self.test_vals:
            result = func(self.mono_l, target)
            if result >= 0:
                print("upper bound {} found for {} at index {}"
                      .format(self.mono_l[result], target, result))
            else:
                print("upper bound for {} not found".format(target))
        print()


if __name__ == '__main__':
    if False:
        unittest.main()
    elif True:
        # Depends on runTest being defined (or bypassed ?)
        TBS = TestBinarySearch()
        set_trace()
        TBS.init_data()
        print("\n\t  Direct call:")
        TBS.test_find_equal(interpolation_search_equals)
        # unittest.main()     # NOTE: This must be last, because basically it calls exit.
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBinarySearch)
        unittest.TextTestRunner(verbosity=3).run(suite)
