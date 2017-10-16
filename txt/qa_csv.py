#!/usr/bin/env python3
import csv


def csv_read(path, newline=None, delimiter=',', quotechar='"'):
    ''' Return a list of row-tuples read from a CSV file; not QA-specific. '''
    rows = []
    try:
        with open(path, 'rt', newline=newline) as in_file:
            reader = csv.reader(in_file, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                rows.append(row)
    except Exception as ex:
        print("csv_read failed to get rows from ({}) with error: {}".format(path, ex))
    return rows

def csv_write(rows, path, newline=None, delimiter=',', quotechar='"'):
    ''' Write a list of row-tuples to a CSV file; not QA-specific. '''
    try:
        with open(path, "w", newline=newline) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for row in rows:
                writer.writerow(row)
    except Exception as ex:
        print("csv_write_qa failed to write rows to ({}) with error: {}".format(path, ex))

def csv_read_qa(path, newline=None, delimiter=',', quotechar='"'):
    ''' Return a list of (question, answer)-tuples read from a CSV file. '''
    quandas = []
    try:
        with open(path, 'rt', newline=newline) as in_file:
            reader = csv.reader(in_file, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                row[0] = int(row[0])
                if len(row) > 3:
                    row[3] = int(row[3])
                quandas.append(row)
    except Exception as ex:
        print("csv_read_qa failed to get quandas from ({}) with error: {}".format(path, ex))
    return quandas

def csv_write_qa(quandas, path, newline=None, delimiter=',', quotechar='"'):
    ''' Write a list of (question, answer)-tuples to a CSV file. '''
    try:
        with open(path, "w", newline=newline) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for quanda in quandas:
                writer.writerow(quanda)
    except Exception as ex:
        print("csv_write_qa failed to write quandas to ({}) with error: {}".format(path, ex))

def add_offset(inpath, outpath, offset=100, newline=None, delimiter=',', quotechar='"'):
    '''Add a fixed offset to the indices in all QuandA rows.'''
    quandas = csv_read_qa(inpath, newline=newline, delimiter=delimiter, quotechar=quotechar)
    for qax in quandas:
        qax[0] = int(qax[0]) + offset
        qax[3] = int(qax[3]) + offset
    csv_write_qa(quandas, outpath, newline=newline, delimiter=delimiter, quotechar=quotechar)
