#!/anaconda2/bin/python


import sys, os
import json
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import cluster 

# script to build dataframe from model 

# attempt to load model and corups pickles
fn_filepath = './data/fake_news.json'
model, corpus_full, dictionary_full = cluster.loadtopics(fn_filepath)

print(dictionary_full)


# loadings = model[corpus_full]
# for document in loadings:
#     print(document)