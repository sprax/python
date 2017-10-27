#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''read text file, print regex-split words.'''

import text_fio

########################################################
# util functions

def sort_numbered_lines_with_blanks(inpath, outpath, verbose=True, charset='utf8'):
    '''read numbered lines and output them in sorted order, with blanks for skipped numbers.'''
    lines = sorted(text_fio.read_text_lines(inpath, charset=charset))
    prev = int(lines[0].split()[0]) - 1
    with open(outpath, "w") as outfile:
        for line in lines:
            toks = line.split()
            lnum = int(toks[0])
            if lnum == prev:
                if verbose:
                    print("LNUM == PREV:", lnum, prev, "AT: ", line)
                print(file=outfile)
                print(file=outfile)
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
    for idx, line in enumerate(text_fio.read_text_lines(inpath, charset=charset)):
        toks = line.split()
        lnum = int(toks[0])
        rnum = int(toks[1])
        onum = idx + offset
        if lnum != onum:
            if verbose:
                print("LNUM != ONUM:", lnum, onum, "AT: ", line)
            if lnum in tran:
                print("WARNING: lnum %d already encountered!" % lnum)
                while lnum in tran:
                    lnum += 1
                    onum += 1
                    # rnum += 1
            tran[lnum] = onum
        toks[0] = onum
        toks[1] = rnum
        lines.append((line, toks))
    with open(outpath, "w") as outfile:
        for line, toks in lines:
            lnum = toks[0]
            rnum = toks[1]
            if rnum in tran:
                rnum = tran[rnum]
            print(lnum, rnum, line[8:], sep=sep, file=outfile)


def reorder_lines_and_ids(inpath, outpath, devlen=200, offset=200, verbose=False, sep="\t", charset='utf8'):
    '''Renumber lines to give a constant offset between ID and refID (first and last fields as int).'''
    lines, tran, lnums = [], {}, set()
    for idx, line in enumerate(text_fio.read_text_lines(inpath, charset=charset)):
        toks = line.split()
        lnum = int(toks[0])
        rnum = int(toks[1])
        if idx < devlen:
            # change ref number to constant offset from id number (offset number)
            lnums.add(lnum)
            onum = lnum + offset
            if rnum != onum:
                if verbose:
                    print("RNUM != ONUM:", rnum, onum, "AT: ", line)
                if rnum in tran:
                    # raise Exception("ERROR: rnum %d already encountered!" % rnum)
                    print("WARNING: rnum %d already encountered!" % rnum)
                    rnum += 1
            tran[rnum] = onum
            toks[0] = lnum
            toks[1] = onum
            lines.append((line, toks))
        else:
            # change id number to matched changed ref number (offset number)
            if lnum in tran:
                toks[0] = tran[lnum]
            elif rnum in lnums:
                toks[0] = lnum
            else:
                raise Exception("ERROR: unknown lnum %d after index %d!" % (rnum, devlen))

            toks[1] = rnum
            lines.append((line, toks))

    lines.sort(key=lambda item: item[1])
    with open(outpath, "w") as outfile:
        for line, toks in lines:
            lnum = toks[0]
            rnum = toks[1]
            print(lnum, rnum, line[8:], sep=sep, file=outfile)
