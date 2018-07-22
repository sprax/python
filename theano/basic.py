#!/usr/bin/env python3
''' regression.py: LINEAR REGRESSION using Theano -- tests installation
    From http://www.marekrei.com/blog/theano-tutorial/
    Written for: anaconda python 3.5; conda install theano=1.0.2
'''

from __future__ import print_function
import numpy as np
import theano
# from theano import tensor as T

def basic_theano():
    '''Theano variabls, function def, and function call'''

    # We first define a Theano variable x_vec to be a vector of 32-bit floats,
    # and give it name ‘x_vec’:
    x_vec = theano.tensor.fvector('x_vec')
    print("x_vec of type:", type(x_vec), x_vec)

    # Create a Theano variable w_tsv, assign its value to be vector [0.2, 0.7],
    # and name it ‘w_tsv’:
    w_tsv = theano.shared(np.asarray([0.2, 0.7]), 'w_tsv')
    print("w_tsv of type:", type(w_tsv), w_tsv)

    # Define y_sum to be the sum of all elements in the element-wise multiplication of x_vec and w_tsv:
    y_sum = (x_vec * w_tsv).sum()
    print("y_sum = (x_vec * w_tsv).sum(), of type:", type(y_sum), y_sum)

    # Define a Theano function x_dot_w_func, which takes as input x_vec and outputs y_sum:
    x_dot_w_func = theano.function([x_vec], y_sum)
    print("x_dot_w_func of type:", type(x_dot_w_func), x_dot_w_func)

    # Call this function, giving as the argument vector [1.0, 1.0],
    # essentially setting the value of variable x_vec:
    output = x_dot_w_func([1.0, 1.0])
    print("output = x_dot_w_func([1.0, 1.0]), of type:", type(output), output)

    # The script prints out the summed product of [0.2, 0.7] and [1.0, 1.0], which is:
    # 0.2*1.0 + 0.7*1.0 = 0.9
    print("output:", output)


basic_theano()
