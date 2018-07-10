# fibonacci_list.py -- tested with python 2.7 and 3.5
'''list method for computing Fibonacci numbers up to given bound'''
def fib(sup): # return Fibonacci series up to sup
    """Return a list containing the Fibonacci series up to sup."""
    result = []
    a, b = 0, 1
    while a < sup:
        result.append(a)    # see below
        a, b = b, a + b
    return result

F100 = fib(100) # call the function
print(F100)     # print the result
