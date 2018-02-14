#!/anaconda2/bin/python
import os, sys
import json
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import stop_words
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
import logging
import pprint



fn_filepath = './data/fake_news.json'

def buildtopics(num_topics):
    wordnet_lemmatizer = WordNetLemmatizer()

    with open(fn_filepath) as data_file:    
        fake_news = json.load(data_file)

    # print(fake_news[1])

    # prepare dictionary
    corpus_full, dictionary_full = prepare_dtm(fake_news)

    # log and build models
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
        level=logging.INFO)
    model = gensim.models.LdaModel(corpus_full, num_topics=num_topics, 
        id2word=dictionary_full, passes=20)

    # save stuff!
    joblib.dump(model, 'model.pkl')

    # pprint.pprint(model.print_topics(num_topics=20, num_words=5))


def prepare_dtm(data):
    texts = []
    for text in data:
        # clean and tokenize document string (forcing unicode)

        text = text['text'].encode('ascii', 'ignore').lower()
        # if using python 2
        text = text.translate(None, string.digits)
        text = text.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(text)

        # remove stop words from tokens
        tokens = [i for i in tokens if not i in stop_words.ENGLISH_STOP_WORDS]

        # add tokens to list
        texts.append(tokens)
    
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_n_most_frequent(50)

    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus, dictionary


# run script if main
if __name__ == '__main__':
    buildtopics(sys.argv[1]) 