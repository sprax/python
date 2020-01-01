#!/usr/bin/env python3
'''
@file: qa_csv.py
Read and write CSV files for QA
'''
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
    except IOError as ex:
        print("csv_read failed to get rows from ({}) with error: {}".format(path, ex))
    return rows

def csv_write(rows, path, newline=None, delimiter=',', quotechar='"'):
    ''' Write a list of row-tuples to a CSV file; not QA-specific. '''
    try:
        with open(path, "w", newline=newline) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for row in rows:
                writer.writerow(row)
    except IOError as ex:
        print("csv_write_qa failed to write rows to ({}) with error: {}".format(path, ex))

def csv_read_qa(path, maxrows=0, delimiter='\t', quotechar='"', verbose=False):
    ''' Returns a list of quats (question-answer tuples) read from a CSV file. '''
    quats = []
    try:
        with open(path, 'rt') as in_file:
            reader = csv.reader(in_file, delimiter=delimiter, quotechar=quotechar)
            for idx, row in enumerate(reader):
                if verbose:
                    print("ROW %3d: " % idx, row)
                lenrow = len(row)
                if lenrow < 1 or row[0] and row[0][0] == '#':
                    continue
                assert lenrow > 2
                id_num = int(row[0])
                try:
                    label = int(row[1])
                    question = row[2]
                    answer = row[3] if lenrow > 3 else None
                except ValueError:
                    try:
                        label = int(row[3])
                        question = row[1]
                        answer = row[2]
                    except Exception as oex:
                        raise ValueError("No label found at row {}:  {}  [{}]\n".format(idx, row, oex))

                quat = Quat(id=id_num, label=label, question=question, answer=answer)
                quats.append(quat)
                if maxrows == 1:
                    break
                else:
                    maxrows -= 1
    except IOError as ex:
        print("csv_read_qa failed to read Quats from ({}) with error: ({})".format(path, ex))
    return quats

def csv_write_qa(quats, path, delimiter='\t', quotechar='"'):
    ''' Write a list of (question, answer)-tuples to a CSV file. '''
    try:
        with open(path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for quat in quats:
                assert len(quat) > 3
                assert isinstance(quat.id, int)
                assert isinstance(quat.label, int)
                writer.writerow(quat)
    except IOError as ex:
        print("csv_write_qa failed to write Quats to ({}) with error: {}".format(path, ex))

def add_offset(inpath, outpath, offset=100, delimiter=',', quotechar='"'):
    '''Add a fixed offset to the indices in all QuandA rows.'''
    quats = csv_read_qa(inpath, delimiter=delimiter, quotechar=quotechar)
    for qax in quats:
        qax[0] = int(qax[0]) + offset
        qax[3] = int(qax[3]) + offset
    csv_write_qa(quats, outpath, delimiter=delimiter, quotechar=quotechar)
