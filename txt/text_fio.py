#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''
import argparse
import csv
import errno
import os.path
import pickle
import random
import re
import sys
from utf_print import utf_print
import text_ops

########################################################
# util functions

def cwd():
    '''current working directory'''
    return os.path.dirname(os.path.realpath('.'))

def get_abs_path(path):
    '''Convert the specified path to an absolute path (if it isn't already one).
    Returns the corresponding absolute path.'''
    return os.path.abspath(path)

def make_abs_path(dirpath, filepath):
    '''Given a directory path and a filename or relative file path,
    get the absolute path for the specified file under that directory.
    Returns this absolute path as a string suitable as an argument to open().'''
    return os.path.abspath(os.path.join(dirpath, filepath))

def print_stdout_stderr(text):
    '''print text to stdout and stderr'''
    print("sys.stdout: ", text, file=sys.stdout)
    print("sys.stderr: ", text, file=sys.stderr)

def open_out_file(file_spec, label='text'):
    '''returns a file handle open for writing, to be closed by the caller, else None'''
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

def read_lines(file_spec, charset='utf8'):
    '''read and yield all lines of a text file as a iter of str'''
    with open(file_spec, 'r', encoding=charset) as text:
        for line in text:
            yield line.rstrip()

def read_text_lines(file_spec, charset='utf8'):
    '''read and yield non-empty lines of a text file as a iter of str'''
    with open(file_spec, 'r', encoding=charset) as text:
        for line in text:
            line = line.strip()
            if line:
                yield line


def pickle_file(in_path, out_path, data_struct, data_adder, charset='utf8'):
    '''read in_file into data_struct via data_adder then save to out_path'''
    lines_in = 0
    lines = read_text_lines(in_path, charset)
    for line in lines:
        data_adder(data_struct, line)
        lines_in += 1
    with open(out_path, 'wb') as out_file:
        pickle.dump(data_struct, out_file)
    return (lines_in, len(data_struct))

def pickle_word_list(in_path, out_path, word_set=None, adder=set.add, charset='utf8'):
    '''read single words/strings per line from in_file and save them as a set to out_path as a pickle file'''
    if word_set is None:
        word_set = set()
    return pickle_file(in_path, out_path, word_set, adder, charset)

def read_file(file_spec, charset='utf8'):
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


# try to read ascii or utf-8 and failover to iso-8859-1, etc.
def read_text_file(file_spec):
    '''read and return all contents of file as one str'''
    try:
        return read_file(file_spec, 'utf-8')
    except UnicodeDecodeError:
        return read_file(file_spec, 'iso-8859-1')


def utf_print_words(fspec):
    '''utf_print a text file word-by-word'''
    with open(fspec, 'r', encoding="utf8") as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    utf_print(word)
            utf_print(words)

def print_file_words(file_spec):
    '''Open a file 'r' and print all its white-space separated words.'''
    with open(file_spec, 'r') as text:
        for line in text:
            words = re.split(r'\W+', line.rstrip())
            for word in words:
                if len(word) > 0:
                    print(word)
            print(words)

def print_words(text_iter):
    '''print all white-space separated words read from a text iter (e.g. text file handle)'''
    for line in text_iter:
        words = re.split(r'\W+', line.rstrip())
        for word in words:
            if len(word) > 0:
                print(word)
        print(words)

def print_sentences(sentences, list_numbers, max_words, out_file):
    '''print sentences or any enumerable collection of text to an open file'''
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

###############################################################################
def csv_read(path, newline=None, delimiter=',', quotechar='"'):
    ''' Return a list of tuples read from a CSV file. '''
    tuples = []
    try:
        with open(path, 'rt', newline=newline) as in_file:
            reader = csv.reader(in_file, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                tuples.append(row)
    except IOError as ex:
        print("csv_read failed to read from ({}) with error: {}".format(path, ex))
    return tuples

def csv_write(tuples, path, newline=None, delimiter=',', quotechar='"'):
    ''' Write a list of tuples to a CSV file. '''
    try:
        with open(path, "w", newline=newline) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for tup in tuples:
                writer.writerow(tup)
    except IOError as ex:
        print("csv_write_qa failed to write tuples to ({}) with error: {}".format(path, ex))

########################################################

def unit_test(text_file, opt):
    """Output a summary of a text file."""

    # Read initial text corpus:
    text = read_file(text_file, opt.charset)

    # Try to open output (file):
    out_file = open_out_file(opt.out_file)

    # Announce output:
    print(text_file, '====>', '<stdout>' if out_file == sys.stdout else opt.out_file)
    print('-------------------------------------------------------------------')

    if opt.repr:
        print(repr(text), file=out_file)
    else:
        print(text, file=out_file)

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
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-error', dest='error_text', type=str, default='log this msg',
                        help='write same message to stderr and stdout, then exit')
    parser.add_argument('-index', dest='indices_only', action='store_true',
                        help='output only the indices of summary sentences')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each summary sentence')
    parser.add_argument('-max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-number', type=int, nargs='?', const=10, default=0,
                        help='number of sentences to keep (default: 0), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', const='-',
                        help='output file for summarized text (default: None)')
    parser.add_argument('-pickle_set_of_text_lines', '-pst', action='store_true',
                        help='pickle a set of words from a text file')
    parser.add_argument('-percent', dest='sum_percent', type=float, nargs='?',
                        const=16.6667, default=10.0,
                        help='percentage of sentences to keep (default: 10.0%%)')
    parser.add_argument('-repr', action='store_true',
                        help='output repr of data, not raw data')
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

    if args.pickle_set_of_text_lines:
        lines_in, words_out = pickle_word_list(args.text_file, args.out_file)
        print("Pickled %d words from %d lines in %s into %s:" % (
            words_out, lines_in, args.text_file, args.out_file))
        with open(args.out_file, 'rb') as pick:
            word_set = pickle.load(pick)
        if words_out <= args.number:
            print("word_set entire:", word_set)
        else:
            print("word_set sample:", random.sample(word_set, args.number))
        exit(0)

    if args.error_text:
        print_stdout_stderr(args.error_text)
        exit(1)



    # summary_file = getattr(args, 'out_file', None)
    unit_test(args.text_file, args)

if __name__ == '__main__':
    main()
