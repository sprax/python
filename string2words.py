# python
# Usage: python string2words.py words.txt rainrajatacozapsrakezarfabetrainzany

# import modules
import sys
 
debug = 1
WordCount = 0
MinWordLength =  2
MaxWordLength = 24
hDictionary = {}


def string2wordsFromEndOne(string, wordsAlreadyParsed):
    '''recursively divide a string into string of words, backing up greedily from the end.
    Returns a string with spaces inserted between the words, or Node if the parse fails.'''

    if (debug > 1):
        print("string2wordFromEnds: string(", string, ") words(", wordsAlreadyParsed, ")\n")

    # If the this string is a word, just return it with any words already parsed.
    if isWord(string):
        if wordsAlreadyParsed:
            return string + " " + wordsAlreadyParsed
        else:
            return string

    # Else divide the string into two parts, and if the 2nd part is a word, keep going.
    # Use min and max word lengths to skip checking substrings that cannot be words.
    maxIndex = len(string)
    minIndex = maxIndex - MaxWordLength
    if (minIndex < 0):
        minIndex = 0
    maxIndex -= MinWordLength;
    while (maxIndex > minIndex):
        substr = string[maxIndex:]
        if isWord(substr):
            if wordsAlreadyParsed:
                substr += " " + wordsAlreadyParsed
            moreWords = string2wordsFromEndOne(string[0:maxIndex], substr)
            if moreWords:
                return moreWords
        maxIndex -= 1
    return None          # string did not parse


def string2wordsFromBegAll(string, wordsAlreadyParsed, allParses):
    '''recursively divide a string into array of strings of words, going greedily from the beginning.
    Returns a string with spaces inserted between the words, or None if the parse fails.'''

    if (debug > 1):
        print("string2wordsFromBegAll: string(", string, ") words(", wordsAlreadyParsed, ")\n")

    # If the this string is a word, just return it with any words already parsed.
    if isWord(string):
        if wordsAlreadyParsed:
            parsed = string + " " + wordsAlreadyParsed
        else:
            parsed = string
        allParses.append(parsed)

    # Else divide the string into two parts, and if the 2nd part is a word, keep going.
    # Use min and max word lengths to skip checking substrings that cannot be words.
    maxIndex = len(string)
    minIndex = maxIndex - MaxWordLength
    if (minIndex < 0):
        minIndex = 0
    maxIndex -= MinWordLength;
    while (maxIndex > minIndex):
        substr = string[maxIndex:]
        if isWord(substr):
            if wordsAlreadyParsed:
                substr += " " + wordsAlreadyParsed
            string2wordsFromBegAll(string[0:maxIndex], substr, allParses)
        maxIndex -= 1

    # No return value; any results were appended to allParses.


def loadDictionary(fileName):
    global hDictionary
    wordCount = 0
    for line in open(fileName):  # opened in text-mode; all EOLs are converted to '\n'
        line = line.rstrip('\n')
        size = len(line)
        wordCount += 1;
        hDictionary[line] = size
    print("Read ", wordCount , " words from dictionary file: ", fileName, "\n");

def isWord(string):
    global hDictionary
    return hDictionary.get(string)


def isPalindrome(data):
    halfLength = int(len(data) / 2);
    for j in range(halfLength):
        if (data[j] != data[-j-1]):
            return False
    return True


def isPalindrome_test(string):
    print("(1 > 0)", (1 > 0));
    print("(1 > 2)", (1 > 2));
    if (0):
        print('0 is True')
    if (1):
        print('1 is True')
    print("string", string, "is a palindrome? ", isPalindrome(string));
    tuple = (1, 2, 3, 2, 1);
    print("tuple", tuple, "is a palindrome? ", isPalindrome(tuple));
    list = [4, 5, 6, 7, 7, 6, 5, 4];
    print("list", list, "is a palindrome? ", isPalindrome(list));


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = "words.txt"

    if len(sys.argv) > 2:
        strings = [sys.argv[2:]]
    else:
        strings = ["minimumergold", "garbageatone", 'atone']


    isPalindrome_test(strings[0])

    loadDictionary(fileName)    

    if len(sys.argv) > 3:
        word = sys.argv[3]
        print("isWord(", word, ") returned ", isWord(word), "\n");

    numStr = len(strings)
    for j in range(numStr):
        ret = string2wordsFromEndOne(strings[j], "")
        numParses = 0
        if ret != None:
            numParses = 1
        print("string2wordsFromEndOne got", numParses, "(", ret, ")")
        allParses = [];
        ret =  string2wordsFromBegAll(strings[j], "", allParses)
        numParses = len(allParses)
        print("string2wordsFromBegAll got", numParses, "(", allParses, ")")
