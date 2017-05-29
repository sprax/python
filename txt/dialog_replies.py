#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''
dialog module: DialogReplies class
Used by: cirtify.py
'''

import argparse
import random
from collections import defaultdict
import nltk
# import text_fio
import dialog_util as dutil

PROMPT = '> %s\n\t'

def get_input_text(in_prompt):
    return input(PROMPT % in_prompt)

class DialogReplies:
    '''random responses'''
    def response_stock(parts):
        return random.choice(["How do you feel about that?",
            "What's your favourite animal?",
            "Tell me about your mother?"])

    def response_noun1(parts):
        responses = ["Why do you like %s?", "What do you like most about %s?",
                "Tell me more about %s?"]
        if 'NN' in parts:
            return random.choice(responses) % random.choice(parts['NN'])

    def response_nouns2(parts):
        if 'NN' in parts:
            noun = random.choice(parts['NN'])
            return "%s, %s, %s! Can you talk about something else please?!" % (
                    noun, noun.title(), noun.upper())

    def response_nouns1(parts):
        responses = ["Tell me how %s make you feel?", "You want to tell me how you feel about %s?"]
        if 'NNS' in parts:
            return random.choice(responses) % random.choice(parts['NNS'])

    def response_verb1(parts):
        if 'VB' in parts:
            verb = random.choice(parts['VB'])
            day = random.choice('Mondays Wednesdays Toast Acid'.split())
            return "Wow, I love to %s too, especially on %s. When do you like to %s?" % (
                    verb, day, verb)


def next_prompt(parts):
    funcs = [f for f in DialogReplies.__dict__.values() if callable(f)]
    while True:
        resp = random.choice(funcs)
        funcs.remove(resp)
        prompt = resp(parts)
        if prompt:
            return prompt

def cirtify(verbose=0):
    '''Responses like Eliza'''
    cli = dutil.CliInputText()    # TODO: put this block in class derived from abstract InputText?
    # INPUT: Get next input (phrase, sentence, or paragraph)
    input_text = cli.read_next("Please give me a sentence to paraphrase, or hit return to quit:")
    while input_text:
        # CLASSIFY: What is it?  Word, phrase, sentence, or paragraph?
        nlpt = dutil.NLPTextMixed(input_text)
        parts = nlpt.get_tags_to_words_map(verbose)
        topic = nlpt.find_topic_from_parts(input_text)
        if topic:
            print("Can I rephrase that idea for you?  The topic is {}, and you said:\n\t{}".format(
                topic, input_text))
            break
        else:
            prompt = next_prompt(parts)
        input_text = cli.read_next(prompt)

def main():
    '''Eliza-like dialog.'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description=__doc__)
    parser.add_argument('-number', dest='sum_count', type=int, nargs='?', const=1, default=0,
                        help='number of retries (default: 5), overrides -percent')
    parser.add_argument('-out_file', type=str, nargs='?', const='-',
                        help='output file for summarized text (default: None)')
    parser.add_argument('-repr', action='store_true',
                        help='output repr of data, not raw data')
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
