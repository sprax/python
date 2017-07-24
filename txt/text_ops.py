#!/usr/bin/env python3
# Note: do not use Latin-1 encoding, because it would force string
# literals to use byte encoding, which results in unicode characters > 255
# being ignored in regular expression strings.
# That is, do NOT put the following on the first or second line: -*- coding: latin-1 -*-
#
#
# Sprax Lines       2016.09.01      Written with Python 3.5
'''Common operations for textual corpora, including:
   * File readers that yield one paragraph at a time.
   * Frequency-based word filtering.
'''

# from string import punctuation
import argparse
import math
import re
import sys
from collections import defaultdict, namedtuple

from utf_print import utf_print

INF_NUM_WORDS = 2**30

RE_PARA_SEPARATOR = re.compile(r'\s*\n')

################################################################################

def filter_stop_word_counts(word_counts, stopwords):
    """ remove any word in stopwords or whose count is below the min or above the max threshold """
    count_removed = 0
    for word in stopwords:
        count_removed += word_counts.pop(word, 0)
    return count_removed

################################################################################

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
        if count > max_freq_count or word in stopwords:
            stop_words_to_remove.append(word)
        elif count < min_freq_count:
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
################################################################################

def resolve_count(sub_count, percent, total_count):
    '''returns reconciled sub-count and percentage of total, where count trumps percentage'''
    if total_count < 1:
        raise ValueError("total_count must be > 0")
    if not sub_count:
        sub_count = int(math.ceil(percent * total_count / 100.0))
    if  sub_count > total_count:
        sub_count = total_count
    if  sub_count < 1:
        sub_count = 1
    percent = sub_count * 100.0 / total_count
    return sub_count, percent

################################################################################

def paragraph_iter(fileobj, rgx_para_separator=RE_PARA_SEPARATOR, sep_lines=0):
    '''
    yields paragraphs from text file and regex separator, which by default matches
    one blank line (only space before a newline, or r"\s*\n").  All but the first
    paragraph will begin with the separator, unless it contains only whitespace,
    which is stripped from the end of every line.
    TODO: Consider adding span-matching for square brackets, that is, never
    breaking a paragraph on text between an open bracket [ and a matching, i.e.
    balance end bracket ].  Likewise { no break between curly braces }.
    '''
    ## Makes no assumptions about the encoding used in the file
    paragraph, blanks = '', 0
    for line in fileobj:
        #print("    PI: line(%s) para(%s)" % (line.rstrip(), paragraph))
        if re.match(rgx_para_separator, line) and paragraph and blanks >= sep_lines:
            yield paragraph
            paragraph, blanks = '', 0
        line = line.rstrip()
        if line:
            blanks = 0
            if not paragraph:
                paragraph = line
            elif paragraph.endswith('-'):
                paragraph += line
            else:
                paragraph += ' ' + line
        else:
            blanks += 1
    if paragraph:
        yield paragraph

def paragraph_multiline_iter(fileobj, rgx_para_separator=r'\s*\n\s*\n\s*|\s*\n\t\s*'):
    '''yields paragraphs from text file and regex separator, which by default matches
    one or more blank lines (two line feeds among whitespace),
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

def print_paragraphs(path, charset='utf8', rgx_para_separator=RE_PARA_SEPARATOR):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text, rgx_para_separator)):
            print("    Paragraph {}:".format(idx))
            utf_print(para)
            print()

def print_paragraphs_split_join_str(path, max_words, charset='utf8', rgx_para_separator=RE_PARA_SEPARATOR):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs:")
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(paragraph_iter(text, rgx_para_separator)):
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

def print_paragraphs_nth_regex(path, max_words=INF_NUM_WORDS, out_file=sys.stdout, charset='utf8'):
    '''Prints sequence numbers and paragraphs.'''
    print("print_paragraphs_nth_substr(", path, max_words, charset, ")")
    with open(path, 'r', encoding=charset) as text:
        for para in paragraph_iter(text):
            print_paragraph_regex_count(para, max_words, out_file)
            print(file=out_file)

def print_paragraph_regex_count(para, max_words=INF_NUM_WORDS, out_file=sys.stdout,
        elliptical='...'):
    '''split paragraph into words using regex and print up to max_words words.'''
    if para:
        index = index_regex_count(para, max_words)
        if elliptical and len(para) - index > 3:
            utf_print(para[:index], '...', outfile=out_file)
        else:
            utf_print(para[:index], outfile=out_file)

def index_regex_count(string, count=0, rgx=re.compile(r'\s+|$')):
    '''Character index of Nth or last occurrence of regex pattern in string.
    Returns the index of the Nth occurrence where N <= count, or
    -1 if the pattern is not found at all.'''
    offset = 0
    if not string:
        return offset
    lens = len(string)
    for _ in range(count):
        if lens <= offset:
            return offset
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

def paragraph_reader(path, charset="utf8", rgx_para_separator=RE_PARA_SEPARATOR):
    '''opens text file and returns paragraph iterator'''
    try:
        text_stream = open(path, 'r', encoding=charset)
        return paragraph_iter(text_stream, rgx_para_separator), text_stream
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


def print_sentences(sentences, list_numbers, max_words, out_file):
    '''prints an array of sentences, with optional numbering'''
    if list_numbers:
        if 0 < max_words and max_words < 15:
            idx_format = '{} '
        else:
            idx_format = '\n    {}\n'
    for idx, sentence in enumerate(sentences):
        if list_numbers:
            print(idx_format.format(idx), end=' ')
        if max_words:
            print_paragraph_regex_count(sentence, max_words, out_file=out_file)
        else:
            utf_print(sentence, outfile=out_file)

def para_iter_file(path, rgx_para_separator=RE_PARA_SEPARATOR, sep_lines=0, charset='utf8'):
    '''Generator yielding filtered paragraphs from a text file'''
    # print("para_iter_file: pattern: %s" % rgx_para_separator.pattern)
    with open(path, 'r', encoding=charset) as text:
        for para in paragraph_iter(text, rgx_para_separator, sep_lines):
            yield para

def filter_file(para_filter, path, charset='utf8'):
    '''Generator yielding filtered paragraphs from a text file'''
    with open(path, 'r', encoding=charset) as text:
        for para in paragraph_iter(text):
            yield para_filter.filter_paragraph(para)


REC_FIRST_WORD_TOKEN = re.compile(r'^\W*(\w+)')

def first_token(text, default=None):
    try:
        return REC_FIRST_WORD_TOKEN.match(text).groups()[0]
    except:
        return default


def print_groups(match):
    if match:
        for grp in match.groups():
            print("  {}".format(grp))

REP_UPPER_WORD = r'^\s*([A-Z-]+)\b\s*'
REC_UPPER_WORD = re.compile(REP_UPPER_WORD)

# REP_WEBSTER1 = r'\n([A-Z-]+)\s+([^\s,]+)[^,]*,\s+((?:[a-z]\.\s*)+)(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s)([^.]+)?'
# REP_WEBSTER = r'([A-Z\'-]+)\s+([^\s,]+)[^,]*,\s+((?:[a-z]\.\s*)+)(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s+)?((?:[^.]+.\s+)*)'

REP_SPC = r'[\s.,]+'
REP_WEBSTER = r'([A-Z-]+)\s+([^\s\(\[,]+)\s*(\([^(]+\))?(\[[^\]]+\])?([^,]*,?)\s+((?:[a-z]\.\s*)+)?(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s+)?((?:[^.]+.\s+)*)'
REC_WEBSTER = re.compile(REP_WEBSTER)

REM_WEBSTER = re.compile(r"""
    (?P<word_1>[A-Z'-]+)                      # WORD 1 and whitespace
    (?:;\s+(?P<word_2>[A-Z'-]+))?\s+          # WORD 2+ (variant spellings) and whitespace
    (?P<pron_1>[^\s\(\[,]+)\s*                # pronunciation 1
    (?:,\s*(?P<pron_2>\w[^\s\(\[,.]+))?\s*    # pronunciation 2+
    (?P<part1a>(?:[a-z]\.\s*)+)?              # part of speech for first definition (order varies)
    (?P<pren1a>\([^\)]+\))?                   # parenthesized 1a ?
    (?P<brack1>\[[^\]]+\])?                   # bracketed ?
    (?P<sepsp1>[^,]*,?)?\s*                   # space, punctuation(period, comma)
    (?P<part1b>(?:[a-z]\.\s*)+)?              # part of speech for first definition (may be right before defn.)
    (?P<pren1b>\([^\)]+\))?\s*                # parenthesized 1b ?
    (?:Etym:\s+\[(?P<etym_1>[^\]]+)\])?\s*    # etymology
    (?:(?P<dftag1>Defn:|1\.)\s+(?P<defn_1>[^.]+))?\.\s*   # definition 1 tag
    (?:;)?\s*                               # optional separator
    (?P<usage1>".*"[^\d]+)?\s*                # example 1
    (?P<defn_2>\d.\s[^\d]+)?                  # definition 2, ...
    (?P<cetera>.*)?$                          # etc.
""", re.VERBOSE)

REM_PART = re.compile(r"""
    (?P<word_1>[A-Z'-]+)                      # WORD 1 and whitespace
    (?:;\s+(?P<word_2>[A-Z'-]+))?\s+          # WORD 2+ (variant spellings) and whitespace
    (?P<pron_1>[^\s\(\[,]+)\s*                # pronunciation 1
    (?:,\s*(?P<pron_2>\w[^\s\(\[,.]+))?\s*    # pronunciation 2+
    (?P<part1a>(?:[a-z]\.\s*)+)?              # part of speech for first definition (order varies)
    (?P<cetera>.*)?$                          # etc.
""", re.VERBOSE)

Webster = namedtuple('Webster', 'word_1 word_2 pron_1 parenth bracket sep_spc part_1 etymology defn1 usage1 defn2 etc')

class WebsterEntry:
    '''Represents a parsed dictionary entry a la Webster's Unabridged'''
    def __init__(self, entry_dict, options=None):
        '''TODO: bifurcate on word_2 if present'''
        self.dict = entry_dict
        self.word_1 = entry_dict['word_1'].lower()
        word_2 = entry_dict['word_2']
        self.word_2 = word_2.lower() if word_2 else None
        self.pron_1 = entry_dict['pron_1']
        self.pron_2 = entry_dict['pron_2']

        parenthesis_1 = entry_dict['pren1a']
        self.pren_1 = parenthesis_1 if parenthesis_1 else entry_dict['pren1b']

        self.brack1 = entry_dict['brack1']
        self.csep = entry_dict['sepsp1']
        part1 = entry_dict['part1a']
        self.part_1 = part1 if part1 else entry_dict['part1b']
        self.etym_1 = entry_dict['etym_1']
        self.dftag1 = entry_dict['dftag1']
        self.defn_1 = entry_dict['defn_1']
        self.usage1 = entry_dict['usage1']
        self.defn_2 = entry_dict['defn_2']
        self.cetera = entry_dict['cetera']

    def __str__(self):
        return('''
    word_1: {:<24}    word_2: {}
    pron_1: {:<24}    pron_2: {}
    part_1: ({})
    dftag1: ({})
    defn_1: ({})
    usage1: ({})
    defn_2: ({})
    cetera: ({})
    '''.format(self.word_1, self.word_2, self.pron_1, self.pron_2, self.part_1,
               self.dftag1, self.defn_1, self.usage1, self.defn_2, self.cetera))

def print_webster(webster):
    print("    Webster tuple:")
    print("\tword:", webster.word_1)
    print("\tpron:", webster.pron_1)
    print("\tpart:", webster.part_1)
    print("\tetym:", webster.etymology)
    print("\tdef1:", webster.defn1)
    print("\tuse1:", webster.usage1)
    print("\tdef2:", webster.defn2)
    print("\tmore:", webster.etc)


def match_webster_entry(entry):
    '''return regex match on dictionary entry text; trying only one pattern for now'''
    return REM_WEBSTER.match(entry)

def parse_webster_entry(entry):
    '''Return a dict representing a parsed dictionary entry.
    For now we just return the dict from a match's named groups.'''
    match = match_webster_entry(entry)
    if match:
        return match.groupdict()
    return None


def parse_webster_file(path, beg, end, charset, verbose=1):
    metrics = defaultdict(int)
    for idx, entry in enumerate(para_iter_file(path, REC_UPPER_WORD, sep_lines=1, charset=charset)):
        if idx >= beg:
            metrics['tried'] += 1
            entry_dict = parse_webster_entry(entry)
            if verbose > 3 or verbose > 1 and not entry_dict:
                print("\nPARAGRAPH {:5}\n({})".format(idx, entry))
            if entry_dict:
                metrics['parsed'] += 1
                if entry_dict['defn_1']:
                    metrics['defined'] += 1
                entry = WebsterEntry(entry_dict)
                if verbose > 2:
                    print("entry:\n", entry)
                # print("WebsterEntry.__str__: (%s)\n" % entry.__str__())
                # print("WebsterEntry.__dict__: (%s)\n" % entry.__dict__)
            else:
                metrics['unparsed'] += 1
                if verbose > 0:
                    print(" {:<20} >>>>NO MATCH<<<< {:>6}".format(first_token(entry), idx))
                bad_match = REM_PART.match(entry)
                print(bad_match.groups())
        if end > 0 and idx >= end:
            break
    print_metrics(metrics)

def print_metrics(metrics):
    print("def/parsed/unparsed/tried: %d/%d:%d/%d" % (
        metrics['defined'], metrics['parsed'], metrics['unparsed'], metrics['tried']))

# aaa = 'A A (named a in the English, and most commonly ä in other languages). Defn: The first letter of the English and of many other alphabets. The capital A of the alphabets of Middle and Western Europe, as also the small letter (a), besides the forms in Italic, black letter, etc., are all descended from the old Latin A, which was borrowed from the Greek Alpha, of the same form; and this was made from the first letter (Aleph, and itself from the Egyptian origin. '
# mm = re.match(r'([A-Z-]+)\s+([^\s,]+)[^,]*,?\s+((?:[a-z]\.\s*)+)?(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s+)?((?:[^.]+.\s+)*)', aaa); mm

# TODO: REC_DICT_ENTRY := (WORD) (PRON) (Anything up to one of:) ([Etym: .*]|Defn .*|Lang...|Ref...|POS)
# where definition text gets parsed into an array of glosses)
# and POS := (n.|v. i.|v. t.|etc.|)
# and Usage stuff also goes into a list of variants.

CONST_MAX_WORDS = 5
DEFAULT_NUMBER = 10
CONST_START_INDEX = 1
CONST_STOP_INDEX = 10
DEFAULT_START_INDEX = 0
DEFAULT_STOP_INDEX  = 0

def main():
    '''Driver to iterate over the paragraphs in a text file.'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='text file containing quoted dialogue')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-function', type=int, nargs='?', const=1, default=0,
                        help='paragraph printing function: 0=all (default: 0)')
    parser.add_argument('-number', type=int, nargs='?', const=CONST_MAX_WORDS,
                        default=DEFAULT_NUMBER,
                        help='max number of entries to parse (defaults: %d/%d)' % (
                            CONST_MAX_WORDS, DEFAULT_NUMBER))
    parser.add_argument('-start_index', '-beg', type=int, nargs='?',
                        const=CONST_START_INDEX, default=DEFAULT_START_INDEX,
                        help='start_index (defaults: %d/%d)' % (CONST_START_INDEX, DEFAULT_START_INDEX))
    parser.add_argument('-stop_index', '-end', type=int, nargs='?',
                        const=CONST_STOP_INDEX, default=DEFAULT_STOP_INDEX,
                        help='stop_index (defaults: %d/%d)' % (CONST_STOP_INDEX, DEFAULT_STOP_INDEX))
    parser.add_argument('-webster', action='store_true',
                        help='parse a dictionary in the format of Websters Unabridged.')
    parser.add_argument('-words', dest='max_words', type=int, nargs='?', const=CONST_MAX_WORDS, default=0,
                        help='maximum words per paragraph: print only the first M words,\
                        or all if M < 1 (default: 0)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    verbose = args.verbose

    if args.webster:
        parse_webster_file(args.text_file, args.start_index, args.stop_index, args.charset, verbose)
        exit(0)

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
