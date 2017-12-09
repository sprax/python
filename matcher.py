#!/usr/bin/env python3
# Sprax Lines       2016.07.25      Written with Python 3.5
'''regex matcher with rules from json file'''

import json
import re
import sys

def load_json_file(path, key='rules'):
    with open(path) as fh:
        return json.load(fh)[key]

def match_rules(rules, body):
    for rule in rules:
        match = rule['re'].match(body)
        if match:
            print("pattern({})  body({})  match({})  groups({})".format(rule['pattern'], body, match, match.groups()))

def compile(rules):
    """
    Precompiles all pattern rules into an 're' key.
    """
    for rule in rules:
        rule['re'] = re.compile(rule['pattern'], re.IGNORECASE)

def load_rules(path='social_graces_regex.json'):
    '''read rules from JSON file'''
    rules = load_json_file(path, 'rules')
    compile(rules)
    return rules

def my_print(line):
    print(line.encode("utf-8"))

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
