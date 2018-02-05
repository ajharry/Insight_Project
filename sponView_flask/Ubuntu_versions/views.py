from sponView_flask.sponViewAnalysis import run_classifier,  get_captions, download_subs #, document_features
from flask import render_template
from sponView_flask import app
from flask import request
import flask
# -*- coding: utf-8 -*-



@app.route('/')
@app.route('/input')
def data_input():
    return render_template("input.html")

@app.route('/output')
def data_output():
  #pull 'video_id' from input field and store it
  video_id = request.args.get('video_id')

  #run pretrained model
  captions, result, prob = run_classifier(video_id)
  
  if result is None:
    result_sentence = '<font color=\"red\", size = 10>The result cannot be determined.</font><br/><font size = 6>Either the video ID is invalid or there are no captions for this video.</font>'
  else:
    prob = prob * 100
    if result == 'no':
      result_sentence = '<font color=\"red\", size = 10>Not sponsored.</font><br/><font size = 6>There is a %.0f%% chance that this video DOES NOT contain sponsored content.</font>' % (100-prob)
    else:
      result_sentence = '<font color=\"red\", size = 10>Sponsored.</font><br/><font size = 6>There is a %.0f%% chance that this video DOES contain sponsored content.</font>' % prob
  return render_template("output.html", result = result_sentence, video_id = video_id)
  
  
@app.route('/googlef02e120d95706e7d.html')
def google_verification():
  return render_template("googlef02e120d95706e7d.html")
      
      
    
    
