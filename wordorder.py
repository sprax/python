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
    dd = {}
    for j in range(count):
        wd = input().strip()
        ct = dd.get(wd)
        if ct:
            dd[wd] = ct+1
        else:
            dd[wd] = 1
            words.append(wd)

    print(len(dd))
    for wd in words:
        print(dd.get(wd), '', end='')
    print()

main()
