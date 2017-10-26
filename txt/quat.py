#!/usr/bin/env python3
# Sprax Lines       2016.12.27
'''QUAT = Question Und Answer Tuple'''

from collections import namedtuple

Quat = namedtuple("Quat", "id question answer label")

def test():
    '''Test Quat, a 4-tuple: (id, label, question, answer)'''

    quat1 = Quat(1, 'salutation', "What's up?", "Nothing.")
    print("quat1: ", quat1)
    quat2 = Quat(2, 'indexical', "What's that?", "I don't know.")
    print("quat2: ", quat2)

if __name__ == '__main__':
    test()
