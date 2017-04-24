#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''
import argparse
import errno
import heapq
import os.path
import re
import math
import sys
from utf_print import utf_print
import text_ops

from utf_print import utf_print

def read_lines(file_spec, charset='utf8'):
    '''read and return all lines of a text file as a list of str'''
    with open(file_spec, 'r', encoding=charset) as text:
        for line in text:
            # utf_print(line.rstrip())
            yield line.rstrip()

def read_file(file_spec, charset='utf8'):
    '''read and return all contents of file as one str'''
    with open(file_spec, 'r', encoding=charset) as src:
        return src.read()

def read_file_eafp(file_spec):
    '''read contents of file_spec, Easier to Ask for Forgiveness than ask Permission.'''
    try:
        src = open(file_spec, 'r')
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

########################################################
# util functions

def cwd():
    return os.path.dirname(os.path.realpath('.'))

########################################################

def unit_test(text_file, opt):
    """Output a summary of a text file."""

    # Read initial text corpus:
    # text = read_file(text_file, charset)

    # Try to open output (file):
    out_file = open_out_file(opt.out_file)

    # Announce output:
    print(text_file, '====>', '<stdout>' if out_file == sys.stdout else opt.out_file)
    print('-------------------------------------------------------------------')
    if out_file and out_file != sys.stdout:
        out_file.close()

###############################################################################

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='file containing text to summarize')
    parser.add_argument('-index', dest='indices_only', action='store_true',
                        help='output only the indices of summary sentences')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each summary sentence')
    parser.add_argument('-max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-number', dest='sum_count', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', const='-',
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
    unit_test(args.text_file, args)

if __name__ == '__main__':
    main()
