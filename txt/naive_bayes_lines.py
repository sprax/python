#!/usr/bin/env python3
# Sprax Lines       2017.01.29
'''Summarize text(s).'''

#SPRAX
# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize
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

LINE_MAX = 15

class TextFileWordFreqs:
    '''Text file line contents and word frequencies'''

    def __init__(self, file_spec, min_freq=0.1, max_freq=0.9, verbose=1, charset='utf8'):
        '''Initialize the text file word counter.'''
        self._min_freq = min_freq
        self._max_freq = max_freq
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self._filtered = False
        self._input_words = 0
        self._count_words = 0
        self._text_lines = []
        self._line_word_lists = []
        self._verbose = verbose
        self._word_counts = defaultdict(int)
        sum_len = 0
        for line in text_fio.read_lines(file_spec, charset):
            self._text_lines.append(line)
            sum_len += self.count_words(line)
        print(self._text_lines[ 0])
        print(self._text_lines[ 1])
        print(self._text_lines[-1])

    def count_words(self, line):
        '''Add a single paragraph containing one or more sentences.
        Return the count of sentences in text'''
        word_hash = {}
        word_list = nltk.word_tokenize(line.lower())
        # word_list = nltk.word_tokenize(sentence.decode("utf8").lower())
        for word in word_list:
            self._input_words += 1
            self._word_counts[word] += 1
            word_hash[word] = 1 + (word_hash[word] if word in word_hash else 0)
        self._line_word_lists.append(word_hash)
        return len(line)

    def sentence_count(self):
        return len(self._text_lines)

    def filter_words(self):
        '''apply thresholding and remove stop words if not already filtered'''
        if not self._filtered:
            self._count_words = text_ops.filter_word_counts(self._word_counts, self._stopwords,
                self._min_freq, self._max_freq, self._verbose)
            self._filtered = True

    def summarize_all_idx(self, summary_count):
        '''summarize all stored text and return indices of ranked extracted sentences'''
        self.filter_words()
        sentence_count = len(self._text_lines)
        words_per_sentence = self._count_words / sentence_count
        ranking = defaultdict(int)
        for idx, snt_words in enumerate(self._line_word_lists):
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        return rank_dict_by_value(summary_count, ranking)

    def summarize_all_snt(self, summary_count):
        '''summarize all stored text and return the extracted sentences sorted by index'''
        sents_idx = self.summarize_all_idx(summary_count)
        sents_idx.sort()
        return [self._text_lines[j] for j in sents_idx]

    def summarize_next_idx(self, text, summary_count, summary_percent):
        '''summarize another chunk of text, based on previous chunks,
        and return ranked indices'''
        saved_sentence_count = len(self._text_lines)
        added_sentence_count = self.add_text(text)
        if added_sentence_count < 1:
            return []
        self.filter_words()
        total_sentence_count = len(self._text_lines)
        assert total_sentence_count == saved_sentence_count + added_sentence_count
        words_per_sentence = self._count_words / total_sentence_count
        ranking = defaultdict(int)
        summary_count, _ = text_ops.resolve_count(summary_count, summary_percent
                , added_sentence_count)
        for idx in range(saved_sentence_count, total_sentence_count):
            snt_words = self._line_word_lists[idx]
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        sents_idx = rank_dict_by_value(summary_count, ranking)
        return sents_idx

    def summarize_next_snt(self, text, summary_count, summary_percent):
        '''summarize another chunk of text, based on previous chunks,
        and return sentences sorted by index'''
        sents_idx = self.summarize_next_idx(text, summary_count, summary_percent)
        sents_idx.sort()
        return [self._text_lines[j] for j in sents_idx]

    def _score_sentence(self, snt_words, words_per_sentence):
        score = 0
        words = 0
        for word, count in snt_words.items():
            words += count
            if word in self._word_counts:
                score += self._word_counts[word]
        return score * math.log(words_per_sentence*(1.0 + 1.0/len(snt_words)))
        # return score

###############################################################################

def rank_dict_by_value(summary_count, ranking):
    '''Return the highest ranked N sentences.'''
    return heapq.nlargest(summary_count, ranking, key=ranking.get)

###############################################################################

def print_ranked_idx(idx, sorted_idx):
    '''Show ranked and sorted indices.'''
    size = len(idx)
    if size < LINE_MAX:
        print(idx, '==> ', end='')
    elif size < LINE_MAX*2:
        print(idx, "==>")
    else:
        print(idx)
        print("==>")
    print(sorted_idx)

###############################################################################

def classify_lines(class_files, opt, charset='utf8'):
    """Output a summary of a text file."""

    classes = []

    # input class files:
    for file_spec in class_files:
        classes.append(TextFileWordFreqs(file_spec, opt.min_freq, opt.max_freq, opt.verbose))

    '''Text file line contents and word frequencies'''

    exit(0)


    # Try to open output (file):
    out_file = text_fio.open_out_file(opt.out_file, label='summary')

    # Create summarizer and initialize with text:
    sentence_count = text_freqs.add_text(text)

    max_words = opt.max_print_words

    # Announce output:
    print(file_spec, '====>', '<stdout>' if out_file == sys.stdout else opt.out_file)
    sum_count, act_percent = text_ops.resolve_count(opt.sum_count, opt.sum_percent, sentence_count)
    print("Keeping {} ({:.4} percent) of {} sentences."
            .format(sum_count, act_percent, sentence_count))
    print('-------------------------------------------------------------------')

    # Summarize and show results:
    if opt.indices_only:
        sents_idx = text_freqs.summarize_all_idx(sum_count)
        print("Sentence indices in [0, {})".format(sentence_count))
        print_ranked_idx(sents_idx, sorted(sents_idx))
    else:
        summary_sentences = text_freqs.summarize_all_snt(sum_count)
        if out_file:
            text_ops.print_sentences(summary_sentences, opt.list_numbers, max_words, out_file)

    if opt.serial:
        if not out_file:
            out_file = sys.stdout
        print('-------------------------------------------------------------------', file=out_file)
        if opt.indices_only:
            sents_idx = text_freqs.summarize_next_idx(text, sum_count, opt.sum_percent)
            sents_idx = [x - sentence_count for x in sents_idx]
            print("Sentence indices in [0, {})".format(sentence_count))
            print_ranked_idx(sents_idx, sorted(sents_idx))
        else:
            summary_sentences = text_freqs.summarize_next_snt(text, sum_count, opt.sum_percent)
            if out_file:
                text_ops.print_sentences(summary_sentences, opt.list_numbers, max_words, out_file)

    print('-------------------------------------------------------------------', file=out_file)
    if out_file and out_file != sys.stdout:
        out_file.close()

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
    classify_lines([args.text_spec], args)

if __name__ == '__main__':
    main()
