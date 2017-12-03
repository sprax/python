#!/usr/bin/env python3
'''scrape questions'''
import requests
from bs4 import BeautifulSoup

import qa_csv

def get_url_text(url):
    '''should validate url?'''
    try:
        got = requests.get(url)
        return got.text
    except:
        print("Could not open connection to {}".format(url))
    return ""

#css selectors:
#non-main quizzes
#.all-other-quizzes a
def sparknotes_qa_pairs(text):
    '''Get QA pairs from SparkNotes quiz pages'''
    soup = BeautifulSoup(text, 'lxml')
    question_nodes = soup.find_all(class_='quick-quiz-question')

    qa_pairs = []
    for node in question_nodes:
        # Get question and answer texts
        q_text = node.find_all('h3')[0].text.strip(r'1234567890. \s\t\n').strip().replace("\n", " ").replace("’", "'")
        a_text = node.find_all(class_='border-blue semi-bold true-answer'
                              )[0].text.strip().replace("\n", " ").replace("’", "'")
        qa_pairs.append((q_text, a_text))
    return qa_pairs


def enotes_qa_pairs(text):
    '''Get QA pairs from eNotes quiz pages'''
    soup = BeautifulSoup(text, 'lxml')
    question_nodes = soup.find_all(class_='quick-quiz-question')

    qa_pairs = []
    for node in question_nodes:
        # Get question and answer texts
        q_text = node.find_all('h3')[0].text.strip(r'1234567890. \s\t\n').strip(
            ).replace("\n", " ").replace("’", "'")
        a_text = node.find_all(class_='border-blue semi-bold true-answer'
                              )[0].text.strip().replace("\n", " ").replace("’", "'")
        qa_pairs.append((q_text, a_text))
    return qa_pairs

def get_quiz_relative_paths(text):
    '''subpaths'''
    soup = BeautifulSoup(text, 'lxml')
    link_nodes = soup.select(".all-other-quizzes a")

    relative_paths = []
    for node in link_nodes:
        relative_paths.append(node.get('href'))
    return relative_paths

def scrape_and_save_qa(url, path):
    '''scrape QA pairs (SparkNotes) from one quiz and save them to CSV'''
    raw_text = get_url_text(url)
    if raw_text:
        qa_pairs = sparknotes_qa_pairs(raw_text)
        if qa_pairs:
            qa_csv.csv_write_qa(qa_pairs, path)

def scrape_moby_sparknotes_quizzes(start=1570, stop=1590):
    '''scrape and save QA pairs from a range of quiz URLs'''
    for quiz_id in range(start, stop):
        url = "http://www.sparknotes.com/lit/mobydick/section16.rhtml?quickquiz_id=%s" % quiz_id
        scrape_and_save_qa(url, "MobySparkNotesQuiz%s.csv" % quiz_id)
