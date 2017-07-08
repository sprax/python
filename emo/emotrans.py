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
from collections import Counter
from collections import defaultdict
from functools import partial

import emoji as EJ
import emotuples as ET
import text_fio
import text_regex
# import sylcount

SENTENCES = [
    " The wind and waves.",
    # "Wind and waves may rock the boat, but only you can tip the crew.",
    # "I love you",
    # "So it's the US vs. Canada in football, I mean soccer!?",
    # "Lady Astor: “Winston, if I were your wife I’d put poison in your coffee.",
    # "Winston Churchill: “Nancy, if I were your husband I’d drink it.",
    # "I'm 100% sure <3 ain't a 4-letter word, even on Rhys' say-so?!",
    # "When the eagles are silent, the parrots begin to jabber.",
    # "If you have an important point to make, don’t try to be subtle or clever. Use a pile driver. Hit the point once. Then come back and hit it again. Then hit it a third time -- a tremendous whack.",
    # "Success consists of going from failure to failure without loss of enthusiasm.",
    # "Character may be manifested in the great moments, but it is made in the small ones.",
    # "Men occasionally stumble over the truth, but most of them pick themselves up and hurry off as if nothing has happened.",
]

# def is_emoji(uchar):
#   return uchar in EJ.UNICODE_EMOJI

# def extract_emojis(str):
#   return ''.join(c for c in str if c in emoji.EMOJI_UNICODE)

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
    '''TODO: replace with real synonyms from a dedicated class'''
    try:
        return EMO_SYNONYMS[word]
    except KeyError:
        return [word]

def is_plural(word):
    '''FIXME: this is ridiculous'''
    try:
        return word[-1] == 's'
    except IndexError:
        return false

def pluralize(word):
    '''
    Return (plural, is_changed) where plural is the plural form of the
    given word, and is_changed is True IFF word != plural.
    TODO: replace with real plurals from a dedicated class
    '''
    if word.endswith('ss'):
        return word + 'es', True
    last = word[-1]
    if last != 's':
        return word + 's', True
    else:
        return word, False

def singularize(word):
    '''FIXME: make it work like pluralize (but better)'''
    try:
        if word[-1] == 's':
            return word[0:-1], True
        return word, False
    except IndexError:
        return word, False

def show_sorted_dict(dct, idx, lbl=''):
    for key, val in sorted(dct.items(), key=lambda dit: dit[idx].lower()):
        print("{} {} => {}".format(lbl, key, val))

MAX_MULTI_EMO_LEN = 11
MIN_SOLIT_EMO_LEN = 1
SHOW_GENERATED_DICTS = 7

class EmoTrans:
    def __init__(self, options):
        self.options = options
        self.verbose = options.verbose
        self.usables = self.gen_usables()
        if self.verbose > SHOW_GENERATED_DICTS:
            self.print_usable_emojis()
        self.presets = self.gen_presets(options)
        self.txt_to_emo = self.gen_txt_to_emo(self.presets)
        self.emo_to_txt = self.gen_emo_to_txt(self.presets)
        self.emo_chr_counts = self.count_emo_chrs()


    def count_emo_chrs(self):
        counter = Counter()
        for tt in self.usables:
            counter.update(tt[ET.INDEX_EMOJI_UNICHRS])
        if self.verbose > 7:
            print("Most common emo parts (single unichars):", counter.most_common(12))
        return counter

    def gen_usables(self, i_flags = ET.INDEX_DISPLAY_FLAGS):
        return [tup for tup in ET.EMO_TUPLES if tup[i_flags] > 0]

    def print_usable_emojis(self):
        print("Read %d usable emoji tuples:" % len(self.usables))
        for tt in self.usables:
            print(tt[ET.INDEX_EMOJI_UNICHRS], end='  ')
        print()

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
        txt_to_emo = presets
        i_flags = ET.INDEX_DISPLAY_FLAGS
        i_monos = ET.INDEX_WORDSYLLABLES
        i_words = ET.INDEX_FREQUENT_WORDS
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        for tt in self.usables:
            for txt in tt[i_words]:
                emo = tt[i_unchr]
                try:
                    txt_to_emo[txt].append(emo)
                except KeyError:
                    txt_to_emo[txt] = [emo]
                # print("txt(%s) => emo( %s )" % (txt, tt[i_unchr]))
        return txt_to_emo

    def gen_emo_to_txt(self, presets):
        '''generate emoji to texts mapping'''
        emo_to_txt = {}
        for txt, lst in presets.items():
            for emo in lst:
                try:
                    emo_to_txt[emo].append(txt)
                except KeyError:
                    emo_to_txt[emo] = [txt]

        # print("PRESET emo_to_txt:", emo_to_txt)
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        i_words = ET.INDEX_FREQUENT_WORDS
        for tt in self.usables:
            emo_to_txt[tt[i_unchr]] = tt[i_words]
        return emo_to_txt

    def rev_txt_to_gen(self, verbose):
        '''reverse of gen_txt_to_emo: map each emoji to a list of word-phrases'''
        emo_to_txt = {}
        for txt, lst in sorted(self.txt_to_emo.items()):
            # print("emo_to_txt 1: {} => {}".format(txt, lst))
            for emo in lst:
                emo_to_txt[emo].append(txt)
                if verbose > 1:
                    print("emo_to_txt 3: {} => {}".format(emo, txt))
        return emo_to_txt

    def emojize_token(self, word):
        '''return emoji string translation of word or None
        TODO: make protected ?'''
        try:
            lst = self.txt_to_emo[word]
            if self.verbose > 4:
                print("ET: {} => {}".format(word, lst))
        except KeyError:
            lwrd = word.lower()
            try:
                lst = self.txt_to_emo[lwrd]
                if self.verbose > 4:
                    print("ET: {} => {}".format(lwrd, lst))
            except KeyError:
                if self.verbose > 3:
                    print("ET: {} => {}".format(word, word))
                return None
        emo = random.choice(lst)
        if self.verbose > 3:
            print("ET: {} => {}".format(word, emo))
        return emo

    def emojize_word(self, src_word, space=' '):
        words = emo_synonyms(src_word)
        for word in words:
            emojis = self.emojize_token(word)
            if emojis:
                # print("emojize_word: about to return ({} + {}):".format(emojis, space))
                return emojis + space
            # # FIXME: If using subtraction, lip == lips - S ~= <kiss> - S == 💋 - S == 💋 <-> <S>
            # plural, changed = pluralize(word)
            # if changed:
            #     emojis = self.emojize_token(plural)
            #     if emojis:
            #         return emojis + space
            elif is_plural(word):
                singular, singularized = singularize(word)
                if singularized:
                    emojis = self.emojize_token(singular)
                    if emojis:
                        emostr = emojis + space + emojis + space
                        print("EW: {} => {}".format(src_word, emostr))
                        return emostr
        return src_word

    def emojize_match(self, match_obj, space=' '):
        word = match_obj.group()
        return self.emojize_word(word, space)

    def emojize_sentence_subs(self, sentence, space=' '):
        beg, body, end = text_regex.sentence_body_and_end(sentence)
        if self.verbose > 6:
            print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))

        emojize_match_bound = partial(self.emojize_match, space=space)
        subs = text_regex.replace_words_extended(emojize_match_bound, body)
        tend = self.emojize_token(end)
        if tend:
            end = space + tend
        emo_tran = ''.join([beg, subs, end])
        return emo_tran

    def emojize_phrase(self, txt_phrase, space=' '):
        # srcs = re.split('\W+', txt_phrase.strip())
        srcs = text_regex.word_splits(txt_phrase.strip())
        if self.verbose > 2:
            print(srcs)
        emo_phrase = []
        for raw in srcs:
            dst = self.emojize_word(raw, space)
            emo_phrase.append(dst)
        return emo_phrase

    def emojize_sentence_split_join(self, sentence, space=' '):
        beg, body, end = text_regex.sentence_body_and_end(sentence)
        if verbose > 2:
            print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))
        emo_list = self.emojize_phrase(txt_to_emo, body, space)
        emo_join = space.join(emo_list)
        emo_tran = ''.join([beg, emo_join, end])
        if self.verbose > 5:
            print("    %s ==>\n    %s\n" % (sentence, emo_tran))
        return emo_tran

    def is_emoji_chr(self, uchr):
        '''Is uchr an emoji or any part of an emoji (modifier)?'''
        return self.emo_chr_counts[uchr]

    def is_emoji_chr_bad(self, uchr):
        '''FIXME: optimize?  use RE?'''
        lst = self.emo_to_txt[uchr]
        if len(lst) > 0:
            return True
        # if is_emoji(uchr):
        #     return True
        return False

    def textize_emo_span_recurse_busted(self, emo_span):
        '''FIXME: busted.  translate a string or slice of emojis into a text string'''
        if self.verbose > 2:
            print("TSPAN: span({})".format(emo_span))

        try:
            lst = self.emo_to_txt[emo_span]
            if self.verbose > 1:
                print("TES: {} => {}".format(emo_span, lst))
            return lst[0]  # random.choice(lst)
        except KeyError:
            # return self.textize_emo_span_recurse(emo_span[0:-1]) + self.textize_emo_span_recurse(emo_span[-1:])
            return emo_span

    def textize_emo_chars(self, emo_span, space=' ', verbose=1):
        '''translate a string or slice of emojis char by char into a text string'''
        if verbose > 3:
            print("TCHRS: span({})".format(emo_span))
        text = ''
        prev = False
        for uchr in emo_span:
            try:
                lst = self.emo_to_txt[uchr]
                if verbose > 1:
                    print("TES: {} => {}".format(uchr, lst))
                text += lst[0]  # random.choice(lst)
                prev = True
            except KeyError:
                if prev and uchr == space:
                    prev = False
                else:
                    text += uchr
        return text

    def append_word(self, word, word_list=None):
        print("append_word:  word({})  list({})".format(word, word_list))
        if word_list:
            if word_list[-1] == word:
                if is_singular(word):
                    plural, different = pluralize(word)
                    if different:
                        word_list[-1] = plural
                        return word_list
            word_list.append(word)
        return [word]

    def textize_emo_span_from_end(self, emo_span, word_list=None):
        '''
        Recursively divide a string of emoji chars into a string of words, backing up greedily
        from the end.  The string (or "span") of emoji chars may contain spaces
        Returns a string with spaces inserted between the words, or None if the parse fails.
        '''
        if  self.verbose > 6:
            print("TESFE A:  span({})  word_list({})".format(emo_span, word_list))

        # If the this (whole or remaining) span can be parsed as a single emoji with an (English)
        # translation, just return it, concatenated with any words already parsed.
        try:
            # if emo_span[-1] == space:
            #     lst = self.emo_to_txt[emo_span[0:-1]]
            # else:
            #     lst = self.emo_to_txt[emo_span]
            lst = self.emo_to_txt[emo_span.rstrip()]
            if self.verbose > 4:
                print("TESFE B:  {} => {}".format(emo_span, lst))
            wrd = lst[0]  # random.choice(lst)
            return self.append_word(wrd, word_list)
        except KeyError as ie:
            print("Except:", ie)
            # Else divide the string into two parts, and if the 2nd part is a word, keep going.
            # Use min and max word lengths to skip checking substrings that cannot be words.
            max_index = len(emo_span)
            min_index = max_index - MAX_MULTI_EMO_LEN
            if  min_index < 0:
                min_index = 0
            max_index -= MIN_SOLIT_EMO_LEN
            while max_index > min_index:
                substr = emo_span[max_index:]
                nxt = self.emo_to_txt.get(substr, [])
                if len(nxt) > 0:
                    wrd = nxt[0]  # random.choice(lst)
                    txt = self.append_word(wrd, word_list)
                    print("TESFE C: Calling textize_emo_span_from_end({}, {})".format(
                            emo_span[0:max_index], txt))
                    more_words = textize_emo_span_from_end(emo_span[0:max_index], txt)
                    if more_words:
                        return more_words
                max_index -= 1
        return None          # string did not parse


    def textize_sentence_subs(self, emo_sent, space=' ', verbose=1):
        '''
        return text with each emoji replaced by a value from emo_to_txt.
        FIXME: emoji combinations representing a single word will not translate
        back to the orignal word, but turn into a word combination calc, which
        may be gibberish or worse.
        '''
        txt_sent, emo_span, emo_prev = '', '', None
        for uchr in emo_sent:
            if self.is_emoji_chr(uchr):
                emo_span += uchr
                emo_prev = uchr
            elif space == uchr and emo_prev:
                emo_span += uchr
                emo_prev = None
            elif emo_span:
                print("TSS: TESFE({})".format(emo_span))
                txt_list = self.textize_emo_span_from_end(emo_span)
                print("TSS lst: txt_list({})".format(txt_list))
                if txt_list:
                    txt_list.reverse()
                    txt_sent += space.join(txt_list)
                    print("TSS txt:", txt_sent)
                else:
                    print("TSS add: {} += {}", txt_sent, emo_span)
                    txt_sent += emo_span
                emo_span = ''
                emo_prev = None
                txt_sent += uchr
            else:
                txt_sent += uchr
        if emo_span:
            txt_list = self.textize_emo_span_from_end(emo_span)
            # if txt_list:
            #     txt_sent = txt_sent.rstrip() + space.join(txt_list)
            # else:
            #     txt_sent += emo_span
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
        emo_sent = emotrans.emojize_sentence_subs(sentence)
        print("txt => emo (%s)" % emo_sent)
        txt_sent = emotrans.textize_sentence_subs(emo_sent)
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
    if args.verbose > 7:
        print("module emoji:", EJ)

    test_emo_tuples(args)

if __name__ == '__main__':
    test_emojize()
