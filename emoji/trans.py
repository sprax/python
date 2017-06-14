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

def selflist(word):
    return [word]

def getsyl(map, word):
    syls = map.get(word)
    return sysl if syls else word

def trans():
    wtsl = defaultdict(selflist)
    sent = "wind and waves may rock the boat, but only you can tip the crew"
    words = re.split(r'\W+', sent.rstrip())
    print(words)
    for word in words:
        print("{} => {}".format(word, getsyl(wtsl, word)))


if __name__ == '__main__':
    trans()
    print(u'\U0001f604'.encode('unicode-escape'))
    print(u'\U0001f604')
