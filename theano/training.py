#!/usr/bin/env python3
''' regression.py: LINEAR REGRESSION using Theano -- tests installation
    From http://www.marekrei.com/blog/theano-tutorial/
    Written for: anaconda python 3.5; conda install theano=1.0.2
'''

from __future__ import print_function
import numpy as np
import theano
# from theano import tensor as T

def train_theano():
    '''Theano variables, function def, and function call'''

    # We first define a Theano variable x_vec to be a vector of 32-bit floats,
    # and give it name ‘x_vec’:
    x_vec = theano.tensor.fvector('x_vec')
    print("x_vec of type:", type(x_vec), x_vec)

    # We create a second input variable called target, which will act as
    # the target value we use for training:
    target = theano.tensor.fscalar('target')
    print("target of type:", type(target), target)

    # Create a Theano variable w_tsv, assign its value to be vector [0.2, 0.7],
    # and name it ‘w_tsv’:
    w_tsv = theano.shared(np.asarray([0.2, 0.7]), 'w_tsv')
    print("w_tsv of type:", type(w_tsv), w_tsv)

    # Define y_sum to be the sum of all elements in the element-wise multiplication of x_vec and w_tsv:
    y_sum = (x_vec * w_tsv).sum()
    print("y_sum = (x_vec * w_tsv).sum(), of type:", type(y_sum), y_sum)

    # In order to train the model, we need a cost function.
    # Here we use a simple squared distance from the target:
    cost = theano.tensor.sqr(target - y_sum)
    print("cost of type:", type(cost), cost)

    # Next, we want to calculate the partial gradients for the parameters
    # that will be updated, with respect to the cost function. Luckily,
    # Theano will do that for us. We simply call the grad function, pass
    # in the real-valued cost and a list of all the variables we want gradients
    # for, and it will return a list of those gradients:
    gradients = theano.tensor.grad(cost, [w_tsv])
    print("gradients of type:", type(gradients), gradients)

    # Now let’s define a symbolic variable for what the updated version of the
    # parameters will look like. Using gradient descent, the update rule is to
    # subtract the gradient, multiplied by the learning rate:
    W_updated = w_tsv - (0.1 * gradients[0])
    W_updated = w_tsv - (0.1 * gradients[0])
    print("W_updated of type:", type(W_updated), W_updated)

    # Create a list of updates. More specifically, a list of tuples
    # where the first element is the variable we want to update, and
    # the second element is a variable containing the values that we
    # want the first variable to contain after the update.
    # This is just a syntax that Theano requires.
    updates = [(w_tsv, W_updated)]
    print("updates of type:", type(updates), updates)



    # Define a Theano function again, with a couple of changes:
    # It now takes two input arguments – one for the input vector,
    # and another for the target value used for training.
    # And the list of updates also gets attached to the function as well.
    # Every time this function is called, we pass in values for x and target,
    # get back the value for y as output, and Theano performs all the updates in the update list.
    f = theano.function([x_vec, target], y_sum, updates=updates)

    # In order to train the parameters, we repeatedly call this function
    # (10 times in this case). Normally, we’d pass in different examples
    # from our training data, but for this example we use the same x=[1.0, 1.0]
    # and target=20 each time:

    for i in range(10):
        output = f([1.0, 1.0], 20.0)
        print("output:", output)


train_theano()


################################################################################################




''' When the script is executed, the output looks like this:
1
2
3
4
5
6
7
8
9
10
0.9
8.54
13.124
15.8744
17.52464
18.514784
19.1088704
19.46532224
19.679193344
19.8075160064
'''
