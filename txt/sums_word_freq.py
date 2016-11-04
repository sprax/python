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
import nltk
import string
from collections import defaultdict

from utf_print import utf_print

class FrequencySummarizer:

    def __init__(self, min_freq=0.1, max_freq=0.9):
        '''Initilize the text summarizer.'''
        self._min_freq = min_freq
        self._max_freq = max_freq 
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self._total_words = 0
        self._word_counts = defaultdict(int)
        self._text_paragraphs = []
        self._text_sentences = []
        self._snt_word_lists = []

    def add_text(self, text):
        '''Add text that may contain one or more blank-line separated paragraphs.'''
        paragraphs = nltk.blankline_tokenize(text)
        for para in paragraphs:
            self.add_paragraph(para)    

    def add_paragraph(self, paragraph):
        '''Add a single paragraph containing one or more sentences.'''
        self._text_paragraphs.append(paragraph)
        sentences = nltk.sent_tokenize(paragraph)
        self._text_sentences.extend(sentences)
        for sentence in sentences:
            word_hash = {}
            word_list = nltk.word_tokenize(sentence.lower())
            # word_list = nltk.word_tokenize(sentence.decode("utf8").lower())
            for word in word_list:
                self._total_words += 1
                self._word_counts[word] += 1
                word_hash[word] = 1 + (word_hash[word] if word in word_hash else 0)
            self._snt_word_lists.append(word_hash)

    def filter_words(self):
        '''apply thresholding and remove stop words'''
        filter_word_counts(self._word_counts, self._stopwords, self._min_freq, self._max_freq)

    def summarize(self, summary_count, summary_percent):
        self.filter_words()
        words_per_sentence = self._total_words / len(self._text_sentences)
        ranking = defaultdict(int)
        input_count = len(self._text_sentences)
        if not summary_count:
            summary_count = int(math.ceil(summary_percent * input_count / 100.0))
        if  summary_count > input_count or summary_count < 1:
            summary_count = 1

        for idx, snt_words in enumerate(self._snt_word_lists):
            # ranking[idx] = self._score_sentence(snt_words) * (1.0 + 1.0/len(snt_words))
            ranking[idx] = self._score_sentence(snt_words) * math.log(words_per_sentence*(1.0 + 1.0/len(snt_words)))
        sents_idx = self._rank(summary_count, ranking)    
        return [self._text_sentences[j] for j in sents_idx]

    def _score_sentence(self, snt_words):
        score = 0
        words = 0
        for word, count in snt_words.items():
            words += count
            if word in self._word_counts:
                score += self._word_counts[word]
        return score # / math.log2(len(snt_words))

    def _rank(self, summary_count, ranking):
        '''Return the highest ranked N sentences.'''
        return heapq.nlargest(summary_count, ranking, key=ranking.get)

###############################################################################

def filter_word_counts(word_counts, stopwords, min_freq, max_freq):
    """ remove any word in stopwords or whose count is below the min or above the max threshold """
    max_word_count = 0
    for word, count in word_counts.items():
        if count > max_word_count and word not in stopwords:
            max_word_count = count
    min_freq_count = max_word_count * min_freq
    max_freq_count = max_word_count * max_freq
    words_to_remove = []
    for word, count in word_counts.items():
        if count <= min_freq_count or count >= max_freq_count or word in stopwords:
            words_to_remove.append(word)
    for key in words_to_remove:
        word_counts.pop(key, None)

def summarize_text_file(text_file, summary_file, min_freq, max_freq, sum_number, sum_percent, verbose):
    """ Return a list of N sentences which represent the summary of text.  """
    with open(text_file, 'r') as src:
        text = src.read()
        src.close()

    freqsum = FrequencySummarizer(min_freq, max_freq)
    freqsum.add_text(text)

    title = text_file
    print(text_file, '====>', summary_file)
    print("Keeping", (sum_number if sum_number else "{} percent of the".format(sum_percent)), "sentences.")
    print('---------------------------------------------------------------------------')
    summary_sentences = freqsum.summarize(sum_number, sum_percent)
    with open(summary_file, 'w') as outfile:
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
    parser.add_argument('-max_freq', type=float, nargs='?', const=1, default=0.9,
                        help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-min_freq', type=float, nargs='?', const=1, default=0.1,
                        help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-number', type=int, nargs='?', const=1,
                        help='number of sentences to keep (default: 5), overrides -percent')
    parser.add_argument('-percent', type=float, nargs='?', const=1, default=10.0,
                        help='percentage of sentences to keep (default: 10.0%)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        print("args:", args)
        print(__doc__)

    summarize_text_file(args.text_file, args.summary_file, args.min_freq, args.max_freq,
            args.number, args.percent, args.verbose)


if __name__ == '__main__':
    main()

