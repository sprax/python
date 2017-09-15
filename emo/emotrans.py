#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plan for General sentence translation [square brackets for the still TBD parts]:
    while not completely translated, try translating in this order:
        phrases => emojis
            [trigrams -> emojis] ?
            bigrams -> emojis
        phrases -> words
            words => emojis (orthonyms)
        words => (lemmas/stems) => sets of synonymous tokens (synonyms)
            synsets -> emojis
        words => phonemic string representations
            phonetic reps -> emojis (homonyms)
        words -> phonemic syllables
            syllables -> emojis
        [words -> sub-syllabic phonemes (possibly multiple phonemic decompositions)
            phonemes combined across word boundaries into phrases for whole sentences
                (or just the untranslated parts)
            match sublists of phonemes from sentences and emoji-to-word translations
                (virtual or realized lattices weighted by probabilities and/or scores)
            recombine into sentences and/or objects that contain sentences and skeletons
                tracking original word boundaries] ?

    score and rank each (partial) translation
    show top ranked (partial) translation(s)

    Alternatively:
        Score each partial translation when formed
        Stop after a threshold is reached
        Show top ranked translation(s), or just choose

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
import struct
from collections import Counter
from collections import defaultdict
from functools import partial
import time
import editdistance
import word_phonetics

import nltk
from nltk.corpus import wordnet
from nltk.corpus import cmudict

import emotuples as ET
import inflection
import text_fio
import text_regex
from emo_test_data import SENTENCES
# import sylcount

DEFAULT_SENTENCE = '"Rocks and waves may rock the boat," she said, "but only you can tip the crew!!"'
DEFAULT_SENTENCE = '"Rocks, paper, and scissors can rock, cover, or cut your hand, but you can\'t know when!!"'
DEFAULT_SENTENCE = '"Rocks," she said, "and paper, too, y\'know!!"'

# def is_emoji(uchar):
#   return uchar in EJ.UNICODE_EMOJI

# def extract_emojis(str):
#   return ''.join(c for c in str if c in emoji.EMOJI_UNICODE)

def test_load():
    '''load emodict.json'''
    emodict = json.loads(open('../../emodict.json').read())
    for i, tup in enumerate(sorted(emodict.items(), key=lambda x: int(x[1]['order']), reverse=True)):
        if i > 5:
            break
        ucs = unicode_chr_str(tup[0])
        print(ucs, "\t", len(ucs), "\t", tup[1]['order'], "\t", tup[0], "\t", tup[1]['shortname'])

def selflist(word):
    '''return argument as sole element in list'''
    return [word]

def getsyl(table, word):
    '''syllables'''
    syls = table.get(word)
    return syls if syls else word

def trans():
    '''Translate to syllables?'''
    wtsl = defaultdict(selflist)
    sent = SENTENCES[0]
    words = re.split(r'\W+', sent.rstrip())
    print(words)
    for word in words:
        print("{} --> {}".format(word, getsyl(wtsl, word)))

def char(i):
    '''return arg converted to chr'''
    try:
        return chr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')

def unicode_chr_str(hex_unicode):
    '''print hexadecimal-encoded emoji code/key as unichars'''
    if '-' not in hex_unicode:
        return char(int(hex_unicode, 16))
    parts = hex_unicode.split('-')
    return ''.join(char(int(x, 16)) for x in parts)

EMO_SYNONYMS = {}

def wordnet_syn_set(word, pos, lower_only=True):
    '''
    Returns a list of wordnet synonyms of word based on part of speech
    identifier(s) in the string pos.  The recognized POS identifiers are
    the single letters [a, n, r, s, v], a.k.a. the wordnet module constants
    [ADJ, NOUN, ADV, ADJ_SAT, VERB], that is,
    ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'.
    In practice, satellite synsets (s or ADJ_SAT) are not useful for simple
    word substitution.  Just use the first letter from a common NLTK POS tagger.
    If lower_only is True, only lowercase synonyms are included.
    The list may contain duplicates, which are likely to be more common words.
    '''
    synonyms = []
    synsets = wordnet.synsets(word, pos)
    for synset in synsets:
        lemmas = synset.lemma_names()
        # print(synonyms)
        if lower_only:
            for lemma in lemmas:
                if lemma.islower():
                    synonyms.append(lemma.replace('_', ' '))
        else:
            for lemma in lemmas:
                synonyms.append(lemma.replace('_', ' '))
    return synonyms

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
    '''returns a loaded pickle'''
    with open(path, 'rb') as pkl:
        return pickle.load(pkl)

def show_sorted_dict(dct, idx, lbl=''):
    '''print sorted dictionary'''
    for key, val in sorted(dct.items(), key=lambda dit: dit[idx].lower()):
        print("{}  {} => {}".format(lbl, key, val))

def _add_txt_emo_multiples(preset_dict):
    '''Add preset word-to-multiple-emojis mapping'''
    preset_dict.update({
        "crew"   : ['👦 👲🏽 👧🏿 👨 👦🏽'],
        "husband": ['💑 👈', '💏 👈', '👩❤👨 ⬅'],
        "eye'd"    : ["👁 '🇩"],
        "I'd"    : ["👁 '🇩"],
        'wife'   : ['👉 💑', '👉 💏', '➡ 👩❤👨'],
    })

def print_tagged(tagged):
    '''Pretty prints words and the POS-tags aligned on two lines.'''
    maxlen = [max(len(tag[0]), len(tag[1])) for tag in tagged]
    # print(tagged)
    print("+++++> txt => tok (", end='')
    for mxl, tup in zip(maxlen, tagged):
        print("%*s" % (mxl, tup[0]), end=' ')
    print(")")
    print("+++++> tok => pos (", end='')
    for mxl, tup in zip(maxlen, tagged):
        print("%*s" % (mxl, tup[1]), end=' ')
    print(")")

RE_TONED_EMO_NAME = re.compile(r"^:\w+tone\d:$")

TOKENIZER_NOT_NON_WORD = 1
TOKENIZER_WORD_EXTENDED = 2

MAX_MULTI_EMO_LEN = 8
MIN_SOLIT_EMO_LEN = 1

# Verbosity levels:
SHOW_TOKEN_TRANS = 3
SHOW_LIST_VALUES = 4
SHOW_TEXT_BUILDERS = 5
SHOW_NOUN_SINGPLUR = 6
SHOW_TEXT_DIVISION = 7
SHOW_TEXT_BIGRAMS = 8
SHOW_TEXT_PHONETICS = 8
SHOW_USABLE_EMOJIS = 10

class EmoTrans:
    '''
    Translate text to emojis, emojis to text.
    TODO: disallow 'uh' for 'a', etc.
    TODO: finish gen* -> _gen*
    TODO: simple anaphora: 'Neil is an astronaut.  He[astronaut] went to the moon.'  Beware dog syllogisms.
    TODO: break up into 2 or 3 classes: Translater, POSer, Chunker, SynSubber?
    TODO: Add lattice & scoring, probability weighting.
    '''
    def __init__(self, options=None):
        self.options = self._init_options(options)
        # print("EmoTrans: self.options: ", self.options)
        self.verbose = self.options.verbose
        self.cmu_pro = cmudict.dict() # get the CMU Pronouncing Dict # TODO: wrap in sep class
        self.usables = self._gen_usables()
        if self.verbose > SHOW_USABLE_EMOJIS:
            self.print_usable_emojis()
        self.presets = self._gen_txt_emo_presets()
        self.txt_emo = self.gen_txt_to_emo(self.presets)
        self.emo_txt = self.gen_emo_to_txt(self.presets)
        self.pro_emo = self._gen_pros_to_emos(self.txt_emo)
        self.emo_chr_counts = self.count_emo_chrs()
        self.singular_nouns = set(text_fio.read_text_lines('en_singular_nouns_different_from_plural.txt'))
        self.plural_nouns = set(text_fio.read_text_lines('en_plural_nouns_different_from_singular.txt'))
        # print("DBG self.plural_nouns:", self.plural_nouns)

    def _init_options(self, options):
        '''initialize options with default values'''
        if options == None:
            options = argparse.Namespace(
                all_skin_tones = False,
                arithmetic = False,
                multiples = False,
                no_articles = False,
                phonetics = True,
                pluralize = True,
                random = False,
                singularize = True,
                verbose = 2,
            )
        return options

    def get_opt(self, opt):
        '''get option value'''
        try:
            return self.options.__getattribute__(opt)
        except AttributeError as aex:
            if self.options.verbose > 1:
                print("EmoTrans option not set: ", aex)
            return None

    def count_emo_chrs(self):
        '''count chars used in emoji codes'''
        counter = Counter()
        for tup in self.usables:
            counter.update(tup[ET.INDEX_EMOJI_UNICHRS])
        if self.verbose > 7:
            print("Most common emo parts (single unichars):", counter.most_common(12))
        return counter

    def _gen_usables(self, i_flags=ET.INDEX_DISPLAY_FLAGS, i_short=ET.INDEX_SHORT_NAME):
        '''
        Generate list of emo tuples to use on this platform
        TODO: generalize.
        '''
        if self.options.all_skin_tones and self.options.multiples:
            return [tup for tup in ET.EMO_TUPLES if tup[i_flags] > 0]
        if self.options.all_skin_tones:
            return [tup for tup in ET.EMO_TUPLES if tup[i_flags] == 1]
        if self.options.multiples:
            return [tup for tup in ET.EMO_TUPLES if tup[i_flags] > 0 and
                    not RE_TONED_EMO_NAME.match(tup[i_short])]
        return [tup for tup in ET.EMO_TUPLES if tup[i_flags] == 1 and
                not RE_TONED_EMO_NAME.match(tup[i_short])]

    def print_usable_emojis(self):
        '''Print the usable emojis'''
        print("Read %d usable emoji tuples:" % len(self.usables))
        for tup in self.usables:
            print(tup[ET.INDEX_EMOJI_UNICHRS], end='  ')
        print()

    def _gen_txt_emo_presets(self):
        '''populate preset text to emoji mappings'''
        presets = {}
        if self.options.no_articles:
            presets.update({'a': [' '], 'an': [' '], 'but': [' '], 'the': [' ']})
        if self.options.arithmetic:
            presets.update({'can': ['🍬 ➖ D'], 'crew': ['© ➕ 🍺 ➖ 🐝'], 'you': ['🆕 ➖ N']})
        if self.options.multiples:
            _add_txt_emo_multiples(presets)
        return presets

    # FIXME stub
    def gen_phonetic_repl(self, text):
        '''Returns single phonetic spelling representation of the given text.'''
        return word_phonetics.cmu_phonetic(self.cmu_pro, text, verbose=(self.verbose > SHOW_USABLE_EMOJIS + 1))

    # FIXME stub
    def gen_phonetic_word(self, text):
        '''Returns a PhoneticWord object based on text'''
        return word_phonetics.PhoneticWord(self.cmu_pro, text, verbose=(self.verbose > SHOW_USABLE_EMOJIS + 1))

    def _gen_pros_to_emos(self, txt_emo):
        '''Generates a pronunciation-to-emojis mapping.
        NB: Call this AFTER self.txt_emo is initialized.'''
        pro_emo = {}
        for txt_key, emo_lst in txt_emo.items():
            # FIXME: Single key for now
            pro_key = self.gen_phonetic_repl(txt_key)
            if pro_key:
                try:
                    pro_emo[pro_key].extend(emo_lst)
                except KeyError:
                    pro_emo[pro_key] = emo_lst
                if self.verbose > SHOW_USABLE_EMOJIS:
                    print("PRO_EMO: {} -> {} -> {}".format(txt_key, pro_key, pro_emo[pro_key]))
        return pro_emo

    def gen_txt_to_emo(self, presets, i_words=ET.INDEX_FREQUENT_WORDS):
        '''Generates the text-to-emojis mapping.'''
        txt_emo = presets
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        for tup in self.usables:
            emo = tup[i_unchr]
            for txt in tup[i_words]:
                try:
                    txt_emo[txt].append(emo)
                except KeyError:
                    txt_emo[txt] = [emo]
                # print("txt(%s) --> emo( %s )" % (txt, tup[i_unchr]))
        return txt_emo

    def gen_emo_to_txt(self, presets, i_words=ET.INDEX_FREQUENT_WORDS):
        '''
        Generates the emoji to texts mapping by first reverse mapping the preset
        text-to-emojis map, then extending text lists (which are the map's values).
        '''
        emo_txt = {}
        for txt, lst in presets.items():
            for emo in lst:
                try:
                    emo_txt[emo].append(txt)
                except KeyError:
                    emo_txt[emo] = [txt]
        # print("PRESET emo_txt:", emo_txt)
        i_unchr = ET.INDEX_EMOJI_UNICHRS
        for tup in self.usables:
            emo = tup[i_unchr]
            try:
                emo_txt[emo].extend(tup[i_words])
            except KeyError:
                emo_txt[emo] = tup[i_words]
        return emo_txt

    def rev_txt_to_gen(self):
        '''reverse of gen_txt_to_emo: map each emoji to a list of word-phrases'''
        emo_txt = {}
        for txt, lst in sorted(self.txt_emo.items()):
            # print("emo_txt 1: {} -:> {}".format(txt, lst))
            for emo in lst:
                emo_txt[emo].append(txt)
                if self.verbose > 1:
                    print("emo_txt 3: {} --> {}".format(emo, txt))
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
        The token is to be matched as-is; it will not be transformed in any way.
        If it is meant to match an all lower-case key, the token
        must already be itself all lower-case.
        '''
        try:
            lst = self.txt_emo[token]
            if self.verbose > SHOW_LIST_VALUES:
                print("ET: {} -:> {}".format(token, lst))
        except KeyError:
            if self.verbose > SHOW_TOKEN_TRANS:
                print("ET: {} -:> {}".format(token, None))
            return None
        emo = random.choice(lst) if self.options.random else lst[0]
        if self.verbose > SHOW_TOKEN_TRANS:
            print("ET: {} :-> {} -> {}".format(token, lst, emo))

        return emo

    def emojize_phone(self, phone, space=' '):
        '''
        Return emoji string translation of phone or None.
        Like a bottom-level token, the phone (phonetic string representation)
        is to be matched as-is, and will not be transformed in any way.
        '''
        try:
            lst = self.pro_emo[phone]
            if self.verbose > SHOW_LIST_VALUES:
                print("EP: {} -:> {}".format(phone, lst))
        except KeyError:
            if self.verbose > SHOW_TOKEN_TRANS:
                print("EP: {} -:> {}".format(phone, None))
            return None
        emo = random.choice(lst) if self.options.random else lst[0]
        if self.verbose > SHOW_TOKEN_TRANS:
            print("EP: {} :-> {}".format(phone, emo))
        return emo + space

    def emo_or_txt_token(self, token):
        '''Return translation of token or, failing that, the token itself.'''
        emo = self.emojize_token(token)
        return emo if emo else token

    def minus_s_emo(self):
        '''
        Return string of emoji characters representing "minus S",
        as in singularizing a plural noun.
        '''
        assert '➖' in self.emo_txt
        assert '🇸' in self.emo_txt
        return ' ➖ 🇸 '

    def emojize_plural_noun(self, word, space=' '):
        '''Replaces a plural noun with reduplicated emojis, if one matches the singular form.'''
        singular = singularize(word)
        print("emojize_plural_noun %s -> %s" % (word, singular))
        if singular != word:
            emojis = self.emojize_token(singular)
            if emojis:
                emostr = emojis + space + emojis + space
                if self.verbose > SHOW_NOUN_SINGPLUR:
                    print("EW PLURAL: {} --> {}".format(word, emostr))
                return emostr
        return None

    def emo_synonyms(self, word, pos=None):
        '''
        Returns a list of synonyms of the given word, based on its part of
        speech if specified.
        If word is not already all lower case, put both the orignal
        (partially capitalized) word and its all-lower-cased form in
        the list of synonyms, so as to match proper names.
        That is to support custom emojis and/or syllabified names, but including
        proper names may objuscate common meanings.
        Also note that wordnet always lowercases input words, and returns proper names
        mixed in with lower case words.  You may want to filter out the capitalized
        "synonyms", if you can even call them that.
        '''

        # FIXME: reject synonyms that merely singularize or pluralize the source word.
        rejects = []
        lwrd = word.lower()
        if self.is_singular_noun(lwrd):
            plural = pluralize(lwrd)
            if plural != lwrd:
                rejects.append(plural)
        elif self.is_plural_noun(lwrd):
            singular = singularize(lwrd)
            if singular != lwrd:
                rejects.append(singular)

        # FIXME: stricter: if the source word is singular [plural], so must be any synonyms

        synonyms = [word]
        is_lower = word.islower()
        if pos in [wordnet.ADJ, wordnet.NOUN, wordnet.ADV, wordnet.VERB]:
            try:
                synonyms.extend(wordnet_syn_set(word, pos, is_lower))
                # print("XXX SYNONYMS(%s, %s):" % (word, pos), synonyms)
            except KeyError as kex:
                print("Wordnet Synset KeyError:", kex)
        else:
            try:
                synonyms.extend(EMO_SYNONYMS[word])
                if len(synonyms) > 1:
                    print("YYY EMO_SYNONYMS:", synonyms)
            except KeyError as kex:
                # print("EMO_SYNONYMS KeyError:", kex)
                pass
        if not is_lower:
            lwrd = word.lower()
            synonyms.append(lwrd)
            try:
                synonyms.extend(EMO_SYNONYMS[lwrd])
            except KeyError as kex:
                # print("EMO_SYNONYMS KeyError:", kex)
                pass
        if self.verbose > 11:
            print("SYNS:{} before REJECTS:{}".format(synonyms, rejects))
        synonyms = [syn for syn in synonyms if syn not in rejects]
        return synonyms

    def emojize_word(self, src_word, pos=None, space=' '):
        '''
        Return a translation of src_word into a string of emoji characters,
        or, failing that, return the original src_word.
        '''
        synonyms = self.emo_synonyms(src_word, pos)
        # if len(synonyms) > 1:
        #     synset = set([syn.lower() for syn in synonyms])
        #     if len(synset) > 1:
        #         print("ZZZ emojize_word(%s, %s) with SYNONYMS: " % (src_word, pos), synonyms)
        if self.verbose > SHOW_LIST_VALUES:
            print("EW SYNONYMS: {} -:> {}".format(src_word, synonyms))

        for word in synonyms:
            emojis = self.emojize_token(word)
            if emojis:
                return emojis + space

            if self.options.phonetics:
                phon_word = self.gen_phonetic_word(word)
                if phon_word:
                    for phone_tuple in phon_word.phons():
                        emojis = self.emojize_phone(phone_tuple.phonetics, space)
                        if self.verbose > SHOW_TEXT_PHONETICS:
                            print("PHONETICS: {} --> {} ? ".format(phone_tuple.phonetics, emojis))
                        if emojis:
                            if self.verbose > SHOW_TOKEN_TRANS:
                                print("EW  PHONE: {} -> {} -:> {}".format(word, phone_tuple.phonetics, emojis))
                            return emojis # space already appended
                        if len(phone_tuple.syllables) > 1:
                            emo_lst = []
                            for syllable in phone_tuple.syllables:
                                emojis = self.emojize_phone(syllable, space)
                                if not emojis:
                                    break
                                emo_lst.append(emojis)
                            else:
                                return '➖ '.join(emo_lst) # space already appended

            if self.options.singularize and self.is_plural_noun(word):
                emostr = self.emojize_plural_noun(word, space)
                if emostr:
                    return emostr

                # At least when subtraction is allowed, lip == lips - S ~= <kiss> - S == 💋 - S == 💋 <-> <S>
                # NB: Not elif, because some nouns can be either singular and plural, e.g. fish, sheep, dice,
                # briefs,data, agenda, heuristics,
            if self.options.pluralize:
                if self.is_singular_noun(word):
                    plural = pluralize(word)
                    if plural != word:
                        emojis = self.emojize_token(plural)
                        if emojis:
                            emostr = emojis + self.minus_s_emo()
                            if self.verbose > SHOW_NOUN_SINGPLUR:
                                print("EW SINGLE: {} --> {}".format(word, emostr))
                            return emostr

        hyphenated = src_word.split('-')
        if len(hyphenated) > 1:
            return ' ➖ '.join([self.emo_or_txt_token(token) for token in hyphenated])
        return src_word

    def emojize_match(self, match_obj, space=' '):
        '''Translate word tokens from a regex match.'''
        word = match_obj.group()
        return self.emojize_word(word, space=space)

    def emojize_sentence_beg_mid_end(self, sentence, mid_translator, space=' '):
        ''' Segment sentence into beg, mid, and end, translate each, then recombine, where:
            beg = chars before any words
            end = chars after all words
            mid = everthing between beg and end.
        '''
        beg, body, end = text_regex.sentence_body_and_end(sentence)
        if self.verbose > SHOW_TEXT_DIVISION:
            print("beg(%s)  body(%s)  end(%s)" % (beg, body, end))

        subs = mid_translator(body)
        #print("ESBME: mid(%s) --> subs(%s): " % (body, subs))
        tend = self.emojize_token(end)
        if tend:
            #print("ESBME: end(%s) --> tend(%s): " % (end, tend)
            end = space + tend
        emo_tran = ''.join([beg, subs, end])
        return emo_tran

    def emojize_text_syntags(self, text, space=' '):
        '''
        Translate text word by word to emojis, where possible, using regex substitution.
        By design, text is to be the body of a sentence: the part between any leading or
        trailing punctuation.
        TODO: decouple translation from sentence rendering.  How?
            1. Use same tokenizer for extraction and substitution, and EITHER:
                a. Use regex-replacement to convert body into a template for string-substitution.  OR:
                b. Cut everything into a sequence of strings, translate tokens, and reconcatenate.
        '''
        # emojize_match_bound = partial(self.emojize_match, space=space)

        tokens = text_regex.RE_NOT_NON_WORD_TOKEN.split(text)
        # strips = [tok.strip() for tok in tokens]
        twords = tokens[1::2]
        tagged = nltk.pos_tag(twords)
        print_tagged(tagged)
        subbed = []
        idx, size = 0, len(tokens)
        while idx < size:
            if idx % 2:                     # odd-indexed tokens are wordy
                wrd = tokens[idx]
                if idx + 2 < size and tokens[idx + 1].isspace():
                    bigram = wrd + ' ' + tokens[idx + 2]
                    if self.verbose > SHOW_TEXT_BIGRAMS:
                        print("BIGRAM: ", bigram)
                    lst = self.txt_emo.get(bigram)
                    if not lst and not bigram.islower():
                        lst = self.txt_emo.get(bigram.lower())
                    if lst:
                        emo = random.choice(lst) if self.options.random else lst[0]
                        subbed.append(emo + space)
                        if self.verbose > SHOW_TEXT_BIGRAMS:
                            print("BIGRAM: APPENDED {}  FROM list( {} )".format(emo, lst))
                        idx += 3
                        continue
                # If no bigram match was found, look for single-word match.
                pos = tagged[idx // 2][1][0].lower()
                subbed.append(self.emojize_word(wrd, pos, space=' '))
            else:
                subbed.append(tokens[idx])
            idx += 1
        subs = ''.join(subbed)
        return subs


    def emojize_text_subs(self, text, space=' '):
        '''
        Translate text word by word to emojis, where possible, using regex substitution.
        By design, text is to be the body of a sentence: the part between any leading or
        trailing punctuation.
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
        FIXME: replace splitter with a non-destructive version that keeps the seperators.
        The return product should be a tagged list, i.e. a list of pairs [(token, {word|fill}), ...]
        '''
        srcs = text_regex.words_split_out(txt_phrase.strip())
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
        '''Is uchr an emoji or any part of an emoji (as in a modifier)?'''
        return self.emo_chr_counts[uchr]

    def is_emoji_key(self, uchr):
        '''Is uchr a key in the emoji to text translation table?'''
        return uchr in self.emo_txt

    def textize_emo_span_recurse_busted(self, emo_span):
        '''FIXME: busted.  translate a string or slice of emojis into a text string'''
        if self.verbose > 2:
            print("TSPAN: span({})".format(emo_span))
        try:
            lst = self.emo_txt[emo_span]
            if self.verbose > 1:
                print("TES: {} -:> {}".format(emo_span, lst))
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
                    print("TES: {} -:> {}".format(uchr, lst))
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
                    print("append_to_prev_list:  ({})  -:> ({})".format(word, prev_words))
                return prev_words
        word = random.choice(word_calcs) if self.options.random else word_calcs[0]
        return [word]


    def textize_emo_span_from_end(self, emo_span, prev_words=None):
        '''
        Try to translate a string of emoji chars into a string of English text
        by recursively dividing the string of emoji chars (or "emo_span") into
        a sequence of whole emojis, backing up greedily from the end, and
        translating each one individually.  The string  (or "span") as a whole
        should have already been tried as one key, and it  should not contain
        any spaces.  Going backward from the end simplifies the parsing of
        complex emojis, because appended modifiers can be passed over as found.
        Still, some modifiers are whole emojis in their own right.
        This inherent ambiguity may lead to poor translations.
        Returns a single string containing one word or a phrase of words
        separated by single spaces.  If no emoji to text translation is found,
        the original span is returned as-is.
        '''
        if  self.verbose > SHOW_TEXT_DIVISION:
            print("TESFE A:  span({})  prev_words({})".format(emo_span, prev_words))
        # emo_span = emo_span.rstrip() -- should no longer need (or want) to strip.

        # If the this (whole or remaining) span can be parsed as a single emoji
        # with an (English) translation, just return it, concatenated with any
        # words already parsed.
        try:
            # if emo_span[-1] == space:
            #     lst = self.emo_txt[emo_span[0:-1]]
            # else:
            #     lst = self.emo_txt[emo_span]
            word_calcs = self.emo_txt[emo_span]
            if self.verbose > 5:
                print("TESFE B: {} -:> {}".format(emo_span, word_calcs))
            return self.append_to_prev_list(word_calcs, prev_words).reverse()
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
                    print("while min({})  max({})  substr({})  calcs({})".format(
                        min_index, max_index, substr, word_calcs))
                if len(word_calcs) > 0:
                    txt = self.append_to_prev_list(word_calcs, prev_words)
                    if self.verbose > SHOW_TEXT_DIVISION:
                        print("TESFE D: Calling textize_emo_span_from_end({}, {})".format(
                            emo_span[0:max_index], txt))
                    more_words = self.textize_emo_span_from_end(emo_span[0:max_index], txt)
                    if more_words:
                        return more_words
                max_index -= 1
        return emo_span          # string did not parse


    def _textize_emo_list(self, emo_list, space=' '):
        '''
        Try to translate each emoji or string of several emojis into a list of strings,
        each one representing words or phrases.  If no translation is found for an item
        in the input list, that item is places as-is in the output list.
        The output list will have the same number of items (length) as the input list.
        TODO: Helper methods.
        '''
        if  self.verbose > SHOW_LIST_VALUES:
            print("TEL A input{}".format(emo_list))

        txt_list = []           # output
        old_emos = None         # to detect reduplication
        for idx, emo_str in enumerate(emo_list):
            # Special case: reduplication
            if old_emos == emo_str:
                calc = txt_list[-1]
                # FIXME TODO NEXT: Test should not be is this calc singular,
                # but is there any calc for the emo that is singular.
                if self.is_singular_noun(calc):
                    txt_list[-1] = pluralize(calc)
                else:
                    txt_list.append(calc)
                continue
            # Special case: singularization using "<minus><S>" (➖ 🇸)
            elif idx > 1 and emo_str == '🇸' and old_emos == '➖':
                all_calcs = self.emo_txt.get(emo_list[idx - 2])
                old_emos = emo_str
                if all_calcs:   # could be None if we didn't forward translate the txt to emo
                    sing_calcs = []
                    for calc in all_calcs:
                        all_words = calc.split()
                        last_word = all_words[-1]
                        if self.is_plural_noun(last_word):
                            sing_calcs.append(all_words)
                    if sing_calcs:
                        sing_words = random.choice(sing_calcs) if self.options.random else sing_calcs[0]
                        sing_last = singularize(sing_words[-1])
                        if len(sing_words) > 1:
                            sing_words[-1] = sing_last
                            sing_calc = space.join(sing_words)
                        else:
                            sing_calc = sing_last
                        if self.verbose > SHOW_NOUN_SINGPLUR:
                            print("TEL SING:  list{}  prev{} ::> sing{}  old({})  now({}) -> ({})".format(
                                emo_list, all_calcs, sing_calcs, old_emos, emo_str, sing_calc))
                        txt_list[-2] = sing_calc
                        txt_list.pop()  # truncate list by popping off the calc for <-> ('➖')
                        continue
            else:
                old_emos = emo_str
            try:
                # Is the whole emo_str a key?
                word_calcs = self.emo_txt[emo_str]
                calc = random.choice(word_calcs) if self.options.random else word_calcs[0]
                if self.verbose > SHOW_LIST_VALUES:
                    print("TEL emo_txt: {} -:> {} --> ({})".format(emo_str, word_calcs, calc))
                txt_list.append(calc)
            except KeyError:
                # Else divide the string recursively into parts, and try to tranlate each part.
                if self.verbose > SHOW_TEXT_DIVISION:
                    print("TEL : Calling TESFE(%s)" % emo_str)
                calc = self.textize_emo_span_from_end(emo_str)
                txt_list.append(calc)
        return txt_list

    def textize_emo_span(self, emo_span):
        '''translate string of emojis to text'''
        emo_span.rstrip()
        try:
            # Is the whole span a key?
            return self.emo_txt[emo_span]
        except KeyError:
            emo_list = emo_span.split()         # NB: call plain split(), not split(space)
            return self._textize_emo_list(emo_list)

    def textize_sentence_subs(self, emo_sent, space=' '):
        '''
        return text with each emoji replaced by a value from emo_txt.
        FIXME: emoji combinations representing a single word will not always
        translate back to the orignal word, but turn into a word combination
        calc, which may be gibberish or worse.
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
                    if self.verbose > SHOW_LIST_VALUES:
                        print("TSS list: {}".format(txt_list))
                    txt_join = space.join(txt_list)
                    if self.verbose > SHOW_TOKEN_TRANS:
                        print("TSS REBUS: {} --> {}".format(emo_span, txt_join))
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
                txt_join = space.join(txt_list)
                if self.verbose > SHOW_LIST_VALUES:
                    print("TSS list: {}".format(txt_list))
                if self.verbose > SHOW_TOKEN_TRANS:
                    print("TSS REBUS: {} --> {}".format(emo_span, txt_join))
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
        emojize_body = self.emojize_text_subs
        if self.options.split_join:
            emojize_body = self.emojize_text_split_join
        else:
            emojize_body = self.emojize_text_syntags
        # NOTE: emojize_text_subs is being deprecated?
        return self.emojize_sentence_beg_mid_end(sentence, emojize_body, space=' ')

    def textize_sentence(self, sentence):
        '''translate emoji sentence to text according to options'''
        return self.textize_sentence_subs(sentence)

    def trans_to_emo_and_back(self, sentence):
        '''translate text sentence to emoji and back, showing stages according to options'''
        print("=====> src => txt (%s)" % sentence)
        emo_sent = self.emojize_sentence(sentence)
        print("=====> txt => emo (%s)" % emo_sent)
        txt_sent = self.textize_sentence(emo_sent)
        print("=====> emo => txt (%s)" % txt_sent)

        dist = editdistance.eval(sentence, txt_sent)
        print("Edit distance: {:>4}".format(dist))

def shuffled_list(seq):
    '''Randomly shuffle an iterable into a list.
    Call this on the list of indices to avoid modifying a source list in-place.'''
    shuffled = list(seq)
    random.shuffle(shuffled)
    return shuffled

def translate_sentences(options):
    '''Test translation from Enlish to emojis and back.'''
    emotrans = EmoTrans(options)
    txt_emo = emotrans.txt_emo
    emo_txt = emotrans.emo_txt
    if options.txt_emo:
        show_sorted_dict(txt_emo, 0)
    if options.emo_txt:
        show_sorted_dict(emo_txt, 0)
    if options.sentence:
        emotrans.trans_to_emo_and_back(options.sentence)
        exit(0)

    # rand_order = shuffled_list(range(len(SENTENCES)))
    # for idx in rand_order:
    #     emotrans.trans_to_emo_and_back(SENTENCES[idx])
    #     print()

    if not options.order:
        random.shuffle(SENTENCES)
    for sentence in SENTENCES:
        emotrans.trans_to_emo_and_back(sentence)
        print()

    if options.text_file:
        for sentence in text_fio.read_text_lines(options.text_file, options.charset):
            emotrans.trans_to_emo_and_back(sentence)

def main():
    '''test english -> emoji translation'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('-arithmetic', action='store_true',
                        help='use addition and subtraction of letters or syllables (rebus)')
    parser.add_argument('-all_skin_tones', action='store_true',
                        help='use all skin tones for hads, faces, etc.')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-end', dest='print_end', type=str, nargs='?', const=' ', default='\n',
                        help='end= argument to give print')
    parser.add_argument('-extract_words', action='store_true',
                        help='extract words from emotuples')
    parser.add_argument('-input', dest='sentence', type=str, nargs='?', default=None,
                        const=DEFAULT_SENTENCE, help='input a sentence to translate (or use default)')
    parser.add_argument('-emo_txt', action='store_true',
                        help='show the emoji-to-text mapping')
    parser.add_argument('-flags', action='store_true',
                        help='use flag emojis in translations of words not representing countries')
    parser.add_argument('-multiples', action='store_true',
                        help='use multiple emojis for words when needed (not only for presets)')
    parser.add_argument('-no_articles', '-noa', action='store_true',
                        help='remove articles (a, an, the)')
    parser.add_argument('-order', '-original', action='store_true',
                        help='Translate and show sentences in original order, not in random order')
    parser.add_argument('-phonetics', action='store_false',
                        help='Disable phonetic matching (which is on by default)')
    parser.add_argument('-pluralize', action='store_false',
                        help='Disable pluralization (which is on by default)')
    # parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
    #                     help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-random', action='store_true',
                        help='Choose random emojis or words from translation lists '\
                             '(instead of always choosing the first)')
    parser.add_argument('-singularize', action='store_false',
                        help='Disable singularization (which is on by default)')
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

    if args.extract_words:
        print("Collecting words from emotuples.nemo_tuples...")
        words = set()
        emt = ET.EmoTuples()
        for nut in emt.nemo_tuples:
            for phrase in nut.words:
                words.update(text_regex.gen_normal_word_tokens(phrase, 2))
        text_regex.print_sorted(words, args.print_end)
        # words = extract_words_from_file(args.input_file, gen_normal_word_tokens))
        exit(0)

    # if args.verbose > 7:
    #     print("module emoji:", EJ)
    #     print("Type(args): ", type(args))
    #     print(args)
    translate_sentences(args)

if __name__ == '__main__':
    START_TIME = time.time()
    main()
    print("----- %.4f seconds elapsed -----" % (time.time() - START_TIME))
