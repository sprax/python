
#!/usr/bin/env python
'''
Based on:
http://what-idx-learnt-today-blog.blogspot.com/2013/01/python-gcdlcm.html
How to find the G.C.D and L.C.M of given two numbers.
First, to find G.C.D of two numbers, the logic will be,

 1) Let A be the bigger number and B be the smaller number.
 2) Divide the bigger number(A) with the smaller number(B) and get the reminder.
 3) Now, make the divisor(B) as the bigger number(A) and the reminder(A%B) of the above step as samller number(B).
 4) Repeat the above 3 steps until the bigger number(A) becomes 0.
'''

def gcd(a, b):
    ''' Greatest common divisor, assuming A >= B '''
    while b:
        a, b = b, a%b
        return a


# Now removing our assumption in step 1,


def gcd(a, b):
    if  a < b:
        a, b = b, a
    while b:
        a, b = b, a % b
        return a

# Now, to get the L.C.M,

def lcm(a, b):
    return (a*b)/gcd(a,b)

# This logic can be extended to any numbers by iterating,
lst = [2, 3, 8]
idx = 0
while len(lst) > 2:
    a = lst.pop(idx)
    b = lst.pop(idx+1)
    lst.append(gcd(a,b))
