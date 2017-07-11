#!/usr/bin/env python3
# -*- encoding: <utf-8> -*-
# Sprax Lines       2017.04.01      Written with Python 3.5
# To re-import a library in Python 3.4+ (re-import), do:
# import importlib
# importlib.reload(nameOfModule)
'''text filter functions'''

import argparse
import heapq
import os.path
import re
import math
import string
import sys
import text_ops
from utf_print import utf_print

###############################################################################
TRANS_NO_WHAT = str.maketrans(u"\u2018\u2019\u201c\u201d", "\'\'\"\"")
TRANS_NO_SMART = str.maketrans("\x91\x92\x93\x94", "''\"\"")
TRANS_NO_PUNCT = str.maketrans('', '', string.punctuation)

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
        return in_str.translate(self.translation)
    # def translate(self, in_str):
    #     return translate_iso_to_ascii(in_str)

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


def translate_para_file(para_filter, in_path, out_path, charset='utf8'):
    '''Generator yielding filtered paragraphs from a text file'''
    with open(in_path, 'r', encoding=charset) as in_text:
        with open(out_path, 'w') as out_file:
            for para in text_ops.paragraph_iter(in_text):
                output = para_filter.filter_line(para)
                print(output if output else ' ', file=out_file)

def translate_lines_in_file(line_translators, in_path, out_path, charset='utf8'):
    '''Translate input line by line to output file'''
    with open(in_path, 'r', encoding=charset) as in_text:
        with (sys.stdout if out_path == '-' else open(out_path, 'w')) as out_file:
            for line in in_text:
                for translator in line_translators:
                    line = translator.translate(line)
                if line:
                    print(line, file=out_file)

########################################################

def translate_file(in_path, out_path, opt):
    """Rewrite a text file."""

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

def abs_path(dir_spec, file_spec):
    '''Returns an absolute path based on a dir_spec and a (relative) file_spec'''
    if os.path.isabs(file_spec):
        return file_spec
    return os.path.join(dir_spec, file_spec)

def filter_text_file():
    '''Filter lines or sentences in a text file.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test text_filters")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/Text',
                        help='directory to search for input_file')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each filtered sentence')
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

    if args.verbose > 3:
        print("output_file: <{}>".format(args.output_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    in_path = abs_path(args.text_dir, args.input_file)
    out_path = args.output_file
    if out_path != '-':
        out_path = abs_path(args.text_dir, args.output_file)

    translate_file(in_path, out_path, args)

if __name__ == '__main__':
    filter_text_file()
