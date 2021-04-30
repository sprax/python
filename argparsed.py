#!/usr/bin/env python3
'''argparse example'''
@file: argparsed.py
@auth: Sprax Lines
@date: 2016-09-12 23:09:56 Mon 12 Sep

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
