#!/usr/bin/env python3
# Note: do not use Latin-1 encoding, because it would force string
# literals to use byte encoding, which results in unicode characters > 255
# being ignored in regular expression strings.
# That is, do NOT put the following on the first or second line: -*- coding: latin-1 -*-
#
#
# Sprax Lines       2016.09.01      Written with Python 3.5
'''File readers that yield one paragraph at a time.'''

import argparse
import re
import sys

from utf_print import utf_print

INF_NUM_WORDS = 2**30


def paragraph_iter(fileobj, rgx_para_separator=r'\s*\n\s*'):
    '''yields paragraphs from text file and regex separator, which by default matches
    either one or more blank lines (two line feeds among whitespace),
    or one line-feed followed by a tab, possibly in the middle of other whitespace.'''
    ## Makes no assumptions about the encoding used in the file
    paragraph = ''
    for line in fileobj:
        if re.match(rgx_para_separator, line) and paragraph:
            yield paragraph
            paragraph = ''
        else:
            line = line.rstrip()
            if line:
                if line.endswith('-'):
                    paragraph += line
                else:
                    paragraph += line + ' '
    if paragraph:
        yield paragraph

def paragraph_multiline_iter(fileobj, rgx_para_separator=r'\s*\n\s*\n\s*|\s*\n\t\s*'):
    '''yields paragraphs from text file and regex separator, which by default matches
    either one or more blank lines (two line feeds among whitespace),
    or one line-feed followed by a tab, possibly in the middle of other whitespace.'''
    ## Makes no assumptions about the encoding used in the file
    paragraph = ''
    for line in fileobj:
        if re.match(rgx_para_separator, line) and paragraph:
            yield paragraph
            paragraph = ''
        else:
            line = line.rstrip()
            if line:
                if paragraph.endswith('-'):
                    paragraph += line
                else:
                    paragraph += ' ' + line
    if paragraph:
        yield paragraph

def print_paragraphs(path, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text)):
            print("    Paragraph {}:".format(idx))
            utf_print(para)
            print()

def print_paragraphs_split_join_str(path, max_words, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text)):
            words = para.split()[:max_words]
            print("    Paragraph {}:".format(idx))
            utf_print(' '.join(words))
            print()

def print_paragraphs_split_join_rgx(path, max_words, rgx_pat=r'^|\W*\s+\W*', charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text)):
            words = re.split(rgx_pat, para)[:max_words]
            print("    Paragraph {}:".format(idx))
            utf_print(' '.join(words))
            print()

def print_paragraphs_nth_substr(path, max_words, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs_nth_substr(", path, max_words, charset, ")")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text)):
            index = index_substr_nth(para, max_words)
            print("    Paragraph {}:".format(idx))
            utf_print(para[:index])
            print()

def print_paragraphs_nth_regex(path, max_words=INF_NUM_WORDS, outfile=sys.stdout, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs_nth_substr(", path, max_words, charset, ")")
    with open(path, 'r', encoding=charset) as text:
        for para in paragraph_iter(text):
            print_paragraph_regex_count(para, max_words)
            print()

def print_paragraph_regex_count(para, max_words=INF_NUM_WORDS, outfile=sys.stdout, elliptical='...'):
    '''split paragraph into words using regex and print first max_words words.'''
    if para:
        index = index_regex_count(para, max_words)
        if elliptical and len(para) - index > 3:
            utf_print(para[:index], '...')
        else:
            utf_print(para[:index])

def index_regex_count(string, count=0, rgx=re.compile(r'\s+|$')):
    '''Character index of Nth or last occurrence of regex pattern in string.
    Returns the index of the Nth occurrence where N <= count, or
    -1 if the pattern is not found at all.'''
    offset = 0
    if not string:
        return offset
    lens = len(string)
    for z in range(count):
        if lens <= offset:
            return offset;
        mat = rgx.search(string, offset)
        if not mat:
            return offset
        mat_span = mat.span()
        offset = mat_span[1]
    return mat_span[0]

def index_substr_nth(string, count=0, subs=' ', overlap=False):
    '''index of nth occurrence of substring in string'''
    skip = 1 if overlap else len(subs)
    index = -skip
    for _ in range(count + 1):
        index = string.find(subs, index + skip)
        if index < 0:
            break
    return index

def index_regex_nth(string, count=0, rgx=re.compile(r'\s+|$')):
    '''index of Nth occurrence of regex pattern in string, or -1 if count < n'''
    offset = 0
    for _ in range(count + 1):
        mat = rgx.search(string, offset)
        if not mat:
            return -1
        mat_span = mat.span()
        offset = mat_span[1]
    return mat_span[0]


def print_paragraphs_trunc(path, max_words, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text)):
            words = para.split()[:max_words]
            print("    Paragraph {}:".format(idx))
            utf_print(' '.join(words))
            print()

def paragraph_reader(path, charset="utf8"):
    '''opens text file and returns paragraph iterator'''
    try:
        text_stream = open(path, 'r', encoding=charset)
        return paragraph_iter(text_stream), text_stream
    except FileNotFoundError as ex:
        print("Warning:", ex)
        return None, None

def print_paragraphs_leaky(path):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    para_iter, fileobj = paragraph_reader(path)
    for idx, para in enumerate(para_iter):
        print("    Paragraph {}:".format(idx))
        utf_print(para)
        print()
    fileobj.close()

def main():
    '''Driver to iterate over the paragraphs in a text file.'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='text file containing quoted dialogue')
    parser.add_argument('-function', type=int, nargs='?', const=1, default=0,
                        help='paragraph printing function: 0=all (default: 0)')
    parser.add_argument('-max_words', type=int, nargs='?', const=1, default=5,
                        help='maximum words per paragraph: print only the first M words,\
                        or all if M < 1 (default: 0)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        print("args:", args)
        print(__doc__)

    if args.function == 0:
        print_paragraphs(args.text_file)
    elif args.function == 1:
        print_paragraphs_trunc(args.text_file, args.max_words)
    elif args.function == 2:
        print_paragraphs_split_join_str(args.text_file, args.max_words)
    elif args.function == 3:
        print_paragraphs_split_join_rgx(args.text_file, args.max_words)
    elif args.function == 4:
        print_paragraphs_nth_substr(args.text_file, args.max_words)
    elif args.function == 5:
        print_paragraphs_nth_regex(args.text_file, args.max_words)
    else:
        print("\n\t LEAKY VERSION: \n")
        print_paragraphs_leaky(args.text_file)

if __name__ == '__main__':
    main()
