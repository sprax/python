
#!/usr/bin/env python
'''
From:
http://what-i-learnt-today-blog.blogspot.com/2013/01/python-gcdlcm.html
How to find the GCD and LCM of two non-zero integers.
Find the GCD first:

 Given A >= B,
 1) Divide the A by B to get the remainder R = A % B.
 2) Now B >= A % B, so switch places A=B and B=R, and compute B % R.
 3) Repeat the above 2 steps until the bigger number A == 0.
'''
from __future__ import print_function

def _extra_char(s_a, s_b):
    ''' extra char, assuming len(s_a) - len(s_b) == 1 '''
    ans = ord(s_a[0])
    for c_a in s_a[1:]:
        ans ^= ord(c_a)
    for c_b in s_b:
        ans ^= ord(c_b)
    return chr(ans)

def extra_char(s_a, s_b):
    ''' extra char, assuming length difference of 1 '''
    alb = len(s_a) - len(s_b)
    if alb == 1:
        return _extra_char(s_a, s_b)
    elif alb == -1:
        return _extra_char(s_b, s_a)
    return None
