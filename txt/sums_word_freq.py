#!/usr/bin/env python3
# Sprax Lines       2016.10.07
# From http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
'''Summarize text(s).'''

# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize
# from string import punctuation
import argparse
import heapq
import math
import string
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

    def summarize_all(self, summary_count, summary_percent, indices, verbose):
        '''summarize all stored text'''
        self.filter_words()
        sentence_count = len(self._text_sentences)
        words_per_sentence = self._count_words / sentence_count
        ranking = defaultdict(int)
        summary_count = resolve_count(summary_count, summary_percent, sentence_count)
        for idx, snt_words in enumerate(self._snt_word_lists):
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        sents_idx = _rank(summary_count, ranking)
        sents_idx.sort()
        if indices or verbose > 2:
            print("Sentence indices:", sents_idx)
            if indices:
                return []
        return [self._text_sentences[j] for j in sents_idx]

    def summarize_next(self, text, offset, summary_count, summary_percent, indices, verbose):
        '''summarize another chunk of text, based on previous chunks'''
        saved_sentence_count = len(self._text_sentences)
        added_sentence_count = self.add_text(text)
        self.filter_words()
        total_sentence_count = len(self._text_sentences)
        assert total_sentence_count == saved_sentence_count + added_sentence_count
        words_per_sentence = self._count_words / total_sentence_count
        ranking = defaultdict(int)
        summary_count = resolve_count(summary_count, summary_percent, added_sentence_count)
        for idx in range(saved_sentence_count, total_sentence_count):
            snt_words = self._snt_word_lists[idx]
            ranking[idx] = self._score_sentence(snt_words, words_per_sentence)
        sents_idx = _rank(summary_count, ranking)
        sents_idx.sort()
        if indices or verbose > 2:
            print("Sentence indices: [", end="")
            for idx in sents_idx:
                print("{}, ".format(idx - offset), end="")
            print("]")
            if indices:
                return []
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

def resolve_count(summary_count, summary_percent, sentence_count):
    '''returns count of sentences to be extracted into summary'''
    if not summary_count:
        summary_count = int(math.ceil(summary_percent * sentence_count / 100.0))
    if  summary_count > sentence_count:
        summary_count = sentence_count
    if  summary_count < 1:
        summary_count = 1
    return summary_count

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

def summarize_text_file(text_file, summary_file, min_freq, max_freq, sum_number, sum_percent,
                        do_serial, indices, verbose, charset='utf8'):
    """ Return a list of N sentences which represent the summary of text.  """
    with open(text_file, 'r', encoding=charset) as src:
        text = src.read()
        src.close()

    freqsum = FrequencySummarizer(min_freq, max_freq, verbose)
    sentence_count = freqsum.add_text(text)

    print(text_file, '====>', summary_file)
    print("Keeping", (sum_number if sum_number else "{} percent of the".format(sum_percent)),
          "sentences.")
    print('---------------------------------------------------------------------------')
    summary_sentences = freqsum.summarize_all(sum_number, sum_percent, indices, verbose)
    with open(summary_file, 'w') as outfile:
        for sum_sentence in summary_sentences:
            if verbose > 0:
                utf_print(sum_sentence)
                print()
            print(sum_sentence, file=outfile)
        if do_serial:
            print('---------------------------------------------------------------------------')
            summary_sentences = freqsum.summarize_next(text, sentence_count,
                                                       sum_number, sum_percent, indices, verbose)
            for sum_sentence in summary_sentences:
                if verbose > 0:
                    utf_print(sum_sentence)
                    print()
                print(sum_sentence, file=outfile)
        outfile.close()
    print('---------------------------------------------------------------------------')

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer'",
        )
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='text file containing quoted dialogue')
    parser.add_argument('summary_file', type=str, nargs='?', default='corpus_summary.txt',
                        help='output file of quoted dialogue extracted from the corpus')
    parser.add_argument('-index', action='store_true',
                        help='show only indices of summary sentences')
    parser.add_argument('-max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-number', type=int, nargs='?', const=1,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-percent', type=float, nargs='?', const=1, default=10.0,
                        help='percentage of sentences to keep (default: 10.0%)')
    parser.add_argument('-serial', action='store_true',
                        help='summarize each paragraph in series')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        print("args:", args)
        print(__doc__)

    summarize_text_file(args.text_file, args.summary_file, args.min_freq, args.max_freq,
                        args.number, args.percent, args.serial, args.index, args.verbose)

if __name__ == '__main__':
    main()
