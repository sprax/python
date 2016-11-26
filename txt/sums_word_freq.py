#!/usr/bin/env python3
# Sprax Lines       2016.10.07
# From http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
'''Summarize text(s).'''

# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize
# from string import punctuation
import argparse
import errno
import heapq
import math
import string
import sys
from collections import defaultdict
import nltk
import paragraphs
from utf_print import utf_print
import text_file

class FrequencySummarizer:
    '''Text summarization based on word frequencies'''

    def __init__(self, min_freq=0.1, max_freq=0.9, verbose=1):
        '''Initialize the text summarizer.'''
        self._min_freq = min_freq
        self._max_freq = max_freq
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self._filtered = False
        self._input_words = 0
        self._count_words = 0
        self._word_counts = defaultdict(int)
        self._text_paragraphs = []
        self._text_sentences = []
        self._snt_word_lists = []
        self._verbose = verbose

    def add_text(self, text):
        '''Add text that may contain one or more blank-line separated paragraphs.
        Return the count of sentences in text'''
        sentence_count = 0
        paragraphs = nltk.blankline_tokenize(text)
        for para in paragraphs:
            sentence_count += self.add_paragraph(para)
        return sentence_count

    def add_paragraph(self, paragraph):
        '''Add a single paragraph containing one or more sentences.
        Return the count of sentences in text'''
        self._text_paragraphs.append(paragraph)
        sentences = nltk.sent_tokenize(paragraph)
        self._text_sentences.extend(sentences)
        for sentence in sentences:
            word_hash = {}
            word_list = nltk.word_tokenize(sentence.lower())
            # word_list = nltk.word_tokenize(sentence.decode("utf8").lower())
            for word in word_list:
                self._input_words += 1
                self._word_counts[word] += 1
                word_hash[word] = 1 + (word_hash[word] if word in word_hash else 0)
            self._snt_word_lists.append(word_hash)
        return len(sentences)

    def filter_words(self):
        '''apply thresholding and remove stop words if not already filtered'''
        if not self._filtered:
            self._count_words = filter_word_counts(self._word_counts, self._stopwords,
                                                   self._min_freq, self._max_freq, self._verbose)
            self._filtered = True

    def summarize_all_idx(self, summary_count, verbose):
        '''summarize all stored text and return indices of ranked extracted sentences'''
        self.filter_words()
        sentence_count = len(self._text_sentences)
        words_per_sentence = self._count_words / sentence_count
        ranking = defaultdict(int)
        for idx, snt_words in enumerate(self._snt_word_lists):
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        return _rank(summary_count, ranking)

    def summarize_all_snt(self, summary_count, verbose):
        '''summarize all stored text and return the extracted sentences sorted by index'''
        sents_idx = self.summarize_all_idx(summary_count, verbose)
        sents_idx.sort()
        return [self._text_sentences[j] for j in sents_idx]

    def sum_next_idx(self, text, offset, summary_count, summary_percent, verbose):
        '''summarize another chunk of text, based on previous chunks,
        and return ranked indices'''
        saved_sentence_count = len(self._text_sentences)
        added_sentence_count = self.add_text(text)
        self.filter_words()
        total_sentence_count = len(self._text_sentences)
        assert total_sentence_count == saved_sentence_count + added_sentence_count
        words_per_sentence = self._count_words / total_sentence_count
        ranking = defaultdict(int)
        summary_count, act_percent = resolve_count(summary_count, summary_percent, added_sentence_count)
        for idx in range(saved_sentence_count, total_sentence_count):
            snt_words = self._snt_word_lists[idx]
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        sents_idx = _rank(summary_count, ranking)
        if offset > 0:
            sents_idx = [x - offset for x in sents_idx]
        return sents_idx

    def sum_next_snt(self, text, offset, summary_count, summary_percent, verbose):
        '''summarize another chunk of text, based on previous chunks,
        and return sentences sorted by index'''
        sents_idx = self.sum_next_idx(text, offset, summary_count, summary_percent, verbose)
        sents_idx.sort()
        return [self._text_sentences[j] for j in sents_idx]

    def _score_sentence(self, snt_words, words_per_sentence):
        score = 0
        words = 0
        for word, count in snt_words.items():
            words += count
            if word in self._word_counts:
                score += self._word_counts[word]
        return score * math.log(words_per_sentence*(1.0 + 1.0/len(snt_words)))

###############################################################################

def _rank(summary_count, ranking):
    '''Return the highest ranked N sentences.'''
    return heapq.nlargest(summary_count, ranking, key=ranking.get)

def resolve_count(sub_count, percent, total_count):
    '''returns reconciled sub-count and percentage of total, where count trumps percentage'''
    if not sub_count:
        sub_count = int(math.ceil(percent * total_count / 100.0))
    if  sub_count > total_count:
        sub_count = total_count
    if  sub_count < 1:
        sub_count = 1
    percent = sub_count * 100.0 / total_count
    return sub_count, percent

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
        if count >= max_freq_count or word in stopwords:
            stop_words_to_remove.append(word)
        elif count <= min_freq_count:
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


def print_sentences(sentences, list_numbers, max_words, out_file):
    if list_numbers:
        if 0 < max_words and max_words < 15:
            idx_format = '{} '
        else:
            idx_format = '\n    {}\n'
    for idx, sentence in enumerate(sentences):
        if list_numbers:
            print(idx_format.format(idx), end=' ')
        if max_words:
            paragraphs.print_paragraph_regex_count(sentence, max_words, outfile=out_file)
        else:
            utf_print(sentence, outfile=out_file)

########################################################

def summarize_text_file(file_spec, opt, charset='utf8'):
    """Output a summary of a text file."""

    # Read initial text corpus:
    text = text_file.read_file(file_spec, charset)

    # Try to open output (file):
    out_file = text_file.open_out_file(opt.out_file, label='summary')

    # Create summarizer and initialize with text:
    freqsum = FrequencySummarizer(opt.min_freq, opt.max_freq, opt.verbose)
    sentence_count = freqsum.add_text(text)

    max_words = opt.max_print_words

    # Announce output:
    print(file_spec, '====>', '<stdout>' if out_file==sys.stdout else opt.out_file)
    sum_count, act_percent = resolve_count(opt.sum_count, opt.sum_percent, sentence_count)
    print("Keeping {} ({:.4} percent) of {} sentences.".format(sum_count, act_percent, sentence_count))
    print('-------------------------------------------------------------------')

    if opt.indices_only:
        sents_idx = freqsum.summarize_all_idx(sum_count, opt.verbose)
        print("Sentence indices in [0, {})".format(sentence_count))
        print(sents_idx)
    else:
        summary_sentences = freqsum.summarize_all_snt(sum_count, opt.verbose)
        if out_file:
            print_sentences(summary_sentences, opt.list_numbers, max_words, out_file)

    if opt.serial:
        if not out_file:
            out_file = sys.stdout
        print('-------------------------------------------------------------------', file=out_file)
        if opt.indices_only:
            sents_idx = freqsum.sum_next_idx(text, sentence_count, sum_count, opt.sum_percent, opt.verbose)
            print("Sentence indices in [0, {})".format(sentence_count))
            print(sents_idx)
        else:
            summary_sentences = freqsum.sum_next_snt(text, sentence_count,
                                                 sum_count, opt.sum_percent, opt.verbose)
            if out_file:
                print_sentences(summary_sentences, opt.list_numbers, max_words, out_file)

    print('-------------------------------------------------------------------', file=out_file)
    if out_file and out_file != sys.stdout:
        out_file.close()

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
    parser.add_argument('-max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-number', dest='sum_count', type=int, nargs='?', const=1, default=0,
                        help='number of sentences to keep (default: 5), overrides -percent')
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
    summarize_text_file(args.text_spec, args)

if __name__ == '__main__':
    main()
