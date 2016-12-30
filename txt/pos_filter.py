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

    def __init__(self, out_tags=['RB'], con_tags=['CC', ',']
            , negatives=['no', 'not', 'never', "don't", "n't"]):
        '''Initialize the POS filter with the tags of words to filter,
        and the tags of joining words to filter.'''
        self._stopwords = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self.out_tags = out_tags
        self.con_tags = con_tags
        self.negatives = negatives

    def filter_paragraph(self, paragraph):
        '''Filter a single paragraph containing one or more sentences.'''
        filtered = []
        sentences = nltk.sent_tokenize(paragraph)
        for sentence in sentences:
            xdv(1)
            xdv(1, sentence)
            inside = False
            output = []
            tokens = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokens)
            precon = []
            for (tok, tag) in tagged:
                if tag in self.out_tags:
                    if not inside:
                        inside = True
                        precon = []
                    if tag == 'RB' and tok in self.negatives:
                        output.append(tok)
                        xdv(3, "Preserve neg:", tag, tok)
                    else:
                        xdv(2, "Filter out:", tag, tok)
                elif inside and tag in self.con_tags:
                    xdv(4, "Filter con?", tag, tok)
                    precon.append(tok)      # push
                else:
                    # TODO: Heuristics!
                    if output and len(precon) > 1 and (precon[-2] != precon[-1] or tag == 'PRP'):
                        con = precon.pop()
                        xdv(3, "Append con:", con)
                        output.append(con)
                    xdv(4, "Append tok:", tag, tok)
                    output.append(tok)
                    if inside:
                        inside = False
                        precon = []
                        xdv(5, "INSIDE precon:", precon)
            filtered.extend(output)
        return join_tokenized(output)

def join_tokenized(tokens):
    '''Join tokens into a sentence; partial inverse of word_tokenize.'''
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation and i not in ["n't"]
        else i for i in tokens]).strip()

###############################################################################

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('text_spec', type=str, nargs='?', default='corpus.txt',
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
    filter = PosFilter()
    for sent in text_ops.filter_file(filter, args.text_spec, charset='utf8'):
        print(sent)
    print('======== Remove Adjectives [JJ] ===============================================')
    filter = PosFilter(['JJ'], ['RB', 'CC', ','])
    for sent in text_ops.filter_file(filter, args.text_spec, charset='utf8'):
        print(sent)
    print('======== Remove Adv and Adj [JJ, RB] ==========================================')
    filter = PosFilter(['JJ','RB'], ['RB', 'CC', ','])
    for sent in text_ops.filter_file(filter, args.text_spec, charset='utf8'):
        print(sent)

if __name__ == '__main__':
    main()
