#!/anaconda2/bin/python


import sys, os
import json
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import cluster 

# script to build dataframe from model 

# attempt to load model and corups pickles
model, corpus_full, dictionary_full = cluster.loadtopics()
loadings = model[corpus_full]


topic_count = [0] * 40
for loading in loadings:
    for topic in loading:
        topic_count[topic[0]] += 1

# print(topic_count)

topic_frequency = [0] * 40

for i, count in enumerate(topic_count):
    topic_frequency[i] = count / 1000.0

# print(corpus_full)
# print(topic_frequency)

#
topic_label = list(range(0, 40))
label_names = ['wikileaks', 'NA', 'obama', 'NA', 'obamacare','courts', 
'police', 'canada', 'NA', 'foundation', 'spanish','israel', 'gold', 
'guns/vets', 'intelligence', 'refugees', 'ufo', 'christian','soros', 
'NA', 'NA', 'syria', 'patriotic-trump', 'china', 'russia', 'dapl', 'voter fraud', 
'muslims', 'climate change', 'NA', 'emails', 'weed', 'NA', 'NA', 'NA', 'medical', 
'russia-again', 'drought', 'spanish', 'fbi']

topics_df = pd.DataFrame({"topic_num": topic_label, "frequency": topic_frequency, "topic_name": label_names})
articles_df = pd.read_json('./data/fake_news.json')

topics = [list(), list(), list()]

for loading in loadings: 
    count = 0
    for topic in loading:
        if count < 3:
            topics[count].append(topic[0])
            count += 1

    while count < 3:
        topics[count].append(-1)
        count += 1

articles_df['topic1'] = np.asarray(topics[0])
articles_df['topic2'] = np.asarray(topics[1])
articles_df['topic3'] = np.asarray(topics[2])

articles_df.to_csv('./data/fake_news_clustered.csv', encoding = 'utf-8')
topics_df.to_csv('./data/fake_news_topic_key.csv', encoding = 'utf-8')




