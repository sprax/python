#!/usr/bin/env python3
# Sprax Lines       2016.12.27
'''Filter POS-tagged text'''

# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize, pos_tag
# from string import punctuation
import argparse
import heapq
import math
import string
import sys
from collections import defaultdict
import nltk
import text_ops
import text_fio
import text_ops

LINE_MAX = 15

class PosFilter:
    '''Filter out some parts of speech, such as adverbs'''

    def __init__(self, verbose=1, out_tags=['RB'], con_tags=['CC', ',']):
        '''Initialize the POS filter with the tags of words to filter,
        and the tags of joining words to filter.'''
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self.out_tags = out_tags
        self.con_tags = con_tags
        self.verbose = verbose

    def filter_paragraph(self, paragraph):
        '''Filter a single paragraph containing one or more sentences.'''
        filtered = []
        sentences = nltk.sent_tokenize(paragraph)
        for sentence in sentences:
            if self.verbose > 1:
                print()
                print(sentence)
            inside = False
            output = []
            tokens = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokens)
            for wt in tagged:
                if wt[1] in self.out_tags:
                    inside = True
                    if self.verbose > 1:
                        print("Filter out:", wt[0])
                elif inside and wt[1] in self.con_tags:
                    print("Filter con:", wt[0])
                else:
                    inside = False
                    output.append(wt[0])
            filtered.extend(output)
        # return ' '.join(filtered[:-1]) + filtered[-1] if filtered else ''
        return join_tokenized(output)

def join_tokenized(tokens):
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

def filter_file(filter, path, verbose, charset='utf8'):
    '''Filter all paragraphs in a text file'''
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(text_ops.paragraph_iter(text)):
            if verbose > 3:
                print("    Paragraph {}:".format(idx))
                utf_print(para)
            yield filter.filter_paragraph(para)

###############################################################################

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('text_spec', type=str, nargs='?', default='corpus.txt',
                        help='text file containing text to summarize')
    parser.add_argument('-index', dest='indices_only', action='store_true',
                        help='output only the indices of summary sentences')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each summary sentence')
    parser.add_argument('-fM', '-freq_max', dest='max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-fm', '-freq_min', dest='min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-num_sentences', dest='sum_count', type=int, nargs='?', const=1, default=0,
                        help='max number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', const='-',
                        help='output file for summarized text (default: None)')
    parser.add_argument('-percent', dest='sum_percent', type=float, nargs='?',
                        const=16.6667, default=10.0,
                        help='percentage of sentences to keep (default: 10.0%%)')
    parser.add_argument('-serial', action='store_true',
                        help='summarize each paragraph in series')
    parser.add_argument('-truncate', dest='max_print_words', type=int, nargs='?',
                        const=8, default=0,
                        help='truncate sentences after MAX words (default: INT_MAX)')
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=2,
                        help='verbosity of output (default: 2)')
    args = parser.parse_args()

    if args.verbose > 3:
        print("outfile: <{}>".format(args.out_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    # summary_file = getattr(args, 'out_file', None)
    pos_filter = PosFilter(args.verbose)
    for y in filter_file(pos_filter, args.text_spec, args.verbose, charset='utf8'):
        print(y)

if __name__ == '__main__':
    main()
