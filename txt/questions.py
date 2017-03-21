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
            xdv(2)
            xdv(2, sentence)
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
        description="Extracts questions and statements from text file")
    parser.add_argument('text_spec', type=str, nargs='?', default='debate_questions.txt',
                        help='text file to search for Q and S')
    parser.add_argument('-list_numbers', action='store_true',
                        help='output list number for each filtered sentence')
    parser.add_argument('-verbose', type=int, nargs='?', const=2, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    if args.verbose > 8:
        print("args:", args)
        print(__doc__)
        exit(0)
    set_xdv_verbosity(args.verbose)

    #print('======== Remove Adverbs [RB] ==================================================')
    filter = PosFilter()
    for quands in text_ops.filter_file(filter, args.text_spec, charset='utf8'):
        if quands[0]:
            utf_print('  '.join(quands[0]))
    #print('======== Remove Adjectives [JJ] ===============================================')
    #print('======== Remove Adv and Adj [JJ, RB] ==========================================')

if __name__ == '__main__':
    main()
