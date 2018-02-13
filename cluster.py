#!/anaconda/bin/python
import os
import json
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn import metrics
from sklearn.externals import joblib
import random
from gensim import corpora, models
import gensim
import pprint
import string

if os.name == 'nt':
    root_dir = "..\\..\\data\\"
else:
    root_dir = "../../data/"
    
wordnet_lemmatizer = WordNetLemmatizer()


with open(root_dir + 'clinton_emails.json') as data_file:    
    clinton_emails = json.load(data_file)