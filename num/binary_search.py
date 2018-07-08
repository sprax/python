import unittest
import fibonaccis


class BinarySearch:
    """BinarySearch: find exact values or bounds in a numerical array"""

    def find_equal(self, arr, val):
        """find_equal
        Numerical binary search
        Do a binary search for an index of a value in a sorted array int_array,
        that is, return k s.t. value == int_array[k].
        If the specified value is not in int_array, return -1.

        @param int_array     sorted array
        @param val   value to be searched for in int_array
        @return      an index k s.t. v == int_array[k], or -1 (invalid index)
        """
        tove = 0
        hive = len(arr) - 1
        while (tove <= hive):
            mive = (hive + tove) // 2
            if (arr[mive] == val):
                return mive
            if (arr[mive] > val):
                hive = mive - 1
            else:
                tove = mive + 1
        return -1

    def find_lower_bound(self, arr, val):
        """find_lower_bound
        Return an index for the largest element v in int_array such that
        v <= specified value.
        If there is no such element in arr, return -1
        """
        tove, mive, hive = 0, 0, len(arr) - 1
        while (tove <= hive):
            mive = (hive + tove) >> 1
            if (arr[mive] == val):
                return mive
            if (arr[mive] > val):
                hive = mive - 1
            else:
                tove = mive + 1

        if (arr[mive] <= val):
            return mive

        mive = mive - 1
        if (mive >= 0 and arr[mive] <= val):
            return mive
        return -1

    def find_upper_bound(self, arr, val):
        """find_upper_bound
        Return index of smallest element v in arr s.t v >= specified value.
        If there is no such element in arr, return -1.
        """
        tove, mive, hive = 0, 0, len(arr) - 1
        while (tove <= hive):
            mive = (hive + tove) >> 1
            if (arr[mive] == val):
                return mive
            if (arr[mive] > val):
                hive = mive - 1
            else:
                tove = mive + 1

        if (arr[mive] >= val):
            return mive

        mive = mive + 1
        if (mive < len(arr) and arr[mive] >= val):
            return mive
        return -1

    def interpolation_search_equals(int_array, val):
        """  /**
        binary search for an index for the value v in a sorted array int_array,
        that is, find k s.t. v == int_array[k].  Obviously, v must be the value
        of an actual element in int_array.

        @param int_array     sorted array of int
        @param val   value to be search for in int_array
        @return      an index k s.t. v == int_array[k], or -1 (invalid index)
        """
        # Must do error checking before allowing interpolation
        if not int_array:
            return None
        tove = 0
        hive = len(int_array) - 1
        if val < int_array[tove] or val > int_array[hive]:
            return None

        mive = 0
        while tove <= hive:
            if (int_array[hive] == int_array[tove]
                ):      # value of int_array is const in [tove .. hive];
                # either this value == v, or v is not in int_array.
                if int_array[tove] == val:
                    return tove          # So return the smallest index found,
                break                # or return NotFound.
            else:
                delta = (hive - tove) * (val -
                                     int_array[tove]) / (int_array[hive] - int_array[tove])
                if delta > 1.0 or delta < -1.0:
                    mive = tove + int(delta)
                else:
                    mive = (tove + hive) >> 1

    #        if (0.0 <= delta && delta <= 1.0)
    #          mive = tove + 1;
    #        else if (-1.0 <= delta && delta < 0.0)
    #          mive = tove - 1;
    #        else
    #          mive = tove + (int)delta;

            if (int_array[mive] == val):
                return mive

            if (int_array[mive] > val):
                hive = mive - 1
            else:
                tove = mive + 1

        return -1


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
      for (int v : SS) {
        if (v >=  medVal) {
          modVal = v;       # mode val: first v in int_array s.t. v >= medVal
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
    '''Tests for class BinarySearch'''

    def setUp(self):
        ''' init test data '''
        self.int_array = [y for y in fibonaccis.fib_generate(20)]
        self.test_vals = [-2, 0, 1, 2, 20, 21, 22, 8888]
        print(str(BinarySearch.__doc__))
        print(str(self.id()), '\n')

    def test_find_equal(self):
        ''' tests find_equal '''
        bins = BinarySearch()
        func = bins.find_equal
        print(str(func.__doc__))
        for val in self.test_vals:
            res = func(self.int_array, val)
            if (res >= 0):
                print(
                    "exact value",
                    self.int_array[res],
                    "found at index",
                    res)
            else:
                print("exact value", val, "not found")
        print()

    def test_find_lower_bound(self):
        '''tests find_lower_bound'''
        bins = BinarySearch()
        func = bins.find_lower_bound
        print(str(func.__doc__))
        print(self.int_array)
        for val in self.test_vals:
            res = func(self.int_array, val)
            if (res >= 0):
                print(
                    "lower bound",
                    self.int_array[res],
                    "found for",
                    val,
                    "at index",
                    res)
            else:
                print("lower bound for", val, "not found")
        print()

    def test_find_upper_bound(self):
        '''tests find_upper_bound'''
        bins = BinarySearch()
        func = bins.find_upper_bound
        print(str(func.__doc__))
        print(self.int_array)
        for val in self.test_vals:
            res = func(self.int_array, val)
            if (res >= 0):
                print(
                    "upper bound {} found for {} at index {}".format(self.int_array[res], val, res))
            else:
                print("upper bound for {} not found".format(val))
        print()


if __name__ == '__main__':
    unittest.main()
