textize_emo_list_from_endemo_list#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plan:
        General sentence translation:
    while not completely translated:
        phrases => emojis
        phrases -> words
            words => emojis
        words -> syllables
            sysllables -> emojis
        words -> phonemes (possibly multiple phonemic decompositions)
            phonemes combined across word boundaries into phrases for whole sentences (or just the untranslated parts)
            match sublists of phonemes from sentences and emoji-to-word translations
            recombine into sentences and/or objects that contain sentences and skeletons tracking original word boundaries

    score and rank each (partial) translation
    show top ranked (partial) translation(s)

    Alternatively:
        Score each partial translation when formed
        Stop after a threshold is reached
        Show top ranked translation(s)




        Syllabic:
    Words|phrases -> words => [phonetic syllables reprs]
    Emojis => [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import argparse
import json
import pickle
import random
import re
from collections import Counter
from collections import defaultdict
from functools import partial
import time
import editdistance

import nltk
import emotuples as ET
import inflection
import text_fio
import text_regex
from emo_test_data import SENTENCES
# import sylcount

DEFAULT_SENTENCE = '"Rocks and waves may rock the boat," she said, "but only you can tip the crew!!"'
DEFAULT_SENTENCE = '"Rocks, paper, and scissors can rock, cover, or cut your hand," she said, "but you can\'t know when!!"'
DEFAULT_SENTENCE = '"Rocks and paper!!"'

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
    '''
    TODO: replace with real synonyms from a dedicated class
    FIXME: if word is not already all lower case, put both
    the orignal word and its lowered form in the list of
    synonyms, so as to match proper names.  (Custom emojis,
    syllabified names.)
    '''
    syns = [word]
    try:
        syns.extend(EMO_SYNONYMS[word])
    except KeyError:
        pass
    if not word.islower():
        lwrd = word.lower()
        syns.append(lwrd)
        try:
            syns.extend(EMO_SYNONYMS[lwrd])
        except KeyError:
            pass
    return syns

def pluralize(word):
    '''
    Return the plural form of the given word.
    TODO: Check that word is a noun (or an adjective or at any rate can
    be sensibly used as a noun) before calling inflection.pluralize?
    If not, return (word, false)
    FIXME BUGS: inflection is often wrong, e.g. (safe <-> saves)
    '''
    if word.lower()[-3:] == 'afe':
        return word + 's'
    return inflection.pluralize(word)

def singularize(word):
    '''
    Return the singular form of the given word.
    TODO: Check that word is a noun (or an adjective or at any rate can
    be sensibly used as a noun) before calling inflection.singularize?
    FIXME BUGS: inflection returns many wrong answers by pattern:
        *aves -> *afe
    It uses incomplete special case matching (octopus),
    and does not recognize many other pairs such as:
        (locus, loci)
    NB: pattern3.en is not yet functional (2017.07.10)
    '''
    if word.lower()[-4:] == 'aves':
        return word.rstrip('sS')
    return inflection.singularize(word)


def is_singular(word):
    '''
    Deprecated for now,
    even if used only to answer the question,
    "Might the pluralized form of this word be different?"
    FIXME: Get better data for a LUT implementation,
    '''
    return word != pluralize(word)

def is_plural(word):
    '''Deprecated until replaced by a LUT; @see is_singular.'''
    return word != singularize(word)

def read_pickle(path):
    with open(path, 'rb') as pkl:
        return pickle.load(pkl)

def show_sorted_dict(dct, idx, lbl=''):
    for key, val in sorted(dct.items(), key=lambda dit: dit[idx].lower()):
        print("{} {} => {}".format(lbl, key, val))

def add_preset_multiples(preset_dict):
    '''Add preset word to multiple emoji mapping'''
    preset_dict.update({
        "crew"   : ['👦 👲🏽 👧🏿 👨 👦🏽'],
        "husband": ['💑 👈', '💏 👈', '👩❤👨 ⬅'],
        "eye'd"    : ["👁 '🇩"],
        "I'd"    : ["👁 '🇩"],
        'wife'   : ['👉 💑', '👉 💏', '➡ 👩❤👨'],
    })

def print_tagged(tagged):
    maxlen = [max(len(tag[0]), len(tag[1])) for tag in tagged]
    # print(tagged)
    print("++++> txt => tok (", end='')
    for mxl, tup in zip(maxlen, tagged):
        print("%*s" % (mxl, tup[0]), end=' ')
    print(")")
    print("++++> tok => pos (", end='')
    for mxl, tup in zip(maxlen, tagged):
        print("%*s" % (mxl, tup[1]), end=' ')
    print(")")

TOKENIZER_NOT_NON_WORD = 1
TOKENIZER_WORD_EXTENDED = 2

MAX_MULTI_EMO_LEN = 8
MIN_SOLIT_EMO_LEN = 1

# Verbosity levels:
SHOW_TOKEN_TRANS = 3
SHOW_LIST_VALUES = 4
SHOW_TEXT_BUILDERS = 5
SHOW_TEXT_DIVISION = 6
SHOW_USABLE_EMOJIS = 7

class EmoTrans:
    def __init__(self, options):
        self.options = options
        self.verbose = options.verbose
        self.usables = self.gen_usables()
        if self.verbose > SHOW_USABLE_EMOJIS:
            self.print_usable_emojis()
        self.presets = self.gen_presets(options)
        self.txt_emo = self.gen_txt_to_emo(self.presets)
        self.emo_txt = self.gen_emo_to_txt(self.presets)
        self.emo_chr_counts = self.count_emo_chrs()
        self.singular_nouns = read_pickle('en_nouns_singular.pkl')
        self.plural_nouns = read_pickle('en_nouns_plural.pkl')

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
            presets.update({'a': [' '], 'an': [' '], 'but': [' '], 'the': [' ']})
        if options.arithmetic:
            presets.update({'can': ['🍬 ➖ D'], 'crew': ['© ➕ 🍺 ➖ 🐝'], 'you': ['🆕 ➖ N']})
        if options.multiple:
            add_preset_multiples(presets)
        return presets

    def gen_txt_to_emo(self, presets):
        '''generate text to emoji mapping'''
        txt_emo = presets
        i_flags = ET.INDEX_DISPLAY_FLAGS
        i_monos = ET.INDEX_WORDSYLLABLES
        i_words = ET.INDEX_FREQUENT_WORDS
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        for tt in self.usables:
            for txt in tt[i_words]:
                emo = tt[i_unchr]
                try:
                    txt_emo[txt].append(emo)
                except KeyError:
                    txt_emo[txt] = [emo]
                # print("txt(%s) => emo( %s )" % (txt, tt[i_unchr]))
        return txt_emo

    def gen_emo_to_txt(self, presets):
        '''generate emoji to texts mapping'''
        emo_txt = {}
        for txt, lst in presets.items():
            for emo in lst:
                try:
                    emo_txt[emo].append(txt)
                except KeyError:
                    emo_txt[emo] = [txt]

        # print("PRESET emo_txt:", emo_txt)
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        i_words = ET.INDEX_FREQUENT_WORDS
        for tt in self.usables:
            emo_txt[tt[i_unchr]] = tt[i_words]
        return emo_txt

    def rev_txt_to_gen(self):
        '''reverse of gen_txt_to_emo: map each emoji to a list of word-phrases'''
        emo_txt = {}
        for txt, lst in sorted(self.txt_emo.items()):
            # print("emo_txt 1: {} => {}".format(txt, lst))
            for emo in lst:
                emo_txt[emo].append(txt)
                if self.verbose > 1:
                    print("emo_txt 3: {} => {}".format(emo, txt))
        return emo_txt


    def is_plural_noun(self, word):
        '''
        Somewhat deprecated for now,
        especially if used to answer the question,
        "Might the singularized form of this word be different?"
        FIXME: Get data for a better LUT implementation,
        '''
        return word in self.plural_nouns

    def is_singular_noun(self, word):
        '''
        Somewhat deprecated for now,
        especially if used to answer the question,
        "Might the pluralized form of this word be different?"
        FIXME: Get data for a better LUT implementation,
        '''
        return word in self.singular_nouns


    def emojize_token(self, token):
        '''
        Return emoji string translation of token or None.
        The token will not be transformed in any way.  If
        it is meant to match an all lower-case key, the token
        must already be itself all lower-case.
        TODO: make protected ?
        '''
        try:
            lst = self.txt_emo[token]
            if self.verbose > SHOW_LIST_VALUES:
                print("ET: {} => {}".format(token, lst))
        except KeyError:
            if self.verbose > SHOW_TOKEN_TRANS:
                print("ET: {} => {}".format(token, token))
            return None
        emo = random.choice(lst) if self.options.random else lst[0]
        if self.verbose > SHOW_TOKEN_TRANS:
            print("ET: {} => {}".format(token, emo))
        return emo

    def emo_or_txt_token(self, token):
        '''Return translation of token or, failing that, the token itself.'''
        emo = self.emojize_token(token)
        return emo if emo else token

    def minus_s_emo(self):
        '''
        Return string of emoji characters representing "minus S",
        as in singularizing a plural noun.
        '''
        assert('➖' in self.emo_txt)
        assert('🇸' in self.emo_txt)
        return ' ➖ 🇸 '

    def emojize_word(self, src_word, space=' '):
        '''
        Return a translation of src_word into a string of emoji characters,
        or, failing that, return the original src_word.
        '''
        synonyms = emo_synonyms(src_word)
        if self.verbose > SHOW_LIST_VALUES:
            print("EW SYNOMS:", synonyms)
        for word in synonyms:
            emojis = self.emojize_token(word)
            if emojis:
                if self.verbose > SHOW_TOKEN_TRANS:
                    print("EW  TOKEN: {} => {}".format(word, emojis))
                return emojis + space
            if self.options.pluralize:
                if self.is_plural_noun(word):
                    singular = singularize(word)
                    if singular != word:
                        emojis = self.emojize_token(singular)
                        if emojis:
                            emostr = emojis + space + emojis + space
                            if self.verbose > SHOW_TOKEN_TRANS:
                                print("EW PLURAL: {} => {}".format(word, emostr))
                            return emostr
                # At least when subtraction is allowed, lip == lips - S ~= <kiss> - S == 💋 - S == 💋 <-> <S>
                # NB: Not elif, because some nouns can be either singular and plural, e.g. fish, sheep, dice,
                # briefs,data, agenda, heuristics,
                if self.is_singular_noun(word):
                    plural = pluralize(word)
                    if plural != word:
                        emojis = self.emojize_token(plural)
                        if emojis:
                            emostr = emojis + self.minus_s_emo()
                            if self.verbose > SHOW_TOKEN_TRANS:
                                print("EW SINGLE: {} => {}".format(word, emostr))
                            return emostr
        hyphenated = src_word.split('-')
        if len(hyphenated) > 1:
            return ' ➖ '.join([self.emo_or_txt_token(token) for token in hyphenated])
        return src_word

    def emojize_match(self, match_obj, space=' '):
        '''Translate word tokens from a regex match.'''
        word = match_obj.group()
        return self.emojize_word(word, space)


    def emojize_sentence_beg_mid_end(self, sentence, mid_translator, space=' '):
        ''' Segment sentence into beg, mid, and end, translate each, then recombine, where:
            beg = chars before any words
            end = chars after all words
            mid = everthing between beg and end.
        '''
        beg, body, end = text_regex.sentence_body_and_end(sentence)
        if self.verbose > SHOW_TEXT_DIVISION:
            print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))

        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        print_tagged(tagged)

        subs = mid_translator(body)
        #print("ESBME: mid(%s) ==> subs(%s): " % (body, subs))
        tend = self.emojize_token(end)
        if tend:
            #print("ESBME: end(%s) ==> tend(%s): " % (end, tend)
            end = space + tend
        emo_tran = ''.join([beg, subs, end])
        return emo_tran

    def emojize_text_subs(self, text, space=' '):
        '''
        Translate text word by word to emojis, where possible, using regex substitution.
        Intenting text to be the body of a sentence: the part between any leading or trailing punctuation.
        '''
        emojize_match_bound = partial(self.emojize_match, space=space)

        # TODO: Determine the best tokenizer(s).
        if self.options.tokenizer == TOKENIZER_WORD_EXTENDED:
            subs = text_regex.replace_words_extended(emojize_match_bound, text)
        else:
            subs = text_regex.replace_non_non_words(emojize_match_bound, text)
        return subs

    def emojize_phrase(self, txt_phrase, space=' '):
        '''
        Split phrase in to tokens (destructive), translate words,
        then join them back together.  Characters lost in the split
        are genearlly not restorable.  So round trips are not faithful.
        '''
        srcs = text_regex.word_splits(txt_phrase.strip())
        if self.verbose > 2:
            print(srcs)
        emo_phrase = []
        for raw in srcs:
            dst = self.emojize_word(raw, space)
            emo_phrase.append(dst)
        return emo_phrase


    def emojize_text_split_join(self, text, space=' '):
        '''
        Deprecated somewhat: Phrase translation by emojize_phrase is lossy and not
        reversible.  Characters lost in the split are genearlly
        not restorable.  So round trips are not faithful.
        '''
        emo_list = self.emojize_phrase(text, space)
        emo_join = space.join(emo_list)
        return emo_join

    def emojize_sentence_split_join(self, sentence, space=' '):
        '''
        Split sentence into beginning, middle, and end, translate
        these parts separately, then join them back together.
        Phrase translation by emojize_phrase is lossy and not
        reversible.  Characters lost in the split are genearlly
        not restorable.  So round trips are not faithful.
        '''
        return self.emojize_sentence_beg_mid_end(sentence, self.emojize_text_split_join, space)

    def is_emoji_chr(self, uchr):
        '''Is uchr an emoji or any part of an emoji (modifier)?'''
        return self.emo_chr_counts[uchr]

    def is_emoji_chr_bad(self, uchr):
        '''FIXME: optimize?  use RE?'''
        lst = self.emo_txt[uchr]
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
            lst = self.emo_txt[emo_span]
            if self.verbose > 1:
                print("TES: {} => {}".format(emo_span, lst))
            txt = random.choice(lst) if self.options.random else lst[0]
            return txt
        except KeyError:
            # return self.textize_emo_span_recurse(emo_span[0:-1]) + self.textize_emo_span_recurse(emo_span[-1:])
            return emo_span

    def textize_emo_chars(self, emo_span, space=' '):
        '''translate a string or slice of emojis char by char into a text string'''
        if self.verbose > SHOW_TEXT_BUILDERS:
            print("TCHRS: span({})".format(emo_span))
        text = ''
        prev = False
        for uchr in emo_span:
            try:
                lst = self.emo_txt[uchr]
                if self.verbose > 1:
                    print("TES: {} => {}".format(uchr, lst))
                txt = random.choice(lst) if self.options.random else lst[0]
                text += txt
                prev = True
            except KeyError:
                if prev and uchr == space:
                    prev = False
                else:
                    text += uchr
        return text

    def append_to_prev_list(self, word_calcs, prev_words=None):
        '''
        Select word from the word_calcs list and append it to
        the list of previously translated words.
        '''
        if self.verbose > 7:
            print("append_to_prev_list:  word_calcs({})  list({})".format(word_calcs, prev_words))
        if prev_words:
            for word in word_calcs:
                # unreduplicate
                if prev_words[-1] == word:
                    if is_singular(word):
                        plural = pluralize(word)
                        if plural != word:
                            prev_words[-1] = plural
                            return prev_words
                # resingularize
                if prev_words[-1] == '-' and len(prev_words) > 1 and prev_words[-2] == 'S':
                    if self.is_plural_noun(word):
                        singular = singularize(word)
                        if singular != word:
                            prev_words.pop()
                            prev_words[-1] = singular
                            return prev_words
                prev_words.append(word)
                if self.verbose > 7:
                    print("append_to_prev_list:  ({})  => ({})".format(word, prev_words))
                return prev_words
        word = random.choice(word_calcs) if self.options.random else word_calcs[0]
        return [word]


    def textize_emo_span_from_end_old(self, emo_span, prev_words=None):
        '''
        Recursively divide a string of emoji chars into a string of words, backing up greedily
        from the end.  The string (or "span") of emoji chars may contain spaces
        Returns a string with spaces inserted between the words, or None if the parse fails.
        '''
        if  self.verbose > SHOW_TEXT_DIVISION:
            print("TESFE A:  span({})  prev_words({})".format(emo_span, prev_words))

        # If the this (whole or remaining) span can be parsed as a single emoji with an (English)
        # translation, just return it, concatenated with any words already parsed.
        emo_span = emo_span.rstrip()
        try:
            # if emo_span[-1] == space:
            #     lst = self.emo_txt[emo_span[0:-1]]
            # else:
            #     lst = self.emo_txt[emo_span]
            word_calcs = self.emo_txt[emo_span]
            if self.verbose > 5:
                print("TESFE B: {} => {}".format(emo_span, word_calcs))
            return self.append_to_prev_list(word_calcs, prev_words)
        except KeyError:
            # Else divide the string into two parts, and if the 2nd part is a word, keep going.
            # Use min and max word lengths to skip checking substrings that cannot be words.
            max_index = len(emo_span)
            min_index = max_index - MAX_MULTI_EMO_LEN
            if  min_index < 0:
                min_index = 0
            max_index -= MIN_SOLIT_EMO_LEN
            while max_index >= min_index:
                substr = emo_span[max_index:]
                word_calcs = self.emo_txt.get(substr, [])
                if self.verbose > SHOW_TEXT_DIVISION:
                    print("while min({})  max({})  substr({})  calcs({})".format(min_index, max_index, substr, word_calcs))
                if len(word_calcs) > 0:
                    txt = self.append_to_prev_list(word_calcs, prev_words)
                    if self.verbose > SHOW_TEXT_DIVISION:
                        print("TESFE D: Calling textize_emo_span_from_end_old({}, {})".format(emo_span[0:max_index], txt))
                    more_words = self.textize_emo_span_from_end_old(emo_span[0:max_index], txt)
                    if more_words:
                        return more_words
                max_index -= 1
        return None          # string did not parse


    def textize_emo_list_from_end(self, emo_span, emo_list=None, list_idx=None, prev_words=None):
        '''
        Recursively divide a string of emoji chars into a string of words, backing up greedily
        from the end.  Consuming the string in reverse simplies the parsing of modifiers: they
        can be ignored until a root character is reached.
        The string (or "span") of emoji chars may contain spaces
        Returns a string with spaces inserted between the words, or None if the parse fails.
        '''
        if  self.verbose > SHOW_TEXT_DIVISION:
            print("TESFE A:  span({})  list{}  idx:{}  words{}".format(emo_span, emo_list, list_idx, prev_words))

        # If the this (whole or remaining) span can be parsed as a single emoji with an (English)
        # translation, just return it, concatenated with any words already parsed.
        if  emo_list == None:
            emo_list = emo_span.split()
            list_idx = len(emo_list) - 1
        try:
            # if emo_span[-1] == space:
            #     lst = self.emo_txt[emo_span[0:-1]]
            # else:
            #     lst = self.emo_txt[emo_span]
            word_calcs = self.emo_txt[emo_span]
            if self.verbose > 5:
                print("TESFE B: {} => {}".format(emo_span, word_calcs))
            return self.append_to_prev_list(emo_list, list_idx, word_calcs, prev_words)
        except KeyError:
            # Else divide the string into two parts, and if the 2nd part is a word, keep going.
            # Use min and max word lengths to skip checking substrings that cannot be words.
            while list_idx >= 0:
                emo_str = emo_list[list_idx]
                word_calcs = self.emo_txt.get(emo_str, [])
                if self.verbose > SHOW_TEXT_DIVISION:
                    print("while idx({})  emo_str({})  calcs({})".format(list_idx, emo_str, word_calcs))
                if len(word_calcs) > 0:
                    txt_list = self.append_to_prev_list(emo_list, list_idx, word_calcs, prev_words)
                    if self.verbose > SHOW_TEXT_DIVISION:
                        print("TESFE D: Calling textize_emo_list_from_end({}, {}, {})".format(emo_list, list_idx, txt_list))
                    more_words = self.textize_emo_list_from_end(emo_span, emo_list, list_idx, txt_list)
                    if more_words:
                        return more_words
                list_idx -= 1
        return None          # string did not parse

    def textize_emo_span(emo_span, space=' '):
        try:
            txt = emo_txt[emo_span]:
            return txt or something
        except KeyError:
            emo_list = emo_span.split(space)
            txt_list = self.textize_emo_list_from_end(emo_list, list_idx)

    def textize_sentence_subs(self, emo_sent, space=' '):
        '''
        return text with each emoji replaced by a value from emo_txt.
        FIXME: emoji combinations representing a single word will not translate
        back to the orignal word, but turn into a word combination calc, which
        may be gibberish or worse.
        '''
        txt_sent, emo_span, emo_prev, first = '', '', None, True
        for uchr in emo_sent:
            if self.is_emoji_chr(uchr):
                emo_span += uchr
                emo_prev = uchr
            elif space == uchr and emo_prev:
                emo_span += uchr
                emo_prev = None
            elif emo_span:
                txt_list = self.textize_emo_span(emo_span)
                if txt_list:
                    txt_list.reverse()
                    if self.verbose > SHOW_LIST_VALUES:
                        print("TSS list: ({})".format(txt_list))
                    txt_join = space.join(txt_list)
                    if self.verbose > SHOW_TOKEN_TRANS:
                        print("TSS REBUS: {} => {}".format(emo_span, txt_join))
                    if first:
                        txt_sent += txt_join.capitalize()
                        first = False
                    else:
                        txt_sent += txt_join
                    if self.verbose > SHOW_TEXT_BUILDERS:
                        print("TSS text: ({})".format(txt_sent))
                else:
                    if self.verbose > SHOW_TEXT_BUILDERS:
                        print("TSS add: {} += {}", txt_sent, emo_span)
                    txt_sent += emo_span
                emo_span = ''
                emo_prev = None
                txt_sent += uchr
            else:
                txt_sent += uchr
                first = False
        if emo_span:
            txt_list = self.textize_emo_span(emo_span)
            if txt_list:
                txt_list.reverse()
                txt_join = space.join(txt_list)
                if self.verbose > SHOW_LIST_VALUES:
                    print("TSS list: {}".format(txt_list))
                if self.verbose > SHOW_TOKEN_TRANS:
                    print("TSS REBUS: {} => {}".format(emo_span, txt_join))
                if txt_list[0].isalnum():
                    txt_sent = txt_sent + txt_join
                else:
                    txt_sent = txt_sent.rstrip() + txt_join
            else:
                txt_sent += emo_span
        return txt_sent

    def emojize_sentence_subs(self, sentence, space=' '):
        '''translate text sentence to emojis using regex substitution'''
        return self.emojize_sentence_beg_mid_end(sentence, self.emojize_text_subs, space)

    def emojize_sentence(self, sentence):
        '''translate text sentence to emojis according to options'''
        if self.options.split_join:
            return self.emojize_sentence_split_join(sentence)
        else:
            return self.emojize_sentence_subs(sentence)

    def textize_sentence(self, sentence):
        '''translate emoji sentence to text according to options'''
        return self.textize_sentence_subs(sentence)

    def translate_sentence_to_emo_and_back(self, sentence):
        '''translate text sentence to emoji and back, showing stages according to options'''
        print("====> src => txt (%s)" % sentence)
        emo_sent = self.emojize_sentence(sentence)
        print("====> txt => emo (%s)" % emo_sent)
        txt_sent = self.textize_sentence(emo_sent)
        print("====> emo => txt (%s)" % txt_sent)

        dist = editdistance.eval(sentence, txt_sent)
        print("edit distance: {:>5}".format(dist))

def translate_sentences(options):
    '''Test translation from Enlish to emojis and back.'''
    emotrans = EmoTrans(options)
    txt_emo = emotrans.txt_emo
    emo_txt = emotrans.emo_txt
    if options.txt_emo:
        show_sorted_dict(txt_emo, 0)
    if options.emo_txt:
        show_sorted_dict(emo_txt)
    if options.sentence:
        emotrans.translate_sentence_to_emo_and_back(options.sentence)
        exit(0)

    for sentence in SENTENCES:
        emotrans.translate_sentence_to_emo_and_back(sentence)
        print()

    if options.text_file:
        for sentence in text_fio.read_text_lines(options.text_file, options.charset):
            emotrans.translate_sentence_to_emo_and_back(sentence)

def main():
    '''test english -> emoji translation'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('-arithmetic', action='store_true',
                        help='use addition and subtraction of letters or syllables (rebus)')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-input', dest='sentence', type=str, nargs='?', default=None,
                        const=DEFAULT_SENTENCE, help='input a sentence to translate (or use default)')
    parser.add_argument('-emo_txt', action='store_true',
                        help='show the emoji-to-text mapping')
    parser.add_argument('-flags', action='store_true',
                        help='use flag emojis in translations of words not representing countries')
    parser.add_argument('-multiple', action='store_true',
                        help='use multiple emoji for some words (presets)')
    parser.add_argument('-no_articles', '-noa', action='store_true',
                        help='remove articles (a, an, the)')
    parser.add_argument('-pluralize', '-singularize', action='store_false',
                        help='Disable pluralization and singularization (which are on by default)')
    # parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
    #                     help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-random', action='store_true',
                        help='Choose random emojis or words from translation lists '
                                '(instead of always choosing the first)')
    parser.add_argument('-split_join', '-sj', action='store_true',
                        help='translate using split and join (irreversible because destructive), '
                                'not substitution (conservative)')
    parser.add_argument('-text_file', dest='text_file', type=str, nargs='?',
                        const='quotations.txt', default=None,
                        help='translate sentences from this text_file')
    parser.add_argument('-tokenizer', type=int, nargs='?',
                        const=TOKENIZER_WORD_EXTENDED, default=TOKENIZER_NOT_NON_WORD,
                        help='specify tokenizer as: 1=NOT_NON_WORD, 2=WORD_EXTENDED')
    parser.add_argument('-txt_emo', action='store_true',
                        help='show the text-to-emoji mapping')
    parser.add_argument('-usable', action='store_true',
                        help='show all usable emoji under current options')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    # if args.verbose > 7:
    #     print("module emoji:", EJ)

    translate_sentences(args)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("----- %.4f seconds elapsed -----" % (time.time() - start_time))
