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

def main():
    '''test pretty_print_xml'''
    pretty_print_xml(XML_EXAMPLE_RAW)

if __name__ == '__main__':
    main()
