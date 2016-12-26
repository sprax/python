import unittest
import fibonaccis

class LinHomoRecWithConstCoeffs:
    """LHRWCC: Linear Homogenous Recurrence With Constant Coefficients"""

    def __init__(self, coeffs, inits):
        assert len(coeffs) == len(inits)
        self.order = len(coeffs)
        self.coeffs = coeffs
        self.inits = inits

    def a_n_rec(self, n):
        if (n < self.order):
            return self.inits[n]
        tot = 0
        for k in range(self.order):
            tot += self.coeffs[k] * self.a_n_rec(n - k - 1)
        return tot



class TestLinHomoRecWithConstCoef(unittest.TestCase):

    def setUp(self):
        self.intArray = [y for y in fibonaccis.fib_generate(20) ]
        self.testVals = [-2, 0, 1, 2, 20, 21, 22, 8888]
        print(str(LinHomoRecWithConstCoeffs.__doc__))
        print(str(self.id()), '\n')

    def test_fibs(self):
        print("test_fibs")
        fibs = LinHomoRecWithConstCoeffs([1, 1], [1, 1])
        print("fibs.order: {}".format(fibs.order))
        for j in range (30):
            print("fibs.a_n_rec({}) => {}".format(j, fibs.a_n_rec(j)))

if __name__ == '__main__':
    unittest.main()

