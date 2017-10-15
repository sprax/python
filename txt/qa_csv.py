
#!/usr/bin/env python3
import csv

def csv_read_qa(path, newline=None, delimiter=',', quotechar='"'):
    ''' Return a list of (question, answer)-tuples read from a CSV file. '''
    qa_pairs = []
    try:
        with open(path, 'rt', newline=newline) as in_file:
            reader = csv.reader(in_file, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                qa_pairs.append(row)
    except Exception as ex:
        print("csv_read_qa failed to get qa_pairs from ({}) with error: {}".format(path, ex))
    return qa_pairs

def csv_write_qa(qa_pairs, path, newline=None, delimiter=',', quotechar='"'):
    ''' Write a list of (question, answer)-tuples to a CSV file. '''
    try:
        with open(path, "w", newline=newline) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            for pair in qa_pairs:
                writer.writerow(pair)
    except Exception as ex:
        print("csv_write_qa failed to write qa_pairs to ({}) with error: {}".format(path, ex))
