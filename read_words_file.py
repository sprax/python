#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5

import re

with open('text.txt', 'r') as f:
    for line in f:
        words = re.split(r'\W+', line.rstrip())
        for word in words:
            if len(word) > 0:
                print(word)
        print(words)

