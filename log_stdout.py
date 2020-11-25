#!/usr/bin/env python3
# @file: log_stdout.py
# @auth: Sprax Lines
# @date: 2017-12-20 01:01:25 Wed 20 Dec

'''direct logging output to stdout'''

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    '''test logging'''
    string = sys.argv[1] if len(sys.argv) > 1 else 'Jesus Mary and Joseph'
    logging.info(string)


if __name__ == '__main__':
    main()
