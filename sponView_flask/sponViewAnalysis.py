import pandas as pd

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import re

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pickle

from nltk.tokenize import word_tokenize # or use some other tokenizer
from nltk.corpus import stopwords
import string


#### given video id pull captions
######input video_id
def get_captions(video_id):
    ###### for MVP just take from table. for next week figure out authentication and implement parsing
    dbname = 'youtubeSpon'
    username = 'april' # change this to your username

    engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
    con = None
    con = psycopg2.connect(database = dbname, user = username)

    # query:
    sql_query = """SELECT "youtubeEmmy"."fullCaptions" FROM "youtubeEmmy" WHERE "youtubeEmmy".video_id = '%s';"""%video_id
    selectedCaption = pd.read_sql_query(sql_query,con)
    return str(selectedCaption.iloc[0])
    
    
##### featurize captions
def document_features(document):
    document_words = document.split()
    filename = '/Users/april/Documents/Insight/Insight_Project/sponView_flask/dictionary.sav'
    word_features = pickle.load(open(filename, 'rb'))
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features
    
    
    
#### run classifier
def run_classifier(video_id):
    #load model
    filename = '/Users/april/Documents/Insight/Insight_Project/sponView_flask/sponView_classifier.sav'
    classifier = pickle.load(open(filename, 'rb'))
    captions = get_captions(video_id)
    return classifier.classify(document_features(captions))
    
    
    
