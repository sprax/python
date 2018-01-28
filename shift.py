'''reverse a string'''

import sys

def shift_string(string):
    '''shift ==> tisfh'''
    # return string[::-2] + string[1:-1:-2]
    return string[::-2] + string[0:-1][::-2]

if __name__ == '__main__':
    STRING = sys.argv[1] if len(sys.argv) > 1 else 'Jesus Mary and Joseph'
    print(STRING, '==>', shift_string(STRING))
