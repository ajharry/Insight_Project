import pandas as pd

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import re

import pickle

#import nltk
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


def stem_tokens(tokens, ps):
    
    #remove numbers
    tokens = [token for token in tokens if token.isalpha()]
    #print(len(tokens))
    
    
    #remove stop words
    stop = stopwords.words('english') + list(string.punctuation)
    tokens = [token for token in tokens if token not in stop]
    #print(len(tokens))
    
    
    # stem
    stemmed = []
    for item in tokens:
        stemmed.append(ps.stem(item))
    return stemmed

def stemmedCaption(text):
    ps = PorterStemmer()
    text = text.lower()
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, ps)
    return ' '.join(stems)
