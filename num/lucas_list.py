# lucas_list.py -- tested with python 2.7 and 3.5
'''Lucas numbers computed as lists'''
from __future__ import print_function
import sys
import fibonaccis

def lucas_interval(inf, sup):
    '''Return a list of Lucas numbers between inf and sup, inclusive.'''
    result = []
    am2, am1 = 1, 3
    while am2 <= sup:
        if inf <= am2:
            result.append(am2)
        am2, am1 = am1, am2 + am1
    return result

def lucas_list(length):
    '''Return a list of Lucas numbers.'''
    result = []
    am2, am1 = 1, 3
    while length > 0:
        result.append(am2)
        am2, am1 = am1, am2 + am1
        length -= 1
    return result


# Golden Ratio
PHI = (1 + 5**0.5) / 2
OMP = (1 - PHI)

def lucas_binet(idx):
    '''Uses Binet's formula (only good for n < 70)'''
    return int(round(pow(PHI, idx) + pow(OMP, idx)))

DEFAULT_LEN = 34

def main():
    '''Print lists of Lucas numbers (default length 34)'''
    argc = len(sys.argv)
    end_num = int(sys.argv[1]) if argc > 1 else DEFAULT_LEN
    end_fib = fibonaccis.fib_binet(end_num + 2)
    numbers = lucas_interval(1, end_fib)
    print(numbers)
    numbers = lucas_list(end_num)
    print(numbers)
    binets = [lucas_binet(num) for num in range(1, end_num + 1)]
    print("Binet's formula:")
    print(binets)

if __name__ == '__main__':
    main()
