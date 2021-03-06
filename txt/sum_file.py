#!/usr/bin/env python3
# -*- encoding: <utf-8> -*-
# Sprax Lines       2017.04.01      Written with Python 3.5
# sum_file.py (2019.06) based on test_filters.py (2017.04.01)
# To re-import a library in Python 3.4+ (re-import), do:
# import importlib
# importlib.reload(nameOfModule)
'''selected text-filtering functions, e.g. for git blame output'''

import argparse
import heapq
import os.path
import re
import math
import pdb
from pdb import set_trace
import string
import sys
import text_ops
from utf_print import utf_print
import inflection
from collections import defaultdict
# from collections import Counter


###############################################################################
TRANS_NO_WHAT = str.maketrans(u"\u2018\u2019\u201c\u201d", "\'\'\"\"")
TRANS_NO_SMART = str.maketrans("\x91\x92\x93\x94", "''\"\"")
TRANS_NO_PUNCT = str.maketrans('', '', string.punctuation)
TRANS_NO_DIGITS = str.maketrans('', '', string.digits)

UNICODE_TO_ASCII = str.maketrans({
    u"\u2018" : "'",
    u"\u2019" : "'",
    u"\u201c" : '"',
    u"\u201d" : '"',
    })

ISO_TO_ASCII = str.maketrans({
    "`" : "'",
    u"\x91" : "'",
    u"\x92" : "'",
    u"\x93" : '"',
    u"\x94" : '"',
    u"\x97" : '--',
    u"\xf0" : '-',
    })

def translate_smart_quotes(in_str, table=TRANS_NO_SMART):
    '''Replace curly quotes with straight ones.'''
    return in_str.translate(table)

def translate_iso_to_ascii(in_str):
    '''Replace curly quotes with straight ones, etc.'''
    return in_str.translate(ISO_TO_ASCII)

def remove_punctuation(in_str, table=TRANS_NO_PUNCT):
    '''Remove all string.punctuation characters.'''
    return in_str.translate(table)

def replace_quotes(instr):
    '''Replace curly quotes one-by-one (slow)'''
    return instr.replace("\x91", "'").replace("\x92", "'")\
                .replace("\x93", '"').replace("\x94", '"')

def replace_emdashes(in_str):
    '''Replace each em-dash with two hyphens (--).'''
    return in_str.replace("\x97", "--")

#TODO: if really bored, implement reverse_trans for each class

class IsoToAscii:
    '''Translate non-ASCII characters to ASCII or nothing'''
    translation = ISO_TO_ASCII
    def translate(self, in_str):
        '''Translate non-ASCII characters to ASCII or nothing'''
        try:
            return in_str.encode('ascii')
        except UnicodeEncodeError:
            out = in_str.translate(self.translation)
            return ''.join([asc for asc in out if ord(asc) < 128])

class NoSpaceBeforePunct:
    '''Eliminate spaces before punctuation'''
    regex = re.compile(r' ([!%,./:;?])')
    def translate(self, in_str):
        '''Eliminate spaces before punctuation'''
        result = re.sub(r'\s+', ' ', in_str)
        return self.regex.sub(r'\1', result)

class TwoSingleQuoteToDoubleQuote:
    '''Translate two single-quotes to one double-quote marker'''
    regex = re.compile(" ''([ !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]|$)")
    def translate(self, in_str):
        '''Translate two single-quotes to one double-quote marker'''
        return self.regex.sub(r' "\1', in_str)

class JoinContractions:
    '''Rejoin tokenized contractions.'''
    regex = re.compile(r"\b(.*) (n't|'s) ")
    def translate(self, in_str):
        '''Rejoin tokenized contractions.'''
        return self.regex.sub(r"\1\2 ", in_str)

class JoinPossessive:
    '''Rejoin tokenized word and possive apostrophe marker'''
    regex = re.compile(" ' ")
    def translate(self, in_str):
        '''Rejoin tokenized word and possive apostrophe marker'''
        return self.regex.sub(r"' ", in_str)

class JoinQuoted:
    '''Rejoin quatation marks with the text they quote'''
    regex = re.compile(r"([\"']) ((?:\\\1|.)*?) \1")
    def translate(self, in_str):
        '''Rejoin quatation marks with the text they quote'''
        return self.regex.sub(r"\1\2\1", in_str)

def filter_non_ascii(in_str):
    '''deprecated because 'filter'''
    return "".join(filter(lambda x: ord(x) < 128, in_str))

def remove_non_ascii(in_str):
    '''filter out non-ASCII characters'''
    return "".join(i for i in in_str if ord(i) < 128)

def translate_to_ascii(in_str):
    '''try to translate any text to ASCII'''
    try:
        return translate_iso_to_ascii(in_str)
    except UnicodeDecodeError:
        return in_str

###############################################################################

def read_lines_to_ascii(file_spec, charset='utf-8'):
    '''read and return all lines of a text file as a list of ASCII str'''
    with open(file_spec, 'r', encoding=charset) as text:
        for line in text:
            # utf_print(line.rstrip())
            line = line.decode(encoding=charset, errors='ignore')
            # .encode('ascii', errors='ignore')
            # line = str(line, charset, errors='ignore')
            # .encode('ascii', errors='ignore')
            yield line.rstrip()

def utf_print_words(fspec):
    '''print each word in an ASCII or UTF-8 encoded text'''
    with open(fspec, 'r', encoding="utf8") as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    utf_print(word)
            utf_print(words)


def rank_dict_by_value(summary_count, ranking):
    '''Return the highest ranked N dictionary entries.'''
    return heapq.nlargest(summary_count, ranking, key=ranking.get)

def resolve_count(sub_count, percent, total_count):
    '''returns reconciled sub-count and percentage of total, where count trumps percentage'''
    if not sub_count:
        sub_count = int(math.ceil(percent * total_count / 100.0))
    if  sub_count > total_count:
        sub_count = total_count
    if  sub_count < 1:
        sub_count = 1
    percent = sub_count * 100.0 / total_count
    return sub_count, percent


def map_file(function, in_path, out_path, charset='utf8'):
    '''Apply function to every line in the input file'''
    with open(in_path, 'r', encoding=charset) as text:
        with open(out_path, 'w') as out_file:
            for line in text:
                output = function(line.rstrip())
                if output:
                    print(output, file=out_file)


def translate_para_file(para_filter, in_path, out_path, charset='utf8'):
    '''Generator yielding filtered paragraphs from a text file'''
    with open(in_path, 'r', encoding=charset) as text:
        with open(out_path, 'w') as out_file:
            for para in text_ops.paragraph_iter(text):
                output = para_filter.filter_line(para)
                print(output if output else ' ', file=out_file)

def translate_lines_in_file(line_translators, in_path, out_path, charset='utf8'):
    '''
    Translate input line by line to output file.
    Usage: translate_lines_in_file(line_translators, in_path, out_path, charset='utf8')
    '''
    with open(in_path, 'r', encoding=charset) as text:
        with (sys.stdout if out_path == '-' else open(out_path, 'w')) as out_file:
            for line in text:
                for translator in line_translators:
                    line = translator.translate(line)
                if line:
                    print(line, file=out_file)

########################################################

def translate_file(in_path, out_path, opt):
    """Rewrite a text file."""

    if opt.git_sum:
        return add_git_sums_to_file(in_path, out_path, opt.charset)

    # Announce output:
    print(in_path, '====>', '<stdout>' if out_path == '-' else out_path)
    print('-------------------------------------------------------------------')
    translators = [IsoToAscii(),
                   JoinContractions(),
                   NoSpaceBeforePunct(),
                   TwoSingleQuoteToDoubleQuote(),
                   JoinPossessive(),
                   JoinQuoted()]
    translate_lines_in_file(translators, in_path, out_path, opt.charset)

###############################################################################

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

def plural_if_diff(word):
    '''return the plural form of word if different from the singular, else None'''
    plur = pluralize(word)
    sing = singularize(word)
    return plur if plur != sing else None

def singular_if_diff(word):
    '''return the singular form of word if different from the plural, else None'''
    plur = pluralize(word)
    sing = singularize(word)
    return sing if plur != sing else None

###############################################################################

def abs_path(dir_spec, file_spec):
    '''Returns an absolute path based on a dir_spec and a (relative) file_spec'''
    if os.path.isabs(file_spec):
        return file_spec
    return os.path.join(dir_spec, file_spec)

########################################################

AUTHOR_NAME = {
    'dav' : 'DMSJ',
    'dms' : 'DMSJ',
    'spr' : 'Sprax',
    'syl' : 'Syler',
    '5yl' : 'Syler',
    'dun' : 'Duncan',
    'alb' : 'Albert',
    'jay' : 'JayMW',
    'mit' : 'MHebert',
    'ter' : 'T2',
    'dex' : 'Dexai',
}
AUTHOR_NAME = defaultdict(lambda:"OTHER", AUTHOR_NAME)

def print_author_count(ddct, out_file=sys.stdout, prefix="git_blames"):
    '''Print the author_count dict to stdout (default) or a file'''
    total = 0.0
    for _, val in ddct.items():
        total += val
    for key, val in sorted(ddct.items(), key=lambda dit: dit[1], reverse=True):
        # author = AUTHOR_NAME[key]
        author = key
        percent = val * 100.0 / total
        print("%s:  %14s: %6d %7.2f%%" % (prefix, author, val, percent), file=out_file)

def add_git_sums_to_file(in_path, out_path, charset='utf8'):
    '''
    Translate input line by line to output file.
    Usage: translate_lines_in_file(line_translators, in_path, out_path, charset='utf8')
    '''
    print("GIT SUM: in/out: %s -> %s" % (in_path, out_path))
    out_of_sum = True
    with open(in_path, 'r', encoding=charset) as text:
        with (sys.stdout if out_path == '-' else open(out_path, 'w')) as out_file:
            total_counts = defaultdict(int)
            for line in text:
                # set_trace()
                line = line.rstrip()
                toks = re.split(r'\W+', line.lstrip())
                if len(toks) > 2 and toks[1] == 'author':
                    author = toks[2]
                    count = int(toks[0])    # TODO: check if parseint succeeds
                    # print("================= %s => %d" % (author, count))
                    if out_of_sum:
                        out_of_sum = False
                        author_count = defaultdict(int)
                    author_count[author] += count
                    total_counts[author] += count
                else:
                    if not out_of_sum:
                        print_author_count(author_count, out_file=out_file)
                        out_of_sum = True
                    elif line:
                        print(line, file=out_file)
            print_author_count(total_counts, out_file=out_file, prefix="GIT_TOTALS")

def sum_text_file():
    '''Filter lines or sentences in a text file.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test text_filters")
    parser.add_argument('in_path', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/Text',
                        help='directory to search for in_path')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-git_sum', action='store_true',
                        help='output original file with added git blame summaries')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each filtered sentence')
    parser.add_argument('-map_file', action='store_true',
                        help='test map_file')
    parser.add_argument('-number', dest='max_lines', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-out_path', type=str, nargs='?', default='-',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-truncate', dest='max_words', type=int, nargs='?',
                        const=8, default=0,
                        help='truncate sentences after MAX words (default: INT_MAX)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.map_file:
        # map_file(singular_if_diff, args.in_path, args.out_path)
        map_file(singularize, args.in_path, args.out_path)
        exit(0)

    if args.verbose > 7:
        print("out_path: <{}>".format(args.out_path))
        print("args:", args)
        print(__doc__)
        exit(0)

    in_path = abs_path(args.text_dir, args.in_path)
    out_path = args.out_path
    if out_path != '-':
        out_path = abs_path(args.text_dir, args.out_path)

    translate_file(in_path, out_path, args)

if __name__ == '__main__':
    sum_text_file()
