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
from utf_print import utf_print

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

    def summarize_all(self, summary_count, indices, verbose):
        '''summarize all stored text'''
        self.filter_words()
        sentence_count = len(self._text_sentences)
        words_per_sentence = self._count_words / sentence_count
        ranking = defaultdict(int)
        for idx, snt_words in enumerate(self._snt_word_lists):
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        sents_idx = _rank(summary_count, ranking)
        sents_idx.sort()
        if indices or verbose > 2:
            print("Sentence indices in [0, {})".format(len(self._text_sentences)))
            print(sents_idx)
            if indices:
                return []
        return [self._text_sentences[j] for j in sents_idx]

    def sum_next_idx(self, text, offset, summary_count, summary_percent, verbose):
        '''summarize another chunk of text, based on previous chunks, and return indices'''
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
        sents_idx.sort()
        if offset > 0:
            sents_idx = [x - offset for x in sents_idx]
        if verbose > 2:
            print("Sentence indices in [0, {})".format(len(self._text_sentences)), end="")
            print(sents_idx)
        return sents_idx

    def sum_next_snt(self, text, offset, summary_count, summary_percent, verbose):
        '''summarize another chunk of text, based on previous chunks, and return sentences'''
        sents_idx = self.sum_next_idx(text, offset, summary_count, summary_percent, verbose)
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
    '''returns count and percentage of sentences, where count trumps percentage '''
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

def summarize_text_file(text_file, opt, charset='utf8'):
    """Output a summary of a text file."""

    # Read initial text corpus:
    with open(text_file, 'r', encoding=charset) as src:
        text = src.read()
        src.close()

    # Try to open output (file):
    if opt.out_file in ['-', 'stdout']:
        out_file = sys.stdout
    elif opt.out_file:
        try:
            out_file = open(out_file, 'w')
        except IOError as ex:
            if ex.errno != errno.ENOENT:
                raise
            print("IOError opening summary file [{}]:".format(out_file), ex)
            out_file = sys.stdout
    else:
        out_file = None

    freqsum = FrequencySummarizer(opt.min_freq, opt.max_freq, opt.verbose)
    sentence_count = freqsum.add_text(text)

    print(text_file, '====>', '<stdout>' if out_file==sys.stdout else opt.out_file)
    sum_count, act_percent = resolve_count(opt.sum_count, opt.sum_percent, sentence_count)
    print("Keeping {} ({:.4} percent) of {} sentences.".format(sum_count, act_percent, sentence_count))
    print('-------------------------------------------------------------------')
    summary_sentences = freqsum.summarize_all(sum_count, opt.indices_only, opt.verbose)


    if out_file:
        if opt.list_numbers:
            for idx, sum_sentence in enumerate(summary_sentences):
                print('\n   ', idx)
                utf_print(sum_sentence, outfile=out_file)
        else:
            for sum_sentence in summary_sentences:
                utf_print(sum_sentence, outfile=out_file)

    if opt.serial:
        print('-------------------------------------------------------------------', file=out_file)
        summary_sentences = freqsum.sum_next_snt(text, sentence_count,
                                                 sum_count, sum_percent, opt.verbose)
        for sum_sentence in summary_sentences:
            utf_print(sum_sentence, outfile=out_file)
    print('-------------------------------------------------------------------', file=out_file)
    if out_file and out_file != sys.stdout:
        out_file.close()

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='file containing text to summarize')
    parser.add_argument('-index', dest='indices_only', action='store_true',
                        help='output only the indices of summary sentences')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each summary sentence')
    parser.add_argument('-max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-number', dest='sum_count', type=int, nargs='?', const=1,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', const='-',
                        help='output file for summarized text (default: None)')
    parser.add_argument('-percent', dest='sum_percent', type=float, nargs='?', const=16.6667,
                        help='percentage of sentences to keep (default: 10.0%%)')
    parser.add_argument('-serial', action='store_true',
                        help='summarize each paragraph in series')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 3:
        print("outfile: <{}>".format(args.out_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    # summary_file = getattr(args, 'out_file', None)
    summarize_text_file(args.text_file, args)

if __name__ == '__main__':
    main()
