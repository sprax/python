#!/usr/bin/env python3
'''Example usage of kwargs with argparsed args and kwargs'''
@file: kwargs_args.py
@auth: Sprax Lines
@date: 2018-01-13 18:06:45 Sat 13 Jan

import argparse
import pprint
from pdb import set_trace


def print_kwargs(**kwargs):
    ''' print the **kwargs as a pretty printed dict.
        To print argparsed args, call print_kwargs(**vars(args))
    '''
    pprint.pprint(kwargs)


def main():
    '''get args and try stuff'''
    const_zoid, default_zoid = 2, 7777777

    parser = argparse.ArgumentParser(
        description="Drive boto3 Elasticsearch client")
    parser.add_argument('query', type=str, nargs='?',
                        default='IT', help='query string for search')
    parser.add_argument('-size', type=int, nargs='?', const=5, default=6,
                        help='Maximum number of results (default: 6)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='Verbosity of output (default: 1)')
    parser.add_argument('-zoid', '-bot_id', metavar='ID', type=int, nargs='?',
                        const=const_zoid, default=default_zoid,
                        help='Bot ID (const: %d, default: %d)' % (const_zoid, default_zoid))
    args = parser.parse_args()

    print("Type(args): ", type(args))
    print("======> pprint(args):")
    pprint.pprint(args, indent=4)
    print("======> print_kwargs(**vars(args)):")
    print_kwargs(**vars(args))


if __name__ == '__main__':
    main()
