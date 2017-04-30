#!/usr/bin/env python3
# Sprax Lines       2016.12.27
'''Filter POS-tagged text'''

# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize, word_tokenize, pos_tag
# from string import punctuation
import argparse
import string
import nltk
import text_ops
from utf_print import utf_print
from xdv import xdv, set_xdv_verbosity


class PosFilter:
    '''Filter out some parts of speech, such as adverbs'''

    def __init__(self):
        '''Initialize the POS filter with the tags of words to filter,
        and the tags of joining words to filter.'''
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))

    def filter_paragraph(self, paragraph):
        '''Filter a single paragraph containing one or more sentences.'''
        sentences = nltk.sent_tokenize(paragraph)
        questions = []
        statements = []
        for sentence in sentences:
            xdv(1)
            xdv(1, sentence)
            if self.is_question(sentence):
                questions.append(sentence)
            else:
                statements.append(sentence)
        return questions, sentences

    def is_question(self, sentence):
        if sentence[-1] == '?':
            return True
        return False

def join_tokenized(tokens):
    '''Join tokens into a sentence; partial inverse of word_tokenize.'''
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation and i not in ["n't"]
        else i for i in tokens]).strip()

###############################################################################

def main():
    '''Extract questions from text?'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('text_spec', type=str, nargs='?', default='questions.txt',
                        help='text file containing text to summarize')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each filtered sentence')
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=2,
                        help='verbosity of output (default: 2)')
    args = parser.parse_args()

    if args.verbose > 8:
        print("args:", args)
        print(__doc__)
        exit(0)
    set_xdv_verbosity(args.verbose)

    print('======== Remove Adverbs [RB] ==================================================')
    pos_filter = PosFilter()
    for sent in text_ops.filter_file(pos_filter, args.text_spec, charset='utf8'):
        print(sent)
    print('======== Remove Adjectives [JJ] ===============================================')
    print('======== Remove Adv and Adj [JJ, RB] ==========================================')

if __name__ == '__main__':
    main()
