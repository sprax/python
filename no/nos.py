#!/usr/bin/env python3
# Sprax Lines       2016.09.01      Written with Python 3.5
'''How many ways have writers written "No"?'''

import argparse
import heapq
import itertools
import re
import sys
from collections import defaultdict
from collections import Counter

import utf_print

class GetNo:
    '''Counts ways of saying No'''
    def __init__(self, adverb_file, corpus_file, verbose):
        self.adverb_file = adverb_file
        self.corpus_file = corpus_file
        self.corpus_words = count_words(corpus_file)
        self.adverb_freqs = load_counted_word_file(adverb_file)
        self.corpus_adverbs = count_counted_words(self)
        self.verbose = verbose
        numfreq = 20

        ## print_paragraphs(corpus_file)

        self.replies, self.denials = find_quoted_replies(corpus_file, verbose)

        if self.verbose > 1:
            print("The", numfreq, "most common corpus words:")
            for word, count in self.corpus_words.most_common(numfreq):
                print('    {:>7d} {}'.format(count, word))

        if self.verbose > 3:
            print("All adverbs in the corpus:")
            for word, count in self.corpus_adverbs.items():
                print(word, count)

        print("The", numfreq, "most common corpus adverbs:")
        for word in sorted(self.corpus_adverbs.keys(), key=self.corpus_adverbs.get,
            reverse=True)[:numfreq]:
            count = self.corpus_adverbs[word]
            print('    {:>7d} {}'.format(count, word))

        numfreq *= 4
        print("The", numfreq, "most common reply phrases:")
        for phrase, count in self.replies.most_common(numfreq):
            utf_print.utf_print('    {:>7d} {}'.format(count, phrase))

        print("The", numfreq, "most common denials:")
        for phrase, count in self.denials.most_common(numfreq):
            utf_print.utf_print('    {:>7d} {}'.format(count, phrase))


    def find_no(self):
        '''Look for ways of sayning No'''

    def show_no(self):
        '''Show frequent ways of saying No'''



def paragraphs(fileobj, separator='\n'):
    """Iterate a fileobject by paragraph"""
    ## Makes no assumptions about the encoding used in the file
    lines = []
    for line in fileobj:
        if line == separator and lines:
            yield ' '.join(lines)
            lines = []
        else:
            lines.append(line)
    yield ' '.join(lines)

def paragraphs_re(fileobj, separator='\n'):
    """Iterate a fileobject by paragraph"""
    ## Makes no assumptions about the encoding used in the file
    lines = []
    for line in fileobj:
        if re.match(separator, line) and lines:
            yield ' '.join(lines)
            lines = []
        else:
            line = line.rstrip().replace('’', "'")
            if line:
               lines.append(line)
    yield ' '.join(lines)


def print_paragraphs(path):
    print("print_paragraphs:")
    with open(path) as f:
        for idx, para in enumerate(paragraphs_re(f)):
            print("    Paragraph {}:".format(idx))
            print(para)
            print()

def count_counted_words(self):
    word_counts = {}
    for word in self.adverb_freqs.keys():
        count = self.corpus_words[word]
        if count > 0:
            word_counts[word] = count
    return word_counts

def load_counted_word_file(path):
    '''reads a text file of format <count word> into a dictionary'''
    word_counts = {}
    with open(path, 'r') as text:
        for line in text:
            count, word = line.split()
            word_counts[word] = count
            # print(count, word)
    return word_counts

def count_words(path):
    '''Returns a Counter that has counted all ASCII-only words found in a text file.'''
    rgx_match = re.compile(r"[A-Za-z]+")
    counter = Counter()
    with open(path, 'r', encoding="utf8") as text:
        for line in text:
            words = re.findall(rgx_match, line.rstrip())
            words = [x.lower() if len(x) > 1 else x for x in words]
            counter.update(words)
    return counter

def find_quoted_replies(path, verbose):
    '''Finds first 3 (or fewer) words starting quoted replies.
       Returns a defaultdict mapping these phrases to their counts.
       Words longer than 1-letter are lowercased.'''
    rgx_quoted_B = re.compile(r'(["])(?:(?=(\\?))\2.)*?\1')
    rgx_quoted_A = re.compile(r'([^"]+)')
    rgx_quoted = re.compile(r'"([^"]*)"')
    rgx_word = re.compile(r"[A-Z'’a-z]+")
    rgx_para_numbering = re.compile(r"^[^A-Za-z]*(\d|[ivx]+\.)")
    reply_counter = Counter()
    denial_counter = Counter()
    idx = 0
    with open(path, 'r', encoding="utf8") as text:
        for para in paragraphs_re(text):
            if re.match(rgx_para_numbering, para):
                continue
            quotes = re.findall(rgx_quoted, para)
            phrases = []
            is_denial = False
            for quote in quotes:
                if verbose > 3:
                    print("quote {}: {}".format(idx, quote))
                idx += 1
                phrase = []
                words = re.findall(rgx_word, quote)
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
                    is_question = is_question_word(phrase[0])
                    if is_denial and not is_question:
                        is_denial = False
                        denial_counter.update([joined])
                    phrases.append(joined)
            reply_counter.update(phrases)
            ## for ppp in phrases:
            ##    print("ppp: ", ppp)
    return reply_counter, denial_counter

def is_question_word(word):
    if word == "what":
        return True
    if word == "when":
        return True
    if word == "where":
        return True
    if word == "why":
        return True
    if word == "who":
        return True
    if word == "how":
        return True
    if word == "whence":
        return True
    return False

def count_chars_from_words(word_counter):
    '''Count chars from all words times their counts'''
    char_counter = Counter()
    for item in word_counter.items():
        for _ in range(item[1]):
            char_counter.update(item[0])
    return char_counter

def find_quoted_no_phrases(adverb_file, corpus_file, verbose):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.
    Uses the GetNo class.
    '''
    subs = GetNo(adverb_file, corpus_file, verbose)
    subs.find_no()

def main():
    '''Get file names for cipher and corpus texts and call
    find_quoted_no_phrases.'''

    parser = argparse.ArgumentParser(
            # usage='%(prog)s [options]',
            description="Count some quoted ways of saying 'No'",
            )
    parser.add_argument('adverb_file', type=str, nargs='?', default='adverb.txt',
            help='text file containing counted adverbs')
    parser.add_argument('corpus_file', type=str, nargs='?', default='corpus.txt',
            help='text file containing quoted dialogue')
    parser.add_argument('-verbose', nargs='?', const=1, default=2,
            help='verbosity of output (default: 1)')

    args = parser.parse_args()
    print(__doc__)
    print("args:", args)

    find_quoted_no_phrases(args.adverb_file, args.corpus_file, args.verbose)


if __name__ == '__main__':
    main()
