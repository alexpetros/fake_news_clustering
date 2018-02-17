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



def getDataFile():

    fn_filepath = './data/fake_news.json'
    fake_news = None

    try:
        with open(fn_filepath) as data_file:    
            fake_news = json.load(data_file)
    except IOError as e:
        raise IOError('Fake news json file not found - make sure ./data/fake_news.json exists')

    return fake_news


def buildtopics(num_topics, corpus, dictionary):
    '''
    using the corpus and dictionary of the 
    preconditons:
        num_topics - the number of topics we want to find in the corpus
        corpus - the group of documents,
        dictionary - word dictionary
    '''
    

    # log and build models
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
        level=logging.INFO)
    model = gensim.models.LdaModel(corpus, num_topics=num_topics, 
        id2word=dictionary, passes=20)

    # save stuff!
    joblib.dump(model, 'pickles/model.pkl')
    return model

    # pprint.pprint(model.print_topics(num_topics=20, num_words=5))


def prepare_dtm(data):
    '''
    builds document-text matrix from a list of dictionaries
    where each dictionary represents an article, and has a 'text' attribute
    preconditions:
        data - a list of dictonaries, descrived above
    postconditions:
        returns the corpus and dictonary objects 

    '''
    texts = []
    for text in data:
        # clean and tokenize document string (forcing unicode)

        text = text['text'].encode('ascii', 'ignore').lower()
        # if using python 2 - we are, regrettably
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

    # save and return stuff!
    joblib.dump(corpus, './pickles/corups.pkl')
    joblib.dump(dictionary, './pickles/corup.pkl')
    return corpus, dictionary


def loadtopics():
    ''''
    attempts to load the pickled model, 
    and builds neccesary components if they do not exits
    preconditon:
        if pickles do exist, they exist in './pickles'
        fake news file is in './data/fake_news.json'
    postcondition:
        returns model, corpus, and dictonary
    '''
    num_topics = 40

    model = None
    corpus = None
    dictionary = None

    # attempt to load corpus and dictionary, build if not found
    try:
        corpus = joblib.load('./pickles/corpus.pkl')
        dictionary = joblib.load('./pickles/dictionary.pkl')
    except Exception as e:
        # print documents in loadings
        print('pickle not found - building corpus and dictionary')
        fake_news = getDataFile()
        corpus, dictionary = prepare_dtm(fake_news)

    # attempt to load model, build if not found
    try:
        model = joblib.load('./pickles/model.pkl')
    except Exception as e:
        print('pickle not found - building model')
        model = buildtopics(num_topics, corpus, dictionary)

    return (model, corpus, dictionary)


# run script if main
if __name__ == '__main__':
    buildtopics(sys.argv[1]) 