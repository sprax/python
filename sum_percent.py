#!/usr/bin/env python
'''
@file: sum_percent.py
@auth: Sprax Lines
@date: 2019.10.06
Convert size/name pairs, such as from uniq -c, into a table with percentages
Written for Python 3.7.4
'''
# from __future__ import print_function
# import pdb
# from pdb import set_trace
import fileinput

def sum_percent(beg=0, end=1):
    total_tags, total_debt = 0, 0
    auths, debts = [], []
    for line in fileinput.input():
        tokens = line.split()
        if len(tokens) > end:
            try:
                size = int(tokens[beg])
                name = tokens[end]
                if name[0] == '@':
                    total_tags += size
                    auths.append([size, name])
                elif name in ['FIXME', 'TODO']:
                    total_debt += size
                    debts.append([size, name])
            except ValueError:
                pass

    print("%12s %7s  % 7s" % ("AUTHOR", "Count", "Percent"))
    for tokens in auths:
        size, name = tokens[0:2]
        percent = size * 100 / total_debt
        print("%12s %7d  % 7.1f" % (name, size, percent))

    print("%12s %7s  % 7s" % ("MARKER", "-----", "-----"))
    for tokens in debts:
        size, name = tokens[0:2]
        percent = size * 100 / total_debt
        print("%12s %7d  % 7.1f" % (name, size, percent))

    print("%12s %7d  % 7.1f" % ("TOTALS", total_debt, 100.0))

if __name__ == '__main__':
    sum_percent()
