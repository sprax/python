#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''
CIRTIFY: Can I Rephrase That Idea For You?
Interactive paraphrasing program.
Goals:
    1.  Parse words of initial idea to guess what it is: Question, Statement, Topic, ...
            Verify guess, as needed, to decide top-level class (QST-class), and go to 2.
    2.  Use QST-class to parse: PoS-tags, tree, etc., and identify topic(s) with confidence
        Loop: When confidence is sufficient, go to 3.
            Dialog: ask questions to clarify
    3.  Suggest a paraphrase in a canonical-form and ask:
            Yes/Done, No/Refine, Add/More paraphrases, Cancel/Abandon
        Loop: When yes, save and go to 4, or if cancel, delete and go to 4.
    4.  Acknowledge Finish or Canceled.
'''

import argparse
import dialog_util
import dialog_replies

def cirtify(verbose=0):
    '''Can I Rephrase That Idea For You?'''
    cli = dialog_util.CliInputText()
    # INPUT: Get next input (phrase, sentence, or paragraph)
    input_text = cli.read_next("Please give me a sentence to paraphrase, or hit return to quit:")
    while input_text:
        # CLASSIFY: What is it?  Word, phrase, sentence, or paragraph?
        nlpt = dialog_util.TaggedNLPText(input_text)
        parts = nlpt.get_tags_to_words_map(verbose)
        topic = dialog_util.find_topic_from_parts(parts)
        if topic:
            print("Can I rephrase that idea for you?  The topic is {}, and you said:\n\t{}".format(
                topic, input_text))
            break
        else:
            prompt = dialog_replies.next_prompt(parts)
        input_text = cli.read_next(prompt)

def main():
    '''Extract summary from text.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Extractive text summarizer")
    parser.add_argument('text_file', type=str, nargs='?', default='corpus.txt',
                        help='file containing text to summarize')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
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
    parser.add_argument('-repr', action='store_true',
                        help='output repr of data, not raw data')
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
    cirtify(args.verbose)

if __name__ == '__main__':
    main()
