
#!/usr/bin/env python
'''
@file: unpack_scoops.py
Load binary scoop data that was serialized and saved to file using
ScoopIo (in scoop_io.cc).  Deserialize the binary data into Python
variables using struct.unpack.  The data formats used for decoding
are human-written, not machine-generated, so maintenance needs care.
The difference between this unpacker and the one in dexai-python is
that this one verifies byte format; that one simply assumes it's all good.

Written for Python 2.7.15

NOTE: @see also https://github.com/DexaiRobotics/dexai-python/blob/master/dexai/unpack_scoops.py
'''
from __future__ import print_function
import argparse
from collections import namedtuple
# import pdb
# from pdb import set_trace
from inspect import getsourcefile
import os
import os.path
import struct
import sys

import fileinput

beg, end = 0, 1
total_size = 0
lines = []
for line in fileinput.input():
    tokens = line.split()
    if len(tokens) > end:
        try:
            size = int(tokens[beg])
            name = tokens[end]
            total_size += size
            lines.append([size, name])
        except ValueError:
            break   # lines.append([line])

print("%12s %7s  % 7s" % ("AUTHOR", "Count", "Percent"))
for tokens in lines:
    if len(tokens) > 1:
        size, name = tokens[0:2]
        percent = size * 100 / total_size
        print("%12s %7d  % 7.1f" % (name, size, percent))
    else:
        print(tokens[0])
print("%12s %7d  % 7.1f" % ("TOTALS", total_size, 100.0))
