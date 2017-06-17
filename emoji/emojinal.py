#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-
'''
Plan:
    Words|phrases -> words >= [phonetic syllables reprs]
    Emojis >= [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import emoji
import re
from collections import defaultdict


    aa = ['??', '??', '??', '??', '??', '??']

:sunny:
:umbrella:
:cloud:
:snowflake:
:snowman:
:zap:
:cyclone:
:foggy:
:ocean:

def extract_emojis(str):
    return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)


a_str = '?? ?? me as�, bla es se ?? ds ??????'

emojis = extract_emojis(a_str)
print("emojis: ", emojis)

a_list = ['?? ?? me as�, bla es se ?? ds ??????']

# is_emoji("??") #True
# is_emoji("????") #False

re.findall(r'[^\w\s,]', a_list[0])
