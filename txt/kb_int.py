#!/usr/bin/env python
import re
import time

rgxb = re.compile(r"^\s*['\"]")

def tr(ex):
    if (ex):
            print('True')
    else:
            print('false')

sp = "'Why, it's what I'm obliged to keep a little of in the house, to putinto the blessed infants' Daffy , when they ain't well, Mr. Bumble,'replied Mrs. Mann as she opened a corner cupboard, and took down abottle and glass.  'It's gin.  I'll not deceive you, Mr. B.  It's gin.'"

def kbint():
    count = 0
    print("kbint BEG", count)
    while True:
        try:
            time.sleep(1)
            count += 1
        except KeyboardInterrupt:
            print("\nCaught KeyboardInterrupt at", count)
            if count > 5:
                break;
    print("kbint END", count)
