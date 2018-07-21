#!/usr/bin/env python3
''' regression.py: LINEAR REGRESSION using Theano -- tests installation
    From https://github.com/Newmu/Theano-Tutorials/blob/master/1_linear_regression.py
    Written for: anaconda python 3.5; conda install theano=1.0.2
'''

from __future__ import print_function
import theano
from theano import tensor as T
import numpy as np

trX = np.linspace(-1, 1, 101)
trY = 2 * trX + np.random.randn(*trX.shape) * 0.33

X = T.scalar()
Y = T.scalar()

def model(X, w):
    return X * w

w = theano.shared(np.asarray(0., dtype=theano.config.floatX))
y = model(X, w)

cost = T.mean(T.sqr(y - Y))
gradient = T.grad(cost=cost, wrt=w)
updates = [[w, w - gradient * 0.01]]

train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)

for i in range(100):
    for x, y in zip(trX, trY):
        train(x, y)

print(w.get_value())
# something around 2
