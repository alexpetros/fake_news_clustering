#!/anaconda2/bin/python


import sys, os
import json
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import cluster 

# script to build dataframe from model 

# attempt to load model and corups pickles
model = None
corpus_full = None
dictionary_full = None

try:
    model = joblib.load('./pickles/model.pkl')
except FileNotFoundError as e:
    print('pickle not found - building model')
    model = cluster.buildtopics(40)

try:
    corpus_full = joblib.load('./pickles/corpus_full.pkl')
    dictionary_full = joblib.load('./pickles/dictionary_full.pkl')
except Exception as e:
    print('pickle not found - building corpus and dictionary')
    model = cluster.buildtopics(40)


# print documents in loadings
fn_filepath = './data/fake_news.json'
with open(fn_filepath) as data_file:    
    fake_news = json.load(data_file)

corpus_full, dictionary_full = cluster.prepare_dtm(fake_news)

joblib.dump(corpus_full, 'corpus_full.pkl')
joblib.dump(dictionary_full, 'dictionary_full.pkl')


loadings = model[corpus_full]
for document in loadings:
    print(document)