#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''
dialog_promps module: DialogReplies class
Used by: cirtify.py
'''

import argparse
import random
from collections import defaultdict
import nltk
# import text_fio

PROMPT = '> %s\n\t'

def get_input_text(in_prompt):
    return input(PROMPT % in_prompt)

def get_tags_to_words_map(text, verbose=0):
    '''External method version of *get_parts*: throws away temp data'''
    words = nltk.word_tokenize(text)
    parts = nltk.pos_tag(words)
    if verbose:
        print("parts tags:", parts)
    dic = defaultdict(list)
    for word, part in parts:
        dic[part].append(word)
    return dic


def throw_io_error():
    '''throw an error'''
    raise IOError('refusenik user')

def constant_factory(value):
    '''constant generator'''
    return lambda: value

def ask_yes_no(prompt, retries=3, complaint='Yes or no, please!',
        default_function=constant_factory(False)):
    '''prompt for and take in y/n response'''
    while True:
        answer = input(prompt)
        yesno = answer.lower()
        if yesno.lower() in ('y', 'ye', 'yep', 'yes'):
            return True
        if yesno in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries <= 0:
            return default_function()
        print(complaint)

def ask_for_new_idea():
    sentence = input("Please give me a sentence to paraphrase, or an empty line to quit:\n\t")
    return sentence

def find_topic_from_parts(parts, verbose=0):
    if verbose > 0:
        print("parts DD is", parts)
    for val in parts['NNP']:
        yesno = ask_yes_no("So you want to talk about %s?\n\t" % (val))
        if yesno:
            return val
    for val in parts['NN']:
        yesno = ask_yes_no("Do you wish to ask a question about %s?\n\t" % val)
        if yesno:
            return val
    for val in parts['NNS']:
        yesno = ask_yes_no("Is the topic %s?\n\t" % val)
        if yesno:
            return val
    return None


class InputText(object):
    '''get the next unit of text'''
    def read_next(self, in_prompt):
        raise NotImplementedError

class CliInputText(InputText):
    '''Command-line input text'''
    def __init__(self, prompt='> %s\n\t', farewell="Thanks for playing."):
        super().__init__()
        self.prompt = prompt
        self.farewell = farewell

    def read_next(self, in_prompt):
        input_text = input(self.prompt % in_prompt)
        if not input_text:
            print(self.farewell)
        return input_text

class NLPText():
    '''Base class: Add data cleaning'''
    def __init__(self, text):
        self.text = text


class PartsOfSpeechMixin(object):
    '''One-shot *get_parts* mixin class'''
    def get_tags_to_words_map(self, verbose=0):
        self.parts = get_tags_to_words_map(self.text, verbose=0)
        return self.parts


class TopicFromPartsMixin(object):
    '''One-shot *get_parts* mixin class'''
    def find_topic_from_parts(self, verbose=0):
        return find_topic_from_parts(self.parts, verbose=0)


class NLPTextMixed(TopicFromPartsMixin, PartsOfSpeechMixin, NLPText):
    '''Lightweight class getting one-shot functionality from mixins'''
    def __init__(self, text):
        super().__init__(text)
        self.text = text

class PartsOfSpeechInterface(object):
    '''Interface for more full-featured *get_parts* functionality'''
    def get_tags_to_words_map(self, verbose=0):
        raise NotImplementedError

    def get_word_tag_pairs(self, verbose=0):
        raise NotImplementedError

    def get_word_tokens(self, verbose=0):
        raise NotImplementedError


class TaggedNLPText(PartsOfSpeechInterface, NLPText):
    '''Concrete *get_parts* class'''
    def __init__(self, text, verbose=0):
        super().__init__(text)
        print("-------- inside PartsOfSpeechNLTK ----------")
        self.words = nltk.word_tokenize(self.text)
        self.parts = nltk.pos_tag(self.words)
        if verbose:
            print("parts tags:", self.parts)
        self.dic = defaultdict(list)
        for word, part in self.parts:
            self.dic[part].append(word)

    def get_tags_to_words_map(self, verbose=0):
        return self.dic

    def get_word_tag_pairs(self, verbose=0):
        return self.parts

    def get_word_tokens(self, verbose=0):
        return self.words


def next_prompt(parts):
    funcs = [f for f in DialogResponses.__dict__.values() if callable(f)]
    while True:
        resp = random.choice(funcs)
        funcs.remove(resp)
        prompt = resp(parts)
        if prompt:
            return prompt

def cirtify(verbose=0):
    '''Can I Rephrase That Idea For You?'''
    cli = CliInputText()    # TODO: put this block in class derived from abstract InputText?
    # INPUT: Get next input (phrase, sentence, or paragraph)
    input_text = cli.read_next("Please give me a sentence to paraphrase, or hit return to quit:")
    while input_text:
        # CLASSIFY: What is it?  Word, phrase, sentence, or paragraph?
        nlpt = TaggedNLPText(input_text)
        parts = nlpt.get_tags_to_words_map(verbose)
        topic = find_topic(input_text)
        if topic:
            print("Can I rephrase that idea for you?  The topic is {}, and you said:\n\t{}".format(
                topic, input_text))
            break
        else:
            prompt = next_prompt(parts)
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
    parser.add_argument('-error', dest='error_text', type=str, nargs='?', const='log this msg',
                        help='write same message to stderr and stdout, then exit')
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

    if args.error_text:
        text_fio.print_stdout_stderr(args.error_text)
        exit(1)

    if args.verbose > 3:
        print("outfile: <{}>".format(args.out_file))
        print("args:", args)
        print(__doc__)
        exit(0)

    # summary_file = getattr(args, 'out_file', None)
    cirtify(args.verbose)

if __name__ == '__main__':
    main()
