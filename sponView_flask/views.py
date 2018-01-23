from sponView_flask.sponViewAnalysis import run_classifier, document_features, get_captions, download_caption_byVidID, get_authenticated_service
from flask import render_template
from sponView_flask import app
from flask import request


@app.route('/index')
def index():
   user = { 'nickname': 'sponView' } 
   return render_template("index.html",
       title = 'sponView',
       user = user)
       
@app.route('/')
@app.route('/input')
def data_input():
    return render_template("input.html")

@app.route('/output')
def data_output():
  #pull 'video_id' from input field and store it
  video_id = request.args.get('video_id')
  
  #youtube requires authenitcation
  youtube = get_authenticated_service()

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
