#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plan:
    Words|phrases -> words >= [phonetic syllables reprs]
    Emojis >= [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import emoji
import re
from collections import defaultdict
import emotuples as ed
import emotrans as et

def gen_emo_tuples():
    old_emos = ed.EmoTuples.emo_tuples

def regen_emo_tuples():
    for t in ed.EMO_TUPLES[4:8]:
        print(tuple([t[0], t[2], 1, t[3], et.unicode_chr_str(t[0]), t[7], t[4], t[5], [], t[6]]))

if __name__ == '__main__':
    regen_emo_tuples()
