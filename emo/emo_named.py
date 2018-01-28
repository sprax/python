#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plans:
    Tuple data:
        Generate the data in emo_tuples as one list of tuples, whose elements refer
            to one or more dicts, keyed on primary unicodes.  (Expect augmented unicodes,
            or unicode pairs, to share the words, say, of the primary unicode/emoji).

    Phonetics:
        Use CMU for now.  Keep it virtual?  Or look up all prons when generating the
            tuple data?  Probably the latter.
        Yes, the latter, and create an "additional prons list" that gets added in,
            optionally, after CMU if not already included.

    Syllabary:
        Words|phrases -> words >= [phonetic syllables reprs]
        Emojis >= [phonetic syllable reprs]
        Text => <syllabic repr> => <emoji>

    Words:
        Dicts and supplemental dicts, but all with POS.  The non POS version should
            just be the set of POS-annotated words stripped of POS.

    Phrases:
        TODO

    Verbs/activities:
        ':person_Xing_Y' => ['person Xing Y', 'Y player'] with male/female variants

    Images:
        Emojis' meanings may be represent using other emojis or images in general.
        Images may translate directly to emojis with no intermediary text or word semantics.

EMO_HELPERS = {
    'code'  : "hyphenated hexcodes",
    'len'   : "how many hexcodes",
    'order' : "ordinal sequence number",
    'category'  : "emoji category (Apple)",
    'flags' : "for usage filters",
    'chr'   : "emoji as a character",
    'shortname' : "emoji shortname",
    'alternates': "also know as/list of other names"
    'texts' : "TODO: value in dict keyed by code",
    'syllables' : "TODO: value in a dict keyed by words in text values",
    'images': "TODO: resource IDs (for files or DB rows)",
    'img_features': "TODO: visual syllabary",
    'sounds': "TODO: sounds need not be only pronounced words",
    'emotions': "TODO: reduced palette of emotional contents",
}
'''

import argparse
# import re
# from collections import defaultdict
from collections import namedtuple

import emo_tuples as E_T

INDEX_HEX_CHR_CODES  = 0
INDEX_UNICHR_LENGTH  = 1
INDEX_DISPLAY_ORDER  = 2
INDEX_EMOJI_CATEGORY = 3
INDEX_DISPLAY_FLAGS  = 4
INDEX_EMOJI_UNICHRS  = 5
INDEX_FREQUENT_WORDS = 6
INDEX_WORD_SYLLABLES = 7
INDEX_SHORT_NAME     = 8
INDEX_ALTERNATIVES   = 9  # not used much; may go away
COUNTRY_FLAGS_RANGE  = range(2120, 2377)

EMO_TUPLES = E_T.gen_emo_tuples()

NemoTuple = namedtuple('NemoTuple', 'code size ord categ flags chrs words short')

def gen_named_emo_tuples(emotups):
    '''generate list of NemoTuples from all emo tuples'''
    nemos = []
    for tup in emotups:
        nemos.append(NemoTuple(tup[INDEX_HEX_CHR_CODES], tup[INDEX_UNICHR_LENGTH],
            tup[INDEX_DISPLAY_ORDER], tup[INDEX_EMOJI_CATEGORY],
            tup[INDEX_DISPLAY_FLAGS], tup[INDEX_EMOJI_UNICHRS],
            tup[INDEX_FREQUENT_WORDS], tup[INDEX_SHORT_NAME]))
    return nemos

class EmoTuples:
    '''class to contain associations between emojis and English text'''
    def __init__(self):
        self.emo_tuples = EMO_TUPLES
        self.emo_header = E_T.EMO_HEADER
        self.nemo_tuples = gen_named_emo_tuples(EMO_TUPLES)

    def print_emo_tuples(self, category):
        '''print all emo tuples'''
        print(self.emo_header)
        print("-----------------------------------------------------------------------------------------")
        for tup in self.emo_tuples:
            if not category or category == tup[INDEX_EMOJI_CATEGORY]:
                print(tup)
        print("-----------------------------------------------------------------------------------------")
        print(self.emo_header)

    def count(self, category):
        '''how many emojis in this category.  TODO: better way of counting?'''
        cats = [tup for tup in self.emo_tuples if tup[INDEX_EMOJI_CATEGORY] == category]
        return len(cats)

def test_emo_tuples(opts):
    '''test the data'''
    emt = EmoTuples()
    emt.print_emo_tuples(opts.category)

def main():
    '''test english/emoji tuple table'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input_file')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-category', type=str, nargs='?', default='',
                        help='category to show, e.g. "people" (default: None)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    # test_misc()
    test_emo_tuples(args)

if __name__ == '__main__':
    main()
