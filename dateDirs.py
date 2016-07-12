#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Updated for Python 3.5
'''
Group photos and videos by date and move them to folders named
for the dates found.  Moves .jpg and .mov files by default, but
the file extensions can be specified.

Usage: python <thisScript> [inputDir [filePatterns [outSuffix]]]
'''
# Sprax Lines  2012 ?

# import modules
from collections import defaultdict
import glob
import os
import re
# from stat import S_ISREG, S_ISDIR, ST_MTIME, ST_MODE
from stat import ST_MTIME
import shutil
import sys
import time

def dicDir(dirpath, dirSuffix, patterns, verbose):
    """ Make dictionary mapping file modification dates to file names """
    # get all entries in the directory w/ stats

    print()
    print("DirPath: ", dirpath)
    print("Patterns: ", patterns)
    print("Directories: ")
    out_dirs = filter(os.path.isdir, os.listdir(dirpath))
    if verbose > 2:
        for dn in out_dirs:
            print("\t", dn)

    for dp in sorted(out_dirs):
        dn = os.path.basename(dp)
        try:
            ts = time.strptime(dn, "%b %d, %Y")
            # print("time.ts: ", ts)
            dates = time.strftime("%Y.%m.%d_%a", ts)
            print("dirName ==> dated :: %s ==> %s" % (dn, dates))
            canonDateDirName = getUniqueDirName(out_dirs, dates)
            if verbose > 1:
                print("unique cannonical dir name: ", canonDateDirName)
            print("Moving ", dn, " to ", canonDateDirName)
            shutil.move(dn, canonDateDirName)
            out_dirs.append(canonDateDirName)
        except:
            if verbose > 0:
                print("dirName (%s) did not parse as a date" % dn)

    print("Files: ")
    files = []
    for pattern in patterns:
        files.extend(filter(os.path.isfile, glob.glob(dirpath + "/" + pattern)))
    pairs = ((os.stat(fn), fn) for fn in files)
    if verbose > 1:
        print(files)

    print()
    print("Dictionary: ")
    date2files = make_date_to_files_dic(pairs, dirSuffix)
    for key in sorted(date2files.keys()):
        print(key)
        dfiles = sorted(date2files[key])
        for fn in dfiles:
            print("\t\t" + fn)
    return out_dirs, date2files


def make_date_to_files_dic(pairs, dirSuffix):
    date2files = defaultdict(list)
    # On Windows `ST_CTIME` is a creation date,
    # but on Unix it could be something else.
    # Use `ST_MTIME` to sort by a modification date
    for fstat, path in sorted(pairs):
        modtime = fstat[ST_MTIME]
        tstruct = time.localtime(modtime)
        datestr = time.strftime("%Y.%m.%d_%a", tstruct)
        if len(dirSuffix) > 0:
            datestr = datestr + "_" + dirSuffix
        print(modtime, datestr, os.path.basename(path))
        print(time.ctime(modtime), os.path.basename(path))
        date2files[datestr].append(path)
    return date2files


def getUniqueDirName(dirs, baseName):
    '''if there is already a directory with this name (baseName), make a new name'''
    suffix = 0
    uniqDirName = baseName
    while uniqDirName in dirs:
        suffix += 1
        uniqDirName = baseName + "_" + str(suffix)
    return uniqDirName


    print("numArgs: ", numArgs)

def mvFilesToDateDirs(dirs, date2files):
    """ Put Acc test results into a canonical CSV format, one column per test run.
    Usage: python canonize.py templateFile outputFile] summaryFile(s)
    NB:  the outputFile name will have '.csv' appended"""

    print("mvFilesToDateDirs")
    print(dirs)
    for key in sorted(date2files.keys()):
        # Get unique directory name
        uniqDirName = getUniqueDirName(dirs, key)
        if not os.path.exists(uniqDirName):
            print("Making directory: ", uniqDirName)
            os.makedirs(uniqDirName)
        dfiles = date2files[key]
        for fn in dfiles:
            print("Moving ", fn, " to ", uniqDirName)
            shutil.move(fn, uniqDirName)


def main():
    """ Print out dictionary of modfication dates and files in a directory."""
    verbose = 3

    # simple, inflexible arg parsing:
    numArgs = len(sys.argv)

    if numArgs > 44:
        print(sys.argv[0])
        print(dicDir.__doc__)

    # path to the directory (relative or absolute)
    # dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.'
    if numArgs > 1:
        dirpath = sys.argv[1]
    else:
        dirpath = "."

    begPatArgs = 2

    if numArgs > 3 and re.match("--s", sys.argv[2]):
        dirSuffix = sys.argv[3]
        if verbose > 0:
            print("Suffix: ", dirSuffix)
        begPatArgs = 4
    else:
        dirSuffix = ''

    if numArgs > begPatArgs:
        patterns = sys.argv[begPatArgs:]
    else:
        patterns = ['*.jpg', '*.mov', '*.png']

    dirs, date2files = dicDir(dirpath, dirSuffix, patterns, verbose)

    if len(date2files.keys()) > 0:
        mvFilesToDateDirs(dirs, date2files)
    else:
        print("The date2files dict is empty.")

if __name__ == '__main__':
    main()

