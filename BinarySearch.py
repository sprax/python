
import unittest
import fibonaccis

class BinarySearch:
    """BinarySearch: find exact values or bounds in a numerical array"""

    def findEquals(self, A, val):
        """findEquals
        Numerical binary search
        Do a binary search for an index of a value in a sorted array intArray, 
        that is, return k s.t. value == intArray[k].  
        If the specified value is not in intArray, return -1.

        @param intArray     sorted array
        @param val   value to be searched for in intArray
        @return      an index k s.t. v == intArray[k], or -1 (invalid index)
        """
        lo = 0
        hi = len(A) - 1
        while (lo <= hi):
            md = (hi + lo) // 2
            if (A[md] == val):
                return md;
            if (A[md] > val):
                hi = md - 1
            else:
                lo = md + 1
        return -1;


    def find_lower_bound(self, A, val):
        """find_lower_bound
        Return an index for the largest element v in intArray such that 
        v <= specified value.
        If there is no such element in A, return -1
        """
        lo, md, hi = 0, 0, len(A) - 1
        while (lo <= hi):
            md = (hi + lo) >> 1
            if (A[md] == val):
                return md;
            if (A[md] > val):
                hi = md - 1
            else:
                lo = md + 1
    
        if (A[md] <= val):
            return md
        
        md = md - 1
        if (md >= 0 and A[md] <= val):
            return md
        return -1


    def find_upper_bound(self, A, val):
        """find_upper_bound
        Return index of smallest element v in A s.t v >= specified value.
        If there is no such element in A, return -1.
        """        
        lo, md, hi = 0, 0, len(A) - 1
        while (lo <= hi):
            md = (hi + lo) >> 1
            if (A[md] == val):
                return md;
            if (A[md] > val):
                hi = md - 1
            else:
                lo = md + 1
    
        if (A[md] >= val):
            return md
        
        md = md + 1
        if (md < len(A) and A[md] >= val):
            return md
        return -1

  
def etc():
    """  /** 
   * binary search for an index for the value v in a sorted array intArray,
   * that is, find k s.t. v == intArray[k].  Obviously, v must be the value
   * of an actual element in intArray.
   * 
   * @param intArray     sorted array of int
   * @param val   value to be search for in intArray
   * @return      an index k s.t. v == intArray[k], or -1 (invalid index)
   */
  public static int interpolationSearchEquals(int intArray[], int val)
  {
    // Must do error checking before allowing interpolation
    if (intArray == null || intArray.length < 1)
      return -1;
    int lo = 0, hi = intArray.length-1;
    if (val < intArray[lo] || val > intArray[hi])
      return -1;
    
    for (int md = 0; lo <= hi; ) 
    {
      if (intArray[hi] == intArray[lo]) {   // value of intArray is const in [lo .. hi];
        if (intArray[lo] == val)     // either this value == v, or v is not in intArray.
          return lo;          // So return the smallest index found,
        break;                // or return NotFound.
      } else {
        double delta = (hi - lo)*(val - intArray[lo])/(double)(intArray[hi] - intArray[lo]);
        if (delta > 1.0 || delta < -1.0) {
          md = lo + (int)delta;
        } else {
          md = (lo + hi) >> 1;
        }

//        if (0.0 <= delta && delta <= 1.0)
//          md = lo + 1;
//        else if (-1.0 <= delta && delta < 0.0)
//          md = lo - 1;
//        else
//          md = lo + (int)delta;

      }
      if (intArray[md] == val)
        return md;

      if (intArray[md] >  val)
        hi = md - 1;
      else
        lo = md + 1;
    }
    return -1;
  }
    
  public static int test_binarySearch(int size) 
  {
    int nRows = 2, nCols = 20;
    int minVal = 10, maxVal = 0;
    int maxInc = 9;
    long  seed = 1; // System.currentTimeMillis();
    int AA[][] = ArrayAlgo.makeRandomRowColSortedArray(nRows, nCols, minVal, maxInc, seed);
  //int SS[] = AA[0];
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
        modVal = v;       // mode val: first v in intArray s.t. v >= medVal
        break;
      }
    }
    for (int j = 0; j < SS.length; j++)
      System.out.format(" %2d", j);
    Sx.puts();
    Sx.putsArray(SS);
    Sx.puts("mode " + modVal + "  median " + medVal + "  middle " + midVal);

    int iF  = findEquals(SS, minVal);
    int iN  = findEquals(SS, modVal);
    int iD  = findEquals(SS, medVal);
    int iA  = findEquals(SS, midVal);
    int iM  = findEquals(SS, mmmVal);
    int iL  = findEquals(SS, maxVal);
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
  
  public static int unit_test(int level) 
  {
    Sx.puts(BinarySearch.class.getName() + ".unit_test");   
    int stat = 0;    
    if (level > 0) {
      stat += test_binarySearch(1);
    }
    return stat;
  }
  
  public static void main(String[] args)
  {
    unit_test(1);
  }
}
"""


class TestBinarySearch(unittest.TestCase):

    def setUp(self):
        self.intArray = [y for y in fibonaccis.fib_generate(20) ]
        self.testVals = [-2, 0, 1, 2, 20, 21, 22, 8888]
        print(str(BinarySearch.__doc__))
        print(str(self.id()), '\n')

    def test_findEquals(self):
        bs = BinarySearch()
        fn = bs.findEquals;
        print(str(fn.__doc__))
        for val in self.testVals:
            r = fn(self.intArray, val)
            if (r >= 0):
                print("exact value", self.intArray[r], "found at index", r)
            else:
                print("exact value", val, "not found")
        print()

    def test_find_lower_bound(self):
        bs = BinarySearch()
        fn = bs.find_lower_bound;
        print(str(fn.__doc__))
        print(self.intArray)
        for val in self.testVals:
            r = fn(self.intArray, val)
            if (r >= 0):
                print("lower bound", self.intArray[r], "found for", val, "at index", r)
            else:
                print("lower bound for", val, "not found")
        print()

    def test_find_upper_bound(self):
        bs = BinarySearch()
        fn = bs.find_upper_bound;
        print(str(fn.__doc__))
        print(self.intArray)
        for val in self.testVals:
            r = fn(self.intArray, val)
            if (r >= 0):
                print("upper bound", self.intArray[r], "found for", val, "at index", r)
            else:
                print("upper bound for", val, "not found")
        print()

if __name__ == '__main__':
    unittest.main()

