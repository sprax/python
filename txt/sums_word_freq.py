#!/usr/bin/env python3
# Sprax Lines       2016.10.07      
# From http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
'''Summarize something.'''

import argparse
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

class FrequencySummarizer:
  def __init__(self, text, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higher than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))
    self._freq = self._init_freqs(text)

  def _init_freqs(self, text):
    """
      Return a list of N sentences 
      which represent the summary of text.
    """
    self._sents = sent_tokenize(text)
    self._word_sent = [word_tokenize(s.lower()) for s in self._sents]
    return self._compute_frequencies(self._word_sent)

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
          word_sent, a list of sentences already tokenized.
      Output: 
          freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for sentence in word_sent:
      for word in sentence:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    keys_to_delete = []
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        keys_to_delete.append(w)
    for key in keys_to_delete:
        freq.pop(key, None)
    return freq


  def summarize(self, text, summary_sentence_count):
    ranking = defaultdict(int)
    assert summary_sentence_count <= len(self._sents)
    for i, sent in enumerate(self._word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, summary_sentence_count)    
    return [self._sents[j] for j in sents_idx]

  def _rank(self, ranking, summary_sentence_count):
    """ return the first count sentences with highest ranking """
    return nlargest(summary_sentence_count, ranking, key=ranking.get)


def summarize_text_file(text_file, summary_file, min_freq, max_freq, sum_sent_count, verbose):
    with open(text_file, 'r') as src:
        text = src.read()
        src.close()

    freqsum = FrequencySummarizer(text, min_cut=min_freq, max_cut=max_freq)
    title = text_file
    print(text_file, '====>', summary_file)
    print(title)
    print('---------------------------------------------------------------------------')
    summary_sentences = freqsum.summarize(text, sum_sent_count)
    with open(summary_file, 'w') as outfile:
        for sum_sentence in summary_sentences:
            if verbose > 0:
                print(sum_sentence)
                print()
            print(sum_sentence, file=outfile)
        outfile.close()

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

