from itertools import islice
from fileinput import input

def sieve():         # from code.activestate.com/recipes
    yield 2          #                 /117119-sieve-of-eratosthenes
    D = {}           # original code by
    c = 3            #       David Eppstein, UC Irvine, 28 Feb 2002
    while True:
        s = D.pop(c, 0)
        if s:
            add(D, c + s, s)
        else:
            yield c
            D[c*c] = 2*c
        c += 2

def postponed_sieve(): # postponed sieve, by Will Ness, ideone.com/WFv4f
    yield 2            #
    D = {}             # see also:  stackoverflow.com/a/10733621/849891
    c = 3                         # stackoverflow.com/a/8871918/849891
    ps = (p for p in sieve())
    p = ps.next() and ps.next()     # 3
    q = p*p                         # 9
    while True:
        s = D.pop(c, 0)
        if s:
            add(D, c + s, s)
        else:
            if c < q:
                yield c
            else:
                add(D, c + 2*p, 2*p)
                p = ps.next()
                q = p*p
        c += 2

def add(D, x, s):
    while x in D:
        x += s
    D[x] = s

def main():
    for line in input():
        n = int(line)
        print(list(islice((p for p in postponed_sieve()), n-1, n+1)))
        break

#                - base -              - postponed -
#
# tested Sept 2012:
#
# 1500000                           11.65s-10.9   n^0.99
# 1000000 11.14s-33.9   n^1.23       7.81s-10.9   n^1.01
#  800000  8.46s-33.6   n^1.10       6.24s-10.9   n^1.11
#  400000  3.96s-21.3   n^1.05       2.89s-10.9   n^1.02
#  200000  1.91s-11.4   n^1.09       1.43s-10.9   n^1.01
#  100000  0.90s-11.4MB              0.71s-10.9MB
#
#
# tested in early 2012:
#
# 1500000                          13.28s-4.7   n^1.09
# 1000000 10.83s-28.0  n^1.23       8.53s-4.7   n^1.08
#  800000  8.23s-28.0  n^1.13       6.70s-4.7   n^1.09
#  400000  3.76s-15.8  n^1.11       3.14s-4.7   n^1.07
#  200000  1.74s-4.9MB              1.50s-4.7MB
