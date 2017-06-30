#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''
import argparse
import errno
import os.path
import re
import sys
from utf_print import utf_print
import text_ops

########################################################
# util functions

def cwd():
    '''current working directory'''
    return os.path.dirname(os.path.realpath('.'))

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
    parser.add_argument('-number', dest='sum_count', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', const='-',
                        help='output file for summarized text (default: None)')
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

    if args.error_text:
        print_stdout_stderr(args.error_text)
        exit(1)

    if args.verbose > 3:
        print("outfile: <{}>".format(args.out_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    # summary_file = getattr(args, 'out_file', None)
    unit_test(args.text_file, args)

if __name__ == '__main__':
    main()
