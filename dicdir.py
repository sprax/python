#!/usr/bin/env python
# Usage: python <thisScript> [inputDir [filePatterns [outSuffix]]]
# Sprax Lines  2012 ?

# import modules
from collections import defaultdict
import glob
import os
import re
from stat import S_ISREG, S_ISDIR, ST_MTIME, ST_MODE
import shutil
import sys
import time

debug = 3

def dicDir(dirpath, dirSuffix, patterns):
    """ Make dictionary mapping file modification dates to file names 
    """
    # get all entries in the directory w/ stats

    print
    print "DirPath: " , dirpath
    print "Patterns: " , patterns

    print 
    print "Directories: "
    dp = dirpath
    #dp = "/asd/PYTHON/AA/"
    dirs = filter(os.path.isdir, os.listdir(dp))
    if debug > 2:
        print dirs
	print "len(patterns): ", len(patterns)
	# exit(0)
    for dp in sorted(dirs):
        dn = os.path.basename(dp)
        try:
            ts = time.strptime(dn, "%b %d, %Y")
            # print "time.ts: ", ts
            dates = time.strftime("%Y.%m.%d_%a", ts)
            print "dirName ==> dated :: %s ==> %s" % (dn, dates)
            canonDateDirName = getUniqueDirName(dirs, dates)
            if debug > 1:
                print "unique cannonical dir name: ", canonDateDirName
            print "Moving ", dn, " to ", canonDateDirName
            shutil.move(dn, canonDateDirName)
            dirs.append(canonDateDirName)
        except:
            if debug > 0:
                print "dirName (%s) did not parse as a date" % dn    

    print 
    print "Files: "
    files = []
    for pattern in patterns:
        print "globbing pattern: ", pattern
        files.extend( filter(os.path.isfile, glob.glob(dirpath + "/" + pattern)) )
    pairs = ((os.stat(fn), fn) for fn in files)
    if debug > 1:
        print files
        # exit(0)

    print
    print "Dictionary: "
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
        print modtime, datestr, os.path.basename(path)
        print time.ctime(modtime), os.path.basename(path)
        date2files[datestr].append(path)

    for key in sorted(date2files.keys()):
        print key
        dfiles = sorted(date2files[key])
        for fn in dfiles:
            print "\t\t" + fn
    return dirs, date2files


def usage(defaultTemplate, defaultOutput):
    print "Default template file: " + defaultTemplate
    print "Default output file: " + defaultOuput

def getUniqueDirName(dirs, baseName):
    suffix = 0
    uniqDirName = baseName
    while uniqDirName in dirs:
        suffix += 1
        uniqDirName = baseName + "_" + str(suffix)
    return uniqDirName


def mvFilesToDateDirs(dirs, date2files):
    """ Put Acc test results into a canonical CSV format, one column per test run.
    Usage: python canonize.py templateFile outputFile] summaryFile(s) 
    NB:  the outputFile name will have '.csv' appended   
    """

    print "mvFilesToDateDirs"
    print dirs
    for key in sorted(date2files.keys()):
        # Get unique directory name
        uniqDirName = getUniqueDirName(dirs, key)
        if not os.path.exists(uniqDirName):
            print "Making directory: ", uniqDirName
            os.makedirs(uniqDirName)
        dfiles = date2files[key]
        for fn in dfiles:
            print "Moving ", fn, " to ", uniqDirName
            shutil.move(fn, uniqDirName)


if __name__ == '__main__':
    """ Print out dictionary of modfication dates and files in a directory.
    """
    # simple, inflexible arg parsing:
    numArgs = len(sys.argv)

    print "numArgs: " , numArgs

    if (numArgs > 44):
        print sys.argv[0]
        print dicDir.__doc__

    # path to the directory (relative or absolute)
    # dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.'
    if numArgs > 1:
        dirpath = sys.argv[1]
    else:
        dirpath = "."

    begPatArgs = 2

    if numArgs > 3 and re.match("--s", sys.argv[2]):
        dirSuffix = sys.argv[3] 
        if debug > 0:
            print "Suffix: ", dirSuffix
        begPatArgs = 4
    else:
        dirSuffix = ''

    if numArgs > begPatArgs:
        patterns = sys.argv[begPatArgs:]
    else:
        patterns = ['*.jpg',  '*.mov']

    dirs, date2files = dicDir(dirpath, dirSuffix, patterns)

    if len(date2files.keys()) > 0:
        mvFilesToDateDirs(dirs, date2files)
    else:
        print "The date2files dict is empty."

