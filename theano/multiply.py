#!/usr/bin/env python3
''' multipy.py: multiply two numbers using Theano -- tests installation
    From https://github.com/Newmu/Theano-Tutorials/blob/master/0_multiply.py
'''

from __future__ import print_function
import theano
from theano import tensor as T

a = T.scalar()
b = T.scalar()

y = a * b

multiply = theano.function(inputs=[a, b], outputs=y)

print(multiply(1, 2)) #2
print(multiply(3, 3)) #9
