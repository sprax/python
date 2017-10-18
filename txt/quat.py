#!/usr/bin/env python3
# Sprax Lines       2016.12.27
'''Filter POS-tagged text'''

from collections import namedtuple

Quat = namedtuple("Quat", "id question answer label")

if __name__ == '__main__':
    quat1 = Quat(1, "What's up?", "Nothing.", 'salutation')
    print("quat1: ", quat1)
    quat2 = Quat(2, "What's that?", "I don't know.", 'indexical')
    print("quat2: ", quat2)
