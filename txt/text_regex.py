#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
Plan:
    Words|phrases -> words >= [phonetic syllables reprs]
    Emojis >= [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import argparse
import re
import string

EXAMPLES = [
    # (text, words, syllables)
    ("There isn't one empyrean ouroborous; everyone knows there've always been several.", 11, 24),
    #  1   2  3  4   5  6 78   9 0 1  2   3 4* 5     6     7  8   9  0    1    2 3 4
    ('"There aren\'t really any homogeneous cultures," you\'ll say, "they\'ve always shown rifts."', 12, 21),
    #   1   2        3   5 6 7  8 9 0 1 2   3  4        5      6      7      8  9     0    1
    ('"Ain\'t all y\'all young\'uns under 17," she\'d said, "like 11- or 15-years old?!"', 13, 21),
    #  1     2      3    4     5   6  7  +3     1     2      3   +3  7  +2  0    1}
    ("Didn't you know my X-15's XLR-99 engine burned 15,000 pounds (6,717 kg) of propellant in 87 seconds?", 17, 35),
    # 1  2   3    4   5 6 +2    +3 +2 4  5    6     +2  +2  1     +3  +8 +3  6    7 8  9   0  +3  4 5
    (" _This Is _My_ Title_, you one-eyed jack-ass!!", 7, 11),
    #    1  2   3  4  5  6     7  8   9    0   1
]

DICTIONARY = {}

def load_dictionary(path, verbose=0):
    '''load dictionary from text file, one word per line'''
    word_count = 0
    with open(path) as text:  # opened in text-mode; all EOLs are converted to '\n'
        for line in text:
            line = line.strip()
            if line:
                word_count += 1
                DICTIONARY[line] = len(line)
    if verbose > 1:
        print("Loaded", word_count, "words from dictionary file: ", path)
    return DICTIONARY, word_count

def is_word(token):
    '''true iff token is in the DICTIONARY'''
    return DICTIONARY.get(token)

def is_name(token):
    '''true iff only first letter is upper word'''
    return len(token) > 1 and token[0].isupper() and token[1:].islower()

def gen_words_only(tokens, verbose=0):
    '''generator that keeps only DICTIONARY words'''
    if not DICTIONARY:
        load_dictionary('../words.txt', verbose)
    return (token for token in tokens if is_word(token))


def gen_words_or_names(tokens, verbose=0):
    '''
    generator that keeps only DICTIONARY words or proper names,
    where names are presumed proper IFF only the first letter is a capital.
    '''
    if not DICTIONARY:
        load_dictionary('../words.txt', verbose)
    # for token in tokens:
    #     if is_name(token) or is_word(token):
    #         yield token
    return (token for token in tokens if is_name(token) or is_word(token))

###############################################################################
RE_LOWER_LETTER_WORD = re.compile(r"\b([a-z]+)\b")

def lower_word_tokens(text):
    '''extract only lowercase alphabetic words'''
    return RE_LOWER_LETTER_WORD.findall(text)

###############################################################################
RE_ANY_LETTER_WORD = re.compile(r"([A-Za-z]+)")

def letter_word_tokens(text, min_len=3):
    '''extract lower-cased alphabetic words'''
    words = []
    for match in RE_ANY_LETTER_WORD.finditer(text):
        token = match.group()
        if len(token) < min_len:
            continue
        words.append(token.lower())
    return words


# WORD_SEP_INTERIOR = r"',."
WORD_SEP_INTERIOR = r"-',."

###############################################################################
RE_NORMAL_WORD = re.compile(r"\b([A-Z]?[a-z]+)\b")

def gen_normal_word_tokens(text, min_len=3):
    '''extract normal alphabetic words'''
    for match in RE_NORMAL_WORD.finditer(text):
        token = match.group()
        if len(token) >= min_len:
            yield token


# WORD_SEP_INTERIOR = r"',."
WORD_SEP_INTERIOR = r"-',."

###############################################################################
RE_WORD_TOKEN = re.compile(r"((?:\w+[{}]\w*)+\w|\w+)".format(WORD_SEP_INTERIOR))

def word_tokens(sentence):
    r'''
    Returns tokens comprised of word chars (\w) embedding one or more single
    interior punctuation characters (',.-) ').  Because \w matches _, tokens
    are stripped of _ (underscores) at either end.
    '''
    words = RE_WORD_TOKEN.findall(sentence)
    return [word.strip('_') for word in words]

###############################################################################
RE_NOT_NON_WORD_TOKEN = re.compile(r"((?:[^\W_]+[{}][^\W_]*)+[^\W_]|[^\W_]+)".format(WORD_SEP_INTERIOR))

def notnonword_tokens(sentence):
    r'''
    Returns tokens comprised of not non-word chars (\W and _) surrounding one or more
    individual interior punctuation characters (-',.) ').  Because \w matches _,
    \W does not match _, so we must add it to the characters that cannot begin, end, or
    be contained inside a word.
    '''
    return RE_NOT_NON_WORD_TOKEN.findall(sentence)
    # return [word.strip('_') for word in words]


def replace_non_non_words(rep_func, text_phrase):
    '''replace other than non-words with text_phrase'''
    return RE_NOT_NON_WORD_TOKEN.sub(rep_func, text_phrase)

###############################################################################
WORD_SEP_EXTERIOR = r'!"#$%&()*+./:;<=>?@[\]^_`{|}~\x82\x83\x84\x85\x86\x87\x88\x89' \
                    r'\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99'

RE_WORD_SEP_PATTERN = r"\s+[{}]+\s*|\s*[{}]+\s+|[{}]*[\s{}]+|\s+".format(
    WORD_SEP_INTERIOR, WORD_SEP_INTERIOR, WORD_SEP_INTERIOR, WORD_SEP_EXTERIOR)

RE_WORD_SPLITTER = re.compile(r"(?:{})".format(RE_WORD_SEP_PATTERN))

RE_WORD_SEPARATOR = re.compile(r"({})".format(RE_WORD_SEP_PATTERN))

def words_split_out(sentence_body):
    '''split out non-empty words'''
    splits = RE_WORD_SPLITTER.split(sentence_body)
    return [ss for ss in splits if len(ss) > 0]

def words_and_separaters(sentence_body):
    '''returns list of words and their separators'''
    separated = RE_WORD_SEPARATOR.findall(sentence_body)
    return [ss for ss in separated if len(ss) > 0]

def gen_words_and_separaters(sentence_body):
    '''generator for words and separators'''
    separated = RE_WORD_SEPARATOR.finditer(sentence_body)
    for sep in separated:
        if len(sep) > 0:
            yield sep


###############################################################################
REC_BEG_MID_END = re.compile(r"(^\W*)\b(\w.*\w)\b(\W*$)", re.DOTALL|re.MULTILINE)

def sentence_beg_body_and_end(sentence):
    '''return sentence parts as [beg, body, end] where beg and end may be 0-length'''
    try:
        return REC_BEG_MID_END.match(sentence).groups()
    except AttributeError:
        return ['', sentence, '']

# The < is for <3, <=, <--, etc.
WORD_EXT_BEG = r'[<]'

# The . is for abbreviations; any sentence-ending punctuation should already be removed.
WORD_EXT_END = r'[_%.>]'

RE_WORD_EXT = re.compile(r"((?:{}?[\w]+[{}]*)[\w]+{}?|{}?\w{}?)".format(
    WORD_EXT_BEG, WORD_SEP_INTERIOR, WORD_EXT_END, WORD_EXT_BEG, WORD_EXT_END))

def replace_words_extended(rep_func, text_phrase):
    '''replace words as matching the extended pattern'''
    return RE_WORD_EXT.sub(rep_func, text_phrase)

###############################################################################
REGEX_PUNCTUATION = re.compile("[{}]".format(string.punctuation))
REGEX_NON_ALPHA = re.compile(r'(?:\W|[0-9])+')
###############################################################################

def extract_word_set_from_file(path, extractor):
    '''extract set of words from file'''
    words = set()
    with open(path, "r") as text:
        for line in text:
            tokens = extractor(line)
            words.update(tokens)
    return words

def extract_lower_words_from_file(path, extractor):
    '''get only the lower-case words from the file at path'''
    words = set()
    with open(path, "r") as text:
        for line in text:
            tokens = extractor(line)
            words.update([tok for tok in tokens if len(tok) > 1 and tok.islower()])
    return words

def print_sorted(iterable, end=' '):
    '''print as list'''
    for item in sorted(list(iterable)):
        print(item, end=end)

def main():
    '''test regex patterns for text: separate words'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test english -> emoji translation")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input_file')
    parser.add_argument('-extract_words', action='store_true',
                        help='extract all lowercase words from a file')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    parser.add_argument('-words_only', '-wrdo', action='store_true',
                        help='extract only dictionary words')
    parser.add_argument('-words_or_names', '-won', action='store_true',
                        help='extract only dictionary words or proper names')
    args = parser.parse_args()
    # test_misc()

    if args.extract_words:
        # print_sorted(extract_lower_words_from_file(args.input_file, notnonword_tokens))
        # print_sorted(extract_word_set_from_file(args.input_file, letter_word_tokens))
        # print_sorted(extract_word_set_from_file(args.input_file, lower_word_tokens))
        words = extract_word_set_from_file(args.input_file, gen_normal_word_tokens)
        if args.words_or_names:
            words = gen_words_or_names(words, args.verbose)
        elif args.words_only:
            words = gen_words_only(words, args.verbose)
        print_sorted(words)
        print()
        exit(0)

    print("NUM_TOKENS          WORD_TOKENS:")
    for sentence, words, syllables in EXAMPLES:
        print("MANUAL", words, sentence)
        tokens = word_tokens(sentence)
        print("TOKENS", len(tokens), tokens)
        swords = words_split_out(sentence)
        print("SPLITS", len(swords), swords)
        nuwrds = notnonword_tokens(sentence)
        print("NOTUNS", len(nuwrds), nuwrds)
        print("SYLABS", syllables)
        print()


if __name__ == '__main__':
    main()
