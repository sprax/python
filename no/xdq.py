#!/usr/bin/env python3
# Note: do not use Latin-1 encoding, because it would force string
# literals to use byte encoding, which results in unicode characters > 255
# being ignored in regular expression strings.
# That is, do NOT put the following on the first or second line: -*- coding: latin-1 -*-
# 
#
# Sprax Lines       2016.09.01      Written with Python 3.5
'''Extract doubly- or singly-quoted strings from a file of paragraphs'''

import argparse
import re
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
            print(para)
            print()

def quotes_per_paragraph_iter(path, verbose):
    '''returns a generator that yields the list of quoted dialogue
    phrases found in each paragraph in the text file, including
    empty lists for quoteless paragraphs.'''
    with open(path, 'r', encoding="utf8") as text:
        for para in paragraph_iter(text):
            if not para:
                print("WARNING: para is empty!")   # TODO: delete this check!
                continue
            yield extract_quoted(para, verbose)

def quoted_phrase_iter(path, verbose):
    '''Generater that merges all quoted phrases into one stream, ignoring paragraph boundaries.'''
    for para_quotes in quotes_per_paragraph_iter(path, verbose):
        if not para_quotes:
            continue
        for quote in para_quotes:
            if verbose > 1:
                utf_print.utf_print("quote:", quote)
            yield quote

def extract_quoted(paragraph, verbose):
    '''Returns list of quotes extracted from paragraph, unless it's a numbered paragraph'''
    # rgx_quote_A = re.compile(r'"([^"]*)"')
    # rgx_quote_B = re.compile(r'"([^"]+)"')
    # rgx_quote_C = re.compile(r'(["])(?:(?=(\\?))\2.)*?\1')
    # rgx_single  = re.compile("(^\s*|[,:-]\s+)'(.*?)[,.!?]'(\s*|$)")
    # rgx_quote_D = re.compile("(^\s*|said\s+|says\s+|\t\s*|[,:-]\s+)['\"](.*?)([,.!?])['\"](\s+|$)")
    # distinguish 'scare' quotes 'dialogue' quotes (which presumably demarcate quoted spech)
    rgx_quoted = re.compile("(?:^\s*|said\s+|says\s+|\t\s*|[,:-]\s+)['\"](.*?)([,.!?])['\"](?:\s+|$)")
    rgx_para_numbering = re.compile(r"^[^A-Za-z]*(\d|[ivx]+\.)")
    if not paragraph:
        print("WARNING: paragraph is empty!")
        return []
    if re.match(rgx_para_numbering, paragraph):
        return []
    para = paragraph.replace('’', "'")
    return re.findall(rgx_quoted, para)

def extract_yes_no_repies(path, beglen, verbose):
    '''Finds first N (or fewer) words starting quoted replies.
       Returns Counters mapping these phrases to their counts.
       Words longer than 1-letter are lowercased.'''
    # rgx_word = re.compile(r"[A-Za-z'’]+")
    rgx_word = re.compile(r"[A-Za-z']+")
    quote_counter = Counter()   # counts any quoted dialog phrase
    reply_counter = Counter()   # counts only replies
    answer_counter = Counter()  # counts only replies to questions
    denial_counter = Counter()  # counts only negative replies to questions
    qindex = 0
    quotes_in_previous_para = False
    prev_quote_was_a_question = False
    for pindex, quotes in enumerate(quotes_per_paragraph_iter(path, verbose)):
        if not quotes:
            quotes_in_previous_para = False
            continue
        quote_counter.update(quotes)
        phrases = []
        is_denial = False
        for qip, quote in enumerate(quotes):
            is_denial = False
            if verbose > 1:
                utf_print.utf_print("para {:3}, quote {:2} {}: {}".format(pindex, qindex, quote[1], quote[0]))
            qindex += 1
            phrase = []
            words = re.findall(rgx_word, quote[0])
            # # words = re.findall(r"\b[a-z']+\b", quote[0], re.I | re.U )
            # # words = re.findall(r"\b[a-z']+", quote[0], re.I)
            # # words = quote[0].split()
            for word in words[:beglen]:
                if len(word) == 1 or word[0] == 'I':
                    phrase.append(word)
                else:
                    low = word.lower()
                    phrase.append(low)
                    if low == "no" or low == "not" or low == "don't":
                        is_denial = True
            if phrase:
                joined = ' '.join(phrase)
                phrases.append(joined)
            if qip == 0 and quotes_in_previous_para:
                reply_counter.update(phrases)
                if prev_quote_was_a_question:
                    answer_counter.update(phrases)
                    if is_denial:
                        denial_counter.update([joined])

        if quote[1] == '?':
            prev_quote_was_a_question = True
        else:
            prev_quote_was_a_question = False
        ## for ppp in phrases:
        ##    print("ppp: ", ppp)
        quotes_in_previous_para = True
    return quote_counter, reply_counter, denial_counter


def main():
    '''Driver to extract quoted dialog from a corpus.'''
    parser = argparse.ArgumentParser(
            # usage='%(prog)s [options]',
            description="Count some quoted ways of saying 'No'",
            )
    parser.add_argument('corpus_file', type=str, nargs='?', default='corpus.txt',
            help='text file containing quoted dialogue')
    parser.add_argument('-beglen', type=int, nargs='?', const=1, default=4,
            help='number of words beginnning a reply (default: 4)')
    parser.add_argument('-topmost', type=int, nargs='?', const=1, default=10,
            help='number of most common denials (default: 10)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
            help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if (args.verbose > 2):
        print("args:", args)
        print(__doc__)

    # print_paragraphs(corpus_file)
    # for quoted in quoted_phrase_iter(corpus_file, verbose):
    #    print("{}{}".format(quoted[0], quoted[1]))
    quotes, replies, denials = extract_yes_no_repies(args.corpus_file, args.beglen, args.verbose)
    
    numfreq = args.topmost
    print("The", numfreq, "most common reply phrases:")
    for phrase, count in replies.most_common(numfreq):
        utf_print.utf_print('    {:>7d} {}'.format(count, phrase))

    print("The", numfreq, "most common denials:")
    for phrase, count in denials.most_common(numfreq):
        utf_print.utf_print('    {:>7d} {}'.format(count, phrase))



if __name__ == '__main__':
    main()
