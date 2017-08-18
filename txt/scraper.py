
#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup

def get_url_text(url):
    # validate url?
    try:
        got = requests.get(url)
        return got.text
    except:
        print("Could not open connection to {}".format(url))
    return ""


#css selectors:
#non-main quizzes
#.all-other-quizzes a
def get_qa_pairs(text):
    soup = BeautifulSoup(text, 'lxml')
    question_nodes = soup.find_all(class_='quick-quiz-question')

    qa_pairs = []
    for node in question_nodes:
        # Get question and answer texts
        q_text = node.find_all('h3')[0].text.strip('1234567890. \s\t\n').strip().replace("\n", " ").replace("’", "'")
        a_text = node.find_all(class_='border-blue semi-bold true-answer')[0].text.strip().replace("\n", " ").replace("’", "'")
        qa_pairs.append((q_text, a_text))
    return qa_pairs

def get_quiz_relative_paths(text):
    soup = BeautifulSoup(text, 'lxml')
    link_nodes = soup.select(".all-other-quizzes a")

    relative_paths = []
    for node in link_nodes:
        relative_paths.append(node.get('href'))
    return relative_paths

def csv_write_qa(qa_pairs, path):
    ''' Write a list of (question, answer) tuples to a CSV file. '''
    try:
        with open(path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for pair in qa_pairs:
                writer.writerow(pair)
    except Exception as ex:
        print("csv_write_qa failed to write qa_pairs to ({}) with error: {}".format(path, ex))

def csv_read_qa(path):
    ''' Return a list of (question, answer) tuples read from a CSV file. '''
    qa_pairs = []
    try:
        with open(path, 'rt') as infile:
            reader = csv.reader(infile)
            for row in reader:
                qa_pairs.append(row)
    except Exception as ex:
        print("csv_read_qa failed to get qa_pairs from ({}) with error: {}".format(path, ex))
    return qa_pairs

def scrape_and_save_qa(url, path):
    raw_text = get_url_text(url)
    if raw_text:
        qa_pairs = get_qa_pairs(raw_text)
        if qa_pairs:
            csv_write_qa(qa_pairs, path)

def scrap_moby_sparknotes():
    for quiz_id in range(1570, 1589):
        url = "http://www.sparknotes.com/lit/mobydick/section16.rhtml?quickquiz_id=%s" % quiz_id
        scrape_and_save_qa(url, "MobySparkNotesQuiz%s.csv" % quiz_id)
