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
import datetime
import errno
import os.path
import random
import re
import sys
from utf_print import utf_print
import text_ops
import time
import nltk
from collections import defaultdict

PROMPT = '> '
INITIAL_PROMPT = 'How are you feeling?'

class Responses:
    def response_stock(parts):
        return random.choice(["How do you feel about that?", "What's your favourite animal?", "Tell me about your mother?"])

    def response_noun1(parts):
        responses = ["Why do you like %s?", "What do you like most about %s?", "Tell me more about %s?"]
        if 'NN' in parts:
            return random.choice(responses) % random.choice(parts['NN'])

    def response_nouns2(parts):
        if 'NN' in parts:
            noun = random.choice(parts['NN'])
            return "%s, %s, %s! Can you talk about something else please!" % (noun, noun.title(), noun.upper())

    def response_nouns1(parts):
        responses = ["Tell me how %s make you feel?", "You want to tell me how you feel about %s?"]
        if 'NNS' in parts:
            return random.choice(responses) % random.choice(parts['NNS'])

    def response_verb1(parts):
        if 'VB' in parts:
            verb = random.choice(parts['VB'])
            day = random.choice('Mondays Wednesdays Toast Acid'.split())
            return "Wow, I love to %s too, especially on %s. When do you like to %s?" % (verb, day, verb)

def get_parts_of_speech(text):
    text = nltk.word_tokenize(text)
    parts = nltk.pos_tag(text)
    dic = defaultdict(list)
    for word, part in parts:
        dic[part].append(word)
    return dic

def throw_io_error():
    raise IOError('refusenik user')

def constant_factory(value):
    return lambda: value

def ask_yes_no(prompt, retries=3, complaint='Yes or no, please!', default_function=constant_factory(False)):
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

def find_topic(sentence):
    parts = get_parts_of_speech(sentence)
    print("parts is", parts)
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

def cirtify():
    output = "Please give me a sentence to paraphrase, or an empty line to quit:"
    while True:
        user_input = input(PROMPT + output + "\n\t")
        if not user_input:
            print("Thanks for playing.")
            return
        parts = get_parts_of_speech(user_input)
        print("Let me try to rephrase that for you.  You said:\n\t{}".format(user_input))
        topic = find_topic(user_input)
        if topic:
            print("Great!  Let's talk about", topic)
            break
        else:
            funcs = [f for (n, f) in Responses.__dict__.items() if callable(f)]
            while True:
                resp = random.choice(funcs)
                funcs.remove(resp)
                output = resp(parts)
                if output:
                    break

def main():
    cirtify()

if __name__ == '__main__':
    main()
