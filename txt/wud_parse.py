#!/usr/bin/env python3
# Note: do not use Latin-1 encoding, because it would force string
# Sprax Lines       2017.07.01      Written with Python 3.5
'''Parase Webster's Unabridge Dictionary.
   * Output will eventually be JSON and Pickle files
   * Semantic graph would be nice, too.
    TODO: Eliminate suffix by making separate metrics dicts.
    TODO: Separate files: matchers, DictEntry(?), WebsterEntry, driver
'''

# from string import punctuation
import argparse
import pprint
import re
# import sys
import time
from collections import defaultdict

from utf_print import utf_print

RE_PARA_SEPARATOR = re.compile(r'\s*\n')


################################################################################

def paragraph_iter(fileobj, rgx_para_separator=RE_PARA_SEPARATOR, sep_lines=0):
    r'''
    yields paragraphs from text file and regex separator, which by default matches
    one blank line (only space before a newline, or r"\s*\n").  All but the first
    paragraph will begin with the separator, unless it contains only whitespace,
    which is stripped from the end of every line.
    TODO: Consider adding span-matching for square brackets, that is, never
    breaking a paragraph on text between an open bracket [ and a matching, i.e.
    balance end bracket ].  Likewise { no break between curly braces }.
    '''
    ## Makes no assumptions about the encoding used in the file
    paragraph, blank_lines = '', 0
    for line in fileobj:
        #print("    PI: line(%s) para(%s)" % (line.rstrip(), paragraph))
        if re.match(rgx_para_separator, line) and paragraph and blank_lines >= sep_lines:
            yield paragraph
            paragraph, blank_lines = '', 0
        line = line.rstrip()
        if line:
            blank_lines = 0
            if not paragraph:
                paragraph = line
            elif paragraph.endswith('-'):
                paragraph += line
            else:
                paragraph += ' ' + line
        else:
            blank_lines += 1
    if paragraph:
        yield paragraph

def is_blank_line(line):
    '''detect blank line by character comparison: SP, TAB, LF, CR'''
    for char in line:
        if char != ' ' and char != '\t' and char != '\n' and char != '\r':
            return False
    return True

REC_BLANK_LINE = re.compile(r'^\s*$')

def is_blank_line_re(line):
    r'''detect blank line by regex r"^\s*$" match '''
    return REC_BLANK_LINE.match(line)

REC_WORDY = re.compile(r'\w+')

def is_wordy_re(line):
    r'''true IFF line contains regex word characters (\w+)'''
    return REC_WORDY.search(line)

def is_not_lower(line):
    r'''true IFF line contains regex word characters (\w+)'''
    return REC_WORDY.search(line)



################################################################################

REP_UPPER_WORD_ONLY = r'^[A-Z-]+\s*$'
REC_UPPER_WORD_ONLY = re.compile(REP_UPPER_WORD_ONLY)

REP_UPPER_ENTRY_KEY = r"^(?P<word_1>(?:[A-Z]+['-]?\ ?)+[A-Z]+['-]?\b|[A-Z]+['-]?|[A-Z\ '-]+)"\
                      r"(?:;\s+(?P<word_2>[A-Z'-]+))?(?:;\s+(?P<word_3>[A-Z'-]+))?$"
REC_UPPER_ENTRY_KEY = re.compile(REP_UPPER_ENTRY_KEY)

def lex_entry_ns_iter(fileobj, rec_para_separator=REC_UPPER_ENTRY_KEY, sep_lines=1):
    '''
    Yields paragraphs (including newlines) representing lexion entries from a text
    file and regex separator, which by default matches a blank line followed by an
    all-uppercase word.  The all-caps word is included in the paragraph, as are any
    newlines upto the next paragraph separator.  In general, lines are not stripped
    of whitespace.
    TODO: stop counting blank_lines and entry_lines.
    '''
    ## Makes no assumptions about the encoding used in the file
    paragraph, blank_lines, entry_lines = '', 0, 0
    for line in fileobj:
        #print("    PI: line(%s) para(%s)" % (line.rstrip(), paragraph))
        match = rec_para_separator.match(line)
        if match and paragraph and blank_lines >= sep_lines:
            yield paragraph.rstrip()
            paragraph, blank_lines, entry_lines = '', 0, 0
        if is_blank_line(line):
            if paragraph:
                paragraph += "\n"
                entry_lines += 1
            blank_lines += 1
        else:
            blank_lines = 0
            if paragraph:
                paragraph += line
                entry_lines += 1
            else:
                paragraph = line
                entry_lines = 1
    if paragraph:
        yield paragraph.rstrip()

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

def paragraph_reader(path, charset="utf8", rgx_para_separator=RE_PARA_SEPARATOR):
    '''opens text file and returns paragraph iterator'''
    try:
        text_stream = open(path, 'r', encoding=charset)
        return paragraph_iter(text_stream, rgx_para_separator), text_stream
    except FileNotFoundError as ex:
        print("Warning:", ex)
        return None, None

def para_iter_file(path, rgx_para_separator=RE_PARA_SEPARATOR, charset='utf8', sep_lines=0):
    '''Generator yielding filtered paragraphs from a text file'''
    # print("para_iter_file: pattern: %s" % rgx_para_separator.pattern)
    with open(path, 'r', encoding=charset) as text:
        for para in paragraph_iter(text, rgx_para_separator, sep_lines):
            yield para

###############################################################################

def para_ns_iter_lex_file(path, rgx_para_separator=REC_UPPER_ENTRY_KEY, charset='utf8', sep_lines=1):
    '''Generator yielding filtered paragraphs (including newlines) from a lexicon file'''
    # print("para_ns_iter_lex_file: pattern: %s" % rgx_para_separator.pattern)
    with open(path, 'r', encoding=charset) as text:
        for para in lex_entry_ns_iter(text, rgx_para_separator, sep_lines):
            yield para

def put(*args, sep=''):
    '''print args with the empty string as the default separator.'''
    utf_print(*args, sep=sep)

REC_FIRST_WORD_TOKEN = re.compile(r'^(-?\w+|\W*\w+-?)')

def first_token(text, default=None):
    '''return the first word-like token parsed from a string'''
    try:
        return REC_FIRST_WORD_TOKEN.match(text).groups()[0]
    except AttributeError:
        return default

def print_groups(match):
    '''print groups from a regex match'''
    if match:
        for grp in match.groups():
            print("  {}".format(grp))

# REP_WEBSTER1 = r'\n([A-Z-]+)\s+([^\s,]+)[^,]*,\s+((?:[a-z]\.\s*)+)'\
#                 '(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s)([^.]+)?'
# REP_WEBSTER = r"([A-Z'-]+)\s+([^\s,]+)[^,]*,\s+((?:[a-z]\.\s*)+)"\
#                "(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s+)?((?:[^.]+.\s+)*)"
#
# REP_SPC = r'[\s.,]+'
# REP_WEBSTER = r'([A-Z-]+)\s+([^\s\(\[,]+)\s*(\([^(]+\))?(\[[^\]]+\])?([^,]*,?)\s+'\
#                '((?:[a-z]\.\s*)+)?(?:Etym:\s+\[([^]]+)\])?\s*(?:Defn:\s+)?((?:[^.]+.\s+)*)'
# REC_WEBSTER = re.compile(REP_WEBSTER)


EXAMPLE = "BACE Bace, n., a., & v."

REP_PART = r'(?:a|adv|conj|i|imp|interj|n|p|pl|pre[pt]|pron|sing|superl|t|v)'

# TODO: Add "fem." (female) like "pl." for plural

# FIXME TODO: Two passes:
# First pass regex to detect the number of words:
#   a) how many variants (word_1, word_2, etc., e.g. IMAM; IMAN; IMAUM)
#   b) how many words in each variant (e.g. BANK BILL, ICELAND MOSS)
# Second pass regex depends on what's found in the first pass.

REC_WEBSTER = re.compile(r"""
    ^(?P<word_1>(?:[A-Z]+['-]?\ ?)+[A-Z]+['-]?\b|[A-Z]+['-]?|[A-Z\ '-]+) # Primary WORD and whitespace
    (?:;\ +(?P<word_2>[A-Z'-]+))?                   # WORD 2 (variant spelling)
    (?:;\ +(?P<word_3>[A-Z'-]+))?\n                 # WORD 3 (variant spelling)
    (?P<pron_1>[A-Z-](?:\w*[\`\'"*-]?\ ?)+\w+[\`\'"*-]?(?:\(\#\))?|[A-Z]-?(?:\(,\ )?)? # Pron 1 (Capitalized)
    (?:(?:,|\ or)\ *(?P<pron_2>[A-Z][^\s\(\[,.]+)(?:\(\#\))?)?          # Pronunciation 2 (for variant 2)
    (?:,\ *(?P<pron_3>[A-Z][^\s\(\[,.]+))?[\ .,]*   # Pronunciation 3 (for variant 2)
    (?:\ *\((?P<pren1a>[^\)]+)\)\.?)?               # parenthesized 1a
    (?:,?\ *(?P<part1a>{}\.(?:(?:,?|\ &|\ or)\ {}\.)*))?   # part of speech for first definition (order varies)
    (?:[\ ,;]*(?P<plural>(?:[A-Z]\.\s+)?pl\.\s+(?:(?:[A-Z]\.\s+)?-?\w+[\w\ -]*-?\w+\s*[;,.(#)]+\ *)+))? # plural form/suffix
    (?:\ *\((?P<pren1b>[^\)]+)\)\s*)?               # parenthesized 1b
    (?:\.?\s*\[(?P<brack1>[^\]]+)\])?               # bracketed 1
    (?:\.?\s*(?P<part1b>(?:{}\s*\.\s*)+))?          # part of speech for first definition (order varies)
    (?:\.?\s*\[(?P<brack2>[^\]]+)\])?               # bracketed 2
    (?:\.?\s*Note:\s+\[(?P<note_1>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?       # Note
    (?:\.?\s*Etym:\s+\[(?P<etym_1>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?     # Etymology
    (?:\.?\s*Etym:\s+\[?(?P<etym_2>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?       # Etymology
    (?:\.?\s*Note:\s+\[(?P<note_2>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?       # Note
    (?:\.?\s*\[(?P<brack3>[^\]]+)\])?               # bracketed 3
    (?:\.?\s+\[(?P<obstag>Obs|R)\.\])?              # Obsolete tag
    (?:\.?[\ \n]\((?P<dtype1>\w[\w\s&.]+\.?)\))?    # subject field abbreviations, e.g. (Arch., Bot. & Zool.)
    (?:\.?\s*(?P<dftag1>Defn:|1\.|\(a\)|Lit\.,?)\s+\.?\s*(?P<defn_1>[^.]+(?:\.|$)))?\s*   # Defn 1 tag and first sentence of definition.
    (?P<defn1a>[A-Z][^.]+\.)?\s*                # definition 1 sentence 2
    (?P<usage1>".*"[^\d]+)?\s*                  # example 1
    (?P<defn_2>\d.\s[^\d]+)?                    # definition 2, ...
    (?P<cetera>.*)?$                            # etc.
""".format(REP_PART, REP_PART, REP_PART), re.DOTALL|re.MULTILINE|re.VERBOSE)

# Negative lookahead: (?:\.?\s*Etym:\s+\[(?P<etym_1>(?!\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)).+)\]?)?
# Negative lookahead: r"(?:\.?\s*Etym:\s+\[(?P<etym_1>(?!\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)).+)\]?)?"
# Breaks more than it fixes: (?:\ *(?P<pron1a>Also\ [A-Z-](?:\w*[\`\'"*-]?\ ?)+\w+[\`\'"*-]?(?:\(\#\))?|[A-Z]-?(?:\(,\ )?))? # Pron 1 (Capitalized)

REC_PARTIAL = re.compile(r"""
    ^(?P<word_1>(?:[A-Z]+['-]?\ ?)+[A-Z]+['-]?\b|[A-Z]+['-]?|[A-Z\ '-]+) # Primary WORD and whitespace
    (?:;\ +(?P<word_2>[A-Z'-]+))?                   # WORD 2 (variant spelling)
    (?:;\ +(?P<word_3>[A-Z'-]+))?\n                 # WORD 3 (variant spelling)
    (?P<pron_1>[A-Z-](?:\w*[\`\'"*-]?\ ?)+\w+[\`\'"*-]?(?:\(\#\))?|[A-Z]-?(?:\(,\ )?)? # Pron 1 (Capitalized)
    (?:(?:,|\ or)\ *(?P<pron_2>[A-Z][^\s\(\[,.]+)(?:\(\#\))?)?          # Pronunciation 2 (for variant 2)
    (?:,\ *(?P<pron_3>[A-Z][^\s\(\[,.]+))?[\ .,]*   # Pronunciation 3 (for variant 2)
    (?:\ *\((?P<pren1a>[^\)]+)\)\.?)?               # parenthesized 1a
    (?:,?\ *(?P<part1a>{}\.(?:(?:,?|\ &|\ or)\ {}\.)*))?   # part of speech for first definition (order varies)
    (?:[\ ,;]*(?P<plural>(?:[A-Z]\.\s+)?pl\.\s+(?:(?:[A-Z]\.\s+)?-?\w+[\w\ -]*-?\w+\s*[;,.(#)]+\ *)+))? # plural form/suffix
    (?:\ *\((?P<pren1b>[^\)]+)\)\s*)?               # parenthesized 1b
    (?:\.?\s*\[(?P<brack1>[^\]]+)\])?               # bracketed 1
    (?:\.?\s*(?P<part1b>(?:{}\s*\.\s*)+))?          # part of speech for first definition (order varies)
    (?:\.?\s*\[(?P<brack2>[^\]]+)\])?               # bracketed 2
    (?:\.?\s*Note:\s+\[(?P<note_1>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?       # Note
    (?:\.?\s*Etym:\s+\[(?P<etym_1>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?     # Etymology
    (?:\.?\s*Etym:\s+\[?(?P<etym_2>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?       # Etymology
    (?:\.?\s*Note:\s+\[(?P<note_2>[^\]]+?(?=\]|\n\n|\s+Defn:|\s+1\.|\n+\(a\)))\]?)?       # Note
    (?:\.?\s*\[(?P<brack3>[^\]]+)\])?               # bracketed 3
    (?:\.?\s+\[(?P<obstag>Obs|R)\.\])?              # Obsolete tag
    (?:\.?[\ \n]\((?P<dtype1>\w[\w\s&.]+\.?)\))?    # subject field abbreviations, e.g. (Arch., Bot. & Zool.)
    (?:\.?\s*(?P<dftag1>Defn:|1\.|\(a\)|Lit\.,?)\s+\.?\s*(?P<defn_1>[^.]+(?:\.|$)))?\s*   # Defn 1 tag and first sentence of definition.
    (?P<defn1a>[A-Z][^.]+\.)?\s*                # definition 1 sentence 2
    (?P<usage1>".*"[^\d]+)?\s*                  # example 1
    (?P<defn_2>\d.\s[^\d]+)?                    # definition 2, ...
    (?P<cetera>.*)?$                            # etc.
""".format(REP_PART, REP_PART, REP_PART), re.DOTALL|re.MULTILINE|re.VERBOSE)

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#
'''
Partial:
    # Add pron1a right after part1a:
    (?:,?\ *(?P<part1a>{}\.(?:(?:,?|\ &|\ or)\ {}\.)*))?   # part of speech for first definition (order varies)
    (?:\ *(?P<pron1a>Also\ [A-Z-](?:\w*[\`\'"*-]?\ ?)+\w+[\`\'"*-]?(?:\(\#\))?|[A-Z]-?(?:\(,\ )?))? # Pron 1 (Capitalized)



Webster:
  # (?:\.?\s*\[(?P<brack1>[^\]]+)\])?               # bracketed
    (?P<sepsp1>[\s.,]*?)?                           # non-greedy space, punctuation(period, comma)
  # (?:\s*(?P<part1b>(?:{}\s*\.\s*)+))?             # part of speech for first definition (order varies)


    (?:,?\ *(?P<part1a>(?:(?:{})\ *\.?(?:\ &|[\ ,;]+|\ or\ )?)+)(?:\.,?|\ (?=\[)|\n\n))?   # part of speech for first definition (order varies)

    (?P<sepsp1>[\s.,]*?)?                       # non-greedy space, punctuation(period, comma)

PLURAL:
    (?:\s*;?\s*(?P<plural>((?:[A-Z]\.\s+)?pl\.\s+\w+[\w\ -]*\w+)\s*[;,.]\s*)+)?
    # plural form or suffix, usually for irregulars

  Webster:
    (?:\s*Etym:\s+\[(?P<etym_1>[^\]]+?)(?:\]\.?|\n\n|\s+Defn:|\s+1\.))?       # etymology

    (?:(?P<dftag1>Defn:|1\.)\s+\.?\s*(?P<defn_1>[^.]+\.))?\s+   # Defn 1 tag and first sentence of definition.

'''

def show_partial_match(matgadd, entry_index, reason):
    '''Show partial regex match as seeded by the match's groupdict'''
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>  Partial  %d  %s  %s" % (entry_index, matgadd["word_1"], reason))
    put("\t",
        "word_1: (", matgadd["word_1"], ") \t",
        "word_2: (", matgadd["word_2"], ") \t",
        "word_3: (", matgadd["word_3"], ") \n\t",
        "pron_1: (", matgadd["pron_1"], ") \t",
        "pron_2: (", matgadd["pron_2"], ") \t",
        "pron_3: (", matgadd["pron_3"], ") \n\t",
        "pren1a: (", matgadd["pren1a"], ") \n\t",
        "part1a: (", matgadd["part1a"], ") \t",
        "plural: (", matgadd["plural"], ") \n\t",
        "pren1b: (", matgadd["pren1b"], ") \n\t",
        "brack1: (", matgadd["brack1"], ") \n\t",
        "part1b: (", matgadd["part1b"], ") \n\t",
        "etym_1: (", matgadd["etym_1"], ") \n\t",
        "etym_2: (", matgadd["etym_2"], ") \n\t",
        "note_2: (", matgadd["note_2"], ") \n\t",
        "brack2: (", matgadd["brack2"], ") \n\t",
        "obstag: (", matgadd["obstag"], ") \n\t",
        "dtype1: (", matgadd["dtype1"], ") \n\t",
        "dftag1: (", matgadd["dftag1"], ") \n\t",
        "defn_1: (", matgadd["defn_1"], ") \n\t",
        "usage1: (", matgadd["usage1"], ") \n\t",
        "defn1a: (", matgadd["defn1a"], ") \n\t",
        "defn_2: (", matgadd["defn_2"], ") \n\t",
        "cetera: (", matgadd["cetera"], ") \n\t",
       )

###############################################################################
class DictEntry:
    def __init__(self, suffix, entry_dict):
        '''Creates a DictEntry from a raw dict, such as from match.groupdict()'''
        self.label = suffix
        self.table = entry_dict
        self.undef = entry_dict.get('defn_1') == None
        self.empty = not entry_dict

    def get(self, key):
        '''Return key's value or KeyError if not present'''
        return self.table[key]

    def getlow(self, key):
        '''Return value lowered or KeyError'''
        text = self.get(key)
        return text.lower() if text else None

def make_dict_entry(metrics, suffix, index, matcher, entry_text):
    '''Create a DectEntry object from a dictionary text entry and update metrics.
    If the entry_text fails to parse, an object with an empty data store is returned.'''
    beg = time.time()
    mat = matcher(entry_text)
    end = time.time()
    metrics[str(index) + suffix] = end - beg
    if mat:
        metrics['matched' + suffix] += 1
        dict_entry = DictEntry(suffix, mat.groupdict())
        if dict_entry.undef:
            metrics['undef' + suffix] += 1
    else:
        metrics['unmatched' + suffix] += 1
        dict_entry = DictEntry(suffix, {})
    return dict_entry


###############################################################################
class WebsterEntry:
    '''Represents a parsed dictionary entry a la Webster's Unabridged'''
    def __init__(self, webs_dict):
        '''TODO: bifurcate on word_2 if present'''
        self.dict = webs_dict
        self.word_1 = webs_dict.getlow('word_1')
        self.word_2 = webs_dict.getlow('word_2')
        self.word_3 = webs_dict.getlow('word_3')
        self.pron_1 = webs_dict.get('pron_1')
        self.pron_2 = webs_dict.get('pron_2')
        self.pron_3 = webs_dict.get('pron_3')
        self.pren1a = webs_dict.get('pren1a')
        self.pren1b = webs_dict.get('pren1b')
        self.brack1 = webs_dict.get('brack1')
        # self.sepsp1 = webs_dict.get('sepsp1')
        part1 = webs_dict.get('part1a')
        self.part_1 = part1 if part1 else webs_dict.get('part1b')
        self.plural = webs_dict.get('plural')
        self.etym_1 = webs_dict.get('etym_1')
        self.dftag1 = webs_dict.get('dftag1')
        self.defn_1 = webs_dict.get('defn_1')
        self.defn1a = webs_dict.get('defn1a')
        self.usage1 = webs_dict.get('usage1')
        self.defn_2 = webs_dict.get('defn_2')
        self.cetera = webs_dict.get('cetera')

    def __str__(self):
        stray = [
            "\tword_1: %s\t" % self.word_1,
            "word_2: %s\t" % self.word_2,
            "word_3: %s\n\t" % self.word_3,
            "pron_1: %s\t" % self.pron_1,
            "pron_2: %s\t" % self.pron_2,
            "pron_3: %s\n\t" % self.pron_3,
            "part_1: %s\n\t" % self.part_1,
            "plural: %s\n\t" % self.plural,
            "brack1: %s\n\t" % self.brack1,
            "etym_1: %s\n\t" % self.etym_1,
            "dftag1: %s\n\t" % self.dftag1,
            "defn_1: %s\n\t" % self.defn_1,
            "defn1a: %s\n\t" % self.defn1a,
            "usage1: %s\n\t" % self.usage1,
            "defn_2: %s\n\t" % self.defn_2,
            "cetera: %s\n\t" % self.cetera,
        ]
        strep = ''.join(stray)
        return strep

    def token_string(self):
        tokens = self.dict.get('word_1')
        word_2 = self.dict.get('word_2')
        if word_2:
            tokens += '; ' + word_2
            word_3 = self.dict.get('word_3')
            if word_3:
                tokens += '; ' + word_3
        return tokens

    def variants(self):
        '''return list of variant spellings'''
        variants = [self.word_1]
        if self.word_2:
            variants.append(self.word_2)
            if self.word_3:
                variants.append(self.word_3)
        return variants

    def parts_of_speech(self):
        '''return all identified parts of speech abbreviations'''
        return self.part_1

def match_webster_entry(entry):
    '''return regex match on dictionary entry text; trying only one pattern for now'''
    return REC_WEBSTER.match(entry)

def parse_webster_entry(entry):
    '''Return a dict representing a parsed dictionary entry.
    For now we just return the dict from a match's named groups.'''
    match = match_webster_entry(entry)
    if match:
        return match.groupdict()
    return None


def match_partial_entry(entry):
    '''return regex match on dictionary entry text; trying only one pattern for now'''
    return REC_PARTIAL.match(entry)

def parse_partial_entry(entry):
    '''Return a dict representing a partially matched dictionary entry.
    For now we just return the dict from a match's named groups.'''
    match = match_partial_entry(entry)
    if match:
        return match.groupdict()
    return None


def common_and_max_len(str_a, str_b):
    '''return index of first difference between two strings, or in other words,
    the length of their common leading substrings, and the maximum of their
    lengths.  May be applied to other subscriptables besides strings.'''
    maxlen = max(len(str_a), len(str_b))
    idx = 0
    for idx in range(maxlen):
        try:
            if str_a[idx] != str_b[idx]:
                return idx, maxlen
        except IndexError:
            break
    return idx + 1, maxlen

def index_diff(sub_a, sub_b):
    '''
    Return index of first difference between two strings or other
    subscriptable objects, or in other words, the length of their common prefixes.
    '''
    idx = 0
    for idx, tup in enumerate(zip(sub_a, sub_b)):
        if tup[0] != tup[1]:
            return idx
    return idx + 1 if idx else 0

def show_entry(entry_text, idx):
    '''Print the (possibly cleaned-up) text entry extracted from the input file.'''
    print("========================== beg Entry %d ==============================" % idx)
    utf_print(entry_text)
    print("-------------------------- end Entry %d ------------------------------" % idx)

###############################################################################

V_SHOW_ERROR = 1
V_SHOW_STATS = 2
V_SHOW_TOKEN_IF_MATCH_FAILED_W = 3
V_SHOW_TOKEN_IF_MATCH_FAILED_P = 4
V_SHOW_TEXT_MAT_FAIL_W = 6
V_SHOW_TEXT_MAT_FAIL_P = 7

# TODO: Start using this:
V_SHOW_BOTH_IF_UNDEF_B = 9      # Show webs and part if both are undefined.

V_SHOW_WEBS_IF_UNDEF_W = 10
V_SHOW_TEXT_IF_UNDEF_W = 11
V_SHOW_PART_IF_UNDEF_W = 12

V_SHOW_PART_IF_UNDEF_P = 13
V_SHOW_TEXT_IF_UNDEF_P = 14
V_SHOW_WEBS_IF_UNDEF_P = 14

V_SHOW_WEBS_ALWAYS = 20
V_SHOW_PART_ALWAYS = 21
V_SHOW_TEXT_ALWAYS = 22

M_DEFN_1_NOT_FOUND = "Main Defn1 Not Found"

def show_entry_on_verbose(webs_dict, part_dict, entry_text, entry_index, opts):
    if (opts.verbose > V_SHOW_TEXT_IF_UNDEF_W and webs_dict.undef and (opts.webster or opts.failover and part_dict.undef) or
        opts.verbose > V_SHOW_TEXT_IF_UNDEF_P and part_dict.undef and (opts.partial or opts.failover and webs_dict.undef) or
        opts.verbose > V_SHOW_TEXT_MAT_FAIL_W and webs_dict.empty and (opts.webster or opts.failover and part_dict.undef) or
        opts.verbose > V_SHOW_TEXT_MAT_FAIL_P and part_dict.empty and (opts.partial or opts.failover and webs_dict.undef) or
        opts.verbose > V_SHOW_TEXT_ALWAYS):
        show_entry(entry_text, entry_index)

def show_diff_webs_part(verbose):
    '''compute and show difference between full and partial regex patterns'''
    partial = REC_PARTIAL.pattern
    webster = REC_WEBSTER.pattern
    comlen, totlen = common_and_max_len(partial, webster)
    is_partial_different = comlen < totlen
    if verbose > V_SHOW_TOKEN_IF_MATCH_FAILED_W:
        if is_partial_different:
            print("Partial pattern matches Webster pattern up to:  %d/%d" % (comlen, totlen))
            print("Webster____%s____" % webster[comlen-24:comlen+24])
            print("Partial____%s____" % partial[comlen-24:comlen+24])
        else:
            print("Partial == Webster pattern:", totlen)
    return is_partial_different


def dict_entry_status(entry, tried):
    if entry.empty:
        return "FAILED MATCH" if tried else "not tried"
    else:
        return "is UNDEFINED" if entry.undef else "is defined"

def webster_partial_status(webs_dict, part_dict, opts):
    webs_stat = " (Webster " + dict_entry_status(webs_dict, opts.webster or opts.failover and part_dict.undef)
    part_stat = "; Partial " + dict_entry_status(part_dict, opts.partial or opts.failover and webs_dict.undef) + ")"
    return webs_stat + part_stat

def show_webster(webs_entry, index, status):
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<  Webster  %d  %s  %s" % (index, webs_entry.token_string(), status))
    utf_print(webs_entry)

###############################################################################
def parse_dictionary_file(path, opts, verbose=1):
    '''
    Parse Webster-like dictionary text file two-ways with failover and metrics.
    TODO: Better diagnostics.
    ALGO:
        #### Laziest that makes sure both A and B are initialized.  Easy to grok.
        if condA:
            A = makeA
            if condB or failover and A.empty:   # case of both condA and condB
                B = makeB
            else:
                B = emptyB
        elif condB:
            B = makeB
            if failover and B.empty:
                A = makeA
            else:
                A = emptyA
        else:
            A, B = emptyA, emptyB
    '''
    metrics = defaultdict(int)
    metrics['beg_time'] = time.time()
    is_partial_different = show_diff_webs_part(verbose)
    max_entry_time, max_time_index = 0, -1
    for idx, entry_text in enumerate(para_ns_iter_lex_file(path, charset=opts.charset)):
        if idx >= opts.start_index:
            metrics['read'] += 1

            beg_entry = time.time()

            if opts.webster:
                webs_dict = make_dict_entry(metrics, '_webs', idx, match_webster_entry, entry_text)
                if opts.partial or opts.failover and webs_dict.undef:
                    part_dict = make_dict_entry(metrics, '_part', idx, match_partial_entry, entry_text)
                else:
                    part_dict = DictEntry('_part', {})
            elif opts.partial:
                part_dict = make_dict_entry(metrics, '_part', idx, match_partial_entry, entry_text)
                if part_dict.undef and opts.failover:
                    webs_dict = make_dict_entry(metrics, '_webs', idx, match_webster_entry, entry_text)
                else:
                    webs_dict = DictEntry('_webs', {})
            else:
                webs_dict = DictEntry('_webs', {})
                part_dict = DictEntry('_part', {})

            entry_time = time.time() - beg_entry
            metrics[idx] = entry_time
            if (max_entry_time < entry_time):
                max_entry_time = entry_time
                max_time_index = idx

            show_entry_on_verbose(webs_dict, part_dict, entry_text, idx, opts)

            # TODO: unfold fields, starting with etym_1 and defn_1

            if verbose > V_SHOW_TOKEN_IF_MATCH_FAILED_W:
                if webs_dict.empty:
                    if opts.webster:
                        print(" {:<20} >>>> WEBSTER MATCH FAILED <<<< {:>6}".format(first_token(entry_text), idx))
                else:
                    webs_entry = WebsterEntry(webs_dict)
                    if (verbose > V_SHOW_WEBS_IF_UNDEF_W and webs_dict.undef or
                        verbose > V_SHOW_WEBS_IF_UNDEF_P and part_dict.undef or
                        verbose > V_SHOW_WEBS_ALWAYS):
                        show_webster(webs_entry, idx, webster_partial_status(webs_dict, part_dict, opts))

            if verbose > V_SHOW_TOKEN_IF_MATCH_FAILED_P:
                if part_dict.empty:
                    if opts.partial:
                        print(" {:<20} >>>> PARTIAL MATCH FAILED <<<< {:>6}".format(first_token(entry_text), idx))
                else:
                    part_entry =  WebsterEntry(part_dict)
                    if (verbose > V_SHOW_PART_IF_UNDEF_P and part_dict.undef or
                        verbose > V_SHOW_PART_IF_UNDEF_W and webs_dict.undef or
                        verbose > V_SHOW_PART_ALWAYS):
                        show_partial_match(part_dict.table, idx, webster_partial_status(webs_dict, part_dict, opts))

        if opts.stop_index > 0 and idx >= opts.stop_index:
            break

    metrics['max_entry_time'] = max_entry_time
    metrics['max_time_index'] = max_time_index
    metrics['end_time'] = time.time()
    return metrics

###############################################################################
def tried_matched_undef_defnd(metrics, suffix):
    match = metrics['matched' + suffix]
    tried = metrics['unmatched' + suffix] + match
    undef = metrics['undef' + suffix]
    defnd = match - undef
    return tried, match, undef, defnd

def percent(count, total):
    '''count/total as a percentage, or NAN if total <= 0'''
    return 100.0 * count / total if total > 0 else float('nan')

def print_metrics(metrics, suffix_a, suffix_b, verbose):
    '''pretty print metrics dict'''
    time_ab = metrics['end_time'] - metrics['beg_time']
    tried_a, match_a, undef_a, defnd_a = tried_matched_undef_defnd(metrics, suffix_a)
    tried_b, match_b, undef_b, defnd_b = tried_matched_undef_defnd(metrics, suffix_b)
    max_mat = max(match_a, match_b)
    print("Matched %d/%d in %.4f seconds, defined/matched:  Webs: %d/%d (%.1f%%),  Part: %d/%d (%.1f%%)" % (
        max_mat, metrics['read'], time_ab,
        defnd_a, match_a, percent(defnd_a, tried_a),
        defnd_b, match_b, percent(defnd_b, tried_b)))
    print("Unmatched & Undefined:    Webs %d & %d,    Part %d & %d" % (
        tried_a - match_a, undef_a,
        tried_b - match_b, undef_b))
    if verbose >= V_SHOW_STATS:
        max_index = metrics['max_time_index']
        print("Max entry parse time %.5f seconds for entry %d  (full: %.6f,  part: %.6f)" % (
            metrics['max_entry_time'], max_index,
            metrics[str(max_index) + suffix_a], metrics[str(max_index) + suffix_b]))
    return max_mat / time_ab if time_ab else 0.0


CONST_MAX_WORDS = 5
DEFAULT_NUMBER = 10
CONST_START_INDEX = 1
CONST_STOP_INDEX = 10
DEFAULT_START_INDEX = 0
DEFAULT_STOP_INDEX = 0

def main():
    '''Driver to iterate over the paragraphs in a dictionary text file.'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='text file containing quoted dialogue')
    parser.add_argument('-args', action='store_true',
                        help='Show args namespace.')
    parser.add_argument('-both', action='store_true',
                        help='Try both match-parsers: WUD and Partial.')
    parser.add_argument('-charset', dest='charset', type=str, default='utf-8',
                        help='Set charset encoding of input text to CHARSET (default utf-8, not iso-8859-1)')
    parser.add_argument('-failover-off', dest='failover', action='store_false',
                        help='Disable failover (trying the other parser if one fails, on by default)')
    parser.add_argument('-number', type=int, nargs='?', const=CONST_MAX_WORDS,
                        default=DEFAULT_NUMBER,
                        help='max number of entries to parse (defaults: %d/%d)' % (
                            CONST_MAX_WORDS, DEFAULT_NUMBER))
    parser.add_argument('-partial', action='store_true',
                        help='Do parse dictionary entries using the Partial matcher (more flexible than WUD).')
    parser.add_argument('-start_index', '-beg', type=int, nargs='?',
                        const=CONST_START_INDEX, default=DEFAULT_START_INDEX,
                        help='start_index (defaults: %d/%d)' % (CONST_START_INDEX, DEFAULT_START_INDEX))
    parser.add_argument('-stop_index', '-end', type=int, nargs='?',
                        const=CONST_STOP_INDEX, default=DEFAULT_STOP_INDEX,
                        help='stop_index (defaults: %d/%d)' % (CONST_STOP_INDEX, DEFAULT_STOP_INDEX))
    parser.add_argument('-webster', action='store_false',
                        help="Don't parse using default format tuned to Webster's Unabridged.")
    parser.add_argument('-words', dest='max_words', type=int, nargs='?', const=CONST_MAX_WORDS, default=0,
                        help='maximum words per paragraph: print only the first M words,\
                        or all if M < 1 (default: 0)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    verbose = args.verbose

    if args.both:
        args.webster = args.partial = True
    elif args.webster and args.partial:
        args.both = True
    if args.args:
        pprint.pprint(args)

    metrics = parse_dictionary_file(args.text_file, args, verbose)
    print_metrics(metrics, '_webs', '_part', verbose)


if __name__ == '__main__':
    main()
