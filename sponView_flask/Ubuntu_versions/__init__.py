from flask import Flask
app = Flask(__name__)
from sponView_flask import views

# # Note: A secret key is included in the sample so that it works.
# # If you use this code in your application, replace this with a truly secret
# # key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = '\xff\x95^SW\xa7\xf0\xf8u\x04\xae\x1b\xb0\\\x93\xe2\x89\xcb\xf2ieV8\xac'
