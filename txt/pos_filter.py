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

    def __init__(self, verbose=1, tags=['RB'], inter_tags=['CC']):
        '''Initialize the POS filter with the tags of words to filter,
        and the tags of joining words to filter.'''
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self.tags = tags
        self.verbose = verbose

    def filter_paragraph(self, paragraph):
        '''Filter a single paragraph containing one or more sentences.'''
        filtered = []
        sentences = nltk.sent_tokenize(paragraph)
        for sentence in sentences:
            output = []
            tokens = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokens)
            for wt in tagged:
                if wt[1] not in self.tags:
                    output.append(wt[0])
                else:
                    print("Filter out:", wt[0])
            filtered.extend(output)
        return ' '.join(filtered)


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
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 3:
        print("outfile: <{}>".format(args.out_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    # summary_file = getattr(args, 'out_file', None)
    pos_filter = PosFilter()
    for y in filter_file(pos_filter, args.text_spec, args.verbose, charset='utf8'):
        print(y)

if __name__ == '__main__':
    main()
