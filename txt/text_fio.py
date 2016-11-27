#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''
import re
import sys
from collections import defaultdict
import text_ops
from utf_print import utf_print
import argparse
import errno
import heapq
import math
import string
import nltk

def print_words(file_spec):
    with open(file_spec, 'r') as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    print(word)
            print(words)

def _rank(summary_count, ranking):
    '''Return the highest ranked N sentences.'''
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

def filter_word_counts(word_counts, stopwords, min_freq, max_freq, verbose):
    """ remove any word in stopwords or whose count is below the min or above the max threshold """
    max_word_count = 0
    for word, count in word_counts.items():
        if count > max_word_count and word not in stopwords:
            max_word_count = count
    min_freq_count = max_word_count * min_freq
    max_freq_count = max_word_count * max_freq
    stop_words_to_remove = []
    rare_words_to_remove = []
    total_count = 0
    for word, count in word_counts.items():
        if count >= max_freq_count or word in stopwords:
            stop_words_to_remove.append(word)
        elif count <= min_freq_count:
            rare_words_to_remove.append(word)
        else:
            total_count += count
    if verbose > 2:
        utf_print("========Removing common words: ", stop_words_to_remove)
        for key in stop_words_to_remove:
            word_counts.pop(key, None)
        utf_print("========Removing rarest words: ", rare_words_to_remove)
        for key in rare_words_to_remove:
            word_counts.pop(key, None)
    return total_count


def read_file_eafp(file_spec):
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

def read_file(file_spec, charset='utf8'):
    with open(file_spec, 'r', encoding=charset) as src:
        return src.read()

def open_out_file(file_spec, label=''):
    if file_spec:
        if file_spec in ['-', 'stdout']:
            return sys.stdout
        else:
            try:
                out_file = open(out_file, 'w')
            except IOError as ex:
                if ex.errno != errno.ENOENT:
                    raise
                print("IOError opening {} file [{}]:".format(label, out_file), ex)
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
            text_ops.print_paragraph_regex_count(sentence, max_words, outfile=out_file)
        else:
            utf_print(sentence, outfile=out_file)

########################################################

def unit_test(text_file, opt, charset='utf8'):
    """Output a summary of a text file."""

    # Read initial text corpus:
    text = read_file(text_file, charset)

    # Try to open output (file):
    out_file = open_out_file(opt.out_file)

    # Announce output:
    print(text_file, '====>', '<stdout>' if out_file==sys.stdout else opt.out_file)
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
