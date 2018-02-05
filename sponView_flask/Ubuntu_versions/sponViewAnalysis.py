import pandas as pd

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import re

import pickle

from nltk.tokenize import word_tokenize # or use some other tokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

import os
import sys

from webvtt import WebVTT

from sklearn import svm, datasets, preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC
from sponView_flask.tokenize import stem_tokens, stemmedCaption

######## download captions using youtube-dl and save to temporary file
##### get video id from url

#### given video id pull captions
def download_subs(video_id, lang="en"):
  video_url = 'https://www.youtube.com/watch?v='+video_id
  
  cmd = [
    "youtube-dl",
    "--skip-download",
    "--write-auto-sub",
    "--sub-format vtt",
    "--sub-lang",
    lang,
    video_url,
    "--output '/home/ubuntu/downloadedCaptions/%(id)s'"
   ]

  os.system(" ".join(cmd))
  return video_url

    
######input video_id
def get_captions(video_id):
  download_subs(video_id, lang="en")
  
  text = []
  
  try:
    captions = WebVTT().read('downloadedCaptions/' + video_id + '.en.vtt')
  except:
    return None
    
  for caption in captions:
    text.append(caption.text)
    
  full_caption = ' '.join(text)
  os.remove('downloadedCaptions/' + video_id + '.en.vtt')
  return full_caption
    
    
    
#### featurize captions
def document_features(document):
    document_words = document.split()
    filename = '/home/ubuntu/sponView_flask/dictionary.sav'
    word_features = pickle.load(open(filename, 'rb'))
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features
    

##### tokenize for SVC

    
    
#### run classifier
def run_classifier(video_id):
    #load captions
    captions = get_captions(video_id)
    if captions is None:
      return None, None, None
    else:
      
      filename = '/home/ubuntu/sponView_flask/feature_extraction.sav'
      feature_extraction  = pickle.load(open(filename, 'rb'))

      stemmed_captions = stemmedCaption(captions)
      
      #load model
      filename = '/home/ubuntu/sponView_flask/svc_classifier.sav'
      clf = pickle.load(open(filename, 'rb'))

      cap_feature = feature_extraction.transform([stemmed_captions])
      result = clf.predict(cap_feature)[0]
      prob = (clf.predict_proba(cap_feature).ravel()[1])
      return captions, result, prob
      
      # #### Naive Bayes ####
      # filename = '/home/ubuntu/sponView_flask/sponView_classifier_stemmed.sav'
      # classifier = pickle.load(open(filename, 'rb'))
      # return captions, classifier.classify(document_features(captions))

