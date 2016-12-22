# loops.py
for j in range(10):
    print(j, end=',')    
print()

k = 9
while (k >= 0):
    print(k, end=' ')
    k = k-1
print('\n')

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')


# fibonacci_generator
def fib_generate(n):
    a, b, x = 0, 1, 0
    while x < n:
        yield a
        a, b = b, a + b
        x = x+1

def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b

print()
fib(2000)
print(fib(0))

def printFibGen(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    print([ y for y in fib_generate(n)] )

printFibGen(18)

def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yep', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise IOError('refusenik user')
        print(complaint)
        
ok = ask_ok("You got it? ") 
if ok:
    print("You got it!")
else:
    print("You don't got it.") 
