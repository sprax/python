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
import string
from collections import defaultdict

import emoji
import emotuples

EXAMPLES = {
    "There isn't one empyrean ouroborous; everyone knows there've always been several" : 24,
    #  1   2  3  4   5  6 78   9 0 1  2   3 4* 5     6     7  8   9  0    1    2 3 4
    '"Ain\'t all y\'all young\'uns under 17," she\'d said, "like 11- or 15-years old?!"' : 21,
    #  1     2      3    4     5   6  7  +3     1     2      3   +3  7  +2  0    1}
}

def qw(ss):
    return ss.split()

VOWEL_GROUPS = qw('a ae ai ay e ea ei eu ey i ie iou o oa oi ou oy u')
WORD_SEP_CHARACTERS = r'!"#$%&()*+,./:;<=>?@[\]^_`{|}~\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99'
WORD_SEP_BOUNDARIES = r"'-"

REGEX_WORD_SEP = r"(?:\s+['-]+\s*|\s*['-]+\s+|[\s{}]+|\s+)".format(WORD_SEP_CHARACTERS)

REGEX_PUNCTUATION = re.compile("[{}]".format(string.punctuation))
REGEX_NON_ALPHA = re.compile(r'(?:\W|[0-9])+')

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


def gen_emo_tuples(emo_dict, limit=5000):
    for i, t in enumerate(sorted(jt.items(), key=lambda x: int(x[1]['order']))):
        if i > limit:
            break
        key, val, chk = t[0], t[1], unicode_chr_str(key)
        print("('%s', '%s', %d, %d, '%s', %s, '%s', [])," % (key, chk, int(val['order']), len(chk), val['shortname'], val['shortname_alternates'], val['category']))


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
        presets.update({'can': ['🍬 ➖ D']})
    src_to_emo = defaultdict(list, presets)
    i_monosyllables = emotuples.INDEX_MONOSYLLABLES
    i_unichr = emotuples.INDEX_EMOJI_UNICHRS
    for tt in emotuples.EMO_TUPLES:
        for src in tt[i_monosyllables]:
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
    print('VOWEL_GROUPS:\n', VOWEL_GROUPS)

if __name__ == '__main__':
    test_it()
