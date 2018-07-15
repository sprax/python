# fibonacci_list.py -- tested with python 2.7 and 3.5
'''list method for computing Fibonacci numbers up to given bound'''
import sys

def fib(sup): # return Fibonacci series up to sup
    """Return a list containing the Fibonacci series up to sup."""
    result = []
    a, b = 0, 1
    while a <= sup:
        result.append(a)    # see below
        a, b = b, a + b
    return result


if __name__ == '__main__':
    NUM = int(sys.argv[1]) if len(sys.argv) > 1 else 89
    FIBS = fib(NUM) # call the function
    print(FIBS)     # print the result
