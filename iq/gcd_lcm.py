
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

def gcd2_a_lte_b(aaa, bbb):
    ''' Greatest common divisor, assuming 1 <= A <= B '''
    while aaa:
        bbb, aaa = aaa, bbb % aaa
    return bbb


def gcd2(aaa, bbb):
    ''' Greatest common divisor of any two numbers. '''
    if  aaa < bbb:
        aaa, bbb = bbb, aaa
    while bbb:
        print("    a, b:", aaa, bbb)
        aaa, bbb = bbb, aaa % bbb
    return aaa if aaa > 0 else -aaa

# Now, to get the L.C.M,

def lcm(aaa, bbb):
    return (aaa*bbb)/gcd2(aaa,bbb)

# # This logic can be extended to any numbers by iterating,
# lst = [2, 3, 8]
# idx = 0
# while len(lst) > 2:
#     aaa = lst.pop(idx)
#     bbb = lst.pop(idx+1)
#     lst.append(gcd2(aaa,bbb))

########################################

def test_ab(aaa, bbb):
    print("testing a, b:", aaa, bbb)
    gcd = gcd2(aaa, bbb)
    print("GCD %d %d: %d" % (aaa, bbb, gcd))

test_ab(2*3*5, 3*3)
test_ab(2*3*5, 3*3)
test_ab(2*3*5, -3*3)
test_ab(-2*3*5, -3*3)
test_ab(2*3*7*17, 2*2*3*5*7*11)
