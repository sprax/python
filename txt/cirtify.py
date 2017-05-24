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
import text_ops

import argparse
import errno
import os.path
import random
import re
import sys
import nltk
from collections import defaultdict

PROMPT = '> %s\n\t'

class Responses:
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
            return "%s, %s, %s! Can you talk about something else please!" % (
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


def throw_io_error():
    raise IOError('refusenik user')

def constant_factory(value):
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

def find_topic(sentence, verbose=0):
    parts = get_tags_to_words_map(sentence, verbose)
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

def get_input_text(in_prompt):
    return input(PROMPT % in_prompt)


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

class PartsOfSpeechMixin(object):
    '''One-shot *get_parts* mixin class'''
    def get_tags_to_words_map(self, verbose=0):
        return get_tags_to_words_map(self.text, verbose=0)

class NLPTextMixed(PartsOfSpeechMixin, NLPText):
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
            funcs = [f for (n, f) in Responses.__dict__.items() if callable(f)]
            while True:
                resp = random.choice(funcs)
                funcs.remove(resp)
                output = resp(parts)
                if output:
                    break
        input_text = cli.read_next(output)

def main():
    verbose = 1
    cirtify(verbose)

if __name__ == '__main__':
    main()
