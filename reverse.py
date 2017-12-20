'''reverse a string'''

import sys

def reverse_string(string):
    '''reverse'''
    return string[::-1]

def main():
    '''test reverse_string'''
    string = sys.argv[1] if len(sys.argv) > 1 else 'Jesus Mary and Joseph'
    print(string, '==>', reverse_string(string))

if __name__ == '__main__':
    main()
