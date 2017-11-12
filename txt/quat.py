#!/usr/bin/env python3
# Sprax Lines       2016.12.27
'''QUAT = Question Und Answer Tuple'''

from collections import namedtuple

class Quat(namedtuple("Quat", "id label question answer")):
    '''Minimal class for counted and labeled QA, based on namedtuple.'''
    __slots__ = ()
    def __str__(self):
        return "%s  %s  %s  %s" % (self.id, self.label, self.question, self.answer)

def smoke_test():
    '''Test Quat, a 4-tuple: (id, label, question, answer)'''

    quat1 = Quat(1, 'salutation', "What's up?", "Nothing.")
    print("quat1: ", quat1)
    quat2 = Quat(2, 'indexical', "What's that?", "I don't know.")
    print("quat2: ", quat2)

if __name__ == '__main__':
    smoke_test()
