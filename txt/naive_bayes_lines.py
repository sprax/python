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
from collections import Counter
import nltk
import text_ops
import text_fio
from utf_print import utf_print

LINE_MAX = 15

class TextFileWordFreqs:
    '''Text file line contents and word frequencies: more than we need for naive Bayes'''

    def __init__(self, file_spec, min_freq=0.1, max_freq=0.9, verbose=1, charset='utf8'):
        '''Initialize the text file word counter.'''
        self._file_spec = file_spec
        self._min_freq = min_freq
        self._max_freq = max_freq
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self._filtered = False
        self._input_words = 0
        self._text_lines = []
        self._line_word_dicts = []
        self._verbose = verbose
        self._word_counts = Counter()
        self._sum_word_len = 0
        for line in text_fio.read_lines(file_spec, charset):
            self._text_lines.append(line)
            self._sum_word_len += self.count_words(line)
        self._counted_words = self._input_words
        print()
        print("verbosity {} for file:".format(self._verbose), file_spec)
        utf_print(self._text_lines[ 0])
        utf_print(self._text_lines[ 1])
        utf_print(self._text_lines[-1])
        print()

    def count_words(self, line):
        '''Add a single paragraph containing one or more sentences.
        Return the count of sentences in text'''
        word_hash = {}
        word_list = nltk.word_tokenize(line.lower())
        self._input_words += len(word_list)
        # word_list = nltk.word_tokenize(sentence.decode("utf8").lower())
        sum_len = 0
        self._word_counts.update(word_list)
        for word in word_list:
            sum_len += len(word)
            # word_hash[word] = 1 + word_hash[word] if word in word_hash else 1
            if word in word_hash:
                word_hash[word] += 1 
            else:
                word_hash[word] = 1
        self._line_word_dicts.append(word_hash)
        return sum_len

    def line_count(self):
        return len(self._text_lines)

    def filter_words(self):
        '''apply thresholding and remove stop words if not already filtered'''
        if not self._filtered:
            self._counted_words = text_ops.filter_word_counts(self._word_counts, self._stopwords,
                self._min_freq, self._max_freq, self._verbose)
            self._filtered = True

    def most_modal_idx(self, count):
        '''Return indices of count lines closest to normal for the set, ranked by self-similar score'''
        self.filter_words()
        line_count = len(self._text_lines)
        words_per_line = self._counted_words / line_count
        ranking = defaultdict(int)
        for idx, line_dicts in enumerate(self._line_word_dicts):
            ranking[idx] = self._score_line_dict(line_dicts, words_per_line)
        return rank_dict_by_value(count, ranking)

    def _score_line_dict(self, line_dicts, words_per_line):
        score = 0
        for word, count in line_dicts.items():
            if word in self._word_counts:
                score += count * math.log((1 + self._word_counts[word])/self._counted_words)
            else:
                print("Warning: _score_line_dict called on non-corpus line")
        # return score * math.log(words_per_line*(1.0 + 1.0/len(line_dicts)))
        return score

    def score_text_line(self, word_list):
        line_score = 0
        for word in word_list:
            if self._verbose > 1 and not word in self._word_counts:
                print("_score_text_line: uncounted word: ", word)
            word_score = math.log((1 + self._word_counts[word])/self._counted_words)
            line_score += word_score
            utf_print("word:", word, "\t\t score: ", word_score)
        return line_score

###############################################################################

def rank_dict_by_value(count, ranking):
    '''Return the highest ranked N lines.'''
    return heapq.nlargest(count, ranking, key=ranking.get)

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

def classify_lines(class_file_specs, opt, charset='utf8'):
    '''Text file line contents and word frequencies'''

    # input class files:
    classes = []
    for file_spec in class_file_specs:
        classes.append(TextFileWordFreqs(file_spec, opt.min_freq, opt.max_freq, opt.verbose))

    text_line = "No Mandrill login was found in the account in question."
    word_list = nltk.word_tokenize(text_line.lower())

    scores = []
    for line_class in classes:
        print("class based on file:", line_class._file_spec)
        scores.append(line_class.score_text_line(word_list))
        print()
    print("Scores:", scores)

    for line_class in classes:
        line_class.filter_words()
        print("Filtered class based on file:", line_class._file_spec)
        scores.append(line_class.score_text_line(word_list))
        print()

    print("Scores:", scores)
    exit(0)


    # Try to open output (file):
    out_file = text_fio.open_out_file(opt.out_file, label='summary')

    # Create summarizer and initialize with text:
    line_count = text_freqs.add_text(text)

    max_words = opt.max_print_words

    # Announce output:
    print(file_spec, '====>', '<stdout>' if out_file == sys.stdout else opt.out_file)
    sum_count, act_percent = text_ops.resolve_count(opt.sum_count, opt.sum_percent, line_count)
    print("Keeping {} ({:.4} percent) of {} sentences."
            .format(sum_count, act_percent, line_count))
    print('-------------------------------------------------------------------')

    # Summarize and show results:
    if opt.indices_only:
        sents_idx = text_freqs.summarize_all_idx(sum_count)
        print("Sentence indices in [0, {})".format(line_count))
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
            sents_idx = [x - line_count for x in sents_idx]
            print("Sentence indices in [0, {})".format(line_count))
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
    parser.add_argument('text_specs', type=str, nargs='+', default='corpus.txt',
                        help='text files containing lines representative of classes')
    parser.add_argument('-index', dest='indices_only', action='store_true',
                        help='output only the indices of summary sentences')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each summary sentence')
    parser.add_argument('-fM', '-freq_max', dest='max_freq', type=float, nargs='?', const=1, default=1.0,
                        help='maximum frequency cut-off (default: 1.0)')
    parser.add_argument('-fm', '-freq_min', dest='min_freq', type=float, nargs='?', const=1, default=0.05,
                        help='minimum frequency cut-off (default: 0.05)')
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
    classify_lines(args.text_specs, args)

if __name__ == '__main__':
    main()
