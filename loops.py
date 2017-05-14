# loops.py
for j in range(10):
    print(j, end=',')
print()

k = 9
while k >= 0:
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
    print([y for y in fib_generate(n)])

printFibGen(18)

def throw_io_error():
    raise IOError('refusenik user')

def constant_factory(value):
    return lambda: value

def ask_yes_no(prompt, retries=3, complaint='Yes or no, please!', default_function=constant_factory(False)):
    while True:
        answer = input(prompt)
        yesno = answer.lower()
        if yesno.lower() in ('y', 'ye', 'yep', 'yes'):
            return True
        if yesno in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries <= 0:
            return default_function()
        print(complaint)

def ask_you_got_it():
    if ask_yes_no("You got it? ", 2, "Give it a yes or no.", default_function=throw_io_error):
        print("You got it!")
    else:
        print("You don't got it.")

if __name__ == '__main__':
    ask_you_got_it()

