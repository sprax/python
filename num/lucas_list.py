# lucas_list.py -- tested with python 2.7

def fib(n): # return Fibonacci series up to n
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 1, 3
    while a < n:
        result.append(a)    # see below
        a, b = b, a+b
    return result

f100 = fib(100) # call the function
print(f100)     # print the result

