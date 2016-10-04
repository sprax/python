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

import utf_print

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

def print_paragraphs(path):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding="utf8") as text:
        for idx, para in enumerate(paragraph_iter(text)):
            print("    Paragraph {}:".format(idx))
            utf_print.utf_print(para)
            print()

def paragraph_reader(path, encoding="utf8"):
    '''opens text file and returns paragraph iterator'''
    # # with open(path, 'r', encoding) as text:
    with open(path, 'r') as text:
        return paragraph_iter(text)

def print_paragraphs_bust(path):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with paragraph_reader(path) as para_iter:
        for idx, para in enumerate(para_iter):
            print("    Paragraph {}:".format(idx))
            print(para)
            print()

def main():
    '''Driver to iterate over the paragraphs in a text file.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Count some quoted ways of saying 'No'",
        )
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='text file containing quoted dialogue')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        print("args:", args)
        print(__doc__)

    print_paragraphs(args.text_file)
    # print("\n\t BUSTED VERSION: \n")
    # print_paragraphs_bust(args.text_file)

if __name__ == '__main__':
    main()
