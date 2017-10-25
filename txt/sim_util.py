#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''
import argparse
import errno
import os.path
import pickle
import random
import re
import sys
from utf_print import utf_print
import text_ops
import text_fio

########################################################
# util functions

def sort_numbered_lines_with_blanks(inpath, outpath, verbose=True, charset='utf8'):
    '''read numbered lines and output them in sorted order, with blanks for skipped numbers.'''
    lines = sorted(read_text_lines(inpath, charset=charset))
    prev = int(lines[0].split()[0]) - 1
    with open(outpath, "w") as outfile:
        for line in lines:
            toks = line.split()
            lnum = int(toks[0])
            rnum = int(toks[-1])
            prev += 1
            if lnum != prev:
                if verbose:
                    print("LNUM != PREV:", lnum, prev, "AT: ", line)
                print(file=outfile)
            print(line, file=outfile)
            prev = lnum


def pack_lines_and_ids(inpath, outpath, offset=100, verbose=True, sep="\t", charset='utf8'):
    '''Renumber lines to fill in any gaps and output them in sorted order.'''
    lines, tran = [], {}
    for idx, line in enumerate(read_text_lines(inpath, charset=charset)):
        toks = line.split()
        lnum = int(toks[0])
        rnum = int(toks[-1])
        onum = idx + offset
        if lnum != onum:
            if verbose:
                print("LNUM != ONUM:", lnum, onum, "AT: ", line)
            if lnum in tran:
                raise Exception("ERROR: lnum %d already encountered!" % lnum)
            tran[lnum] = onum
        toks[0] = onum
        toks[-1] = rnum
        lines.append((line, toks))
    with open(outpath, "w") as outfile:
        for line, toks in lines:
            lnum = toks[0]
            rnum = toks[-1]
            if rnum in tran:
                rnum = tran[rnum]
            print(lnum, line[4:-4], rnum, sep=sep, file=outfile)


def reorder_lines_and_ids(inpath, outpath, offset=200, verbose=True, sep="\t", charset='utf8'):
    '''Renumber lines to give a constant offset between ID and refID (first and last fields as int).'''
    lines, tran = [], {}
    for idx, line in enumerate(text_fio.read_text_lines(inpath, charset=charset)):
        toks = line.split()
        lnum = int(toks[0])
        rnum = int(toks[-1])
        onum = lnum + offset
        if idx < offset and rnum != onum:
            if verbose:
                print("RNUM != ONUM:", rnum, onum, "AT: ", line)
            if rnum in tran:
                raise Exception("ERROR: rnum %d already encountered!" % rnum)
            tran[rnum] = onum
            rnum = onum
        toks[0] = lnum
        toks[-1] = rnum
        lines.append((line, toks))

    with open(outpath, "w") as outfile:
        for idx, line, toks in enumerate(lines):
            lnum = toks[0]
            rnum = toks[-1]
            # if idx < offset and rnum in tran:
            #     rnum = tran[rnum]
            if idx >= offset and lnum in tran:
                lnum = tran[lnum]
            print(lnum, line[4:-4], rnum, sep=sep, file=outfile)
