#!/usr/bin/env python3
''' multipy.py: MULTIPLY two numbers using Theano -- tests installation
    From https://github.com/Newmu/Theano-Tutorials/blob/master/0_multiply.py
    Written for: anaconda python 3.5; conda install theano=1.0.2
'''

from __future__ import print_function
import theano
from theano import tensor as T

ScA = T.scalar()
ScB = T.scalar()

PRODUCT = ScA * ScB

MULTIPLY = theano.function(inputs=[ScA, ScB], outputs=PRODUCT)

print(MULTIPLY(1, 2)) #2
print(MULTIPLY(3, 3)) #9
