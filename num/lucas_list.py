# lucas_list.py -- tested with python 2.7 and 3.5
'''Lucas numbers computed as lists'''
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
    '''Return a list of Fibonacci numbers.'''
    result = []
    am2, am1 = 1, 3
    while length > 0:
        result.append(am2)
        am2, am1 = am1, am2 + am1
        length -= 1
    return result

def main():
    '''Print lists of Lucas numbers (default length 31)'''
    argc = len(sys.argv)
    end_num = int(sys.argv[1]) if argc > 1 else 31
    end_fib = fibonaccis.fib_binet(end_num + 2)
    numbers = lucas_interval(1, end_fib)
    print(numbers)
    numbers = lucas_list(end_num)
    print(numbers)

if __name__ == '__main__':
    main()
