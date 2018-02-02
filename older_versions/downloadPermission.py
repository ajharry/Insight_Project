#!/usr/bin/python

import httplib2
import os
import sys
from authenticateYoutube import get_authenticated_service

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# Call the API's captions.list method to list the existing caption tracks.
#EDITED TO RETURN ONLY CAPTION ID IF IN ENGLISH
def list_captions(youtube, video_id):
  #youtube = get_authenticated_service()
  results = youtube.captions().list(
    part="snippet",
    videoId=video_id
  ).execute()

  for item in results["items"]:
    if(item["snippet"]["language"] == 'en'):
        #print("Caption track '%s(%s)' in '%s' language." % (item["snippet"]["name"], item["id"], item["snippet"]["language"]))
        return item["id"]
    

def download_caption_byVidID(video_id, tfmt):
    youtube = get_authenticated_service()
    caption_id = list_captions(youtube, video_id)
    if caption_id:
        subtitle = youtube.captions().download(
            id=caption_id,
            tfmt=tfmt
        ).execute()
    else:
        subtitle = None
    return(subtitle)


#print(download_caption_byVidID('QDlbOrOO0_E', 'srt'))
