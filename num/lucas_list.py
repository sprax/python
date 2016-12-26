# lucas_list.py -- tested with python 2.7 and 3.5
'''Lucas numbers computed as lists'''
import sys
import fibonaccis

def lucas_interval(inf, sup):
    '''Return a list of Lucas numbers between inf and sup, inclusive.'''
    result = []
    a, b = 1, 3
    while a <= sup:
        if inf <= a:
            result.append(a)
        a, b = b, a+b
    return result

def lucas_list(length): # return list of Lucas numbers up to sup
    '''Return a list containing the Fibonacci series up to sup.'''
    result = []
    a, b = 1, 3
    while length > 0:
        result.append(a)    # see below
        a, b = b, a+b
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
