
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import spacy

NLP = spacy.load('en')
import pandas as pd
import spacy

NLP = spacy.load('en')

def spacy_tokenize_(text):
    doc_ = NLP(text)
    return [i.orth_.lower() for i in doc_ if not i.is_space]

def spacy_tokenize(text):
    doc_ = NLP(text)
    tok_texts = [i.text for i in doc_ if not i.is_space and not i.is_stop and not i.is_punct]
    return tok_texts

def get_vectorizer():
    return CountVectorizer(tokenizer=spacy_tokenize_)

# resume_dataset = pd.read_csv("resumes_text.csv")
def get_resume_dataset():
    '''get the resume dataset'''
    return pd.read_csv("resumes_text.csv")

def get_array_from_dataset_resumes(vectorizer, dataset):
    '''vectorize the result of something like what's returned by get_resumes_dataset'''
    return vectorizer.fit_transform(dataset.resumes)

def get_array_and_feature_names(vectorizer, dataset):
    '''get feature names from vectorizer AFTER calling fit_transform on it.'''
    data_arr = get_array_from_dataset_resumes(vectorizer, dataset)
    features = vectorizer.get_feature_names()
    return data_arr, features

def get_max_weighted_feature(vectorizer, vectorized):
    '''Get maximal feature from, e.g., vectorized = data_array[0]'''
    maxed = vectorized.todense().argmax()
    return vectorizer.get_feature_names()[maxed]


def compare_resumes(res1, res2):
    resvec1 = vectorizer.transform([res1])
    resvec2 = vectorizer.transform([res2])
    return cosine_similarity(resvec1, resvec2)
