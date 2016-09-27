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

dayCodes = ['Mnd', 'Tsd', 'Wnd', 'Thd', 'Frd', 'Std', 'Snd']

def printDates(day_range):
    '''Output dates'''
    date = datetime.datetime.now()
    for day in range(day_range):
        date += datetime.timedelta(days=1)
        tstm = date.timetuple()
        dstr = time.strftime("%Y.%m.%d", tstm)
        locs = 'Home/'
        if tstm.tm_wday < 5:
            locs += 'CIC'
        elif tstm.tm_wday < 6:
            locs += 'NH'
        else:
            locs += 'MIT'
        code = dayCodes[tstm.tm_wday]
        # print(tstm)
        # print("%s ==> %s %s\t%s" % (date, dstr, code, locs))
        print("%s %s\t%s" % (dstr, code, locs))


def main():
    printDates(5)

if __name__ == '__main__':
    main()
