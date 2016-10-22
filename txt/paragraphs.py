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
from collections import Counter

from utf_print import utf_print

def paragraph_iter(fileobj, rgx_para_separator='\n'):
    '''yields paragraphs from text file and regex separator'''
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

def print_paragraphs(path, mode, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text)):
            print("    Paragraph {}:".format(idx))
            utf_print(para)
            print()

def paragraph_reader(path, charset="utf8"):
    '''opens text file and returns paragraph iterator'''
    try:
        text = open(path, 'r', encoding=charset)
        return paragraph_iter(text), text
    except ex:
        print("Warning:", ex)
        return None

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
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Count some quoted ways of saying 'No'",
        )
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='text file containing quoted dialogue')
    parser.add_argument('-mode', type=int, nargs='?', const=1, default=1,
                        help='mode: 1 = ALL, 2 = First 10 words (default: 1)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        print("args:", args)
        print(__doc__)

    print_paragraphs(args.text_file, args.mode)
    print("\n\t LEAKY VERSION: \n")
    print_paragraphs_leaky(args.text_file)

if __name__ == '__main__':
    main()
