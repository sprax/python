#!/usr/bin/env python3
'''
@file: polldir.py
@auth: Sprax Lines
@date: 2016-06-02 17:36:26 Thu 02 Jun

Poll a directory for the latest file matching a file_pat.
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


def get_latest_file_name_and_time(dir_path, file_pat='txt', old_ftime=0, verbose=1):
    ''' yes '''
    latest_fname = None
    latest_ftime = old_ftime
    for fname in filter(os.path.isfile, glob.glob(dir_path + "/" + file_pat)))
        fstat = os.stat(fname)
        ftime = fstat[ST_MTIME]
        if  latest_ftime < ftime:
            latest_ftime = ftime
            latest_fname = fname
            if verbose > 1:
                print("Keep ftime, fname: %d  %f" % (ftime, fname))
    return latest_fname, latest_ftime


def poll_dir_for_new_file(dir_path, file_pat, old_time=0, verbose=1, call_back=None, *cb_args):
    """ poll dir for any new file(s) matching file_pat.
        When a file newer than old_time is found, old_time is set to the new
        time
        and call_back is called as: truthy = call_back(cb_args)
        Or, if call_back is None, the function returns
        the latest file and file mod time.
"""
    # get all entries in the directory w/ stats
    fname = None
    ftime = old_ftime
    while(True):
        fname, ftime = get_latest_file_name_and_time(dir_path, file_pat, old_time, verbose)
        if fname is not None:
            if call_back is None:
                return fname, ftime
            truthy = call_back(*cb_args)
    return fname, ftime


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
    '''
    if there is already a directory with this name (baseName), make a new name
    '''
    suffix = 0
    uniqDirName = baseName
    while uniqDirName in dirs:
        suffix += 1
        uniqDirName = baseName + "_" + str(suffix)
    return uniqDirName


def mvFilesToDateDirs(dirs, date2files):
    """ Put Acc test results into a canonical CSV format, one column per test
    run.
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

    print("numArgs: ", numArgs)

    if numArgs > 44:
        print(sys.argv[0])
        print(poll_dir.__doc__)

    # path to the directory (relative or absolute)
    # dir_path = sys.argv[1] if len(sys.argv) == 2 else r'.'
    if numArgs > 1:
        dir_path = sys.argv[1]
    else:
        dir_path = "."

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
        patterns = ['*.jpg', '*.mov']

    dirs, date2files = poll_dir(dir_path, dirSuffix, patterns, verbose)

    if len(date2files.keys()) > 0:
        mvFilesToDateDirs(dirs, date2files)
    else:
        print("The date2files dict is empty.")


if __name__ == '__main__':
    main()
