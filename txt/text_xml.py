#!/usr/bin/env python3
# Sprax Lines       2017.12      Written for Python 3.5
'''Print (re)formatted XML'''

# import argparse
# import pprint
import re
import xml.dom.minidom

REC_BLANK_ROWS = re.compile(r"\n\s*\n")
REC_BLANK_COLS = re.compile(r">\t\s*\t<")

def pretty_print_xml(raw):
    '''
    Parse a raw XML string and pretty print it compactly.
    In particular, try to remove blank lines.
    '''
    parsed = xml.dom.minidom.parseString(raw)
    pretty = parsed.toprettyxml()
    folded = REC_BLANK_ROWS.sub("\n", pretty)
    packed = REC_BLANK_COLS.sub(">\t<", folded)
    print(packed)


XML_EXAMPLE_RAW = '''
<note> <to>Tove</to> <from>Jani</from> <heading>Reminder</heading><body>Don't forget me this weekend!</body></note>
'''

XML_EXAMPLE_FMT = '''
<note>
    <to>Tove</to>
    <from>Jani</from>
    <heading>Reminder</heading>
    <body>Don't forget me this weekend!</body>
</note>
'''

XML_CATALOG = '''
<CATALOG>
<CD>
<TITLE>Romanza</TITLE>
<ARTIST>Andrea Bocelli</ARTIST>
<COUNTRY>EU</COUNTRY>
<COMPANY>Polydor</COMPANY>
<PRICE>10.80</PRICE>
<YEAR>1996</YEAR>
</CD>
<CD>
<TITLE>The dock of the bay</TITLE>
<ARTIST>Otis Redding</ARTIST>
<COUNTRY>USA</COUNTRY>
<COMPANY>Stax Records</COMPANY>
<PRICE>7.90</PRICE>
<YEAR>1968</YEAR>
</CD>
<CD>
<TITLE>Unchain my heart</TITLE>
<ARTIST>Joe Cocker</ARTIST>
<COUNTRY>USA</COUNTRY>
<COMPANY>EMI</COMPANY>
<PRICE>8.20</PRICE>
<YEAR>1987</YEAR>
</CD>
</CATALOG>
'''

def main():
    '''test pretty_print_xml'''
    pretty_print_xml(XML_EXAMPLE_RAW)

if __name__ == '__main__':
    main()
