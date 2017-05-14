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
import re
import sys
from utf_print import utf_print
import text_ops
import time



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

def cirtify():
    while True:
        sentence = ask_for_new_idea()
        if sentence:
            print("Let me try to rephrase that for you.  You said:\n\t{}".format(sentence))
        else:
            print("Thanks for playing.")
            return

def main():
    cirtify()

if __name__ == '__main__':
    main()
