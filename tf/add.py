'''
# To disable warning:
#   Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.2 AVX AVX2 FMA
'''
import os
import tensorflow as tf


def main():
    '''Add two numbers in TF'''

    # suppress sub-optimal build warning:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # build computational graph
    v_a = tf.placeholder(tf.int16)
    v_b = tf.placeholder(tf.int16)
    addition = tf.add(v_a, v_b)

    # initialize variables
    # init = tf.initialize_all_variables()
    init = tf.global_variables_initializer()

    # create session and run the graph
    with tf.Session() as sess:
        sess.run(init)
        ans = sess.run(addition, feed_dict={v_a: 2, v_b: 3})
        print("Addition:", ans)


if __name__ == '__main__':
    main()
