from sponView_flask.sponViewAnalysis import run_classifier, document_features, get_captions
from flask import render_template
from sponView_flask import app
from flask import request


@app.route('/')
@app.route('/index')
def index():
   user = { 'nickname': 'sponView' } 
   return render_template("index.html",
       title = 'sponView',
       user = user)
@app.route('/input')
def data_input():
    return render_template("input.html")

@app.route('/output')
def data_output():
  #pull 'video_id' from input field and store it
  video_id = request.args.get('video_id')
  result = run_classifier(video_id)
  if result == 'no':
    result_sentence = "DOES NOT"
  else:
    result_sentence = "DOES"
  return render_template("output.html", video_id = video_id, result = result_sentence)
