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

EX = [ ('1f602',  7, 1, 1, '😂', ['joy', 'happy'], ':joy:', [], [], 'people') ,
       ('1f923',  8, 0, 1, '\U0001f923', ['rofl'], ':rofl:', [':rolling_on_the_floor_laughing:'], [], 'people') ,
       ( '263a',  9, 1, 1, '☺', ['relaxed', 'relax', 'chill'], ':relaxed:', [], [], 'people') , ]

def regen_emo_tuples(start=None, stop=None, incr=None):
    for t in ed.EMO_TUPLES[start:stop:incr]:
        print(t[0:4] + (et.unicode_chr_str(t[0]),) + t[5:])

DICT_COLS = ('order', 'flags', 'len', 'chr', 'monosyls', 'shortname', 'alternates', 'polysyls', 'category')
COL_TO_IDX = dict([(v, i) for i, v in enumerate(DICT_COLS)])

def emo_value_col(value, column):
    return value[COL_TO_IDX(column)]

def emo_dict_col(emodict, key, column):
    return emo_value_col(emodict[key], column)

def gen_emo_dict(name='EMO_DICT', start=None, stop=None, incr=None):
    print(name, "= {")
    for t in ed.EMO_TUPLES[start:stop:incr]:
        print("    '%s' : %s," % (t[0], t[1:4] + (et.unicode_chr_str(t[0]),) + t[5:]))
    print("}")

if __name__ == '__main__':
    gen_emo_dict('EMO_DICT', 6, 9)
    print("col_to_idx:", COL_TO_IDX)
