#!/usr/bin/env python3
# Sprax Lines       2016.07.25      Written with Python 3.5
'''regex matcher with rules from json file'''
from __future__ import print_function
import json
import re
import sys

def load_json_file(path, key='rules'):
    ''' load rules from JSON file '''
    with open(path) as fin:
        return json.load(fin)[key]

def match_rules(rules, body):
    ''' find and show matches '''
    for rule in rules:
        match = rule['re'].match(body)
        if match:
            print("pattern({})  body({})  match({})  groups({})".format(rule['pattern'], body, match, match.groups()))

def compile_rules(rules):
    """
    Precompiles all pattern rules into an 're' key.
    """
    for rule in rules:
        rule['re'] = re.compile(rule['pattern'], re.IGNORECASE)

def load_rules(path='social_graces_regex.json'):
    '''read rules from JSON file'''
    rules = load_json_file(path, 'rules')
    compile_rules(rules)
    return rules

def my_print(line):
    ''' print utf-8-encoded line '''
    print(line.encode("utf-8"))


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    ''' print encoded line with options '''
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        func = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(func, objects), sep=sep, end=end, file=file)
