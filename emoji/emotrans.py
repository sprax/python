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
import emotuples as ET
import text_fio
import text_regex
# import sylcount

SENTENCES = [
    # "Wind and waves may rock the boat, but only you can tip the crew.",
    # "I love you",
    "So it's the US vs. Canada in football, I mean soccer!?",
    # "Lady Astor: “Winston, if I were your wife I’d put poison in your coffee.",
    # "Winston Churchill: “Nancy, if I were your husband I’d drink it.",
    # "I'm 100% sure <3 ain't a 4-letter word, even on Rhys' say-so?!",
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

def show_sorted_dict(dct, idx, lbl=''):
    for key, val in sorted(dct.items(), key=lambda dit: dit[idx].lower()):
        print("{} {} => {}".format(lbl, key, val))


class EmoTrans:
    def __init__(self, options):
        self.options = options
        self.verbose = options.verbose
        self.usables = self.gen_usables(ET.INDEX_DISPLAY_FLAGS)
        self.presets = self.gen_presets(options)
        self.txt_to_emo = self.gen_txt_to_emo(self.presets)
        self.emo_to_txt = self.gen_emo_to_txt()

    def gen_usables(self, i_flags):
        tmp = [tup for tup in ET.EMO_TUPLES if tup[i_flags] > 0]
        if self.verbose:
            print("Found %d usable emoji tuples." % len(tmp))
        return tmp

    def gen_presets(self, options):
        presets = {}
        if options.no_articles:
            presets.update({'a': [''], 'but': [''], 'may': [''], 'the': ['']})
        if options.arithmetic:
            presets.update({'can': ['🍬 ➖ D'], 'crew': ['© ➕ 🍺 ➖ 🐝'], 'you': ['🆕 ➖ N']})
        if options.multiple:
            add_preset_multiples(presets)
        return presets

    def gen_txt_to_emo(self, presets):
        '''generate text to emoji mapping'''
        txt_to_emo = defaultdict(list, presets)
        i_flags = ET.INDEX_DISPLAY_FLAGS
        i_monos = ET.INDEX_WORDSYLLABLES
        i_words = ET.INDEX_FREQUENT_WORDS
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        for tt in self.usables:
            for src in tt[i_words]:
                txt_to_emo[src].append(tt[i_unchr])
                # print("src(%s) => emo( %s )" % (src, tt[i_unchr]))
            if self.verbose > 4:
                print(tt[i_unchr], end='  ')
        if self.verbose > 4:
            print()
        return txt_to_emo

    def gen_emo_to_txt(self):
        '''generate emoji to texts mapping'''
        emo_to_txt = defaultdict(list)
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        i_words = ET.INDEX_FREQUENT_WORDS
        for tt in self.usables:
            emo_to_txt[tt[i_unchr]] = tt[i_words]
        return emo_to_txt

    def rev_txt_to_gen(self, verbose):
        '''reverse of gen_txt_to_emo: map each emoji to a list of word-phrases'''
        emo_to_txt = defaultdict(list)
        for txt, lst in sorted(self.txt_to_emo.items()):
            # print("emo_to_txt 1: {} => {}".format(txt, lst))
            for emo in lst:
                emo_to_txt[emo].append(txt)
                if verbose > 1:
                    print("emo_to_txt 3: {} => {}".format(emo, txt))
        return emo_to_txt

    def emojize_token(self, word, verbose):
        '''return emoji string translation of word or None
        TODO: make protected ?'''
        lst = self.txt_to_emo[word]
        num = len(lst)
        if num < 1:
            lst = self.txt_to_emo[word.lower()]
            num = len(lst)
        if num >= 1:
            if verbose > 3:
                print("word subs: {} => {}".format(word, lst))
            return random.choice(lst)
        elif verbose > 4:
            print("word self: {}".format(word))
        return None

    def emojize_word(self, src_word, space=' ', verbose=1):
        words = emo_synonyms(src_word)
        for word in words:
            emojis = self.emojize_token(word, verbose)
            if emojis:
                return emojis + space
        return src_word

    def emojize_match(self, match_obj, space=' ', verbose=1):
        word = match_obj.group()
        return self.emojize_word(word, space, verbose)

    def emojize_sentence_subs(self, sentence, verbose):
        beg, body, end = text_regex.sentence_body_and_end(sentence)
        if verbose > 2:
            print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))

        emojize_match_bound = partial(self.emojize_match, space=' ', verbose=verbose)
        subs = text_regex.replace_words_extended(emojize_match_bound, body)
        tend = self.emojize_token(end, verbose)
        if tend:
            end = ' ' + tend
        emo_tran = ''.join([beg, subs, end])
        return emo_tran

    def emojize_phrase(self, txt_phrase, verbose):
        # srcs = re.split('\W+', txt_phrase.strip())
        srcs = text_regex.word_splits(txt_phrase.strip())
        if verbose > 2:
            print(srcs)
        emo_phrase = []
        for raw in srcs:
            dst = self.emojize_word(raw, verbose)
            emo_phrase.append(dst)
        return emo_phrase

    def emojize_sentence_split_join(self, sentence, verbose):
        beg, body, end = text_regex.sentence_body_and_end(sentence)
        if verbose > 2:
            print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))
        emo_list = self.emojize_phrase(txt_to_emo, body, verbose)
        emo_join = ' '.join(emo_list)
        emo_tran = ''.join([beg, emo_join, end])
        if verbose:
            print("    %s ==>\n    %s\n" % (sentence, emo_tran))
        return emo_tran

    def textize_emo_span(self, span, verbose):
        '''translate a string or slice of emoji into a text string'''
        if verbose > 2:
            print("TES: span({})".format(span))
        text = ''
        prev = False
        for uchr in span:
            try:
                lst = self.emo_to_txt[uchr]
                if verbose > 1:
                    print("TES: {} => {}".format(uchr, lst))
                text += lst[0]  # random.choice(lst)
                prev = True
            except KeyError:
                if prev and uchr == ' ':
                    prev = False
                else:
                    text += uchr
        return text

    def is_emoji_chr(self, uchr):
        '''FIXME: optimize?  use RE?'''
        lst = self.emo_to_txt[uchr]
        if len(lst) > 0:
            return True
        return False

    def textize_sentence_subs(self, emo_sent, verbose):
        '''
        return text with each emoji replaced by a value from emo_to_txt.
        FIXME: emoji combinations representing a single word will not translate
        back to the orignal word, but turn into a word combination calc, which
        may be gibberish or worse.
        '''
        txt_sent, span = '', ''
        for uchr in emo_sent:
            if self.is_emoji_chr(uchr):
                span += uchr
            elif span:
                txt_sent += self.textize_emo_span(span, verbose)
                span = ''
                if uchr != ' ':
                    txt_sent += uchr
            else:
                txt_sent += uchr
        if span:
            txt_sent += self.textize_emo_span(span, verbose)
        return txt_sent

def add_preset_multiples(preset_dict):
    preset_dict.update({
        'crew': ['👦 👲🏽 👧🏿 👨 👦🏽'],
        'husband': ['💑 👈', '💏 👈', '👩❤👨 ⬅'],
        'wife': ['👉 💑', '👉 💏', '➡ 👩❤👨'],
    })


def test_emo_tuples(options):
    emotrans = EmoTrans(options)
    txt_to_emo = emotrans.txt_to_emo
    emo_to_txt = emotrans.emo_to_txt
    if options.txt_to_emo:
        show_sorted_dict(txt_to_emo, 0)
    if options.emo_to_txt:
        show_sorted_dict(emo_to_txt)

    for sentence in SENTENCES:
        print("src => txt (%s)" % sentence)
        emo_sent = emotrans.emojize_sentence_subs(sentence, options.verbose)
        print("txt => emo (%s)" % emo_sent)
        txt_sent = emotrans.textize_sentence_subs(emo_sent, options.verbose)
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
    parser.add_argument('-emo_to_txt', action='store_true',
                        help='show the emoji-to-text mapping')
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
    parser.add_argument('-txt_to_emo', action='store_true',
                        help='show the text-to-emoji mapping')
    parser.add_argument('-usable', action='store_true',
                        help='show all usable emoji under current options')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    # test_misc()
    test_emo_tuples(args)

if __name__ == '__main__':
    test_emojize()
