#!/usr/bin/env python3
# Sprax Lines       2016.09.01      Written with Python 3.5
'''Print UTF-8 text'''

import sys

def uprint(*objects, sep=' ', end='\n', outfile=sys.stdout):
    '''Prints non-ASCII Unicode (UTF-8) characters in a safe (but possibly
    ugly) way even in a Windows command terminal.  Unicode-enabled terminals
    such as on Mac or KDE have no problem, nor do most IDE's, but calling
    Python's built-in print to print such characters (e.g., an em-dash)
    from a Windows cmd or Powershell terminal causes errors such as:
    UnicodeEncodeError: 'charmap' codec can't encode characters in position 32-33:
    character maps to <undefined> '''
    enc = outfile.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=outfile)
    else:
        enc_dec = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(enc_dec, objects), sep=sep, end=end, file=outfile)


if __name__ == '__main__':
    uprint("This is utfprint\n")
