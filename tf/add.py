'''
# To disable warning:
#   Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.2 AVX AVX2 FMA
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
'''
'''
# import tensorflow
import tensorflow as tf


# build computational graph
a = tf.placeholder(tf.int16)
b = tf.placeholder(tf.int16)

addition = tf.add(a, b)

# initialize variables
# init = tf.initialize_all_variables()
init = tf.global_variables_initializer()

# create session and run the graph
with tf.Session() as sess:
    sess.run(init)
    print("Addition: %i" % sess.run(addition, feed_dict={a: 2, b: 3}))

# close session
sess.close()