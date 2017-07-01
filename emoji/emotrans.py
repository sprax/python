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
import text_fio
import sylcount

SENTENCES = [
    # "Wind and waves may rock the boat, but only you can tip the crew.",
    # "I love you",
    "It's the US vs. Canada in football, I mean soccer.",
    "Lady Astor: “Winston, if I were your wife I’d put poison in your coffee.",
    "Winston Churchill: “Nancy, if I were your husband I’d drink it.",
    # "When the eagles are silent, the parrots begin to jabber.",
    # "If you have an important point to make, don’t try to be subtle or clever. Use a pile driver. Hit the point once. Then come back and hit it again. Then hit it a third time -- a tremendous whack.",
    # "Success consists of going from failure to failure without loss of enthusiasm.",
    # "Character may be manifested in the great moments, but it is made in the small ones.",
    # "Men occasionally stumble over the truth, but most of them pick themselves up and hurry off as if nothing has happened.",
]

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
    sent = SENTENCES[0]
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


def emojize(src_to_emo, txt_phrase, verbose):
    # srcs = re.split('\W+', txt_phrase.strip())
    srcs = sylcount.word_splits(txt_phrase.strip())
    if verbose > 2:
        print(srcs)
    emo_phrase = []
    for raw in srcs:
        lst = src_to_emo[raw]
        num = len(lst)
        if num < 1:
            lst = src_to_emo[raw.lower()]
            num = len(lst)
        if num > 1:
            dst = random.choice(lst)
        elif num == 1:
            dst = lst[0]
        else:
            dst = raw
        emo_phrase.append(dst)
    return emo_phrase

def emojize_sentence(src_to_emo, sentence, verbose):
    beg, body, end = sylcount.sentence_body_and_end(sentence)
    if verbose > 2:
        print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))
    emo_list = emojize(src_to_emo, body, verbose)
    emo_join = ' '.join(emo_list)
    emo_tran = ''.join([beg, emo_join, end])
    if verbose:
        print("    %s ==>\n    %s\n" % (sentence, emo_tran))
    return emo_tran

def test_emo_tuples(options):
    presets = {}
    if options.no_articles:
        presets.update({'a': [''], 'but': [''], 'may': [''], 'the': ['']})
    if options.arithmetic:
        presets.update({'can': ['🍬 ➖ D'], 'crew': ['© ➕ 🍺 ➖ 🐝'], 'you': ['🆕 ➖ N']})
    if options.multiple:
        presets.update({'crew': ['👦 👲🏽 👧🏿 👨 👦🏽']})

    src_to_emo = defaultdict(list, presets)
    i_monos = emotuples.INDEX_MONOSYLLABLES
    i_polys = emotuples.INDEX_POLYSYLLABLES
    i_unchr = emotuples.INDEX_EMOJI_UNICHRS
    i_flags = emotuples.INDEX_FLAGS
    usables = [tup for tup in emotuples.EMO_TUPLES if tup[i_flags] > 0]
    print("Found {} usable emotuples.".format(len(usables)))
    for tt in usables:
        for src in tt[i_monos]:
            src_to_emo[src].append(tt[i_unchr])
            # print("src(%s) => emo(%s)" % (src, tt[1]))
        for src in tt[i_polys]:
            src_to_emo[src].append(tt[i_unchr])
            # print("src(%s) => emo( %s )" % (src, tt[i_unchr]))
        if options.usable:
            print(tt[i_unchr], end='  ')
    print()
    for sentence in SENTENCES:
        emojize_sentence(src_to_emo, sentence, options.verbose)
    if options.text_file:
        for sentence in text_fio.read_text_lines(options.text_file, options.charset):
            emojize_sentence(src_to_emo, sentence, options.verbose)

def test_it():
    '''test english -> emoji translation'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('-arithmetic', action='store_true',
                        help='use addition and subtraction of letters or syllables (rebus)')
    parser.add_argument('-directory', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input files')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-flags', action='store_true',
                        help='use flag emojis in translations of words not representing countries')
    parser.add_argument('-multiple', action='store_true',
                        help='use multiple emoji for plural nouns')
    parser.add_argument('-no_articles', '-noa', action='store_true',
                        help='remove articles (a, an, the)')
    parser.add_argument('-number', dest='max_lines', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 0 = all)')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-text_file', dest='text_file', type=str, nargs='?',
                        const='quotations.txt', default=None,
                        help='translate sentences from this text_file')
    parser.add_argument('-usable', action='store_true',
                        help='show all usable emoji under current options')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    # test_misc()
    test_emo_tuples(args)

if __name__ == '__main__':
    test_it()
