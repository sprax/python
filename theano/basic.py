#!/usr/bin/env python3
''' regression.py: LINEAR REGRESSION using Theano -- tests installation
    From http://www.marekrei.com/blog/theano-tutorial/
    Written for: anaconda python 3.5; conda install theano=1.0.2
'''

from __future__ import print_function
import theano
from theano import tensor as T
import numpy as np

# We first define a Theano variable x to be a vector of 32-bit floats,
# and give it name ‘x’:
x = theano.tensor.fvector('x')

# Create a Theano variable W, assign its value to be vector [0.2, 0.7],
# and name it ‘W’:
W = theano.shared(np.asarray([0.2, 0.7]), 'W')

# Define y to be the sum of all elements in the element-wise multiplication of x and W:
y = (x * W).sum()

# Define a Theano function f, which takes as input x and outputs y:
f = theano.function([x], y)

# Call this function, giving as the argument vector [1.0, 1.0],
# essentially setting the value of variable x:
output = f([1.0, 1.0])

# The script prints out the summed product of [0.2, 0.7] and [1.0, 1.0], which is:
# 0.2*1.0 + 0.7*1.0 = 0.9
print("output:", output)
