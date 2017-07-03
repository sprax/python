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
import emoji
import re
import sys
from collections import defaultdict
import emotuples as ed
import emotrans as et
import sylcount as sylc
from nltk.corpus import cmudict


def qw(ss):
    return ss.split()

def qw_list(ss):
    return re.split(r'\W+', ss.rstrip())

def qw_tuple(ss):
    return tuple(qw_list(ss))

def SplitByUnicode():
    jokes = "That's a nice joke 😆😆😆 😛";
    print("Original String:", jokes);
    regexPattern = re.compile(r"[\uD83C-\uDBFF\uDC00-\uDFFF]+")
    # jokeb = string.getBytes("UTF-8");
    # jokeb = new String(utf8, "UTF-8");
    matchList = regexPattern.findall(jokes)
    print(matchList)

def gen_old_tuples():
    return ed.EmoTuples.emo_tuples

def gen_emo_tuples(emo_dict, limit=5000):
    for i, t in enumerate(sorted(jt.items(), key=lambda x: int(x[1]['order']))):
        if i > limit:
            break
        key, val, chk = t[0], t[1], unicode_chr_str(key)
        print("('%s', '%s', %d, %d, '%s', %s, '%s', [])," % (key, chk, int(val['order']), len(chk), val['shortname'], val['shortname_alternates'], val['category']))



EX = [ ('1f602',  7, 1, 1, '😂', ['joy', 'happy'], ':joy:', [], [], 'people') ,
       ('1f923',  8, 0, 1, '\U0001f923', ['rofl'], ':rofl:', [':rolling_on_the_floor_laughing:'], [], 'people') ,
       ( '263a',  9, 1, 1, '☺', ['relaxed', 'relax', 'chill'], ':relaxed:', [], [], 'people') , ]

def regen_emo_tuples(name='EMO_TUPLES', start=None, stop=None, step=None):
    cmu_prons = cmudict.dict() # get the CMU Pronouncing Dict
    print(name, "= [")
    if stop == 0:
        stop = None
    for t in ed.EMO_TUPLES[start:stop:step]:
        monos, polys = [], []   # Changed from: set(), set()
        for word in t[5]:
            if sylc.syl_count(cmu_prons, word) == 1:
                monos.add(word)
            else:
                polys.add(word)
        shorts = sylc.word_splits(t[6])
        for short in shorts:
            if sylc.syl_count(cmu_prons, short) == 1:
                monos.append(short)
            else:
                polys.append(short)
        # print("shorts: {}  monos: {}  polys: {}  alts: {}".format(shorts, monos, polys, t[7]))
        lst = list(t[0:4])
        lst.extend([et.unicode_chr_str(t[0]), list(monos), t[6], t[7], list(polys), t[9]])
        print("    {},".format(tuple(lst)))
    print("]")

def load_country_codes(cc_path='country_codes.txt'):
    '''
    Read country code table from file at cc_path into a dict
    Format of CC file: Name, 2-letter, 3-letter, phone-prefix
    '''
    with open(cc_path, 'r', encoding=charset) as text:
        cc_dict = {}
        for line in text:
            if len(line) > 8 and re.search('[a-z]', line):
                codes = re.split(r'\t', line.rstrip())
                # print(codes)
                cc_dict[codes[1]] = (codes[0], codes[2])
    return cc_dict

def reset_country_codes_to_emoflags(cc_path='country_codes.txt',
        irange=ed.FLAGS_RANGE, charset='utf-8'):
    '''
    Using a country code dict, set the name and syllable fields
    in a copy of emo_tuples.
    '''
    cmu_prons = cmudict.dict() # get the CMU Pronouncing Dict
    cc_dict = load_country_codes(cc_path)

    for tup in ed.EMO_TUPLES[irange.start:irange.stop]:
        cc2 = tup[ed.INDEX_ALTERNATIVES][0].strip(':').upper()
        # print(cc2, '  ', end='')
        monos, polys, names = [], [], [cc2]
        names.extend(nm for nm in tup[ed.INDEX_POLYSYLLABLES] if len(nm) > 2)
        try:
            names.extend(cc_dict[cc2])
            # print(names, file=sys.stderr)
        except KeyError:
            print("{} missing {}\n\tusing: {}".format(
                   cc2, tup, names), file=sys.stderr)
        for name in set(names):
            if sylc.syl_count(cmu_prons, name) == 1:
                monos.append(name)
            else:
                polys.append(name)
        tupal = list(tup)
        tupal[ed.INDEX_MONOSYLLABLES] = monos
        tupal[ed.INDEX_POLYSYLLABLES] = polys
        ret = tuple(tupal)
        print("    {},".format(ret), file=sys.stdout)
        # tupal[ed.INDEX_MONOSYLLABLES] =
    print()

def reflag_emo_tuples(start=None, stop=None, step=None):
    if stop == 0:
        stop = None
    print("reflagging ({}, {}, {})".format(start, stop, step))
    for tup in ed.EMO_TUPLES[start:stop:step]:
        if not tup[ed.INDEX_MONOSYLLABLES]:
            lst = list(tup)
            lst[ed.INDEX_FLAGS] = 0
            tup = tuple(lst)
        # print("{} => {}".format(lst[4], len(lst[4])))
        print("    {},".format(tup))

DICT_COLS = ('order', 'flags', 'len', 'chr', 'monosyls', 'shortname', 'alternates', 'polysyls', 'category')
COL_TO_IDX = dict([(v, i) for i, v in enumerate(DICT_COLS)])

def emo_value_col(value, column):
    return value[COL_TO_IDX(column)]

def emo_dict_col(emodict, key, column):
    return emo_value_col(emodict[key], column)

def gen_emo_dict(name='EMO_DICT', start=None, stop=None, step=None):
    print(name, "= {")
    for t in ed.EMO_TUPLES[start:stop:step]:
        print("    '%s' : %s," % (t[0], t[1:4] + (et.unicode_chr_str(t[0]),) + t[5:]))
    print("}")


def main():
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="generate some maps for english -> emoji translation")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-columns', action='store_true',
                        help='show column names')
    parser.add_argument('-country_codes', '-cc', action='store_true',
                        help='country codes regenerate tuples for flag icons')
    parser.add_argument('-start', '-beg', type=int, nargs='?', const=0, default=0,
                        help='starting index')
    parser.add_argument('-stop', '-end', type=int, nargs='?', const=0, default=0,
                        help='ending index')
    parser.add_argument('-step', '-inc', type=int, nargs='?', const=0, default=1,
                        help='index increment')
    parser.add_argument('-flags', action='store_true',
                        help='recompute the flag field in emo_tuples')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-regen', action='store_true',
                        help='regenerate emo_tuples')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    # gen_emo_dict('EMO_DICT', args.beg, args.end)

    if args.columns:
        print("columns:", sorted(COL_TO_IDX, key=COL_TO_IDX.get))
        for col, idx in sorted(COL_TO_IDX.items(), key=lambda x: x[1]):
            print("{}: {},  ".format(idx, col), end='')
        print()
    if args.country_codes:
        reset_country_codes_to_emoflags()
    if args.flags:
        reflag_emo_tuples(args.beg, args.end, args.inc)
    if args.regen:
        regen_emo_tuples('EMO_TUPLES', args.beg, args.end)

if __name__ == '__main__':
    main()
