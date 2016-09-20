#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#
# Sprax Lines       2016.09.01      Written with Python 3.5
'''Extract doubly-quoted strings from a file of paragraphs'''

import heapq
import itertools
import re
import sys
from collections import defaultdict
from collections import Counter

import utf_print

def paragraph_iter(fileobj, rgx_para_separator='\n'):
    """yields paragraphs from text file and regex"""
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
    print("print_paragraphs:")
    with open(path, 'r', encoding="utf8") as text:
        for idx, para in enumerate(paragraph_iter(text)):
            print("    Paragraph {}:".format(idx))
            print(para)
            print()

def quotes_per_paragraph_iter(path, verbose):
    '''returns a generator that yields the list of quoted dialogue
    phrases found in each paragraph in the text file, including
    empty lists for quoteless paragraphs.'''
    rgx_para_numbering = re.compile(r"^[^A-Za-z]*(\d|[ivx]+\.)")
    with open(path, 'r', encoding="utf8") as text:
        for para in paragraph_iter(text):
            if not para:
                print("WARNING: para is empty!")   # TODO: delete this check!
                continue
            if re.match(rgx_para_numbering, para):
                continue
            para = para.replace('’', "'")
            yield extract_quoted(para, verbose)

def quoted_phrase_iter(path, verbose):
    '''Generater that merges all quoted phrases into one stream, ignoring paragraph boundaries.'''
    for para_quotes in quotes_per_paragraph_iter(path, verbose):
        if not para_quotes:
            continue
        for quote in para_quotes:
            if verbose > 1:
                print("quote:", quote)
            yield quote

def extract_quoted(para, verbose):
    '''Returns list of quotes extracted from paragraph.'''

    # rgx_quote_A = re.compile(r'"([^"]*)"')
    # rgx_quote_B = re.compile(r'"([^"]+)"')
    # rgx_quote_C = re.compile(r'(["])(?:(?=(\\?))\2.)*?\1')
    # rgx_single  = re.compile("(^\s*|[,:-]\s+)'(.*?)[,.!?]'(\s*|$)")
    # rgx_quote_D = re.compile("(^\s*|said\s+|says\s+|\t\s*|[,:-]\s+)['\"](.*?)([,.!?])['\"](\s+|$)")
    # distinguish 'scare' quotes 'dialogue' quotes (which presumably demarcate quoted spech)
    rgx_quoted = re.compile("(?:^\s*|said\s+|says\s+|\t\s*|[,:-]\s+)['\"](.*?)([,.!?])['\"](?:\s+|$)")
    if not para:
        print("WARNING: paragraph is empty!")
        return []
    para = para.replace('’', "'")
    return re.findall(rgx_quoted, para)

def extract_yes_no_repies(path, verbose):
    '''Finds first 3 (or fewer) words starting quoted replies.
       Returns a defaultdict mapping these phrases to their counts.
       Words longer than 1-letter are lowercased.'''
    rgx_word = re.compile(r"[A-Z'’a-z]+")
    reply_counter = Counter()
    denial_counter = Counter()
    idx = 0
    quotes_in_previous_para = False
    for quotes in quotes_per_paragraph_iter(path, verbose):
        if not quotes:
            quotes_in_previous_para = False
            continue
        phrases = []
        is_denial = False
        for qi, quote in enumerate(quotes):
            if verbose > 1:
                print("quote {} {}: {}".format(idx, quote[1], quote[0]))
            idx += 1
            phrase = []
            words = re.findall(rgx_word, quote[0])
            for word in words[:3]:
                if len(word) == 1:
                    phrase.append(word)
                else:
                    low = word.lower()
                    phrase.append(low)
                    if low == "no" or low == "not" or low == "don't":
                        is_denial = True
            if phrase:
                joined = ' '.join(phrase)
                if is_denial:
                    is_denial = False
                    denial_counter.update([joined])
                phrases.append(joined)
        reply_counter.update(phrases)
        ## for ppp in phrases:
        ##    print("ppp: ", ppp)
        quotes_in_previous_para = True
    return reply_counter, denial_counter


def main():
    '''Driver to extract quoted dialog from a corpus.'''

    # simple, inflexible arg parsing:
    argc = len(sys.argv)
    if argc > 4:
        print(sys.argv[0])
        print(__doc__)
        exit(0)

    # Get the paths to the files (relative or absolute)
    corpus_file = sys.argv[1] if argc > 1 else r'corpus.txt'
    verbose = int(sys.argv[2]) if argc > 2 else 1

    # print_paragraphs(corpus_file)
    # for quoted in quoted_phrase_iter(corpus_file, verbose):
    #    print("{}{}".format(quoted[0], quoted[1]))
    replies, denials = extract_yes_no_repies(corpus_file, verbose)       
    
    numfreq = 4
    print("The", numfreq, "most common reply phrases:")
    for phrase, count in replies.most_common(numfreq):
        utf_print.utf_print('    {:>7d} {}'.format(count, phrase))

    print("The", numfreq, "most common denials:")
    for phrase, count in denials.most_common(numfreq):
        utf_print.utf_print('    {:>7d} {}'.format(count, phrase))



if __name__ == '__main__':
    main()
