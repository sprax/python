
import timeit
import re

def one():
        any(s in mystring for s in ('foo', 'bar', 'hello'))

r = re.compile('(foo|bar|hello)')
def two():
        r.search(mystring)


mystring="hello"*1000
print([timeit.timeit(k, number=10000) for k in (one, two)])
mystring="goodbye"*1000
print([timeit.timeit(k, number=10000) for k in (one, two)])
