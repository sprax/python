#!/bin/python3
# https://www.hackerrank.com/challenges/word-order
'''
Input Format

The first line contains the integer, .
The next  lines each contain a word.

Output Format

Output  lines.
On the first line, output the number of distinct words from the input.
On the second line, output the number of occurrences for each distinct
word according to their appearance in the input.
'''

def main():
    '''main'''
    count = int(input().strip())
    words = []
    dct = {}
    for _ in range(count):
        wrd = input().strip()
        cnt = dct.get(wrd)
        if cnt:
            dct[wrd] = cnt+1
        else:
            dct[wrd] = 1
            words.append(wrd)

    print(len(dct))
    for wrd in words:
        print(dct.get(wrd), '', end='')
    print()

main()
