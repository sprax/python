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
from functools import partial

import emoji
import emotuples
import text_fio
import text_regex
# import sylcount

SENTENCES = [
    # "Wind and waves may rock the boat, but only you can tip the crew.",
    # "I love you",
    "So it's the US vs. Canada in football, I mean soccer!?",
    "Lady Astor: “Winston, if I were your wife I’d put poison in your coffee.",
    "Winston Churchill: “Nancy, if I were your husband I’d drink it.",
    "I'm 100% sure <3 ain't a 4-letter word, even on Rhys' say-so?!",
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

EMO_SYNONYMS = {}

def emo_synonyms(word):
    try:
        return EMO_SYNONYMS[word]
    except KeyError:
        return [word]

def emojize_token(txt_to_emo, word, verbose):
    '''return emoji string translation of word or None
    TODO: make protected ?'''
    lst = txt_to_emo[word]
    num = len(lst)
    if num < 1:
        lst = txt_to_emo[word.lower()]
        num = len(lst)
    if num >= 1:
        if verbose > 3:
            print("word subs: {} => {}".format(word, lst))
        return random.choice(lst) + ' '
    elif verbose > 4:
        print("word self: {}".format(word))
    return None

def emojize_word(txt_to_emo, src_word, verbose):
    words = emo_synonyms(src_word)
    for word in words:
        emojis = emojize_token(txt_to_emo, word, verbose)
        if emojis:
            return emojis
    return src_word

def emojize_match(txt_to_emo, match_obj, verbose=1):
    word = match_obj.group()
    return emojize_word(txt_to_emo, word, verbose)

def emojize_sentence_subs(txt_to_emo, sentence, verbose):
    beg, body, end = text_regex.sentence_body_and_end(sentence)
    if verbose > 2:
        print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))

    emojize_match_bound = partial(emojize_match, txt_to_emo, verbose=verbose)
    subs = text_regex.replace_words_extended(emojize_match_bound, body)
    tend = emojize_token(txt_to_emo, end, verbose)
    if tend:
        end = tend
    emo_tran = ''.join([beg, subs, end])
    if verbose > 3:
        print("    %s ==>\n    %s\n" % (sentence, emo_tran))
    return emo_tran

def emojize_phrase(txt_to_emo, txt_phrase, verbose):
    # srcs = re.split('\W+', txt_phrase.strip())
    srcs = text_regex.word_splits(txt_phrase.strip())
    if verbose > 2:
        print(srcs)
    emo_phrase = []
    for raw in srcs:
        dst = emojize_word(txt_to_emo, raw, verbose)
        emo_phrase.append(dst)
    return emo_phrase

def emojize_sentence_split_join(txt_to_emo, sentence, verbose):
    beg, body, end = text_regex.sentence_body_and_end(sentence)
    if verbose > 2:
        print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))
    emo_list = emojize_phrase(txt_to_emo, body, verbose)
    emo_join = ' '.join(emo_list)
    emo_tran = ''.join([beg, emo_join, end])
    if verbose:
        print("    %s ==>\n    %s\n" % (sentence, emo_tran))
    return emo_tran

def textize_sentence_subs(emo_to_txt, emo_sent, verbose):
    '''
    return text with each emoji replaced by a value from emo_to_txt.
    FIXME: emoji combinations representing a single word will not translate
    back to the orignal word, but turn into a word combination calc, which
    may be gibberish or worse.
    '''
    txt_sent = ''
    for uchr in emo_sent:
        try:
            txt_sent += random.choice(list(emo_to_txt[uchr]))
        except:
            txt_sent += uchr
    return txt_sent

def add_preset_multiples(preset_dict):
    preset_dict.update({
        'crew': ['👦 👲🏽 👧🏿 👨 👦🏽'],
        'husband': ['💑 👈', '💏 👈', '👩❤👨 ⬅'],
        'wife': ['👉 💑', '👉 💏', '➡ 👩❤👨'],
    })

def gen_txt_to_emo(presets, verbose):
    txt_to_emo = defaultdict(list, presets)
    i_flags = emotuples.INDEX_DISPLAY_FLAGS
    i_monos = emotuples.INDEX_MONOSYLLABLES
    i_polys = emotuples.INDEX_POLYSYLLABLES
    i_unchr = emotuples.INDEX_EMOJI_UNICHRS
    usables = [tup for tup in emotuples.EMO_TUPLES if tup[i_flags] > 0]
    print("Found {} usable emotuples.".format(len(usables)))
    for tt in usables:
        for src in tt[i_monos]:
            txt_to_emo[src].append(tt[i_unchr])
            # print("src(%s) => emo(%s)" % (src, tt[1]))
        for src in tt[i_polys]:
            txt_to_emo[src].append(tt[i_unchr])
            # print("src(%s) => emo( %s )" % (src, tt[i_unchr]))
        if verbose > 1:
            print(tt[i_unchr], end='  ')
    print()
    return txt_to_emo

def gen_emo_to_txt(txt_to_emo, verbose):
    '''reverse of gen_txt_to_emo: map each emoji to a list of word-phrases'''
    emo_to_txt = defaultdict(set)
    for txt, lst in txt_to_emo.items():
        # print("emo_to_txt 1: {} => {}".format(txt, lst))
        for emo in lst:
            emo_to_txt[emo].add(txt)
            if verbose > 3:
                print("emo_to_txt 3: {} => {}".format(emo, txt))
    return emo_to_txt



def test_emo_tuples(options):
    presets = {}
    if options.no_articles:
        presets.update({'a': [''], 'but': [''], 'may': [''], 'the': ['']})
    if options.arithmetic:
        presets.update({'can': ['🍬 ➖ D'], 'crew': ['© ➕ 🍺 ➖ 🐝'], 'you': ['🆕 ➖ N']})
    if options.multiple:
        add_preset_multiples(presets)

    txt_to_emo = gen_txt_to_emo(presets, options.verbose)
    emo_to_txt = gen_emo_to_txt(txt_to_emo, options.verbose)

    for sentence in SENTENCES:
        print("src => txt (%s)" % sentence)
        emo_sent = emojize_sentence_subs(txt_to_emo, sentence, options.verbose)
        print("txt => emo (%s)" % emo_sent)
        txt_sent = textize_sentence_subs(emo_to_txt, emo_sent, options.verbose)
        print("emo => txt (%s)" % txt_sent)
        print()
    if options.text_file:
        for sentence in text_fio.read_text_lines(options.text_file, options.charset):
            emojize_sentence_subs(txt_to_emo, sentence, options.verbose)

def test_emojize():
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
    test_emojize()
