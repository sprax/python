#!/usr/bin/env python3
# Sprax Lines       2016.10.07      
# From http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
'''Summarize something.'''

# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize
# from string import punctuation
import argparse
import nltk
import string
from collections import defaultdict
from heapq import nlargest

from utf_print import utf_print

class FrequencySummarizer:
  def __init__(self, min_freq=0.1, max_freq=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_freq 
     or higher than max_freq will be ignored.
    """
    self._min_freq = min_freq
    self._max_freq = max_freq 
    self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
    self._word_counts = defaultdict(int)
    self._text_sentences = []
    self._word_sentences = []

  def add_text(self, text):
    sentences = nltk.sent_tokenize(text)
    self._text_sentences.extend(sentences)
    for sentence in sentences:
         word_sentence = nltk.word_tokenize(sentence.lower())
         self._word_sentences.append(word_sentence)
         for word in word_sentence:
             self._word_counts[word] += 1
    filter_word_counts(self._word_counts, self._stopwords, self._min_freq, self._max_freq)


  def summarize(self, text, summary_sentence_count):
    ranking = defaultdict(int)
    assert summary_sentence_count <= len(self._text_sentences)
    for i, sent in enumerate(self._word_sentences):
      for w in sent:
        if w in self._word_counts:
          ranking[i] += self._word_counts[w]
    sents_idx = self._rank(ranking, summary_sentence_count)    
    return [self._text_sentences[j] for j in sents_idx]

  def _rank(self, ranking, summary_sentence_count):
    """ return the first count sentences with highest ranking """
    return nlargest(summary_sentence_count, ranking, key=ranking.get)

###############################################################################

def filter_word_counts(word_counts, stopwords, min_freq, max_freq):
    """ remove any word in stopwords
    or whose count is below the min or above the max threshold """
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

def summarize_text_file(text_file, summary_file, min_freq, max_freq, sum_sent_count, verbose):
    """ Return a list of N sentences which represent the summary of text.  """
    with open(text_file, 'r') as src:
        text = src.read()
        src.close()

    freqsum = FrequencySummarizer(min_freq, max_freq)
    freqsum.add_text(text)

    title = text_file
    print(text_file, '====>', summary_file, "  keeping", sum_sent_count, "sentences.")
    print('---------------------------------------------------------------------------')
    summary_sentences = freqsum.summarize(text, sum_sent_count)
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
    parser.add_argument('-sentence_count', type=int, nargs='?', const=1, default=2,
                        help='summary sentence count (default: 2)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 2:
        print("args:", args)
        print(__doc__)

    summarize_text_file(args.text_file, args.summary_file, args.min_freq, args.max_freq,
            args.sentence_count, args.verbose)


if __name__ == '__main__':
    main()

