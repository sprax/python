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

import argparse
import json
import random
import re
from collections import defaultdict

import emoji
import emotuples

WAW = "wind and waves may rock the boat, but only you can tip the crew"


def is_emoji(uchar):
  return uchar in emoji.UNICODE_EMOJI

def extract_emojis(str):
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)


def test_load():
    emodict = json.loads(open('../../emodict.json').read())
    for i, t in enumerate(sorted(emodict.items(), key=lambda x: int(x[1]['order']), reverse=True)):
        if i > 5:
            break
        ck = unicode_chr_str(t[0])
        print(ck, "\t", len(ck), "\t", t[1]['order'], "\t", t[0], "\t", t[1]['shortname'])

def selflist(word):
    return [word]

def getsyl(map, word):
    syls = map.get(word)
    return sysl if syls else word

def trans():
    wtsl = defaultdict(selflist)
    sent = WAW
    words = re.split(r'\W+', sent.rstrip())
    print(words)
    for word in words:
        print("{} => {}".format(word, getsyl(wtsl, word)))

def char(i):
    try:
        return chr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')

def unicode_chr_str(hex_unicode):
    if '-' not in hex_unicode:
        return char(int(hex_unicode, 16))
    parts = hex_unicode.split('-')
    return ''.join(char(int(x, 16)) for x in parts)

def qw(ss):
    return ss.split()

def qw_list(ss):
    return re.split(r'\W+', ss.rstrip())

def qw_tuple(ss):
    return tuple(qw_list(ss))

def test_misc():
    trans()
    print(u'\U0001f604'.encode('unicode-escape'))
    print(u'\U0001f604')
    ss = u'\U0001f604'
    xx = chr(ss[0])
    print("ss({}) xx({})".format(ss, xx))
    # -*- coding: UTF-8 -*-
    #convert to unicode
    teststring =  "I am happy \U0001f604"
    # #teststring = unicode(teststring, 'utf-8')

    #encode it with string escape
    teststring = teststring.encode('unicode_escape')
    print("💗 Growing Heart")
    print(emoji.emojize('Water! :water_wave:'))
    print(emoji.demojize(u'🌊')) # for Python 2.x
# print(emoji.demojize('🌊')) # for Python 3.x.
    print(u"And \U0001F60D")
    print("(-woman) astronaut", chr(int("0001f680", 16)))
    print("woman_astronaut", chr(int("0x0001f680", 0)))

    print("\U0001f483\U0001f3fe")

    print(chr(0x001f483),chr(0x001f3fe))
    print('💃 🏾 ')
    print(chr(0x001f483)+chr(0x001f3fe))
    print('💃🏾 ')
    print(chr(int('1f483',16))+chr(int('1f3fe',16)))
    print('%8s %8s %8s' % qw_tuple('surf wave whitecap'))
    print("('%s', '%s', '%s')" % qw_tuple("surf's-up wave rip-curl"))



class EmoTuples:
    def __init__(self):
        self.emo_tuples = EMO_TUPLES



def emojize(src_to_emo, txt_phrase):
    srcs = re.split(r'\W+', txt_phrase.rstrip())
    emo_phrase = []
    for src in srcs:
        lst = src_to_emo[src]
        num = len(lst)
        if num > 1:
            dst = random.choice(lst)
        elif num == 1:
            dst = lst[0]
        else:
            dst = src
        emo_phrase.append(dst)
    return emo_phrase

def test_emo_tuples(options):
    presets = {}
    if options.no_articles:
        presets.update({'a': [''], 'but': [''], 'may': [''], 'the': ['']})
    if options.subtraction:
        presets.update({'can': ['🍬 ➖ D'], 'crew': ['© ➕ 🍺 ➖ 🐝']})
    src_to_emo = defaultdict(list, presets)
    i_monos = emotuples.INDEX_MONOSYLLABLES
    i_unichr = emotuples.INDEX_EMOJI_UNICHRS
    i_flags = emotuples.INDEX_FLAGS
    usables = [tup for tup in emotuples.EMO_TUPLES if tup[i_flags] > 0]
    print("Found {} usable emotuples.".format(len(usables)))
    for tt in usables:
        for src in tt[i_monos]:
            # print("type src is: ", type(src), "and uni:", tt[0])
            src_to_emo[src].append(tt[i_unichr])
            # print("src(%s) => emo(%s)" % (src, tt[1]))
    txt_phrase = WAW
    emo_list = emojize(src_to_emo, txt_phrase)
    emo_phrase = ' '.join(emo_list)
    print("    %s ==>\n    %s" % (txt_phrase, emo_phrase))

def test_it():
    '''test english -> emoji translation'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input_file')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-flags', action='store_true',
                        help='use flag emojis for country abbreviations')
    parser.add_argument('-no_articles', action='store_true',
                        help='replace articles (a, an, the) with nothing')
    parser.add_argument('-subtraction', action='store_true',
                        help='allow subtraction of letters or syllables')
    parser.add_argument('-number', dest='max_lines', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-truncate', dest='max_words', type=int, nargs='?',
                        const=8, default=0,
                        help='truncate sentences after MAX words (default: INT_MAX)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    # test_misc()
    test_emo_tuples(args)

if __name__ == '__main__':
    test_it()
