#!/usr/bin/env python3
# -*- encoding: <utf-8> -*-
# Sprax Lines       2017.04.01      Written with Python 3.5
# To re-import a library in Python 3.4+ (re-import), do:
# import importlib
# importlib.reload(nameOfModule)
'''read text file, print regex-split words.'''

import argparse
import errno
import heapq
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

def translate_iso_to_ascii(in_str):
    '''Replace curly quotes with straight ones, etc.'''
    return in_str.translate(ISO_TO_ASCII)

class IsoToAscii:
    '''Translate non-ASCII characters to ASCII or nothing'''
    translation = ISO_TO_ASCII
    def translate(self, in_str):
        return in_str.translate(self.translation)
    # def translate(self, in_str):
    #     return translate_iso_to_ascii(in_str)

class AsciiToCompact:
    '''Eliminate extra spaces and punctuation'''
    regex = re.compile(r' ([,;.?!])')

    def translate(self, in_str):
        result = re.sub(r'\s+', ' ', in_str)
        return self.regex.sub(r'\1', result)

class JoinContractions:
    "Rejoin tokenized contractions."
    regex = re.compile(r"\b(.*) (n't|'s) ")

    def translate(self, in_str):
        return self.regex.sub(r"\1\2 ", in_str)

class MonoPunct:
    regex = re.compile(" '' ")

    def translate(self, in_str):
        return self.regex.sub(r' " ', in_str)

class JoinPossessive:
    regex = re.compile(" ' ")

    def translate(self, in_str):
        return self.regex.sub(r"' ", in_str)


# deprecated because 'filter'
def filter_non_ascii(in_str):
    return "".join(filter(lambda x: ord(x) < 128, in_str))

def remove_non_ascii(in_str):
    return "".join(i for i in in_str if ord(i) < 128)

def translate_to_ascii(in_str):
    try:
        return translate_iso_to_ascii(in_str)
    except:
        return in_str

def translate_iso_to_ascii(in_str):
    return in_str.translate(ISO_TO_ASCII)

def translate_smart_quotes(in_str, table=TRANS_NO_SMART):
    return in_str.translate(table)

def remove_punctuation(in_str, table=TRANS_NO_PUNCT):
    return in_str.translate(table)

def replace_quotes(instr):
    return instr.replace("\x91", "'").replace("\x92", "'")\
                .replace("\x93", '"').replace("\x94", '"')

def replace_emdashes(in_str):
    return in_str.replace("\x97", "--")

###############################################################################


#TODO: try to read ascii or utf-8 and failover to iso-8859-1, etc.

def read_lines(file_spec, charset='utf8'):
    '''read and return all lines of a text file as a list of str'''
    with open(file_spec, 'r', encoding=charset) as text:
        for line in text:
            # utf_print(line.rstrip())
            yield line.rstrip()


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

def read_text_file(file_spec):
    '''read and return all contents of file as one str'''
    try:
        return read_file(file_spec, 'utf-8')
    except UnicodeDecodeError:
        return read_file(file_spec, 'iso-8859-1')

def read_file(file_spec, charset='utf-8'):
    '''read and return all contents of file as one str'''
    with open(file_spec, 'r', encoding=charset) as src:
        return src.read()

def read_file_eafp(file_spec, charset='utf-8'):
    '''
    Read contents of file_spec.
    Easier to Ask for Forgiveness than ask Permission.
    '''
    try:
        src = open(file_spec, 'r', encoding=charset)
    except IOError as ex:
        if ex.errno != errno.ENOENT:
            raise
        print("WARNING: {} does not exist".format(file_spec))
        return None
    else:
        text = src.read()
        src.close()
        return text

def utf_print_words(fspec):
    with open(fspec, 'r', encoding="utf8") as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    utf_print(word)
            utf_print(words)

def print_words(file_spec):
    '''print all white-space separated words read from a file'''
    with open(file_spec, 'r') as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    print(word)
            print(words)

def rank_dict_by_value(summary_count, ranking):
    '''Return the highest ranked N dicionary entries.'''
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


def open_out_file(file_spec, label='text'):
    if file_spec:
        if file_spec in ['-', 'stdout']:
            return sys.stdout
        else:
            try:
                out_file = open(file_spec, 'w')
            except IOError as ex:
                if ex.errno != errno.ENOENT:
                    raise
                print("IOError opening {} file [{}]:".format(label, file_spec), ex)
                out_file = sys.stdout
            return out_file
    else:
        return None

def print_sentences(sentences, list_numbers, max_words, out_file):
    if list_numbers:
        if 0 < max_words and max_words < 15:
            idx_format = '{} '
        else:
            idx_format = '\n    {}\n'
    for idx, sentence in enumerate(sentences):
        if list_numbers:
            print(idx_format.format(idx), end=' ')
        if max_words:
            text_ops.print_paragraph_regex_count(sentence, max_words, out_file=out_file)
        else:
            utf_print(sentence, outfile=out_file)

def translate_para_file(para_filter, in_path, out_path, charset='utf8'):
    '''Generator yielding filtered paragraphs from a text file'''
    with open(in_path, 'r', encoding=charset) as in_text:
        with open(out_path, 'w') as out_file:
            for para in paragraph_iter(in_text):
                output = para_filter.filter_line(para)
                print(output if output else ' ', file=out_file)

def translate_line_file(line_translators, in_path, out_path, charset='utf8'):
    '''Translate input line by line to output file'''
    with open(in_path, 'r', encoding=charset) as in_text:
        with (sys.stdout if out_path == '-' else open(out_path, 'w')) as out_file:
            for line in in_text:
                for translator in line_translators:
                    line = translator.translate(line)
                print(line if line else ' ', file=out_file)


########################################################

def translate_file(in_path, out_path, opt):
    """Rewrite a text file."""

    # Announce output:
    print(in_path, '====>', '<stdout>' if out_path == '-' else out_path)
    print('-------------------------------------------------------------------')
    translators = [IsoToAscii(), AsciiToCompact(),
                   JoinContractions(), MonoPunct(), JoinPossessive()]
    translate_line_file(translators, in_path, out_path, opt.charset)

###############################################################################

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('in_file', type=str, nargs='?', default='Text/train_1000.label',
                        help='file containing text to summarize')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='output only the indices of summary sentences')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each summary sentence')
    parser.add_argument('-number', dest='sum_count', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', default='lab.txt',
                        help='output file for summarized text (default: None)')
    parser.add_argument('-percent', dest='sum_percent', type=float, nargs='?',
                        const=16.6667, default=10.0,
                        help='percentage of sentences to keep (default: 10.0%%)')
    parser.add_argument('-serial', action='store_true',
                        help='summarize each paragraph in series')
    parser.add_argument('-truncate', dest='max_print_words', type=int, nargs='?',
                        const=8, default=0,
                        help='truncate sentences after MAX words (default: INT_MAX)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 3:
        print("outfile: <{}>".format(args.out_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    # summary_file = getattr(args, 'out_file', None)
    translate_file(args.in_file, args.out_file, args)

if __name__ == '__main__':
    main()
