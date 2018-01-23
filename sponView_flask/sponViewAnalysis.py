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

import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

#### given video id pull captions
######input video_id
def get_captions(youtube, video_id):
  try:
    captions = download_caption_byVidID(youtube,video_id, tfmt='srt')
    captions = captions.decode("utf-8")
    caption_table = transformSRTCaptions(captions)
    captions = caption_table.text
  except(HttpError, IndexError):
      captions = None
  return captions
    
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
def run_classifier(youtube, video_id):
    #load captions
    captions = get_captions(youtube, video_id)
    if captions is None:
      return None, None
    else:
      captions = captions.str.cat(sep = " ")
      #load model
      filename = '/Users/april/Documents/Insight/Insight_Project/sponView_flask/sponView_classifier.sav'
      classifier = pickle.load(open(filename, 'rb'))
      return captions, classifier.classify(document_features(captions))
      

def transformSRTCaptions(captions):
    caption_table= pd.DataFrame.from_dict(srt_to_dict(captions))
    caption_table.columns = ['end', 'start','text']
    return(caption_table)
    
    
    

##################################

CLIENT_SECRETS_FILE = "client_secret_webApp.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Authorize the request and store authorization credentials.
def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE)

  storage = Storage("%s-oauth2.json" % 'downloadPermission.py') #sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-api-captions.json", "r") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


#### list caption ids for youtube video id 
# Call the API's captions.list method to list the existing caption tracks.
#EDITED TO RETURN ONLY CAPTION ID IF IN ENGLISH
def list_captions(youtube, video_id):
  results = youtube.captions().list(
    part="snippet",
    videoId=video_id
  ).execute()

  for item in results["items"]:
    if(item["snippet"]["language"] == 'en'):
        #print("Caption track '%s(%s)' in '%s' language." % (item["snippet"]["name"], item["id"], item["snippet"]["language"]))
        return item["id"]
        
#### get youtube captions
def download_caption_byVidID(youtube,video_id, tfmt):
    #filename = '/Users/april/Documents/Insight/Insight_Project/sponView_flask/captionCred.sav'
    #youtube = pickle.load(open(filename, 'rb'))
    #youtube = get_authenticated_service()
    caption_id = list_captions(youtube, video_id)
    if caption_id:
        subtitle = youtube.captions().download(
            id=caption_id,
            tfmt=tfmt
        ).execute()
    else:
        subtitle = None
    return(subtitle)

###############

def srt_time_to_seconds(time):
    split_time=time.split(',')
    major, minor = (split_time[0].split(':'), split_time[1])
    return int(major[0])*1440 + int(major[1])*60 + int(major[2]) + float(minor)/1000

def srt_to_dict(srtText):
    subs=[]
    for s in re.sub('\r\n', '\n', srtText).split('\n\n'):
        st = s.split('\n')
        if len(st)>=3:
            split = st[1].split(' --> ')
            subs.append({'start': srt_time_to_seconds(split[0].strip()),
                         'end': srt_time_to_seconds(split[1].strip()),
                         'text': '<br />'.join(j for j in st[2:len(st)])
                        })
    return subs
    
    

