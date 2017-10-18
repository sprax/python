#!/usr/bin/env python3
import csv
from quat import Quat

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
    ''' Returns a list of quats (question-answer tuples) read from a CSV file. '''
    quats = []
    try:
        with open(path, 'rt', newline=newline) as in_file:
            reader = csv.reader(in_file, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                lenrow = len(row)
                assert lenrow > 1
                row[0] = int(row[0])
                # row[1] = str(row[1])
                if lenrow < 3:
                    row[2] = row[3] = None
                else:
                    row[3] = int(row[3]) if len(row) > 3 else None
                quat = Quat(*row)
                quats.append(quat)
    except Exception as ex:
        print("csv_read_qa failed to read Quats from ({}) with error: ({})".format(path, ex))
    return quats

def csv_write_qa(quats, path, newline=None, delimiter=',', quotechar='"'):
    ''' Write a list of (question, answer)-tuples to a CSV file. '''
    try:
        with open(path, "w", newline=newline) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for quat in quats:
                assert len(quat) > 3
                assert isinstance(quat.id, int)
                assert isinstance(quat.label, int)
                writer.writerow(quat)
    except Exception as ex:
        print("csv_write_qa failed to write Quats to ({}) with error: {}".format(path, ex))

def add_offset(inpath, outpath, offset=100, newline=None, delimiter=',', quotechar='"'):
    '''Add a fixed offset to the indices in all QuandA rows.'''
    quats = csv_read_qa(inpath, newline=newline, delimiter=delimiter, quotechar=quotechar)
    for qax in quats:
        qax[0] = int(qax[0]) + offset
        qax[3] = int(qax[3]) + offset
    csv_write_qa(quats, outpath, newline=newline, delimiter=delimiter, quotechar=quotechar)
