#!/usr/bin/env python3
# Sprax Lines       2016.09.26      Written for Python 3.5
''' Output some dates. '''

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
import datetime

def printDates(day_range):
    '''Output dates'''
    date = datetime.datetime.now()
    for day in range(day_range):
        date += datetime.timedelta(days=day)
        # print("date: ", date)
        dates = time.strftime("%Y.%m.%d_%a", date)
        print("%s ==> %s" % (date, dates))


def main():
    printDates(5)

if __name__ == '__main__':
    main()
