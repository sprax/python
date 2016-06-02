# for.py

for n in range(2, 53):
    for x in range(2, n):
        if n % x == 0:
            print(str(n) + ' equals ' + str(x) + ' * ' + str(n/x))
            break
    else:
        # loop fell through without finding a factor
        print(str(n) + ' is a prime number')

