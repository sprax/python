'''Convert decimal number to Roman numerals'''

NUMERAL = (
    ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400), ("C", 100), ("XC", 90),
    ("L", 50), ("XL", 40), ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1))

def romanize(nin):
    '''Roman numeral representation of number'''
    roman = []
    for ltr, num in NUMERAL:
        (div, nin) = divmod(nin, num)
        roman.append(ltr * div)
    return "".join(roman)


YEAR = 1949
print(YEAR, romanize(YEAR))
