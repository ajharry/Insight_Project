from sponView_flask.sponViewAnalysis import run_classifier, document_features, get_captions, download_caption_byVidID, get_authenticated_service
from flask import render_template
from sponView_flask import app
from flask import request
import flask
# -*- coding: utf-8 -*-

import os
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "/home/ubuntu/sponView_flask/client_secret_webApp.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'



@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)

  #return flask.redirect(flask.url_for('test_api_request'))
  return flask.redirect(flask.url_for('data_input'))


@app.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  # return ('Credentials have been cleared.<br><br>' +
  #         print_index_table())
  return flask.redirect(flask.url_for('data_input'))

############################################################################
############################################################################
############################################################################

@app.route('/')
@app.route('/input')
def data_input():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')
  else:
    return render_template("input.html")

@app.route('/output')
def data_output():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')
    
  #pull 'video_id' from input field and store it
  video_id = request.args.get('video_id')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  youtube = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)
  #run pretrained model
  captions, result = run_classifier(youtube, video_id)
  
  if result is None:
    result_sentence = 'The result cannot be determined because the content creator has restricted access to their video captions.'
  else:
    if result == 'no':
      result_sentence = 'The result is the video (video ID: %s) <font color=\"red\", size = 20>DOES NOT</font> contain sponsored content.' % video_id
    else:
      result_sentence = 'The result is the video (video ID: %s) <font color=\"red\", size = 20>DOES</font> contain sponsored content.' % video_id
  return render_template("output.html", video_id = video_id, result = result_sentence, captions = captions)
